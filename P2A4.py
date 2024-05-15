import numpy as np
import matplotlib.pyplot as plt


def run():
    # Probabilidades de transición
    sl = 0.20  # Sano -> Leve
    lg = 0.15  # Leve -> Grave
    lr = 0.25  # Leve -> Recuperado
    gr = 0.15  # Grave -> Recuperado
    gf = 0.15  # Grave -> Fallecido

    # Matriz de transición
    P = np.array([[1 - sl, sl, 0, 0, 0],
                  [0, 1 - lg - lr, lg, lr, 0],
                  [0, 0, 1 - gr - gf, gr, gf],
                  [0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 1]])

    # Estado inicial
    estado_inicial = np.array([1000000, 0, 0, 0, 0])

    # Simulación por 50 días
    estados = [estado_inicial]
    for _ in range(50):
        estado_actual = estados[-1]
        estado_siguiente = np.dot(estado_actual, P)
        estados.append(estado_siguiente)

    # Resultado final
    resultado_final = estados[-1].astype(int)
    print(resultado_final)

    # Generar gráficas
    dias = range(51)
    sanos, leves, graves, recuperados, fallecidos = zip(*estados)

    plt.figure(figsize=(10, 6))
    plt.plot(dias, sanos, label='Sanos')
    plt.plot(dias, leves, label='Leves')
    plt.plot(dias, graves, label='Graves')
    plt.plot(dias, recuperados, label='Recuperados')
    plt.plot(dias, fallecidos, label='Fallecidos')
    plt.xlabel('Días')
    plt.ylabel('Población')
    plt.title('Evolución de la población')
    plt.legend()
    plt.show()
