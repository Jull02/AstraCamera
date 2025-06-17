class Clasificador:
    def interpretar(self, angulo: float) -> dict:
        """Interpreta el ángulo de flexión de rodilla basado en la tabla clínica"""
        if angulo > 180:
            return {
                "nivel": "Hiperextension",
                "descripcion": "Solo normal en personas hiperlaxas, potencialmente riesgoso",
                "normal": False
            }
        elif angulo >= 170:
            return {
                "nivel": "Extension completa (posición de pie)",
                "descripcion": "Si, extension anatómicamente normal",
                "normal": True
            }
        elif 160 <= angulo <= 169:
            return {
                "nivel": "Extension incompleta o ligera flexion",
                "descripcion": "Si, dentro de lo funcional pero no completamente extendido",
                "normal": True
            }
        elif 130 <= angulo <= 159:
            return {
                "nivel": "Flexion leve o moderada",
                "descripcion": "Si, típico al caminar o bajar escaleras",
                "normal": True
            }
        elif 90 <= angulo <= 129:
            return {
                "nivel": "Flexion moderada (sentado/sentadilla estándar)",
                "descripcion": "Si, común al sentarse o en sentadilla estándar",
                "normal": True
            }
        else:  # ángulo < 90
            return {
                "nivel": "Flexion profunda (cuclillas)",
                "descripcion": "Si, especialmente en actividades deportivas o sentadillas profundas",
                "normal": True
            }
