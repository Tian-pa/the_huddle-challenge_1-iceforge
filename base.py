from abc import ABC, abstractmethod

class EntidadDuelo(ABC):
    def __init__(self, nombre):
        self.nombre = nombre
        self._vidas = 3
        self._balas = 0
        self._esta_protegido = False

    @abstractmethod
    def seleccionar_accion(self):
        """
        Este método será el cerebro. 
        En el Humano pedirá input(), en el Bot será un random.
        """
        pass

    def recargar(self):
        # Lógica base: ¿Debería ser igual para todos?
        self._balas += 1
        print(f"{self.nombre} está cargando su arma...")

    def cubrirse(self):
        self._esta_protegido = True
        print(f"{self.nombre} se pone a cubierto.")

    def recibir_disparo(self, danio=1):
        if self._esta_protegido:
            print(f"¡{self.nombre} bloqueó el ataque!")
        else:
            self._vidas -= danio
            print(f"¡{self.nombre} recibió {danio} de daño! Vidas restantes: {self._vidas}")
        
        # Resetear protección para el siguiente turno
        self._esta_protegido = False
    
    def entregar_bala(self):
        """
        Método para el encapsulamiento: la propia clase gestiona su inventario.
        Retorna True si tenía una bala para dar, False si estaba vacía.
        """
        if self._balas > 0:
            self._balas -= 1
            return True
        return False
    
    def pasar_turno(self):
        """Lógica que ocurre al final de cada turno"""
        # Por defecto, solo reseteamos el escudo por si no recibió disparos
        self._esta_protegido = False
        
        # Si el personaje tiene el contador de Soli, lo sumamos
        if hasattr(self, '_turnos_para_robar'):
            self._turnos_para_robar += 1

    def esta_vivo(self):
        """
        Retorna True si al personaje le quedan vidas, False si no.
        """
        return self._vidas > 0