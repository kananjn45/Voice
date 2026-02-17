# Awaaz ISL - Neural Interpreter 🤟

**Awaaz ISL** is a real-time Indian Sign Language (ISL) interpreter designed to bridge the communication gap for the deaf and hard-of-hearing community. Using advanced computer vision and neural networks, it translates hand gestures into text and speech instantaneously.

---

## ✨ Key Features

-   **Real-time Recognition**: Instant translation of ISL letters and words using MediaPipe and custom neural models.
-   **Dual Modes**:
    -   **LETTER Mode**: Detects individual alphabets for spelling out names or specific terms.
    -   **WORD Mode**: Recognizes complete ISL words and common phrases.
-   **Text-to-Speech (TTS)**: Integrated voice feedback to narrate detected gestures.
-   **Premium UI**: A sleek, dark-themed dashboard built with Tkinter, featuring real-time confidence scores and sentence building.
-   **Self-Healing Environment**: Automatically detects and uses the correct Python interpreter to ensure MediaPipe compatibility.

---

## 🛠️ Requirements

The project requires Python 3.10+ and the following libraries:

-   `opencv-python` (Handle webcam feed)
-   `mediapipe` (Hand landmark detection)
-   `Pillow` (Image processing for UI)
-   `pyttsx3` (Text-to-Speech engine)

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/kananjn45/Voice.git
cd Voice
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r Awaaz_ISL_UI/requirements.txt
```

### 3. Run the Application
You can launch the interpreter using the provided batch script or directly via Python:

-   **Windows (Quick Launch)**: Double-click `Awaaz_ISL_UI/Awaaz_Run.bat`
-   **Manual**:
    ```bash
    cd Awaaz_ISL_UI
    python main.py
    ```

---

## 📁 Project Structure

-   `Awaaz_ISL_UI/`: Main application directory.
    -   `main.py`: Core application logic and UI.
    -   `gesture_simulator.py`: Gesture detection and logic handling.
    -   `word_library.py`: Database/logic for ISL word matching.
    -   `train_model.py`: Script for training the recognition model.
    -   `Awaaz_Run.bat`: Shortcut to launch the application on Windows.
-   `data.csv`: Landmarks data for training/verification.

---

## 🏗️ Development & Training

To train new gestures or update the model:
1. Run `Awaaz_Train.bat` (Windows) or `python train_model.py`.
2. Collect landmarks for desired signs.
3. The model will update the recognition logic used in the main dashboard.

---

## � Dataset Used

The model is trained/validated on the **ISL Data** available on Kaggle:
- **Dataset Link**: [ISL Data by Ananya Arya](https://www.kaggle.com/datasets/ananyaarya22/isl-data)

---

## �📜 License
This project is open-source and available under the MIT License.
