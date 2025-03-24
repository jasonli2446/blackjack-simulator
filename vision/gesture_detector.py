import cv2
import mediapipe as mp
import numpy as np
import time


class GestureDetector:
    """Detects and classifies hand gestures for game control."""

    def __init__(self):
        """Initialize the gesture detector with MediaPipe Hands."""
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        # For tap gesture tracking
        self.last_tap_time = 0
        self.tap_count = 0
        self.tap_timeout = 1.0  # seconds

    def detect_gesture(self, frame):
        """
        Detect gesture in the frame.

        Args:
            frame (numpy.ndarray): The camera frame

        Returns:
            str: The detected gesture or None
        """
        if frame is None:
            return None

        # Convert to RGB (MediaPipe requires RGB input)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Hands
        results = self.hands.process(rgb_frame)

        # Draw hand landmarks on the frame (for debugging)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

                # Identify gesture based on landmarks
                return self._classify_gesture(hand_landmarks)

        return None

    def _classify_gesture(self, landmarks):
        """
        Classify the gesture based on hand landmarks.

        Args:
            landmarks: MediaPipe hand landmarks

        Returns:
            str: The classified gesture or None
        """
        # Extract key landmarks
        wrist = landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
        thumb_tip = landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]

        # Detect V shape (split) - index and middle fingers up
        if (
            index_tip.y < wrist.y
            and middle_tip.y < wrist.y
            and ring_tip.y > middle_tip.y
            and pinky_tip.y > middle_tip.y
        ):
            # Check if fingers are spread apart
            if abs(index_tip.x - middle_tip.x) > 0.05:
                return "split"

        # Detect one finger up (double down)
        if (
            index_tip.y < wrist.y
            and middle_tip.y > index_tip.y
            and ring_tip.y > index_tip.y
            and pinky_tip.y > index_tip.y
        ):
            return "double"

        # Detect wave no (stand) - hand moving horizontally
        # This is more complex and would need tracking across frames
        # For now, we'll detect a flat hand with fingers together
        if (
            abs(index_tip.y - middle_tip.y) < 0.03
            and abs(middle_tip.y - ring_tip.y) < 0.03
            and abs(ring_tip.y - pinky_tip.y) < 0.03
            and all(
                tip.y < wrist.y for tip in [index_tip, middle_tip, ring_tip, pinky_tip]
            )
        ):
            return "stand"

        # Detect tap (hit) - closed fist
        if (
            index_tip.y > wrist.y
            and middle_tip.y > wrist.y
            and ring_tip.y > wrist.y
            and pinky_tip.y > wrist.y
        ):
            current_time = time.time()

            # Reset tap count if too much time has passed
            if current_time - self.last_tap_time > self.tap_timeout:
                self.tap_count = 0

            self.tap_count += 1
            self.last_tap_time = current_time

            # Detect double tap
            if self.tap_count >= 2:
                self.tap_count = 0
                return "hit"

        return None
