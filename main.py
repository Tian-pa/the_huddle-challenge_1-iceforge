# main.py
import random
from entidades.billy import BillyTheKid
from entidades.soli import SoliTheOutlaw
from entidades.graham import GrahamTheFarmer
from motor import JuegoPistolero

def seleccionar_personaje(nombre, es_ia=False):
    if es_ia:
        opcion = str(random.randint(1, 3))
    else:
        while True:
            print(f"\n--- {nombre.upper()}, ELEGI TU PERSONAJE ---")
            print("1. Billy The Kid (Veloz / Carga hasta 3 balas)")
            print("2. Soli The Outlaw (Ladrona / Roba balas cada 2 turnos)")
            print("3. Graham el Granjero (Tanque / Escopeta de doble daño)")
            
            opcion = input(">> Seleccioná (1-3): ")

            if opcion in ["1", "2", "3"]:
                break
            else:
                print("\nOpción inválida. Por favor, ingrese un número dentro del rango (1-3).")

    if opcion == "1":
        return BillyTheKid(nombre)
    elif opcion == "2":
        return SoliTheOutlaw(nombre)
    elif opcion == "3":
        return GrahamTheFarmer(nombre)
    else:
        print("Opción inválida, te asignamos a Billy por defecto.")
        return BillyTheKid(nombre)

if __name__ == "__main__":
    
    # El usuario elige directamente
    jugador_humano = seleccionar_personaje("Jugador") 
    
    # La IA elige al azar
    oponente_ia = seleccionar_personaje("Contrincante", es_ia=True)

    print(f"\n¡EL DUELO COMIENZA!")
    print(f"{jugador_humano.nombre} VS {oponente_ia.nombre}")

    duelo = JuegoPistolero(jugador_humano, oponente_ia)

    duelo.iniciar()