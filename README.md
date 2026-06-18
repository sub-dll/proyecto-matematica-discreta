# Proyecto Final: Matemática Discreta - Ruta Óptima (Grafos Ponderados)

**Integrante:** Diego Fonseca Aguilera

## Descripción General del Problema
Este proyecto modela una red de 15 ciudades europeas mediante un grafo ponderado (conexo, simple y no dirigido). El objetivo es calcular y visualizar la ruta óptima terrestre (camino mínimo en kilómetros) entre una ciudad de origen y una de destino, utilizando el **Algoritmo de Dijkstra**.

## Librerías Utilizadas
El proyecto fue desarrollado en Python y requiere las siguientes librerías:
* `networkx`: Para la creación y manipulación del modelo matemático del grafo.
* `matplotlib`: Para la renderización y visualización espacial de la red.
* `customtkinter`: Para la creación de la interfaz gráfica de usuario.

## Instrucciones de Ejecución y Arranque de la Interfaz Gráfica
Para ejecutar esta aplicación en tu entorno local, sigue estos pasos desde la terminal:

1. **Clonar el repositorio o descargar los archivos:**
   Descarga `main.py` y `requirements.txt` en una misma carpeta.

2. **Crear y activar un entorno virtual (Recomendado):**
   ```bash
   python -m venv .venv
   # En Windows:
   .\.venv\Scripts\activate
   # En Mac/Linux:
   source .venv/bin/activate
3. **Instalar dependencias**
    ```bash
    pip install -r requirements.txt
4. **Iniciar la interfaz grafica**
   ```bash
   python main.py
