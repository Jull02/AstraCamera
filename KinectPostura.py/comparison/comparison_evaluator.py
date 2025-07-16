class ComparisonEvaluator:
    @staticmethod
    def evaluar_rodillas(left_knee, right_knee, umbral=15):
        diferencia = abs(left_knee - right_knee)
        if diferencia > umbral:
            return "Asimetria en rodillas (posible lesion)"
        else:
            return "Rodillas simetricas"

    @staticmethod
    def evaluar_codos(left_elbow, right_elbow, umbral=15):
        diferencia = abs(left_elbow - right_elbow)
        if diferencia > umbral:
            return "Asimetria en codos (posible lesion)"
        else:
            return "Codos simetricos"
