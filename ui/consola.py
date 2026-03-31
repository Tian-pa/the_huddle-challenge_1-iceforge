import os
import time
from ui.interfaz import ARTE_PERSONAJES

class ConsolaUI:
    """
    Responsabilidad única: toda interacción con la terminal.
    Ningún otro módulo debe usar print(), input() ni os.system().
    """

    # ─── Utilidades básicas ────────────────────────────────────────────────

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def esperar_enter(self, mensaje="Presioná ENTER para continuar"):
        input(f"\n[{mensaje}]")

    def pausa(self, segundos=1):
        time.sleep(segundos)

    # ─── Selección de personaje ────────────────────────────────────────────

    def mostrar_menu_personajes(self):
        self.limpiar_pantalla()
        print("--- JUGADOR, ELIGE TU PERSONAJE ---")
        print("1. Billy the Kid  (Max 3 balas)")
        print("2. Soli the Outlaw  (Puede robar)")
        print("3. Graham the Farmer  (Daño x2)")

    def pedir_seleccion_personaje(self):
        """Retorna '1', '2' o '3'. Valida hasta obtener entrada correcta."""
        while True:
            self.mostrar_menu_personajes()
            opcion = input(">> Seleccioná (1-3): ")
            if opcion in ["1", "2", "3"]:
                return opcion
            print("Opción inválida. Intentá de nuevo.")

    # ─── Intro visual ─────────────────────────────────────────────────────

    def mostrar_intro(self, j1, j2):
        self.limpiar_pantalla()
        print("\n" + "=" * 80)
        print("🔥 ¡DUELO EN EL LEJANO OESTE! 🔥".center(80))
        print("=" * 80 + "\n")

        lineas_j1 = ARTE_PERSONAJES.get(type(j1).__name__, ["Sin Arte"] * 15)
        lineas_j2 = ARTE_PERSONAJES.get(type(j2).__name__, ["Sin Arte"] * 15)

        for i in range(15):
            l1 = lineas_j1[i].ljust(40)
            l2 = lineas_j2[i].rjust(40)
            print(f"{l1}   VS   {l2}")

        nombre1 = f"[{j1.nombre}]".center(40)
        nombre2 = f"[{j2.nombre}]".center(40)
        print(f"\n{nombre1}        {nombre2}")
        print("\n" + "=" * 80)
        self.esperar_enter("Presioná ENTER para desenvainar...")

    # ─── Estado del turno ─────────────────────────────────────────────────

    def mostrar_encabezado_duelo(self, j1, j2):
        self.limpiar_pantalla()
        print(f" {j1.nombre} ({type(j1).__name__}) ".center(50, "="))
        print(j1.obtener_estado())
        print("-" * 50)
        print(f" {j2.nombre} ({type(j2).__name__}) ".center(50, "="))
        print(j2.obtener_estado())
        print("=" * 50)

    def mostrar_numero_turno(self, turno):
        print(f"\n>>> TURNO {turno} <<<")

    def mostrar_menu_accion(self, jugador):
        print(jugador.mostrar_menu())

    def pedir_accion(self):
        """Retorna el string de acción ingresado por el usuario."""
        return input(">> Tu acción: ")

    # ─── Resultados de acciones ────────────────────────────────────────────

    def mostrar_encabezado_resultados(self):
        print("\n--- RESULTADOS DEL TURNO ---")

    def mostrar_mensaje(self, mensaje):
        """Canal general para que las entidades comuniquen resultados."""
        print(mensaje)

    # ─── Fin de partida ────────────────────────────────────────────────────

    def mostrar_ganador(self, j1_vivo, j2_vivo, nombre_j1, nombre_j2):
        if not j1_vivo and not j2_vivo:
            print("\n💀 ¡EMPATE! Ambos cayeron.")
        elif not j1_vivo:
            print(f"\n🏆 GANADOR: {nombre_j2}")
        elif not j2_vivo:
            print(f"\n🏆 GANADOR: {nombre_j1}")