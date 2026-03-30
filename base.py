from abc import ABC, abstractmethod

class EntidadDuelo(ABC): # define una clase base abstracta
    def __init__(self, nombre): 
        self.nombre = nombre
        self._vidas = 3
        self._balas = 0
        self._esta_protegido = False
        self._costo_disparo = 1
        self._danio_ataque = 1

    @abstractmethod # método abstracto - se declara pero se implementa en cada una de las subclases
    def mostrar_menu(self): 
        """Retorna el texto del menú para este personaje"""
        pass

    def recargar(self):
        self._balas += 1
        print(f"-> {self.nombre} cargó una bala.")

    def cubrirse(self):
        self._esta_protegido = True
        print(f"-> {self.nombre} se puso a cubierto.")

    def recibir_disparo(self, danio=1):
        if self._esta_protegido:
            print(f" PROTECCION: ¡{self.nombre} bloqueó el ataque!")
        else:
            self._vidas -= danio
            print(f"BANG: ¡{self.nombre} recibió {danio} de daño! Vidas: {self._vidas}")
        self._esta_protegido = False
    
    def pasar_turno(self):
        self._esta_protegido = False

    def esta_vivo(self):
        return self._vidas > 0

    def obtener_estado(self):
        return f"{self.nombre:12} | VIDAS: {self._vidas} | BALAS: {self._balas}"
    
    def puede_disparar(self):
        """Verifica si tiene las balas necesarias para su tipo de ataque"""
        return self._balas >= self._costo_disparo