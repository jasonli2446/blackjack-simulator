import cv2
import time
from input.input_handler import InputHandler
from vision.camera import Camera
from vision.gesture_detector import GestureDetector
from game.strategy import Strategy


class VideoInputHandler(InputHandler):
    """Handles player input from video gestures."""

    def __init__(self, keyboard_fallback=True, display_video=True):
        """
        Initialize the video input handler.

        Args:
            keyboard_fallback (bool): Whether to fall back to keyboard input
            display_video (bool): Whether to display the video feed
        """
        self.camera = None
        self.detector = None
        self.keyboard_fallback = keyboard_fallback
        self.display_video = display_video
        self.last_gesture = None
        self.last_gesture_time = 0
        self.gesture_cooldown = 2.0  # seconds

    def setup(self):
        """Setup the camera and gesture detector."""
        try:
            self.camera = Camera()
            self.camera.start()
            self.detector = GestureDetector()
            if self.display_video:
                cv2.namedWindow("Blackjack Gesture Control", cv2.WINDOW_NORMAL)
            return True
        except Exception as e:
            print(f"Error setting up video input: {e}")
            return False

    def cleanup(self):
        """Clean up camera resources."""
        if self.camera:
            self.camera.stop()
        if self.display_video:
            cv2.destroyAllWindows()

    def get_action(self):
        """
        Get the player's action from video gestures.

        Returns:
            str: The action to take (hit, stand, double, split)
        """
        start_time = time.time()
        last_print_time = 0
        print_interval = 1.0  # seconds

        print(
            "Waiting for gesture (hit: tap twice, stand: wave, double: one finger, split: V sign)"
        )
        print("Press 'q' to use keyboard input instead")

        while time.time() - start_time < 10.0:  # Timeout after 10 seconds
            # Get frame and detect gesture
            frame = self.camera.get_frame()
            if frame is not None:
                gesture = self.detector.detect_gesture(frame)

                # Display the frame
                if self.display_video:
                    # Add gesture text to frame
                    if gesture:
                        cv2.putText(
                            frame,
                            f"Detected: {gesture}",
                            (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            2,
                        )
                    cv2.imshow("Blackjack Gesture Control", frame)

                # Process gesture if detected
                if gesture:
                    current_time = time.time()

                    # Enforce cooldown to prevent accidental double-detection
                    if current_time - self.last_gesture_time > self.gesture_cooldown:
                        self.last_gesture = gesture
                        self.last_gesture_time = current_time

                        # Map gesture to game action
                        if gesture == "hit":
                            print("Gesture detected: HIT")
                            return Strategy.HIT
                        elif gesture == "stand":
                            print("Gesture detected: STAND")
                            return Strategy.STAND
                        elif gesture == "double":
                            print("Gesture detected: DOUBLE")
                            return Strategy.DOUBLE
                        elif gesture == "split":
                            print("Gesture detected: SPLIT")
                            return Strategy.SPLIT

            # Print waiting message every second
            current_time = time.time()
            if current_time - last_print_time > print_interval:
                print("Waiting for gesture...")
                last_print_time = current_time

            # Check for keyboard interrupt
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        # Fall back to keyboard input if enabled
        if self.keyboard_fallback:
            print("No gesture detected or interrupted. Using keyboard input.")
            from input.keyboard_input import KeyboardInputHandler

            keyboard_handler = KeyboardInputHandler()
            return keyboard_handler.get_action()

        return None

    def is_quit(self):
        """
        Check if the player wants to quit.

        Returns:
            bool: True if quit requested, False otherwise
        """
        # We'll use keyboard for quit detection
        from input.keyboard_input import KeyboardInputHandler

        keyboard_handler = KeyboardInputHandler()
        return keyboard_handler.is_quit()

    def get_bet_amount(self, current_balance):
        """
        Get the bet amount from the player.

        Args:
            current_balance (float): Player's current balance

        Returns:
            float or str: The bet amount or command
        """
        # We'll use keyboard for bet amount input
        from input.keyboard_input import KeyboardInputHandler

        keyboard_handler = KeyboardInputHandler()
        return keyboard_handler.get_bet_amount(current_balance)
