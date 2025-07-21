import math

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def recognize_gesture(lm_list):
    if len(lm_list) < 21:
        return None

    # Extract landmarks
    thumb = lm_list[4]
    index = lm_list[8]
    middle = lm_list[12]
    ring = lm_list[16]
    pinky = lm_list[20]
    wrist = lm_list[0]

    # Finger up = tip is above MCP/PIP or far from wrist
    def is_up(tip, base):
        return tip[1] < base[1] - 20  # more forgiving offset

    index_up = is_up(index, lm_list[6])
    middle_up = is_up(middle, lm_list[10])
    ring_up = is_up(ring, lm_list[14])
    pinky_up = is_up(pinky, lm_list[18])

    # Mute: hand wide open
    if distance(thumb, pinky) > 150:
        return "mute"

    # Play/pause: index + middle up, others down
    if index_up and middle_up and not ring_up and not pinky_up:
        return "play_pause"

    # Screenshot: index close to thumb AND middle up
    if distance(thumb, index) < 40 and middle_up:
        return "screenshot"

    # Index up only
        # Index up only
        # Index up only
    if index_up and not middle_up and not ring_up and not pinky_up:
        dx = index[0] - wrist[0]
        dy = wrist[1] - index[1]  # flipped y-axis

        if abs(dx) < 10:
            angle = 90
        else:
            angle = math.degrees(math.atan2(dy, dx))

        # Debug print
        print("Angle:", angle)

        # Right: near 0°, Left: near 180° or -180°, Up: near 90°
        if -40 < angle < 40:
            return "next_track"
        elif angle > 140 or angle < -140:
            return "previous_track"
        else:
            return "volume_up"



    return None
