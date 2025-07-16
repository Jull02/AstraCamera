# Archivo: angle_calculator.py

import math


class AngleCalculator:
    @staticmethod
    def calculate_angle(a, b, c):
        ang = math.degrees(
            math.atan2(c[1] - b[1], c[0] - b[0]) -
            math.atan2(a[1] - b[1], a[0] - b[0])
        )
        return abs((ang + 360) % 360) if ang < 0 else ang

    @staticmethod
    def calculate_knee_angles(landmarks):
        right_hip = landmarks.get('RIGHT_HIP')
        right_knee = landmarks.get('RIGHT_KNEE')
        right_ankle = landmarks.get('RIGHT_ANKLE')

        left_hip = landmarks.get('LEFT_HIP')
        left_knee = landmarks.get('LEFT_KNEE')
        left_ankle = landmarks.get('LEFT_ANKLE')

        if None in [right_hip, right_knee, right_ankle, left_hip, left_knee, left_ankle]:
            return {'right_knee': None, 'left_knee': None}

        right_knee_angle = AngleCalculator.calculate_angle(
            right_hip, right_knee, right_ankle)
        left_knee_angle = AngleCalculator.calculate_angle(
            left_hip, left_knee, left_ankle)

        return {
            'right_knee': right_knee_angle,
            'left_knee': left_knee_angle
        }

    @staticmethod
    def calculate_elbow_angles(landmarks):
        right_shoulder = landmarks.get('RIGHT_SHOULDER')
        right_elbow = landmarks.get('RIGHT_ELBOW')
        right_wrist = landmarks.get('RIGHT_WRIST')

        left_shoulder = landmarks.get('LEFT_SHOULDER')
        left_elbow = landmarks.get('LEFT_ELBOW')
        left_wrist = landmarks.get('LEFT_WRIST')

        if None in [right_shoulder, right_elbow, right_wrist, left_shoulder, left_elbow, left_wrist]:
            return {'right_elbow': None, 'left_elbow': None}

        right_elbow_angle = AngleCalculator.calculate_angle(
            right_shoulder, right_elbow, right_wrist)
        left_elbow_angle = AngleCalculator.calculate_angle(
            left_shoulder, left_elbow, left_wrist)

        return {
            'right_elbow': right_elbow_angle,
            'left_elbow': left_elbow_angle
        }

    @staticmethod
    def calculate_all_angles(landmarks):
        knees = AngleCalculator.calculate_knee_angles(landmarks)
        elbows = AngleCalculator.calculate_elbow_angles(landmarks)
        return {**knees, **elbows}
