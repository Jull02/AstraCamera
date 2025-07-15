class JointExtractor:
    def __init__(self, landmarks, width, height):
        self.landmarks = landmarks
        self.width = width
        self.height = height

    def get_point(self, idx):
        lm = self.landmarks[idx]
        return int(lm.x * self.width), int(lm.y * self.height)
