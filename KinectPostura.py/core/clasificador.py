class Clasificador:
    @staticmethod
    def movimiento_codo(angulo):
        if angulo > 160:
            return "Extension de codo"
        elif angulo < 70:
            return "Flexion de codo"
        else:
            return "Neutro"

    @staticmethod
    def movimiento_rodilla(angulo):
        if angulo > 160:
            return "Extension de rodilla"
        elif angulo < 90:
            return "Flexion de rodilla"
        else:
            return "Neutro"

    @staticmethod
    def diagnostico_general(left_knee, right_knee):
        if 80 <= left_knee <= 110 and 80 <= right_knee <= 110:
            return "correcto"
        else:
            return "incorrecto"
