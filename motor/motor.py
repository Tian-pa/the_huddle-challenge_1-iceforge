import random
from ui.consola import ConsolaUI
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
        self.ui = ConsolaUI() # Referencia a objeto - llamando a la clase ConsolaUI
        # Permite que el motor use todos los métodos de la consola sin tener que heredar de ella

    def configurar_personajes(self):
        """Lógica de selección encapsulada"""
        self.j1 = self._menu_seleccion("JUGADOR")
        self.j2 = self._menu_seleccion("IA", es_ia=True)

    def _menu_seleccion(self, nombre, es_ia=False):
        if es_ia:
            opcion = str(random.randint(1, 3))
        else:
            opcion = self.ui.pedir_seleccion_personaje()

        # Instanciación
        if opcion == "1": return BillyTheKid(nombre)
        if opcion == "2": return SoliTheOutlaw(nombre)
        return GrahamTheFarmer(nombre)

    def iniciar(self):
        self.ui.mostrar_intro(self.j1, self.j2)   # Se muestra la intro visual
        self.ui.limpiar_pantalla()
        self.ui.mostrar_mensaje(f"🔥 DUELO: {self.j1.nombre} vs {self.j2.nombre} 🔥")
        self.ui.pausa(1)

        while self.esta_activo:
            self.ui.mostrar_encabezado_duelo(self.j1, self.j2)
            self.ui.mostrar_numero_turno(self.turno_actual)
            self.ui.mostrar_menu_accion(self.j1)
            accion_h = self.ui.pedir_accion()

            # lógica IA
            opciones_ia = ["1", "2"]

            # Se aplica una regla polimórfica, sólo se disparará si tiene las balas que su clase requiere
            # Si es Graham pide 2, si es Billy o Soli pide 1.
            if self.j2._balas >= self.j2._costo_disparo:
                opciones_ia.append("3")

            # Si la IA es Soli y su habilidad (4) no está en enfriamiento:
            if hasattr(self.j2, '_turnos_para_robar') and self.j2._turnos_para_robar >= 2:
                opciones_ia.append("4")
            accion_ia = random.choice(opciones_ia)

            self.resolver_fases(accion_h, accion_ia)
            self.j1.pasar_turno() # Se desactivan las protecciones
            self.j2.pasar_turno() # //////////////////////////////
            self.verificar_ganador()

            if self.esta_activo:
                self.ui.esperar_enter("Presioná ENTER para el siguiente turno")
                self.turno_actual += 1

    def resolver_fases(self, acc1, acc2):
        self.ui.mostrar_encabezado_resultados()

        # Fase 1: Preparación

        # Protección
        if acc1 == "2": self.ui.mostrar_mensaje(self.j1.cubrirse())
        if acc2 == "2": self.ui.mostrar_mensaje(self.j2.cubrirse())

        # Recargar arma
        if acc1 == "1": self.ui.mostrar_mensaje(self.j1.recargar())
        if acc2 == "1": self.ui.mostrar_mensaje(self.j2.recargar())

        # Habilidades únicas (Soli robar)
        if acc1 == "4" and hasattr(self.j1, 'robar_bala'):
            self.ui.mostrar_mensaje(self.j1.robar_bala(self.j2))
        if acc2 == "4" and hasattr(self.j2, 'robar_bala'):
            self.ui.mostrar_mensaje(self.j2.robar_bala(self.j1))

        # Fase 2: Resolución de Disparos
        # Usamos una lista de tuplas para procesar ambos jugadores con la misma lógica
        for atacante, defensor, accion in [(self.j1, self.j2, acc1), (self.j2, self.j1, acc2)]:
            if accion == "3":
                if atacante._balas >= atacante._costo_disparo:
                    self.ui.mostrar_mensaje(f"¡{atacante.nombre} abre fuego!")
                    atacante._balas -= atacante._costo_disparo
                    self.ui.mostrar_mensaje(defensor.recibir_disparo(danio=atacante._danio_ataque))
                else:
                    self.ui.mostrar_mensaje(f"¡Click! {atacante.nombre} no tiene balas suficientes.")

    def verificar_ganador(self):
        if not self.j1.esta_vivo() and not self.j2.esta_vivo(): # En el caso de empate
            self.ui.mostrar_ganador(False, False, self.j1.nombre, self.j2.nombre)
            self.esta_activo = False
        elif not self.j1.esta_vivo(): # En el caso de que el usuario pierda
            self.ui.mostrar_ganador(False, True, self.j1.nombre, self.j2.nombre)
            self.esta_activo = False
        elif not self.j2.esta_vivo(): # En el caso de que la IA pierda
            self.ui.mostrar_ganador(True, False, self.j1.nombre, self.j2.nombre)
            self.esta_activo = False