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
            print(f"\n--- {nombre.upper()}, ELIGE TU PERSONAJE ---")
            print("1. Billy (Max 3 balas)")
            print("2. Soli (Puede robar)")
            print("3. Graham (Daño x2)")
            opcion = input(">> Seleccioná (1-3): ")
            if opcion in ["1", "2", "3"]: break
            print("Opción inválida.")

    if opcion == "1": return BillyTheKid(nombre if not es_ia else "Billy Contrincante")
    if opcion == "2": return SoliTheOutlaw(nombre if not es_ia else "Soli Contrincante")
    return GrahamTheFarmer(nombre if not es_ia else "Graham Contrincante")

if __name__ == "__main__":
    jugador = seleccionar_personaje("Jugador")
    ia = seleccionar_personaje("IA", es_ia=True)
    
    duelo = JuegoPistolero(jugador, ia)
    duelo.iniciar()