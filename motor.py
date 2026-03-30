import time
import os
import random
from interfaz import ARTE_PERSONAJES
# Se importan las subclases para poder instanciarse más tarde:
from entidades.billy import BillyTheKid
from entidades.soli import SoliTheOutlaw
from entidades.graham import GrahamTheFarmer

class JuegoPistolero:
    def __init__(self):
        self.j1 = None # Inicialización de referencias
        self.j2 = None # Inicialización de referencias
        self.turno_actual = 1
        self.esta_activo = True # Flag: bandera de control

    def configurar_personajes(self):
        """Lógica de selección encapsulada"""
        self.j1 = self._menu_seleccion("JUGADOR")
        self.j2 = self._menu_seleccion("IA", es_ia=True)

    def _menu_seleccion(self, nombre, es_ia=False):
        """Método privado que actúa como 'Fábrica' de objetos"""
        if es_ia:
            opcion = str(random.randint(1, 3))
        else:
            while True:
                self.limpiar_pantalla()
                print(f"--- JUGADOR, ELIGE TU PERSONAJE ---")
                print("1. Billy the Kid (Max 3 balas)")
                print("2. Soli the Outlaw (Puede robar)")
                print("3. Graham the Farmer (Daño x2)")
                opcion = input(">> Seleccioná (1-3): ")
                if opcion in ["1", "2", "3"]: break
                print("Opción inválida.")
        
        # Instanciación
        if opcion == "1": return BillyTheKid(nombre)
        if opcion == "2": return SoliTheOutlaw(nombre)
        return GrahamTheFarmer(nombre)

    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_intro_visual(self):
        self.limpiar_pantalla()
        print("\n" + "="*80)
        print("🔥 ¡DUELO EN EL LEJANO OESTE! 🔥".center(80))
        print("="*80 + "\n")

        # Obtenemos las listas de líneas
        lineas_j1 = ARTE_PERSONAJES.get(type(self.j1).__name__, ["Sin Arte"]*15) # obtiene el nombre de la clase como un texto para buscar su dibujo en el diccionario
        lineas_j2 = ARTE_PERSONAJES.get(type(self.j2).__name__, ["Sin Arte"]*15)

        # Imprimimos línea por línea pegándolas
        for i in range(15):
            l1 = lineas_j1[i].ljust(40) # asegura que cada dibujo ocupe exactamente la mitad de la pantalla
            l2 = lineas_j2[i].rjust(40) 
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
            
            # Encabezado de estado del usuario
            print(f" {self.j1.nombre} ({type(self.j1).__name__}) ".center(50, "="))
            print(self.j1.obtener_estado())
            print("-" * 50)
            
            # Encabezado de estado de la IA
            print(f" {self.j2.nombre} ({type(self.j2).__name__}) ".center(50, "="))
            print(self.j2.obtener_estado())
            print("=" * 50)
            
            print(f"\n>>> TURNO {self.turno_actual} <<<")
            
            # El usuario elige
            print(self.j1.mostrar_menu())
            accion_h = input(">> Tu acción: ")
            
            # La IA elige
            opciones_ia = ["1", "2"] # Recargar y cubrirse siempre están disponibles

            # Se aplica una regla polimórfica, sólo se disparará si tiene las balas que su clase requiere
            # Si es Graham pide 2, si es Billy o Soli pide 1.
            if self.j2._balas >= self.j2._costo_disparo:
                opciones_ia.append("3")

            # Si la IA es Soli y su habilidad (4) no está en enfriamiento:
            if hasattr(self.j2, '_turnos_para_robar') and self.j2._turnos_para_robar >= 2:
                opciones_ia.append("4")

            # La IA elige entre las opciones válidas para su personaje actual
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
            
            # Fase 1: Preparación (Escudos, Recargas y Habilidades especiales)
            # Escudos
            if acc1 == "2": self.j1.cubrirse()
            if acc2 == "2": self.j2.cubrirse()

            # Recargas
            if acc1 == "1": self.j1.recargar()
            if acc2 == "1": self.j2.recargar()
            
            # Habilidades únicas (Soli robar)
            if acc1 == "4" and hasattr(self.j1, 'robar_bala'): self.j1.robar_bala(self.j2)
            if acc2 == "4" and hasattr(self.j2, 'robar_bala'): self.j2.robar_bala(self.j1)

            # Fase 2: Resolución de Disparos
            # Usamos una lista de tuplas para procesar ambos jugadores con la misma lógica
            for atacante, defensor, accion in [(self.j1, self.j2, acc1), (self.j2, self.j1, acc2)]:
                if accion == "3":
                    # Aplicamos Polimorfismo: el objeto dice si puede y cuanto daño hace
                    if atacante._balas >= atacante._costo_disparo:
                        print(f"¡{atacante.nombre} abre fuego!")
                        atacante._balas -= atacante._costo_disparo
                        defensor.recibir_disparo(danio=atacante._danio_ataque)
                    else:
                        print(f"¡Click! {atacante.nombre} no tiene balas suficientes.")

    def verificar_ganador(self):
        if not self.j1.esta_vivo() and not self.j2.esta_vivo():
            print("\n💀 ¡EMPATE! Ambos cayeron.")
            self.esta_activo = False
        elif not self.j1.esta_vivo(): # En el caso de que el usuario haya perdido
            print(f"\n🏆 GANADOR: {self.j2.nombre}") # Gana la IA
            self.esta_activo = False
        elif not self.j2.esta_vivo(): # En el caso de que la IA haya perdido
            print(f"\n🏆 GANADOR: {self.j1.nombre}") # Gana el usuario
            self.esta_activo = False