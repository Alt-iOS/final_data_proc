import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression


def run():
    print("Predicción de Diabetes con regresión logística")
    # 1. Carga de datos
    train = pd.read_csv('./compras.csv')
    train.head(3)

    # Variables de interes: * BMI: índice de masa corporal. Es una métrica o KPI basada en el peso y la altura de
    # cada persona. Un BMI muy alto puede ser indicativo de tener diabetes * Outcome: si la persona tiene diabetes o no

    # # 2. Desarrollo

    # En esta parte nos interesa explorar los datos y explicar el modelo de regresión logística a este caso de diabetes

    # ## 2.1 Exploración de datos

    # Miramos una tabla y una gráfica de los datos que nos interesan
    train[['Time spent in online shop', 'Purchasing behaviour']].head()
    train[['Time spent in online shop', 'Purchasing behaviour']].plot.scatter(x='Time spent in online shop',
                                                                              y='Purchasing behaviour')

    # ## 2.2 Función logística

    # Vamos a pintar una función logistica sobre estos datos
    #
    # $$ f_{w,b}\left(\vec{x}^{(i)}\right)=\frac{1}{1+\exp-\left(w\vec{x}+b\right)}$$
    # Vamos a variar $w,b$ a ver que pasa en los datos
    # pruebas de parametro
    w = 0.09
    b = -3.6
    # despues de hacer el modelos (se explica más adelante)
    # intercepto (b): [-3.68596089]
    # pendiente (w): [[0.09351691]]
    # puntos de la recta
    x = np.linspace(0, train['Time spent in online shop'].max(), 100)
    y = 1 / (1 + np.exp(-(w * x + b)))

    # grafica de la recta
    train.plot.scatter(x='Time spent in online shop', y='Purchasing behaviour')
    plt.plot(x, y, '-r')
    plt.ylim(0, train['Purchasing behaviour'].max() * 1.1)
    # plt.grid()
    plt.show()

    # ## 2.3 Optimización de parámetros

    # Si escogemos esos parametros $w,b$ para el modelo, ¿Qué tan buenos son?
    #
    # Podemos utilizar la siguiente estrategia:
    # * calcular el valor de la función logística para cada dato
    # * calcular la función de pérdida (se denota con L o loss)
    # * calcular el promedio de la pérdida para obtener el costo (se denota con Jo cost)
    #
    # Queremos los valores $w,b$ que resulten en un menor costo
    #
    # Las ecuaciones para las funciones son
    #
    # $$ L\left(f_{w,b}\left(\vec{x}^{(i)}\right),y^{(i)}\right)=-y^{(i)}\log\left(f_{w,b}\left(\vec{x}^{(i)}\right)\right)-\left(1-y^{(i)}\right)\log\left(1-f_{w,b}\left(\vec{x}^{(i)}\right)\right) $$
    #
    # $$ J\left(w,b\right)=\frac{1}{m}\sum_{i=1}^{m}\left[L\left(f_{w,b}\left(\vec{x}^{(i)}\right),y^{(i)}\right)\right] $$
    # calculo de las predicciones
    train['sigmoid'] = 1 / (1 + np.exp(-(train['Time spent in online shop'] * w + b)))

    # calculo de la funcion de error
    train['loss_xi'] = -train['Purchasing behaviour'] * np.log(train['sigmoid']) - (
          1 - train['Purchasing behaviour']) * np.log(1 - train['sigmoid'])
    cost_j = train['loss_xi'].mean()

    # Esto lo hemos hecho con los parametros que hemos obtenido a ojo por ciento. Ahora vamos a ser más refinados y calcularlo para muchos parametros a la vez y luego de ahi mirar el que tenga menor costo.
    #
    # Para eso hacemos lo siguiente:
    # * Construimos un dataframe con valores para $w,b$ que varían sobre una cuadricula o grid
    # * Creamos una función de python que calcule el costo $J$ dados parametros $w,b$
    # * Aplicamos la función sobre el dataframe con los valores $w,b$ en la cuadricula
    # * Podemos ordenar la tabla resultante para obtener los valores $w,b$ con el menor costo
    # * Luego hacemos gráficas para verificar el resultado
    # hacemos dataframe para calcular el error en funcion de los parametros w, b
    array = np.mgrid[0.05:0.15:0.01, -4:-3:0.01].reshape(2, -1).T
    df = pd.DataFrame(data=array,
                      columns=['w', 'b'])

    # round para solventar problema con muchos decimales
    df['w'] = np.round(df['w'], 6)
    df['b'] = np.round(df['b'], 6)

    def sum_error_df(df):
        train['sigmoid'] = 1 / (1 + np.exp(-(train['Time spent in online shop'] * df['w'] + df['b'])))
        train['loss_xi'] = -train['Purchasing behaviour'] * np.log(train['sigmoid']) - (
                  1 - train['Purchasing behaviour']) * np.log(1 - train['sigmoid'])
        j_cost = train['loss_xi'].mean()
        return (j_cost)

    df['error'] = df.apply(sum_error_df, axis=1)
    df.sort_values(by=['error']).head()
    df_3d = df.pivot(index='w', columns='b', values='error')
    df_3d.head()

    x = df_3d.columns
    y = df_3d.index
    X, Y = np.meshgrid(x, y)
    Z = df_3d

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z)
    plt.show()
    x = df_3d.columns
    y = df_3d.index
    X, Y = np.meshgrid(x, y)
    Z = df_3d
    plt.contourf(Y, X, Z, alpha=0.7, cmap=plt.cm.jet)
    plt.show()
    # ## Bonus: Optimizando los parámetros

    # Esta sección es opcional.
    #
    # Vamos a utilizar el método del gradiente descendente para calcular los valores optimos de $w,b$.
    #
    # Para esto tenemos que calcular el gradiente para $w,b$ con respecto de la función J (esta es la que hemos gráficado), sus funciones son
    #
    # $$ \frac{\partial}{\partial w}J\left(w,b\right)=\frac{1}{m}\sum_{i=1}^{m}\left(f_{w,b}\left(\vec{x}^{(i)}\right)-y^{(i)}\right)x^{(i)} $$
    #
    # $$ \frac{\partial}{\partial b}J\left(w,b\right)=\frac{1}{m}\sum_{i=1}^{m}\left(f_{w,b}\left(\vec{x}^{(i)}\right)-y^{(i)}\right)$$

    # Las funciones respectivas en python serían
    def delta_j_w(w, b):
        train['sigmoid'] = 1 / (1 + np.exp(-(train['Time spent in online shop'] * w + b)))
        train['partial_loss'] = (train['sigmoid'] - train['Purchasing behaviour']) * train['Time spent in online shop']
        derivative = train['partial_loss'].mean()
        return (derivative)

    def delta_j_b(w, b):
        train['sigmoid'] = 1 / (1 + np.exp(-(train['Time spent in online shop'] * w + b)))
        train['partial_loss'] = (train['sigmoid'] - train['Purchasing behaviour'])
        derivative = train['partial_loss'].mean()
        return (derivative)

    w_0 = 0.09
    b_0 = -3.57
    alpha_w = 0.001
    alpha_b = 0.1

    w_new = w_0 - alpha_w * delta_j_w(w_0, b_0)
    b_new = b_0 - alpha_b * delta_j_b(w_0, b_0)

    w_0 = w_new
    b_0 = b_new

    print(w_0, b_0)
    # valores optimos de sklearn (más abajo la explicación)
    # w = 0.09351691
    # b = -3.68596089

    # Ahora vamos a hacer lo mismo pero mucho más rápido con sklearn

    # definiendo input y output
    X_train = np.array(train['Purchasing behaviour']).reshape((-1, 1))
    Y_train = np.array(train['Time spent in online shop'])

    # creando modelo
    model = LogisticRegression()
    model.fit(X_train, Y_train)

    # imprimiendo parametros
    print(f"intercepto (b): {model.intercept_}")
    print(f"pendiente (w): {model.coef_}")