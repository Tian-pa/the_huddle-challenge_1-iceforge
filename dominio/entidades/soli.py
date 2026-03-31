from dominio.base import EntidadDuelo

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
            return super().recargar()
        return f"¡{self.nombre} ya tiene su bala lista! No puede cargar más."
    
    def robar_bala(self, oponente):
        if self._turnos_para_robar >= 2:
            if oponente._balas > 0:
                oponente._balas -= 1
                msg = f"¡{self.nombre} le robó una bala a {oponente.nombre}!"
            else:
                msg = f"{self.nombre} intentó robar, pero no había balas."
            self._turnos_para_robar = -1
            return msg
        return "Habilidad aún en enfriamiento."

    def pasar_turno(self):
        super().pasar_turno()
        if self._turnos_para_robar < 2:
            self._turnos_para_robar += 1