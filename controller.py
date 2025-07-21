import cv2
import mediapipe as mp
import pyautogui
from datetime import datetime
import os
import time
from gestures import recognize_gesture
from overlay import draw_overlay

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

# Screenshot folder
os.makedirs("screenshots", exist_ok=True)

# Webcam setup
cap = cv2.VideoCapture(0)

# Gesture state tracking
gesture_state = None
last_trigger_time = 0
cooldown = 1.0  # seconds

def take_screenshot(frame):
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"screenshots/snap_{now}.png"
    cv2.imwrite(path, frame)
    print(f"📸 Screenshot saved: {path}")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    
    h, w, _ = frame.shape
    
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))
            
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            
            gesture = recognize_gesture(lm_list)
            current_time = time.time()
            
            if gesture != gesture_state and (current_time - last_trigger_time) > cooldown:
                gesture_state = gesture
                last_trigger_time = current_time
                
                if gesture == "volume_up":
                    pyautogui.press("volumeup")
                elif gesture == "play_pause":
                    pyautogui.press("playpause")
                elif gesture == "mute":
                    pyautogui.press("volumemute")
                elif gesture == "screenshot":
                    take_screenshot(frame)
                elif gesture == "next_track":
                    pyautogui.press("nexttrack")
                elif gesture == "previous_track":
                    pyautogui.press("previoustrack")
                elif gesture == "minimize":
                    pyautogui.hotkey("win", "down")


                draw_overlay(frame, gesture)
    else:
        gesture_state = None
    
    cv2.imshow("Gesture Controller", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
