import json
import os
from datetime import datetime


class SessionLogger:
    def __init__(self, patient_id, save_path="session_logs"):
        self.patient_id = patient_id
        self.save_path = save_path
        os.makedirs(save_path, exist_ok=True)
        self.session_data = {
            "patient_id": patient_id,
            "timestamp": datetime.now().isoformat(),
            "reference_range": {},
            "evaluated_range": {},
            "result": {}
        }

    def save_ranges(self, reference_range, evaluated_range):
        self.session_data["reference_range"] = reference_range
        self.session_data["evaluated_range"] = evaluated_range

    def save_result(self, result):
        self.session_data["result"] = result

    def save_to_file(self):
        filename = f"{self.patient_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = os.path.join(self.save_path, filename)
        with open(path, "w") as f:
            json.dump(self.session_data, f, indent=4)
        return path


# Ejemplo de uso
logger = SessionLogger(patient_id="P001")

reference_range = {"min": 85.0, "max": 170.0}
evaluated_range = {"min": 100.0, "max": 165.0}
result = {
    "pérdida_flexión": "15.0°",
    "pérdida_extensión": "5.0°",
    "diagnóstico": "Rango funcional alterado"
}

logger.save_ranges(reference_range, evaluated_range)
logger.save_result(result)
saved_path = logger.save_to_file()
saved_path
