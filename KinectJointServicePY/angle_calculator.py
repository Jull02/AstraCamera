import numpy as np


class AngleCalculator:
    def calculate_knee_angle(self, joints, side="left"):
        """Calcula el ángulo de la rodilla izquierda o derecha"""
        try:
            if side == "left":
                hip = joints.get("HipLeft")
                knee = joints.get("KneeLeft")
                ankle = joints.get("AnkleLeft")
            else:
                hip = joints.get("HipRight")
                knee = joints.get("KneeRight")
                ankle = joints.get("AnkleRight")

            if not hip or not knee or not ankle:
                print("Articulaciones faltantes para", side)
                return 0

            v1 = np.array([hip["x"] - knee["x"], hip["y"] -
                          knee["y"], hip["z"] - knee["z"]])
            v2 = np.array([ankle["x"] - knee["x"], ankle["y"] -
                          knee["y"], ankle["z"] - knee["z"]])

            v1 /= np.linalg.norm(v1)
            v2 /= np.linalg.norm(v2)

            dot_product = np.dot(v1, v2)
            angle_rad = np.arccos(np.clip(dot_product, -1.0, 1.0))
            return np.degrees(angle_rad)

        except Exception as e:
            print("Error calculando ángulo:", e)
            return 0

    def calculate_both_knees(self, joints):
        """Devuelve un diccionario con los ángulos de ambas rodillas"""
        left = self.calculate_knee_angle(joints, "left")
        right = self.calculate_knee_angle(joints, "right")
        return {
            "left_knee_angle": left,
            "right_knee_angle": right
        }
