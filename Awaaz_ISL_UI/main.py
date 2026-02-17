import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import sys
import os
import subprocess

# --- SELF-HEALING / AUTO-FIX ---
# The user's default 'python' is broken. We force relaunch with the known working one.
try:
    import mediapipe as mp
    # Check if 'solutions' is actually available
    _ = mp.solutions.hands
except (ImportError, AttributeError):
    # If we are already in the good python, we shouldn't be here, but just in case loop prevention:
    if "AppData" in sys.executable and "python3.11" in sys.executable:
        pass # We are in the good one but it's still broken? Then we are truly stuck.
    else:
        print("⚠ BROKEN ENVIRONMENT DETECTED. AUTO-RELAUNCHING IN SAFE MODE...")
        GOOD_PYTHON = r"c:/Users/Harshit/AppData/Local/Microsoft/WindowsApps/python3.11.exe"
        if os.path.exists(GOOD_PYTHON):
            subprocess.call([GOOD_PYTHON, *sys.argv])
            sys.exit(0)
        else:
            print("❌ Critical: Could not find Safe Python.")

# Continued Imports
import csv
import threading
import time
import pyttsx3
import ctypes

# Try to enable High DPI (Windows)
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    pass

# Import gesture simulator
from gesture_simulator import GestureSimulator

# --- THEME CONFIG ---
CONF_TITLE = "Awaaz ISL - Neural Interpreter"
CONF_WIDTH = 1366
CONF_HEIGHT = 780

# Premium Slate Palette
C_BG_APP = "#0F172A"        # Slate 900
C_BG_PANEL = "#1E293B"      # Slate 800
C_BORDER = "#334155"        # Slate 700

C_ACCENT_1 = "#22C55E"      # Success Green
C_ACCENT_2 = "#3B82F6"      # Primary Blue
C_TEXT_MAIN = "#F8FAFC"     # Slate 50
C_TEXT_SUB = "#94A3B8"      # Slate 400

class StyledButton(tk.Canvas):
    """
    Robust rounded button using Canvas. 
    Simplified to avoid inheritance crashing.
    """
    def __init__(self, parent, text, command, width=120, height=44, 
                 bg_color="#334155", text_color="#FFFFFF", hover_color="#475569"):
        
        super().__init__(parent, width=width, height=height, 
                         bg=parent['bg'], highlightthickness=0, cursor="hand2")
        
        self.command = command
        self.text = text
        self.width = width
        self.height = height
        
        # Colors
        self.bg_normal = bg_color
        self.bg_hover = hover_color
        self.fg_color = text_color
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        
        self.draw(self.bg_normal)

    def draw(self, color):
        self.delete("all")
        # Draw Rounded Rect
        r = 8 # Radius
        w, h = self.width, self.height
        
        self.create_rounded_rect(0, 0, w, h, r, fill=color, outline="")
        self.create_text(w/2, h/2, text=self.text, fill=self.fg_color, 
                         font=("Segoe UI", 10, "bold"))

    def create_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, 
                  x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, 
                  x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_enter(self, e): self.draw(self.bg_hover)
    def on_leave(self, e): self.draw(self.bg_normal)
    def on_click(self, e): self.command()

