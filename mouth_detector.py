import cv2
import mediapipe as mp
import numpy as np
from spotify_runner import play_ringa_ringa_on_active_device

mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

print("Camera opened successfully!")
print("Press 'q' to quit")

# Mouth landmark indices (lips center area)
MOUTH_LANDMARKS = [13, 14]  # Upper and lower lip center

PROXIMITY_THRESHOLD = 80

vape_check = 0
prev_near = False
spotify_triggered = False

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh, mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame. Exiting...")
            break

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_results = face_mesh.process(rgb_frame)

        hand_results = hands.process(rgb_frame)

        mouth_center = None
        something_near_mouth = False

        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                # Get mouth landmarks
                mouth_points = []
                for idx in MOUTH_LANDMARKS:
                    landmark = face_landmarks.landmark[idx]
                    x, y = int(landmark.x * w), int(landmark.y * h)
                    mouth_points.append((x, y))

                # Calculate mouth center
                mouth_center = np.mean(mouth_points, axis=0).astype(int)

                # Draw mouth center
                cv2.circle(frame, tuple(mouth_center), 5, (0, 255, 0), -1)

                # Draw proximity circle around mouth
                cv2.circle(frame, tuple(mouth_center), PROXIMITY_THRESHOLD,
                          (0, 255, 0), 2)

        if hand_results.multi_hand_landmarks and mouth_center is not None:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                # Get fingertips and palm positions
                for landmark in hand_landmarks.landmark:
                    x, y = int(landmark.x * w), int(landmark.y * h)

                    # Calculate distance to mouth
                    distance = np.sqrt((x - mouth_center[0])**2 + (y - mouth_center[1])**2)

                    if distance < PROXIMITY_THRESHOLD:
                        something_near_mouth = True
                        break

        # Display warning if something is near mouth
        if something_near_mouth:
            cv2.putText(frame, f"ALERT: Hand near mouth! Vape Check: {vape_check}", (10, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            cv2.circle(frame, tuple(mouth_center), PROXIMITY_THRESHOLD,
                      (0, 0, 255), 3)

        if something_near_mouth and not prev_near:
            vape_check += 1

        if vape_check >= 5 and not spotify_triggered:
            cv2.putText(frame,
                f"Limit hit: {vape_check}",
                (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            play_ringa_ringa_on_active_device()
            spotify_triggered = True
            
            
        prev_near = something_near_mouth

        # Display instructions
        cv2.putText(frame, "Press 'q' to quit", (10, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow('Mouth Proximity Detector', frame)

        if cv2.waitKey(1) == ord('q'):
            vape_check = 0
            break

cap.release()
cv2.destroyAllWindows()
