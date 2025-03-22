import cv2
import threading
import time


class Camera:
    """Manages camera input for the game."""

    def __init__(self, camera_id=0, width=640, height=480):
        """
        Initialize the camera.

        Args:
            camera_id (int): Camera device ID (default: 0)
            width (int): Frame width (default: 640)
            height (int): Frame height (default: 480)
        """
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap = None
        self.frame = None
        self.running = False
        self.thread = None
        self.lock = threading.Lock()

    def start(self):
        """Start the camera capture thread."""
        self.cap = cv2.VideoCapture(self.camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")

        self.running = True
        self.thread = threading.Thread(target=self._capture_loop)
        self.thread.daemon = True
        self.thread.start()

        # Give the camera time to warm up
        time.sleep(1.0)

    def _capture_loop(self):
        """Continuously capture frames from the camera."""
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.frame = frame
            time.sleep(0.03)  # ~30 FPS

    def get_frame(self):
        """
        Get the current frame from the camera.

        Returns:
            numpy.ndarray: The current frame, or None if no frame is available
        """
        with self.lock:
            return self.frame.copy() if self.frame is not None else None

    def stop(self):
        """Stop the camera capture thread and release resources."""
        self.running = False
        if self.thread is not None:
            self.thread.join(timeout=1.0)

        if self.cap is not None:
            self.cap.release()
