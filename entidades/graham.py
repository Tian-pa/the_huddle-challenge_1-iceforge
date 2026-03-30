from base import EntidadDuelo

class GrahamTheFarmer(EntidadDuelo):
    def __init__(self, nombre):
        super().__init__(nombre)
        self._limite_balas = 2
        self._costo_disparo = 2
        self._danio_ataque = 2

    def mostrar_menu(self):
        menu = "1. Recargar | 2. Escudo"
        if self._balas >= 2:
            menu += " | 3. ¡DOBLE DISPARO! (2 balas)"
        else:
            menu += " | (Necesitás 2 balas para disparar)"
        return menu
    
    def recargar(self):
        if self._balas < 2:
            super().recargar()
        else:
            print(f"¡La escopeta de {self.nombre} ya está llena (2/2)!")

    def puede_disparar(self):
        """Sobrescribe la base para asegurar que Graham solo dispare con 2 balas exactas"""
        return self._balas >= 2