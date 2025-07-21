import cv2

def draw_overlay(frame, gesture):
    overlays = {
        "volume_up":    (" Volume Up", (0, 255, 0)), # Green
        "play_pause":   (" Play/Pause", (0, 255, 255)), # Yellow
        "mute":         (" Mute", (0, 0, 255)), # Red
        "screenshot":   (" Screenshot", (255, 0, 0)), # Blue
        "next_track":   (" Next Track", (128, 0, 128)),  # Purple
        "previous_track":("Previous Track",(255,165,0)),
        "minimize": (" Minimize", (100, 100, 255)),  # Light Blue
    }
    if gesture in overlays:
        text, color = overlays[gesture]
        cv2.putText(frame, text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
