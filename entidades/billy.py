from base import EntidadDuelo

class BillyTheKid(EntidadDuelo):
    def __init__(self, nombre):
        # Llamamos al constructor del padre
        super().__init__(nombre)
        # Atributo único de Billy: capacidad del tambor
        self._capacidad_maxima = 3

    def seleccionar_accion(self):
        """
        Interfaz de consola para Billy. 
        Muestra su estado actual de carga (1/3, 2/3, etc.)
        """
        print(f"\n--- [ TURNO DE: {self.nombre.upper()} ] ---")
        print(f"Vidas: {self._vidas} | Carga: ({self._balas}/{self._capacidad_maxima})")
        print("-----------------------------------")
        print("1. [RECARGAR] (+1 bala)")
        print("2. [ESCUDO]   (Bloquea el siguiente ataque)")
        print("3. [DISPARAR] (Gasta 1 bala / Quita 1 vida)")
        
        accion = input(" Elegí tu movimiento: ")
        return accion

    def recargar(self):
        """Sobrescribimos para añadir el límite de 3 balas"""
        if self._balas < self._capacidad_maxima:
            super().recargar() # Usamos la lógica del padre para sumar la bala
        else:
            print(f"¡{self.nombre} ya tiene el tambor lleno! No podés cargar más.")

    def disparar(self, objetivo):
        """Lógica de disparo estándar pero condicionada a sus balas"""
        if self._balas > 0:
            print(f"¡BANG! {self.nombre} dispara con rapidez.")
            self._balas -= 1
            # Respetamos el encapsulamiento llamando al método del oponente
            objetivo.recibir_disparo(danio=1)
        else:
            print(f"¡CLICK! {self.nombre} intentó disparar sin balas. ¡Qué error!")