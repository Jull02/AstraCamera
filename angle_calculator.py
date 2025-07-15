import math


class AngleCalculator:
    @staticmethod
    def calculate_angle(a, b, c):
        ang = math.degrees(
            math.atan2(c[1] - b[1], c[0] - b[0]) -
            math.atan2(a[1] - b[1], a[0] - b[0])
        )
        return abs((ang + 360) % 360) if ang < 0 else ang
