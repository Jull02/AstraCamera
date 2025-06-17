class SquatTracker:
    def __init__(self, min_angle=90, max_angle=170):
        self.min_angle = min_angle      # Ángulo al estar agachado
        self.max_angle = max_angle      # Ángulo al estar de pie
        self.count = 0
        self.in_squat = False           # Indica si está en sentadilla
        self.ready_to_start = False     # Solo se activa al estar primero de pie

    def update(self, angle):
        # Estado inicial: el usuario debe estar de pie para habilitar el conteo
        if angle >= self.max_angle and not self.ready_to_start:
            self.ready_to_start = True  # Ya puede iniciar sentadilla

        # Si bajó a posición de sentadilla desde estado válido
        if self.ready_to_start and angle <= self.min_angle and not self.in_squat:
            self.in_squat = True

        # Si subió completamente después de bajar: cuenta sentadilla
        elif angle >= self.max_angle and self.in_squat:
            self.count += 1
            self.in_squat = False
            self.ready_to_start = False  # Requiere volver a estar de pie antes de otra

    def get_count(self):
        return self.count
