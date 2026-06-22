# Calculadora de Rutas Óptimas mediante Teoría de Grafos

Este proyecto es una aplicación interactiva en Python que permite calcular y visualizar la ruta más corta entre diferentes ciudades de Argentina utilizando el algoritmo de Dijkstra. Cuenta con una interfaz gráfica moderna y una representación visual del grafo de conexiones.

## Integrantes del Grupo:
- Scarleth Friz Medina
- Jesús Huentemil Catrilaf
- Camila Mardones Molina
- Bayron Salgado Huenuhueque

---

## Descripción General del Problema
El problema abordado consiste en la optimización de rutas de transporte interurbanas, en este caso se utilizan como base 15 ciudades de Argentina (Buenos Aires, Rosario, Santa Fe, Corrientes, Posadas, Córdoba, Tucumán, Mendoza, Neuquén, Mar del Plata, La Plata, Resistencia, Bahía Blanca, San Juan y Salta). 

En el mundo real, la planificación de viajes o logística requiere determinar de forma exacta el camino más eficiente para ahorrar combustible, tiempo y costos. 

Para resolverlo, este software modela la red de carreteras como un Grafo No Dirigido:
- Nodos (Vértices): Representan las ciudades.
- Aristas (Enlaces): Representan las carreteras que conectan directamente a las ciudades.
- Peso (Costo): Representa la distancia física en kilómetros ($km$) entre cada punto.

El sistema procesa dinámicamente estos datos y aplica el Algoritmo de Dijkstra para hallar la ruta con el menor costo acumulado entre un punto de origen y uno de destino seleccionados por el usuario.

---

## Librerías Utilizadas
Para el desarrollo de la aplicación se utilizaron las siguientes librerías:
- NetworkX: representación del grafo y ejecución del algoritmo de Dijkstra.
- CustomTkinter: construcción de la interfaz gráfica de usuario.
- Matplotlib: visualización gráfica de la red de ciudades.
- CSV: lectura de los datos almacenados en archivos CSV.
- OS: localización del archivo de datos dentro del proyecto.

---

## Instrucciones de Ejecución
Para asegurar el buen funcionamiento del programa, el archivo datos_rutas.csv debe estar en la misma carpeta que el código Python. De mismo modo, se deben tener instaladas las librerias anteriormente mencionadas.

1. Ejecutar el código .py
2. Seleccionar ciudad de origen
3. Seleccionar ciudad de destino
4. Presionar el botón de Calcular Ruta
5. Se abre automaticamente la visualización de la ruta como grafo
6. Volver a la ventana anterior para ver la distancia total
