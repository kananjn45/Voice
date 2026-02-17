"""
Gesture Simulator Module
Simulates gesture recognition using simple rule-based logic.
This is a placeholder that will be replaced with a real AI model later.
"""


class GestureSimulator:
    """
    Simulates gesture recognition from hand landmarks.
    
    FUTURE: Replace this entire class with:
        model = load_model('isl_model.h5')
        prediction = model.predict(landmarks)
    """
    
    def __init__(self):
        """Initialize and load model."""
        import pickle
        try:
            with open('model.p', 'rb') as f:
                self.model = pickle.load(f)['model']
        except:
            self.model = None
        
        # Word mode tracking
        self.letter_sequence = []
        self.last_letter_time = 0
        self.word_timeout = 5.0  # seconds before resetting sequence (increased from 3.0)
            
    def predict_gesture(self, hand_results, mode="LETTER"):
        """Predict using trained model or fallback.
        
        Args:
            hand_results: Hand landmark data
            mode: "LETTER" for single letter detection, "WORD" for word detection
            
        Returns:
            Detected letter/word or None
        """
        if not hand_results or not hand_results.hand_landmarks:
            return {"type": "NONE", "value": None}
            
        # Feature Extraction (Must match training logic)
        data_aux = []
        x_ = []
        y_ = []
        
        # Assume single hand focus for now or handle first hand
        # Main app passes list of landmarks for ONE hand in `hand_landmarks` attribute check main.py logic
        # main.py passes: data.hand_landmarks = [list(hand.landmark), ...]
        # So hand_results.hand_landmarks is a LIST of hand landmarks (each being a list of 21 points)
        
        try:
            # We train on single hand. Let's pick the first detected hand.
            if len(hand_results.hand_landmarks) > 0:
                landmarks = hand_results.hand_landmarks[0] # List of 21 {x,y,z} objects (or similar)
                
                # Check data type. main.py passes `list(hand.landmark)` which consists of NormalizedLandmark objects
                
                for lm in landmarks:
                    x_.append(lm.x)
                    y_.append(lm.y)
                
                min_x, max_x = min(x_), max(x_)
                min_y, max_y = min(y_), max(y_)
                
                width = max(max_x - min_x, 0.00001)
                height = max(max_y - min_y, 0.00001)

                for lm in landmarks:
                    data_aux.append((lm.x - min_x) / width)
                    data_aux.append((lm.y - min_y) / height)
                
                if self.model:
                     # Predict letter
                     letter = self.model.predict([data_aux])[0]
                     
                     # Handle word mode
                     if mode == "WORD":
                         import time
                         from word_library import get_word_by_pattern
                         
                         current_time = time.time()
                         
                         # Reset sequence if timeout
                         if current_time - self.last_letter_time > self.word_timeout:
                             if self.letter_sequence:  # Only print if there was a sequence
                                 print(f"[WORD MODE] Timeout - resetting sequence: {self.letter_sequence}")
                             self.letter_sequence = []
                         
                         # Add letter to sequence if it's new
                         if not self.letter_sequence or letter != self.letter_sequence[-1]:
                             self.letter_sequence.append(letter)
                             self.last_letter_time = current_time
                             print(f"[WORD MODE] Added '{letter}' (type: {type(letter)}) -> Sequence: {self.letter_sequence}")
                         else:
                             # Update time even if same letter (to prevent timeout)
                             self.last_letter_time = current_time
                         
                         # Try to match word pattern
                         print(f"[WORD MODE] Checking sequence {self.letter_sequence} against word patterns...")
                         word = get_word_by_pattern(self.letter_sequence)
                         if word:
                             # Found a word match! Return the WORD
                             print(f"[WORD MODE] ✓ MATCHED WORD: {word}")
                             self.letter_sequence = []  # Reset for next word
                             return {"type": "WORD", "value": word}
                         else:
                             print(f"[WORD MODE] No match found for {self.letter_sequence}")
                         
                         # Return current sequence (for display only, not confirmed)
                         sequence_str = "".join(self.letter_sequence)
                         return {"type": "SEQUENCE", "value": sequence_str, "raw_letter": letter}
                     
                     # Letter mode - return single letter
                     return {"type": "LETTER", "value": letter}
        except Exception as e:
            # print(f"Prediction Error: {e}")
            pass
            
        # Fallback (Original Logic)
        return {"type": "NONE", "value": None}
    
    def get_current_sequence(self):
        """Get current letter sequence being built in word mode"""
        return "".join(self.letter_sequence) if self.letter_sequence else ""
