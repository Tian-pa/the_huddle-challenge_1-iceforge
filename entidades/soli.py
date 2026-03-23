from base import EntidadDuelo

class SoliTheOutlaw(EntidadDuelo):
    def __init__(self, nombre):
        # Llamamos al constructor del padre
        super().__init__(nombre)
        self._turnos_para_robar = 0 # Empezamos en 0

    def seleccionar_accion(self):
        """
        Interfaz de consola para Soli.
        """
        print(f"\n--- [ TURNO DE: {self.nombre.upper()} ] ---")
        print(f"Vidas: {self._vidas} | Carga: ({self._balas}/1)")
        print("-----------------------------------")
        print("1. [RECARGAR] (+1 bala)")
        print("2. [ESCUDO]   (Bloquea el siguiente ataque)")
        print("3. [DISPARAR] (Gasta 1 bala / Quita 1 vida)")
        
        # Soli sólo puede robar una bala cada dos turnos a sus oponentes
        if self._turnos_para_robar == 2:
            print("4. ¡¡ROBAR BALA!! (le quita una bala a su oponente)")
        else:
            print("X. [Aún no puedes robar, turno impar]")
        
        accion = input(">> Elegí tu movimiento: ")
        return accion
    
    def robar_bala(self, objetivo):
        """
        Utiliza el método entregar_bala del objetivo para obtener munición.
        """
        if self.turnos_para_robar >= 2:
            print(f'{self.nombre} usa su agilidad para robar!')

            # Intentamos obtener la bala del oponente
            exito = objetivo.entregar_bala()

            if exito:
                self._balas += 1
                print(f"¡Éxito! Robaste una bala de {objetivo.nombre}.")
            else:
                print(f"¡Fallaste! {objetivo.nombre} no tenía balas en su cinturón.")
        
            # Resetear el contador de la habilidad
            self._turnos_para_robar = 0
        else:
            print("Aún no podés robar, ¡esperá el momento justo!")