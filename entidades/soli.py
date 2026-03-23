from base import EntidadDuelo

class SoliTheOutlaw(EntidadDuelo):
    def __init__(self, nombre):
        super().__init__(nombre)
        self._turnos_para_robar = 0

    def mostrar_menu(self):
        menu = "1. Recargar | 2. Escudo | 3. Disparar"
        if self._turnos_para_robar >= 2:
            menu += " | 4. ¡ROBAR BALA!"
        return menu
    
    def recargar(self):
        if self._balas < 1:
            super().recargar()
        else:
            print(f"¡{self.nombre} ya tiene su bala lista! No puede cargar más.")
    
    def robar_bala(self, objetivo):
        if self._turnos_para_robar >= 2:
            exito = objetivo.entregar_bala()
            if exito:
                self._balas += 1
                print(f"¡{self.nombre} le robó una bala a {objetivo.nombre}!")
            else:
                print(f"¡{self.nombre} intentó robar pero no había nada!")
            self._turnos_para_robar = 0