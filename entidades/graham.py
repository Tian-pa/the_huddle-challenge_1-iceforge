from base import EntidadDuelo

class GrahamTheFarmer(EntidadDuelo):
    def __init__(self, nombre):
        super().__init__(nombre)
        self._limite_balas = 2 # Solo dos cañones

    def seleccionar_accion(self):
        """
        Interfaz de consola para Graham.
        """
        print(f"\n--- [ TURNO DE: {self.nombre.upper()} ] ---")
        print(f"Vidas: {self._vidas} | Carga: ({self._balas}/2)")
        print("-----------------------------------")
        print("1. RECARGAR (Mete un cartucho)")
        print("2. ESCUDO   (Bloquea el siguiente ataque)")
        # Graham solo puede disparar si tiene el arma cargada (2 balas)
        if self._balas == 2:
            print("3. ¡DISPARAR ESCOPETA! (Gasta 2 balas, quita 2 vidas)")
        else:
            print("X. [Aún no podes disparar, necesitas dos balas en tu cargador]")
        
        accion = input(">> Elegí tu movimiento: ")
        return accion

    def disparar(self, objetivo):
        if self._balas >= 2:
            print(f"¡BOOM! {self.nombre} descarga ambos cañones.")
            self._balas -= 2
            # Aquí llamamos al método del oponente pasando 2 de daño
            objetivo.recibir_disparo(danio=2)
        else:
            print(f"{self.nombre} intenta disparar pero la escopeta está incompleta.")