import os
import cv2
import mediapipe as mp
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Config
DATA_DIR = r"c:/Users/Harshit/OneDrive/Desktop/kanu/projects/Front-end stack/VOICE/archive/isl_dataset"
MODEL_PATH = "model.p"
LABELS_PATH = "labels.p"

# MediaPipe Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True, 
    min_detection_confidence=0.3, 
    max_num_hands=1
)

data = []
labels = []

# Classes to train (A-Z)
classes = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d)) and d.isalpha() and len(d) == 1]
classes.sort()

print(f"Found {len(classes)} classes: {classes}")

for dir_ in classes:
    class_path = os.path.join(DATA_DIR, dir_)
    print(f"Processing class: {dir_}")
    
    for img_path in os.listdir(class_path)[:200]: # Limit to 200 images for speed during Hackathon
        data_aux = []
        x_ = []
        y_ = []

        img = cv2.imread(os.path.join(class_path, img_path))
        if img is None: continue
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)
                
                # Scale Invariant Normalization
                min_x, max_x = min(x_), max(x_)
                min_y, max_y = min(y_), max(y_)
                
                width = max(max_x - min_x, 0.00001)
                height = max(max_y - min_y, 0.00001)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    # Normalize to 0-1 range relative to hand size
                    data_aux.append((x - min_x) / width)
                    data_aux.append((y - min_y) / height)

            data.append(data_aux)
            labels.append(dir_)

# Train
if len(data) > 0:
    print(f"Training on {len(data)} samples...")
    
    # Pad sequences if valid (should be 42 features for 1 hand)
    # Filter out bad samples
    clean_data = []
    clean_labels = []
    for i, d in enumerate(data):
        if len(d) == 42:
            clean_data.append(d)
            clean_labels.append(labels[i])
            
    print(f"Cleaned samples: {len(clean_data)}")
    
    x_train, x_test, y_train, y_test = train_test_split(clean_data, clean_labels, test_size=0.2, shuffle=True, stratify=clean_labels)
    
    model = RandomForestClassifier()
    model.fit(x_train, y_train)
    
    y_predict = model.predict(x_test)
    score = accuracy_score(y_predict, y_test)
    
    print(f"{score * 100}% of samples were classified correctly !")
    
    f = open('model.p', 'wb')
    pickle.dump({'model': model}, f)
    f.close()
    print("Model saved successfully!")
else:
    print("No valid data collected.")
