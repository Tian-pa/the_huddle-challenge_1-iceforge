import time
import os
import random
from interfaz import ARTE_PERSONAJES

class JuegoPistolero:
    def __init__(self, j1, j2):
        self.j1 = j1
        self.j2 = j2
        self.turno_actual = 1
        self.esta_activo = True

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_intro_visual(self):
        self.limpiar_pantalla()
        print("\n" + "="*80)
        print("🔥 ¡DUELO EN EL LEJANO OESTE! 🔥".center(80))
        print("="*80 + "\n")

        # Obtenemos las listas de líneas
        lineas_j1 = ARTE_PERSONAJES.get(type(self.j1).__name__, ["Sin Arte"]*15)
        lineas_j2 = ARTE_PERSONAJES.get(type(self.j2).__name__, ["Sin Arte"]*15)

        # Imprimimos línea por línea pegándolas
        for i in range(15):
            l1 = lineas_j1[i].ljust(40) # Rellena con espacios a la izquierda
            l2 = lineas_j2[i].rjust(40) # Rellena con espacios a la derecha
            print(f"{l1}   VS   {l2}")

        # Nombres debajo de cada uno
        nombre1 = f"[{self.j1.nombre}]".center(40)
        nombre2 = f"[{self.j2.nombre}]".center(40)
        print(f"\n{nombre1}        {nombre2}")
        print("\n" + "="*80)
        
        input("\nPresioná ENTER para desenvainar...")

    def iniciar(self):
        self.mostrar_intro_visual() # <--- Llamamos a la intro nueva
        self.limpiar_pantalla()
        print(f"🔥 DUELO: {self.j1.nombre} vs {self.j2.nombre} 🔥")
        time.sleep(1)
        
        while self.esta_activo:
            self.limpiar_pantalla()
            
            # --- ENCABEZADO DE ESTADO ---
            print(f" {self.j1.nombre} ({type(self.j1).__name__}) ".center(50, "="))
            print(self.j1.obtener_estado())
            print("-" * 50)
            
            # AQUÍ SE MUESTRA EL PERSONAJE DE LA IA
            print(f" {self.j2.nombre} ({type(self.j2).__name__}) ".center(50, "="))
            print(self.j2.obtener_estado())
            print("=" * 50)
            
            print(f"\n>>> TURNO {self.turno_actual} <<<")
            
            # 1. El Humano elige
            print(self.j1.mostrar_menu())
            accion_h = input(">> Tu acción: ")
            
            # 2. La IA elige (Lógica simple)
            # Si la IA tiene balas, es probable que dispare (3), si no, recarga (1)
            opciones_ia = ["1", "2"]
            if self.j2._balas > 0: opciones_ia.append("3")
            # Si la IA es Soli y puede robar:
            if hasattr(self.j2, '_turnos_para_robar') and self.j2._turnos_para_robar >= 2:
                opciones_ia.append("4")
            
            accion_ia = random.choice(opciones_ia)
            
            # 3. Resolver
            self.resolver_fases(accion_h, accion_ia)
            
            # 4. Finalizar turno
            self.j1.pasar_turno()
            self.j2.pasar_turno()
            self.verificar_ganador()
            
            if self.esta_activo:
                input("\n[Presioná ENTER para el siguiente turno]")
                self.turno_actual += 1

    def resolver_fases(self, acc1, acc2):
        print("\n--- RESULTADOS DEL TURNO ---")
        # Fase 1: Escudos
        if acc1 == "2": self.j1.cubrirse()
        if acc2 == "2": self.j2.cubrirse()

        # Fase 2: Recargas / Robos
        if acc1 == "1": self.j1.recargar()
        if acc2 == "1": self.j2.recargar()
        
        # Habilidad de Soli (Robar)
        if acc1 == "4" and hasattr(self.j1, 'robar_bala'): self.j1.robar_bala(self.j2)
        if acc2 == "4" and hasattr(self.j2, 'robar_bala'): self.j2.robar_bala(self.j1)

        # Fase 3: Disparos
        if acc1 == "3":
            # Caso especial Graham (Daño 2 si tiene 2 balas)
            if hasattr(self.j1, '_limite_balas') and self.j1._balas >= 2:
                print(f"¡{self.j1.nombre} descarga su escopeta!")
                self.j1._balas -= 2
                self.j2.recibir_disparo(danio=2)
            elif self.j1._balas > 0:
                print(f"¡{self.j1.nombre} dispara!")
                self.j1._balas -= 1
                self.j2.recibir_disparo(danio=1)
            else:
                print(f"¡Click! {self.j1.nombre} no tenía balas.")

        if acc2 == "3":
            if hasattr(self.j2, '_limite_balas') and self.j2._balas >= 2:
                print(f"¡{self.j2.nombre} descarga su escopeta!")
                self.j2._balas -= 2
                self.j1.recibir_disparo(danio=2)
            elif self.j2._balas > 0:
                print(f"¡{self.j2.nombre} dispara!")
                self.j2._balas -= 1
                self.j1.recibir_disparo(danio=1)
            else:
                print(f"¡Click! {self.j2.nombre} no tenía balas.")

    def verificar_ganador(self):
        if not self.j1.esta_vivo() and not self.j2.esta_vivo():
            print("\n💀 ¡EMPATE! Ambos cayeron.")
            self.esta_activo = False
        elif not self.j1.esta_vivo():
            print(f"\n🏆 GANADOR: {self.j2.nombre}")
            self.esta_activo = False
        elif not self.j2.esta_vivo():
            print(f"\n🏆 GANADOR: {self.j1.nombre}")
            self.esta_activo = False