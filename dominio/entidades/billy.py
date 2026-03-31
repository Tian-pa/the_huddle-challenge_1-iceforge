from dominio.base import EntidadDuelo

class BillyTheKid(EntidadDuelo):
    def __init__(self, nombre):
        super().__init__(nombre)
        self._capacidad_maxima = 3

    def mostrar_menu(self):
        return "1. Recargar | 2. Escudo | 3. Disparar (1 bala)"

    def recargar(self):
        if self._balas < self._capacidad_maxima:
            return super().recargar()
        return f"¡{self.nombre} tiene el tambor lleno!"