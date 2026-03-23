from abc import ABC, abstractmethod

class EntidadDuelo(ABC):
    def __init__(self, nombre):
        self.nombre = nombre
        self._vidas = 3
        self._balas = 0
        self._esta_protegido = False

    @abstractmethod
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
            print(f"🛡️  ¡{self.nombre} bloqueó el ataque!")
        else:
            self._vidas -= danio
            print(f"💥 ¡{self.nombre} recibió {danio} de daño! Vidas: {self._vidas}")
        self._esta_protegido = False
    
    def entregar_bala(self):
        if self._balas > 0:
            self._balas -= 1
            return True
        return False
    
    def pasar_turno(self):
        self._esta_protegido = False
        if hasattr(self, '_turnos_para_robar'):
            self._turnos_para_robar += 1

    def esta_vivo(self):
        return self._vidas > 0

    def obtener_estado(self):
        return f"{self.nombre:12} | ❤️ HP: {self._vidas} | 🔫 Balas: {self._balas}"