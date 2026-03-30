from motor import JuegoPistolero

if __name__ == "__main__":
    # Instanciamos el motor
    duelo = JuegoPistolero()
    
    # El motor se ocupa de la lógica de selección
    duelo.configurar_personajes()
    
    # Arranca el juego
    duelo.iniciar()