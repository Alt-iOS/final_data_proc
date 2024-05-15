import numpy as np
import matplotlib.pyplot as plt

def run():
    sl = 0.3 # PA -> PM
    lg = 0.45  # PM -> NM
    lr = 0.52  # PM -> PA
    gr = 0.34  # NM -> PM
    gf = 0.22  # NM -> NH

    #Matriz
    P = np.array([[1 - sl, sl, 0, 0, 0],
                  [0, 1 - lg - lr, lg, lr, 0],
                  [0, 0, 1 - gr - gf, gr, gf],
                  [0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 1]])

    estado_inicial = np.array([1000000, 0, 0, 0, 0])

    #50 días
    estados = [estado_inicial]
    for _ in range(50):
        estado_actual = estados[-1]
        estado_siguiente = np.dot(estado_actual, P)
        estados.append(estado_siguiente)

    resultado_final = estados[-1].astype(int)
    print(resultado_final)

    dias = range(51)
    PA, PM, NM, NH, F = zip(*estados)

    plt.figure(figsize=(10, 6))
    plt.plot(dias, PA, label='PA')
    plt.plot(dias, PM, label='PM')
    plt.plot(dias, NM, label='NM')
    plt.plot(dias, NH, label='NH')
    plt.plot(dias, F, label='F')
    plt.xlabel('Días')
    plt.ylabel('INVERSIÓN')
    plt.title('Evolución de inversión')
    plt.legend()
    plt.show()

