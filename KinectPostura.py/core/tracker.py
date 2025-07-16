class Tracker:
    def __init__(self, umbral=3.0, max_frames_sin_cambio=15):
        self.ultimo_valor = {}
        self.frames_estaticos = {}
        self.umbral = umbral
        self.max_frames = max_frames_sin_cambio

    def actualizar(self, nombre, valor_actual):
        if nombre not in self.ultimo_valor:
            self.ultimo_valor[nombre] = valor_actual
            self.frames_estaticos[nombre] = 0
            return "moviendo"

        diferencia = abs(valor_actual - self.ultimo_valor[nombre])
        if diferencia < self.umbral:
            self.frames_estaticos[nombre] += 1
        else:
            self.frames_estaticos[nombre] = 0

        self.ultimo_valor[nombre] = valor_actual

        if self.frames_estaticos[nombre] >= self.max_frames:
            return "sin movimiento"
        else:
            return "moviendo"
