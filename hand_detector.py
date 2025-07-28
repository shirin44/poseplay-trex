# Import OpenCV for webcam access and image processing
import cv2

# Import MediaPipe for hand detection and drawing utilities
import mediapipe as mp

class HandDetector:
    def __init__(self, max_hands=1, detection_confidence=0.7):
        """
        Initializes the hand detector with optional parameters.
        - max_hands: how many hands to track (default is 1)
        - detection_confidence: minimum confidence for hand detection
        """
        self.max_hands = max_hands
        self.mode = False  # False = video stream (not still image)
        self.detection_confidence = detection_confidence
        self.track_confidence = 0.5  # Confidence for tracking after detection

        # Load MediaPipe's hand model
        self.mp_hands = mp.solutions.hands

        # Create a hand detection object with our config
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.track_confidence,
        )

        # Load MediaPipe's drawing utility for visualizing the landmarks
        self.mp_draw = mp.solutions.drawing_utils

    def find_hands(self, frame):
        """
        Takes a video frame, detects hands, and draws the landmarks.
        Returns the annotated frame and detection results.
        """

        # Convert the frame from BGR (OpenCV default) to RGB (MediaPipe requirement)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with the hand detection model
        results = self.hands.process(frame_rgb)

        # If hands are detected, draw their landmarks on the frame
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame,  # The image to draw on
                    hand_landmarks,  # The landmarks to draw
                    self.mp_hands.HAND_CONNECTIONS  # Predefined connections between landmarks
                )

        # Return the image with landmarks and the raw detection result
        return frame, results

    def is_fist(self, results):
        """
        Checks if the detected hand is making a fist.
        Returns True if all fingers (except thumb) are curled.
        """
        if not results.multi_hand_landmarks:
            return False

        hand = results.multi_hand_landmarks[0]  # Use only the first hand
        landmarks = hand.landmark

        # Tip and base landmark indices for fingers (excluding thumb)
        finger_tips = [8, 12, 16, 20]      # Index, Middle, Ring, Pinky tips
        finger_bases = [6, 10, 14, 18]     # Corresponding lower joints

        fingers_folded = 0

        for tip, base in zip(finger_tips, finger_bases):
            if landmarks[tip].y > landmarks[base].y:
                fingers_folded += 1

        # If 3 or more fingers are curled, call it a fist
        return fingers_folded >= 3
