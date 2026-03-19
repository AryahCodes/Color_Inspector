import cv2


class VideoLoader:
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {path}")
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def sample_frames(self, interval_sec):
        frame_skip = int(self.fps * interval_sec)
        if frame_skip == 0:
            frame_skip = 1
        i = 0
        while True:
            frame_num = i * frame_skip
            if frame_num >= self.total_frames:
                break
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = self.cap.read()
            if not ret:
                break
            timestamp_sec = frame_num / self.fps
            yield (timestamp_sec, frame)
            i += 1

    def release(self):
        if self.cap.isOpened():
            self.cap.release()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False
