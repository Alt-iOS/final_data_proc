import matplotlib.pyplot as plt
from random import random, randint, sample
from collections import namedtuple


def run():
    def capitalInvertido(individuo):
        return sum(map(lambda x, y: x * y.precio, individuo, inversiones))


    def rendimiento(individuo):
        return sum(map(lambda x, y: x * y.precio * y.rendim, individuo, inversiones))


    def ajustaCapital(individuo):
        ajustado = individuo[:]
        while capitalInvertido(ajustado) > capital:
            pos = randint(0, len(ajustado) - 1)
            if ajustado[pos] > 0:
                ajustado[pos] -= 1
        return ajustado


    def creaIndividuo(inversiones, capital):
        individuo = [0] * len(inversiones)

        while capitalInvertido(individuo) < capital:
            eleccion = randint(0, len(inversiones) - 1)
            individuo[eleccion] += 1
        return ajustaCapital(individuo)


    def cruza(poblacion, posiciones):
        L = len(poblacion[0])
        hijo = poblacion[posiciones[0]][:]
        inicio = randint(0, L - 1)
        fin = randint(inicio + 1, L)
        hijo[inicio:fin] = poblacion[posiciones[1]][inicio:fin]
        return ajustaCapital(hijo)


    def muta(individuo, tasaMutacion):
        mutado = []
        for i in range(len(individuo)):
            if random() > tasaMutacion:
                mutado.append(individuo[i])
            else:
                mutado.append(randint(0, inversiones[i].cantidad))

        return ajustaCapital(mutado)


    def evoluciona(poblacion, generaciones):
        poblacion.sort(key=lambda x: rendimiento(x))

        N = len(poblacion)
        tasaMutacion = 0.01

        reproduccion = [x for x in range(N) for y in range(x + 1)]
        for i in range(generaciones):
            padres = sample(reproduccion, 2)
            while padres[0] == padres[1]:
                padres = sample(reproduccion, 2)
            hijos = [cruza(poblacion, padres) for x in range(N - 1)]

            hijos = [muta(x, tasaMutacion) for x in hijos]

            hijos.append(poblacion[-1])
            poblacion = hijos

            poblacion.sort(key=lambda x: rendimiento(x))

        return poblacion[-1]


    Inversion = namedtuple("Inversion", ["precio", "cantidad", "rendim"])

    numInver = 100
    maxPrecio = 1000
    maxCant = 10
    maxRend = 0.2

    inversiones = [
        Inversion(random() * maxPrecio, randint(1, maxCant), random() * maxRend)
        for i in range(numInver)
    ]

    print(inversiones)

    capital = 50000
    individuos = 20
    generaciones = 1000

    poblacion = [creaIndividuo(inversiones, capital) for i in range(individuos)]

    mejor = evoluciona(poblacion, generaciones)
    print(mejor, capitalInvertido(mejor), rendimiento(mejor))


    def plot_results(inversiones, mejor):
        precios = [inv.precio for inv in inversiones]
        cantidades = [inv.cantidad for inv in inversiones]
        precios_mejor = [
            inversiones[i].precio for i, cantidad in enumerate(mejor) if cantidad > 0
        ]
        rendimientos_mejor = [
            inversiones[i].precio * inversiones[i].rendim * cantidad
            for i, cantidad in enumerate(mejor)
            if cantidad > 0
        ]

        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.bar(range(len(inversiones)), cantidades)
        plt.xlabel("Inversiones")
        plt.ylabel("Cantidad Invertida")
        plt.title("Cantidad Invertida en cada Inversión")

        plt.subplot(1, 2, 2)
        plt.bar(range(len(precios_mejor)), rendimientos_mejor)
        plt.xlabel("Inversiones")
        plt.ylabel("Rendimiento")
        plt.title("Rendimiento de cada Inversión en el Mejor Individuo")

        plt.tight_layout()
        plt.show()


    plot_results(inversiones, mejor)