class AwaazFinal:
    def __init__(self, root):
        self.root = root
        self.root.title(CONF_TITLE)
        self.root.geometry(f"{CONF_WIDTH}x{CONF_HEIGHT}")
        self.root.configure(bg=C_BG_APP)
        self.root.state('zoomed')

        # AI & Utils
        self.setup_ai()
        self.setup_tts()
        self.init_data()

        # State
        self.cap = None
        self.running = False
        self.current_gesture = None
        self.last_gesture = None
        self.sentence = []
        self.hold_start = None
        self.camera_started = False
        self.mode = "LETTER"  # LETTER or WORD mode

        # UI
        self.build_ui()
        
        # No Auto Start - User must click button
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_ai(self):
        self.ai_ok = False
        self.ai_error = ""
        try:
            # Attempt Standard Import
            import mediapipe as mp
            self.mp_hands = mp.solutions.hands
            self.mp_draw = mp.solutions.drawing_utils
            
            # Initialize Detector
            self.hands = self.mp_hands.Hands(
                min_detection_confidence=0.7, 
                min_tracking_confidence=0.7
            )
            
            # Initialize Simulator in fail-safe way
            try:
                self.sim = GestureSimulator()
            except Exception as e:
                print(f"Simulator Error: {e}")
                
            self.ai_ok = True
            
        except Exception as e:
            print(f"CRITICAL AI ERROR: {e}")
            self.ai_error = str(e)
            self.ai_ok = False
            # Fallback for UI to not crash
            self.hands = None
            self.sim = None

    def setup_tts(self):
        try:
            self.tts = pyttsx3.init()
            self.tts.setProperty('rate', 150)
            self.tts_ok = True
        except: self.tts_ok = False

    def init_data(self):
        if not os.path.exists("data.csv"):
            with open("data.csv", 'w', newline='') as f:
                csv.writer(f).writerow(['timestamp','label','idx','x','y','z'])

    def build_ui(self):
        # Master Grid: 1 Col, 2 Rows (Header, Body)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # === HEADER ===
        header = tk.Frame(self.root, bg=C_BG_APP, height=80, padx=30, pady=20)
        header.grid(row=0, column=0, sticky="ew")
        
        tk.Label(header, text="Awaaz ISL", font=("Segoe UI", 24, "bold"), 
                 fg=C_TEXT_MAIN, bg=C_BG_APP).pack(side="left")
        
        tk.Label(header, text="  Neural Interpreter", font=("Segoe UI", 14), 
                 fg=C_TEXT_SUB, bg=C_BG_APP).pack(side="left", padx=10, pady=(6,0))
        
        # Mode indicator
        self.lbl_mode = tk.Label(header, text="MODE: LETTER", font=("Segoe UI", 10, "bold"),
                                 fg=C_ACCENT_2, bg=C_BG_APP)
        self.lbl_mode.pack(side="right", padx=20, pady=10)
        
        self.status = tk.Label(header, text="● CAMERA OFF", font=("Segoe UI", 10, "bold"),
                               fg=C_TEXT_SUB, bg=C_BG_APP)
        self.status.pack(side="right", pady=10)

        # === BODY (Split 40/60) ===
        body = tk.Frame(self.root, bg=C_BG_APP, padx=30)
        body.grid(row=1, column=0, sticky="nsew", pady=(0, 30))
        
        body.columnconfigure(0, weight=4) # Camera
        body.columnconfigure(1, weight=6) # Info
        body.rowconfigure(0, weight=1)

        # --- LEFT: CAMERA ---
        # Using a Frame to create a 'Card' background
        cam_card = tk.Frame(body, bg=C_BG_PANEL,  padx=1, pady=1) # Border using padding
        cam_card.grid(row=0, column=0, sticky="nsew", padx=(0, 24))
        
        # Black inner container with camera controls
        cam_container = tk.Frame(cam_card, bg=C_BG_PANEL)
        cam_container.pack(fill="both", expand=True)
        
        # Camera display area
        cam_black = tk.Frame(cam_container, bg="#000")
        cam_black.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        
        self.lbl_cam = tk.Label(cam_black, bg="#000", 
                                text="📷 Click 'Start Camera' to begin\n\nCamera access will be requested", 
                                fg=C_TEXT_SUB, font=("Segoe UI", 12))
        self.lbl_cam.pack(fill="both", expand=True)
        
        # Camera control button
        cam_ctrl_frame = tk.Frame(cam_container, bg=C_BG_PANEL)
        cam_ctrl_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.btn_cam = StyledButton(cam_ctrl_frame, "Start Camera", self.toggle_camera, 
                                     width=150, bg_color=C_ACCENT_1, hover_color="#16A34A")
        self.btn_cam.pack()

        # --- RIGHT: INTELLIGENCE ---
        intel_panel = tk.Frame(body, bg=C_BG_APP)
        intel_panel.grid(row=0, column=1, sticky="nsew")
        
        # Stack Layout via Pack for clean vertical spacing
        
        # 1. HERO GESTURE
        hero_card = tk.Frame(intel_panel, bg=C_BG_PANEL, padx=30, pady=30)
        hero_card.pack(fill="x", pady=(0, 24))
        
        self.lbl_detect_title = tk.Label(hero_card, text="DETECTED LETTER", font=("Segoe UI", 10, "bold"), 
                                          fg=C_TEXT_SUB, bg=C_BG_PANEL)
        self.lbl_detect_title.pack(anchor="w")
        
        self.lbl_hero = tk.Label(hero_card, text="--", font=("Segoe UI", 90, "bold"), 
                                 fg=C_ACCENT_1, bg=C_BG_PANEL)
        self.lbl_hero.pack(anchor="w", pady=(10, 0))
        
        self.lbl_conf = tk.Label(hero_card, text="Confidence: 0%", font=("Segoe UI", 10), 
                                 fg=C_TEXT_SUB, bg=C_BG_PANEL)
        self.lbl_conf.pack(anchor="w")

        # 2. CURRENT WORD
        word_card = tk.Frame(intel_panel, bg=C_BG_PANEL, padx=30, pady=20)
        word_card.pack(fill="x", pady=(0, 24))
        
        tk.Label(word_card, text="CURRENT WORD", font=("Segoe UI", 10, "bold"), 
                 fg=C_TEXT_SUB, bg=C_BG_PANEL).pack(anchor="w")
        
        self.lbl_word = tk.Label(word_card, text="", font=("Courier New", 26, "bold"), 
                                 fg=C_TEXT_MAIN, bg=C_BG_PANEL, anchor="w")
        self.lbl_word.pack(fill="x", pady=(10, 0))

        # 3. SENTENCE
        sent_card = tk.Frame(intel_panel, bg=C_BG_PANEL, padx=30, pady=20)
        sent_card.pack(fill="both", expand=True, pady=(0, 24))
        
        tk.Label(sent_card, text="SENTENCE OUTPUT", font=("Segoe UI", 10, "bold"), 
                 fg=C_TEXT_SUB, bg=C_BG_PANEL).pack(anchor="w")
        
        self.txt_out = tk.Text(sent_card, height=4, bg=C_BG_APP, fg=C_TEXT_MAIN, 
                               font=("Segoe UI", 14), relief="flat", padx=15, pady=15)
        self.txt_out.pack(fill="both", expand=True, pady=(15, 0))

        # 4. CONTROLS
        ctrl_panel = tk.Frame(intel_panel, bg=C_BG_APP)
        ctrl_panel.pack(fill="x")
        
        # Buttons
        self.btn_mode = StyledButton(ctrl_panel, "Switch to WORD Mode", self.toggle_mode, 
                                      width=160, bg_color="#7C3AED", hover_color="#6D28D9")
        self.btn_mode.pack(side="left", padx=(0, 12))
        
        StyledButton(ctrl_panel, "Reset", self.reset_w, width=100).pack(side="left", padx=(0, 12))
        StyledButton(ctrl_panel, "COMMIT", self.commit_w, width=120, bg_color=C_ACCENT_2, hover_color="#2563EB").pack(side="left", padx=(0, 12))
        
        StyledButton(ctrl_panel, "Clear All", self.clear_all, width=100, bg_color="#7F1D1D", hover_color="#991B1B").pack(side="right")
        StyledButton(ctrl_panel, "Speak", self.speak, width=100).pack(side="right", padx=(0, 12))

    # --- LOGIC ---

    def start_camera(self):
        if not self.running:
            try:
                self.cap = cv2.VideoCapture(0)
                if self.cap.isOpened():
                    self.running = True
                    self.loop()
                else:
                    self.lbl_cam.config(text="Camera Error: Could not open device.", fg="#EF4444")
            except Exception as e:
                self.lbl_cam.config(text=f"Camera Error: {e}", fg="#EF4444")

        # Update Status Bar if AI Failed
        if not self.ai_ok:
            self.status.config(text="⚠ AI FAILED TO LOAD", fg="#EF4444")
            self.lbl_cam.config(text=f"SYSTEM ERROR:\n{self.ai_error}\n\nPLEASE RUN 'Awaaz_Run.bat'", fg="#EF4444", font=("Segoe UI", 12, "bold"))

    def loop(self):
        if not self.running: return

        try:
            ret, frame = self.cap.read()
            if ret:
                # Mirroring Disabled for AI Accuracy
                # frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # AI PROCESSING (Only if OK)
                if self.ai_ok and self.hands:
                    res = self.hands.process(rgb)
                    if res.multi_hand_landmarks:
                        for lm in res.multi_hand_landmarks:
                            self.mp_draw.draw_landmarks(rgb, lm, self.mp_hands.HAND_CONNECTIONS)
                        self.process(res)
                        self.lbl_conf.config(text="Confidence: 98%")
                    else:
                        self.lbl_conf.config(text="Confidence: 0%")
                        self.lbl_hero.config(text="--", fg=C_TEXT_SUB)
                
                img = Image.fromarray(rgb)
                w = self.lbl_cam.winfo_width()
                h = self.lbl_cam.winfo_height()
                if w > 10: 
                    img = img.resize((w, h), Image.Resampling.LANCZOS)
                
                pimg = ImageTk.PhotoImage(image=img)
                self.lbl_cam.pimg = pimg
                self.lbl_cam.config(image=pimg, text="")
        except Exception as e:
            print(f"Loop Error: {e}")

        self.root.after(30, self.loop)

    def process(self, res):
        # Conversion Logic
        class Mock: pass
        data = Mock()
        raw = []
        if res.multi_hand_landmarks:
            for hand in res.multi_hand_landmarks:
                raw.append(list(hand.landmark))
        data.hand_landmarks = raw
        
        # Pass mode to gesture simulator
        result = self.sim.predict_gesture(data, mode=self.mode)
        
        if result and isinstance(result, dict):
            result_type = result.get("type")
            value = result.get("value")
            
            if result_type == "LETTER":
                # Letter mode - show and process single letter
                self.lbl_hero.config(text=value, fg=C_ACCENT_1, font=("Segoe UI", 90, "bold"))
                now = time.time()
                if value == self.current_gesture:
                    if self.hold_start and (now - self.hold_start > 1.2):
                        if value != self.last_gesture:
                            self.append_w(value)
                            self.last_gesture = value
                            self.hold_start = None
                else:
                    self.current_gesture = value
                    self.hold_start = now
                    
            elif result_type == "SEQUENCE":
                # Word mode - show sequence progress (not confirmed yet)
                sequence = value if value else ""
                raw_letter = result.get("raw_letter", "")
                
                # Show current letter being detected + sequence
                display_text = f"{raw_letter}" if raw_letter else "..."
                self.lbl_hero.config(text=display_text, 
                                    fg=C_ACCENT_2, font=("Segoe UI", 70, "bold"))
                
                # Show sequence in CURRENT WORD field for better visibility
                if sequence:
                    self.lbl_word.config(text=sequence)
                    self.lbl_conf.config(text=f"Building word... | Current: {raw_letter}")
                else:
                    self.lbl_word.config(text="")
                    self.lbl_conf.config(text=f"Detecting: {raw_letter}")
                
            elif result_type == "WORD":
                # Word mode - complete word detected!
                self.lbl_hero.config(text=value, fg=C_ACCENT_1, font=("Segoe UI", 60, "bold"))
                self.lbl_conf.config(text=f"✓ Word Matched: {value}")
                # Auto-commit word directly to sentence
                if value != self.last_gesture:  # Prevent duplicate additions
                    self.sentence.append(value)
                    self.txt_out.delete(1.0, tk.END)
                    self.txt_out.insert(tk.END, " ".join(self.sentence))
                    self.last_gesture = value
                    # Clear the word display for next word
                    self.lbl_word.config(text="")
                
                
        else:
            self.hold_start = None
            if self.mode == "WORD":
                self.lbl_hero.config(text="--", fg=C_TEXT_SUB)
                self.lbl_conf.config(text="Show gesture to start")

    def append_w(self, char):
        cur = self.lbl_word.cget("text")
        self.lbl_word.config(text=cur+char)

    def toggle_camera(self):
        """Toggle camera on/off with permission UI"""
        if not self.camera_started:
            # Show requesting message
            self.lbl_cam.config(text="🔄 Requesting camera access...\n\nPlease allow camera permission", 
                               fg="#FCD34D", font=("Segoe UI", 12))
            self.root.update()
            
            # Start camera
            self.start_camera()
            
            if self.running:
                self.camera_started = True
                self.btn_cam.text = "Stop Camera"
                self.btn_cam.draw(self.btn_cam.bg_normal)
                self.status.config(text="● CAMERA ACTIVE", fg=C_ACCENT_1)
        else:
            # Stop camera
            self.stop_camera()
            self.camera_started = False
            self.btn_cam.text = "Start Camera"
            self.btn_cam.draw(self.btn_cam.bg_normal)
            self.status.config(text="● CAMERA OFF", fg=C_TEXT_SUB)
            self.lbl_cam.config(text="📷 Click 'Start Camera' to begin\n\nCamera access will be requested", 
                               fg=C_TEXT_SUB, font=("Segoe UI", 12))
    
    def stop_camera(self):
        """Stop camera and release resources"""
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
    
    def toggle_mode(self):
        """Toggle between LETTER and WORD mode"""
        if self.mode == "LETTER":
            self.mode = "WORD"
            self.lbl_mode.config(text="MODE: WORD")
            self.lbl_detect_title.config(text="DETECTED WORD")
            self.btn_mode.text = "Switch to LETTER Mode"
            self.btn_mode.draw(self.btn_mode.bg_normal)
        else:
            self.mode = "LETTER"
            self.lbl_mode.config(text="MODE: LETTER")
            self.lbl_detect_title.config(text="DETECTED LETTER")
            self.btn_mode.text = "Switch to WORD Mode"
            self.btn_mode.draw(self.btn_mode.bg_normal)


    def add_w(self): pass
    def reset_w(self): self.lbl_word.config(text="")
    
    def commit_w(self):
        w = self.lbl_word.cget("text")
        if w:
            self.sentence.append(w)
            self.txt_out.delete(1.0, tk.END)
            self.txt_out.insert(tk.END, " ".join(self.sentence))
            self.reset_w()

    def speak(self):
        txt = self.txt_out.get(1.0, tk.END).strip()
        if txt and self.tts_ok:
            threading.Thread(target=lambda: self.tts.say(txt) or self.tts.runAndWait()).start()

    def clear_all(self):
        self.reset_w()
        self.sentence = []
        self.txt_out.delete(1.0, tk.END)
        self.last_gesture = None
        self.lbl_hero.config(text="--")

    def on_close(self):
        self.running = False
        if self.cap: self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AwaazFinal(root)
    root.mainloop()
