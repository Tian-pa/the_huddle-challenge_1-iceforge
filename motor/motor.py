import time
import os
import random
from ui.consola import ConsolaUI
from ui.interfaz import ARTE_PERSONAJES
# Se importan las subclases para poder instanciarse más tarde:
from dominio.entidades.billy import BillyTheKid
from dominio.entidades.soli import SoliTheOutlaw
from dominio.entidades.graham import GrahamTheFarmer

class JuegoPistolero:
    def __init__(self):
        self.j1 = None # Inicialización de referencias
        self.j2 = None # Inicialización de referencias
        self.turno_actual = 1
        self.esta_activo = True # Flag: bandera de control
        self.ui = ConsolaUI()

    def configurar_personajes(self):
        """Lógica de selección encapsulada"""
        self.j1 = self._menu_seleccion("JUGADOR")
        self.j2 = self._menu_seleccion("IA", es_ia=True)

    def _menu_seleccion(self, nombre, es_ia=False):
        if es_ia:
            opcion = str(random.randint(1, 3))
        else:
            opcion = self.ui.pedir_seleccion_personaje()  # <-- delegado

        if opcion == "1": return BillyTheKid(nombre)
        if opcion == "2": return SoliTheOutlaw(nombre)
        return GrahamTheFarmer(nombre)

    def iniciar(self):
        self.ui.mostrar_intro(self.j1, self.j2)   # <-- era mostrar_intro_visual()
        self.ui.limpiar_pantalla()
        self.ui.mostrar_mensaje(f"🔥 DUELO: {self.j1.nombre} vs {self.j2.nombre} 🔥")
        self.ui.pausa(1)

        while self.esta_activo:
            self.ui.mostrar_encabezado_duelo(self.j1, self.j2)
            self.ui.mostrar_numero_turno(self.turno_actual)
            self.ui.mostrar_menu_accion(self.j1)
            accion_h = self.ui.pedir_accion()

            # lógica IA (sin cambios)
            opciones_ia = ["1", "2"]
            if self.j2._balas >= self.j2._costo_disparo:
                opciones_ia.append("3")
            if hasattr(self.j2, '_turnos_para_robar') and self.j2._turnos_para_robar >= 2:
                opciones_ia.append("4")
            accion_ia = random.choice(opciones_ia)

            self.resolver_fases(accion_h, accion_ia)
            self.j1.pasar_turno()
            self.j2.pasar_turno()
            self.verificar_ganador()

            if self.esta_activo:
                self.ui.esperar_enter("Presioná ENTER para el siguiente turno")
                self.turno_actual += 1

    def resolver_fases(self, acc1, acc2):
        self.ui.mostrar_encabezado_resultados()

        # Fase 1: Preparación
        if acc1 == "2": self.ui.mostrar_mensaje(self.j1.cubrirse())
        if acc2 == "2": self.ui.mostrar_mensaje(self.j2.cubrirse())
        if acc1 == "1": self.ui.mostrar_mensaje(self.j1.recargar())
        if acc2 == "1": self.ui.mostrar_mensaje(self.j2.recargar())
        if acc1 == "4" and hasattr(self.j1, 'robar_bala'):
            self.ui.mostrar_mensaje(self.j1.robar_bala(self.j2))
        if acc2 == "4" and hasattr(self.j2, 'robar_bala'):
            self.ui.mostrar_mensaje(self.j2.robar_bala(self.j1))

        # Fase 2: Disparos
        for atacante, defensor, accion in [(self.j1, self.j2, acc1), (self.j2, self.j1, acc2)]:
            if accion == "3":
                if atacante._balas >= atacante._costo_disparo:
                    self.ui.mostrar_mensaje(f"¡{atacante.nombre} abre fuego!")
                    atacante._balas -= atacante._costo_disparo
                    self.ui.mostrar_mensaje(defensor.recibir_disparo(danio=atacante._danio_ataque))
                else:
                    self.ui.mostrar_mensaje(f"¡Click! {atacante.nombre} no tiene balas suficientes.")

    def verificar_ganador(self):
        if not self.j1.esta_vivo() and not self.j2.esta_vivo():
            self.ui.mostrar_ganador(False, False, self.j1.nombre, self.j2.nombre)
            self.esta_activo = False
        elif not self.j1.esta_vivo():
            self.ui.mostrar_ganador(False, True, self.j1.nombre, self.j2.nombre)
            self.esta_activo = False
        elif not self.j2.esta_vivo():
            self.ui.mostrar_ganador(True, False, self.j1.nombre, self.j2.nombre)
            self.esta_activo = False