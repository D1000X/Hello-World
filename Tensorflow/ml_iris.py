# ===========================================
# Classificação das flores Iris com TensorFlow
# ===========================================

import tensorflow as tf
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1. Carregar dados
iris = load_iris()
X = iris.data
y = iris.target

# 2. Pré-processamento: dividir e normalizar
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 3. Construir o modelo (rede neural simples)
model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu', input_shape=(4,)),
    tf.keras.layers.Dense(8, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 4. Treinar o modelo
model.fit(X_train, y_train, epochs=50, batch_size=5, verbose=1)

# 5. Avaliar o modelo
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Acurácia do modelo: {accuracy:.2%}")

# 6. Fazer previsões
amostra = X_test[:5]
previsoes = model.predict(amostra)
print("Previsões (classes):", previsoes.argmax(axis=1))
print("Classes reais:      ", y_test[:5])
