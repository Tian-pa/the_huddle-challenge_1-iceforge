import time
import os
import threading

class JuegoPistolero:
    def __init__(self, jugador1, jugador2):
        self.j1 = jugador1
        self.j2 = jugador2
        self.turno_actual = 1
        self.esta_activo = True

    def limpiar_pantalla(self):
        # Para Windows es 'cls', para Unix es 'clear'
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_introduccion(self):
        self.limpiar_pantalla()
        print("¡DUELO DE PISTOLEROS!")
        print(f"{self.j1.nombre} VS {self.j2.nombre}")
        time.sleep(1)
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        print("¡FUEGO!")

    def iniciar(self):
        self.mostrar_introduccion()
        while self.esta_activo:
            self.ejecutar_turno()
            self.verificar_ganador()

    def obtener_entrada_con_tiempo(self, mensaje, segundos=3):
        print(mensaje)
        respuesta = [None] # Usamos una lista para poder modificarla desde el hilo

        def entrada():
            respuesta[0] = input()

        # Creamos un "hilo" para que el input no bloquee el reloj
        thread = threading.Thread(target=entrada)
        thread.daemon = True
        thread.start()
        thread.join(segundos)

        if thread.is_alive():
            print("\n¡TIEMPO AGOTADO! Te quedaste congelado por el miedo...")
            return "0" # "0" representará "No hizo nada"
        return respuesta[0]

    def ejecutar_turno(self):
        print(f"\n--- TURNO {self.turno_actual} ---")
        
        # 1. Pedir acción al Humano con tiempo
        accion_h = self.obtener_entrada_con_tiempo("¡RÁPIDO! Elegí (1, 2, 3...): ", 3)
        
        # 2. La IA elige (IA básica con random)
        import random
        accion_ia = str(random.randint(1, 3)) 
        
        # 3. PROCESAMIENTO SIMULTÁNEO
        # Primero procesamos defensas, luego ataques
        self.resolver_acciones(accion_h, accion_ia)
        
        # 4. Actualizar contadores al final
        self.turno_actual += 1
        # Aquí llamaríamos a una función de los personajes para avisar que pasó el turno
        self.j1.pasar_turno() 
        self.j2.pasar_turno()
    
    def resolver_acciones(self, acc_j1, acc_j2):
        # Fase 1: Preparación / Escudos
        # Si eligieron "2", activan su estado _esta_protegido
        if acc_j1 == "2": self.j1.cubrirse()
        if acc_j2 == "2": self.j2.cubrirse()

        # Fase 2: Utilidad / Cargas / Robos
        if acc_j1 == "1": self.j1.recargar()
        if acc_j2 == "1": self.j2.recargar()
        
        # Lógica especial para Soli (Opción 4: Robar)
        if acc_j1 == "4" and hasattr(self.j1, 'robar_bala'):
            self.j1.robar_bala(self.j2)
        if acc_j2 == "4" and hasattr(self.j2, 'robar_bala'):
            self.j2.robar_bala(self.j1)

        # Fase 3: Ataque (Simultáneo)
        # Importante: Disparan solo si tienen balas (> 0)
        # Usamos el método recibir_disparo() que ya valida si el otro tiene escudo
        if acc_j1 == "3":
            if self.j1._balas > 0:
                self.j1._balas -= 1
                self.j2.recibir_disparo()
            else:
                print(f"¡Click! {self.j1.nombre} no tiene balas.")

        if acc_j2 == "3":
            if self.j2._balas > 0:
                self.j2._balas -= 1
                self.j1.recibir_disparo()
            else:
                print(f"¡Click! {self.j2.nombre} no tiene balas.")

    def verificar_ganador(self):
        # Si ambos mueren al mismo tiempo
        if not self.j1.esta_vivo() and not self.j2.esta_vivo():
            print("\n💀 ¡EMPATE MORTAL! Ambos cayeron al suelo al mismo tiempo.")
            self.esta_activo = False
        elif not self.j1.esta_vivo():
            print(f"\n🏆 ¡EL GANADOR ES {self.j2.nombre.upper()}!")
            self.esta_activo = False
        elif not self.j2.esta_vivo():
            print(f"\n🏆 ¡EL GANADOR ES {self.j1.nombre.upper()}!")
            self.esta_activo = False