import math
import numpy as np
import matplotlib.pyplot as plt
import logging
import tensorflow as tf
import tensorflow_datasets as tfds


def run():
    # Configurar el nivel de registro
    logger = tf.get_logger()
    logger.setLevel(logging.ERROR)

    # Cargar el dataset de imágenes de ropa
    dataset, metadata = tfds.load('fashion_mnist', as_supervised=True, with_info=True)
    train_dataset, test_dataset = dataset['train'], dataset['test']

    # Definir los nombres de las clases
    class_names = ['Camiseta', 'Pantalón', 'Suéter', 'Vestido', 'Saco', 'Sandalia', 'Camisa', 'Tenis', 'Bolsa', 'Botín']

    # Obtener la cantidad de ejemplos de entrenamiento y prueba
    num_train_examples = metadata.splits['train'].num_examples
    num_test_examples = metadata.splits['test'].num_examples


    # Función de normalización de las imágenes
    def normalize(images, labels):
        images = tf.cast(images, tf.float32)
        images /= 255
        return images, labels


    # Aplicar la normalización a los datasets de entrenamiento y prueba
    train_dataset = train_dataset.map(normalize)
    test_dataset = test_dataset.map(normalize)

    # Estructura de la red neuronal
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
        tf.keras.layers.Dense(50, activation=tf.nn.relu),
        tf.keras.layers.Dense(50, activation=tf.nn.relu),
        tf.keras.layers.Dense(10, activation=tf.nn.softmax)
    ])

    # Compilar el modelo
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    # Configurar el aprendizaje por lotes
    BATCH_SIZE = 32
    train_dataset = train_dataset.repeat().shuffle(num_train_examples).batch(BATCH_SIZE)
    test_dataset = test_dataset.batch(BATCH_SIZE)

    # Entrenar el modelo
    model.fit(
        train_dataset,
        epochs=5,
        steps_per_epoch=math.ceil(num_train_examples / BATCH_SIZE)
    )

    # Evaluar el modelo en el dataset de prueba
    test_loss, test_accuracy = model.evaluate(
        test_dataset,
        steps=math.ceil(num_test_examples / BATCH_SIZE)
    )

    # Imprimir los resultados de precisión
    print("Resultado en las pruebas: ", test_accuracy)

    # Probar el modelo con una imagen de prueba
    for test_images, test_labels in test_dataset.take(1):
        test_images = test_images.numpy()
        test_labels = test_labels.numpy()
        predictions = model.predict(test_images)


        # Funciones auxiliares para visualizar las predicciones
        def plot_image(i, predictions_array, true_labels, images):
            predictions_array, true_label, img = predictions_array[i], true_labels[i], images[i]
            plt.grid(False)
            plt.xticks([])
            plt.yticks([])
            plt.imshow(img[..., 0], cmap=plt.cm.binary)
            predicted_label = np.argmax(predictions_array)
            if predicted_label == true_label:
                color = 'blue'
            else:
                color = 'red'
            plt.xlabel("Predicción: {} {:2.0f}%".format(class_names[predicted_label], 100 * np.max(predictions_array)),
                       color=color)


        def plot_value_array(i, predictions_array, true_label):
            predictions_array, true_label = predictions_array[i], true_label[i]
            plt.grid(False)
            plt.xticks([])
            plt.yticks([])
            thisplot = plt.bar(range(10), predictions_array, color="#888888")
            plt.ylim([0, 1])
            predicted_label = np.argmax(predictions_array)
            thisplot[predicted_label].set_color('red')
            thisplot[true_label].set_color('blue')


        # Mostrar algunas predicciones
        num_rows = 5
        num_cols = 3
        num_images = num_rows * num_cols
        plt.figure(figsize=(2 * 2 * num_cols, 2 * num_rows))
        for i in range(num_images):
            plt.subplot(num_rows, 2 * num_cols, 2 * i + 1)
            plot_image(i, predictions, test_labels, test_images)
            plt.subplot(num_rows, 2 * num_cols, 2 * i + 2)
            plot_value_array(i, predictions, test_labels)
        plt.show()
