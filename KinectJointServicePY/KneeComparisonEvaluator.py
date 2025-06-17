class KneeComparisonEvaluator:
    def __init__(self):
        self.reference_range = {"min": None, "max": None}
        self.evaluated_range = {"min": None, "max": None}

    def update_ranges(self, angle_sana, angle_afectada):
        self.reference_range["min"] = min(
            self.reference_range["min"] or angle_sana, angle_sana)
        self.reference_range["max"] = max(
            self.reference_range["max"] or angle_sana, angle_sana)

        self.evaluated_range["min"] = min(
            self.evaluated_range["min"] or angle_afectada, angle_afectada)
        self.evaluated_range["max"] = max(
            self.evaluated_range["max"] or angle_afectada, angle_afectada)

    def diagnosticar(self):
        min_ref = self.reference_range["min"]
        max_ref = self.reference_range["max"]
        min_eval = self.evaluated_range["min"]
        max_eval = self.evaluated_range["max"]

        flexion_dif = abs(min_ref - min_eval)
        extension_dif = abs(max_ref - max_eval)

        resultado = {
            "pérdida_flexión": f"{flexion_dif:.1f}°",
            "pérdida_extensión": f"{extension_dif:.1f}°",
            "diagnóstico": "Rango funcional alterado" if flexion_dif > 10 or extension_dif > 5 else "Rango funcional dentro de lo esperado"
        }

        return resultado
