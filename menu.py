def main():
    while True:
        try:
            option = int(input("Bienvenido al programa final de Procesamiento de datos\n"
                               "Hecho por Víctor Batarse y Sofia Pérez\n"
                               "Para comenzar seleccione una opción\n"
                               "1. Regresión Lineal\n"
                               "2. Regresión Logística\n"
                               "3. Modelo Epidemiológico\n"
                               "4. Modelo de Inversión\n"
                               "5. Red Neuronal - reconocimiento de números\n"
                               "6. Red Neuronal Tienda de Ropa\n"
                               "7. AGS Asesor de Inversión\n"
                               "8. Colonia de Hormigas\n"
                               "9. Enjambre de Partículas\n"
                               "10. Sistemas inmunes artificiales\n"
                               "11. Salir\n"))
        except ValueError:
            print("Ups, no se ingresó un número. Intente de nuevo.")
            continue

        process_option(option)


def process_option(option):
    match option:
        case 1:
            print("Implementación algoritmo Regresión Lineal")
        case 2:
            print("Implementación algoritmo Regresión Logística")
        case 3:
            print("Implementación Modelo Epidemiológico")
        case 4:
            print("Implementación Modelo de Inversión")
        case 5:
            print("Implementación Red Neuronal - reconocimiento de números")
        case 6:
            print("Implementación Red Neuronal Tienda de Ropa")
        case 7:
            print("Implementación AGS Asesor de Inversión")
        case 8:
            print("Implementación Colonia de Hormigas")
        case 9:
            print("Implementación Enjambre de Partículas")
        case 10:
            print("Implementación Sistemas inmunes artificiales")
        case 11:
            print("Gracias por usar el programa. ¡Hasta pronto!")
            exit(0)
        case _:
            print("Opción no disponible, tiene que ser un número entre 1-11")


if __name__ == "__main__":
    main()
