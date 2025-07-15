import winsound  # Solo en Windows
# import os
# os.system('echo -e "\\a"')


class Validator:
    left_squat_down = False
    right_squat_down = False
    left_squat_count = 0
    right_squat_count = 0

    @staticmethod
    def beep():
        duration = 200  # ms
        freq = 1000     # Hz
        winsound.Beep(freq, duration)

    @staticmethod
    def update_squat_count(left_knee_angle, right_knee_angle, low_thresh=90, high_thresh=160):
        if left_knee_angle < low_thresh:
            Validator.left_squat_down = True
        if Validator.left_squat_down and left_knee_angle > high_thresh:
            Validator.left_squat_count += 1
            Validator.left_squat_down = False
            Validator.beep()

        if right_knee_angle < low_thresh:
            Validator.right_squat_down = True
        if Validator.right_squat_down and right_knee_angle > high_thresh:
            Validator.right_squat_count += 1
            Validator.right_squat_down = False
            Validator.beep()

    @staticmethod
    def is_anomalous_angle(joint, angle):
        limits = {
            "KNEE": (30, 180),
            "ELBOW": (20, 180)
        }
        joint_key = "KNEE" if "KNEE" in joint.upper() else "ELBOW"
        low, high = limits[joint_key]
        return angle < low or angle > high

    @staticmethod
    def is_warning_angle(joint, angle):
        limits = {
            "KNEE": (30, 180),
            "ELBOW": (20, 180)
        }
        joint_key = "KNEE" if "KNEE" in joint.upper() else "ELBOW"
        low, high = limits[joint_key]
        return (low <= angle < low + 10) or (high - 10 < angle <= high)

    @staticmethod
    def get_angle_color(joint, angle):
        if Validator.is_anomalous_angle(joint, angle):
            return (0, 0, 255)      # rojo
        elif Validator.is_warning_angle(joint, angle):
            return (0, 165, 255)    # naranja
        else:
            return (255, 255, 255)  # blanco
