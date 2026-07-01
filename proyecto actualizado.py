import networkx as nx
import customtkinter as ctk
import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D
import csv
import os

# ==========================
# CREAR EL GRAFO
# ==========================
G = nx.Graph()
ciudades_set = set()  
fig = None #variables para reutilizar la ventana del grafo
ax = None
pos = None  # Posiciones del grafo para visualización estable

# ==========================
# CARGAR CONEXIONES DESDE CSV
# ==========================
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
ruta_completa_csv = os.path.join(carpeta_actual, "datos_rutas.csv")

try:
    with open(ruta_completa_csv, mode="r", encoding="utf-8-sig") as archivo:
        # Leer primera línea para detectar el separador
        primera_linea = archivo.readline()
        delimitador = ";" if ";" in primera_linea else ","
        
        # Volvemos al inicio del archivo para procesarlo completo
        archivo.seek(0)
        
        lector_csv = csv.reader(archivo, delimiter=delimitador)   
        next(lector_csv)  # Saltamos el encabezado
        
        for fila in lector_csv: # Aseguramos que la fila tenga al menos 3 elementos (origen, destino, distancia)
            if len(fila) >= 3:
                origen = fila[0].strip() 
                destino = fila[1].strip()
                distancia = float(fila[2].strip()) # Convertimos la distancia a float para poder usarla como numero en el grafo
                
                ciudades_set.add(origen)
                ciudades_set.add(destino)
                G.add_edge(origen, destino, weight=distancia)

except FileNotFoundError:
    print(f"Error: No se encontro el archivo en la ruta: {ruta_completa_csv}")
except Exception as e:
    print(f"Error: Ocurrio un error al leer el archivo: {e}")

# Convertimos a lista ordenada
lista_ciudades = sorted(list(ciudades_set))

# Si el CSV por alguna razón leyera vacío, ponemos un mensaje de alerta en el menú
if not lista_ciudades:
    lista_ciudades = ["Error: CSV sin datos validos"]

# ==========================
# FUNCION PRINCIPAL
# ==========================

def actualizar_destinos(ciudad_seleccionada):
    # Hacemos una copia de la lista original para no modificar la real
    nuevos_destinos = lista_ciudades.copy()
    
    # Borramos la ciudad de origen de esta nueva lista
    if ciudad_seleccionada in nuevos_destinos:
        nuevos_destinos.remove(ciudad_seleccionada)
        
    # Actualizamos el menú de destino con la lista filtrada
    combo_destino.configure(values=nuevos_destinos)
    
    # Si por casualidad el usuario ya tenía elegida esa ciudad en destino, la reseteamos
    if combo_destino.get() == ciudad_seleccionada:
        combo_destino.set("Selecciona ciudad de destino")

def calcular_ruta():
    global fig, ax, pos
    origen = combo_origen.get()
    destino = combo_destino.get()

    if origen not in lista_ciudades or destino not in lista_ciudades:
        resultado.configure(text="Error: Debe seleccionar origen y destino válidos.")
        return

    try:
        ruta = nx.dijkstra_path(G, origen, destino, weight="weight") # Calculamos la ruta óptima usando el algoritmo de Dijkstra
        costo = nx.dijkstra_path_length(G, origen, destino, weight="weight") # Calculamos el costo total de la ruta (distancia total)

        resultado.configure(
            text="Ruta optima:\n\n"
            + " -> ".join(ruta)
            + f"\n\nCosto total: {costo:.0f} km") #se une por la flecha y se muestra el costo total con formato de número entero
        
        # ==========================
        # DIBUJAR GRAFO Y RUTA
        # ==========================
        ruta_aristas = list(zip(ruta, ruta[1:])) 
        
        if pos is None:
            pos = nx.spring_layout(G, k=2.5, iterations=300, seed=42)
        colores_nodos = []

        for ciudad in G.nodes():
            if ciudad == origen:
                colores_nodos.append("green")
            elif ciudad == destino:
                colores_nodos.append("red")
            else:
                colores_nodos.append("lightblue")

        # ==========================
        # REUTILIZAR LA VENTANA DEL GRAFO
        # ==========================
        primera_vez = False
        if fig is None or not plt.fignum_exists(fig.number):
            fig, ax = plt.subplots(figsize=(18, 12))
            primera_vez = True
        else:
            ax.clear()

        nx.draw_networkx_nodes(G, pos, ax=ax, node_size=1800,
            node_color=colores_nodos)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=9, font_weight="bold")
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="lightgray", width=1, alpha=0.6)
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=ruta_aristas, width=4, edge_color="red")
        etiquetas = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(
            G, pos, ax=ax,
            edge_labels=etiquetas,
            label_pos=0.25,  
            font_size=8, 
            font_color="darkblue",
            rotate=False, 
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.9) 
        )
        #congiguracion del texto leyenda
        leyenda = [Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Ciudad de Origen'),
                      Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Ciudad de Destino'),
                      Line2D([0], [0], color='red', lw=3, label='Ruta Optima')]
        ax.legend(handles=leyenda,title= "Referencias",loc="center left")

        ax.set_title(f"Ruta desde {origen} hasta {destino}", fontsize=14, fontweight="bold")
        ax.axis("off")
        fig.tight_layout() #Fuerza a matplotlib a recalcular espacios y evitar colisiones
        
        if primera_vez:
            try:
                fig.canvas.manager.window.state("zoomed")
            except:
                pass
            plt.show(block=False)

        fig.canvas.draw()
        fig.canvas.flush_events()

    except nx.NetworkXNoPath:
        resultado.configure(text="Error: No existe una ruta entre estas ciudades.")
    except Exception as error:
        resultado.configure(text=f"Error:\n{error}")

# ==========================
# CONFIGURACION VENTANA
# ==========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("Buscador de Rutas")
ancho = ventana.winfo_screenwidth()
alto = ventana.winfo_screenheight()
ventana.geometry(f"{ancho}x{alto}"+"+0+0")

titulo = ctk.CTkLabel(ventana, text="Buscador de Rutas", font=("Arial", 24, "bold"))
titulo.pack(pady=15)

# ==========================
# MOSTRAR CIUDADES EN LA VENTANA
# ==========================
titulo_lista = ctk.CTkLabel(ventana, text="Ciudades registradas en el sistema:", font=("Arial", 12, "bold"), text_color="lightblue")
titulo_lista.pack(pady=(5, 0))

ciudades_texto = ", ".join(lista_ciudades) if "Error" not in lista_ciudades[0] else "Ninguna (Revisa tu archivo datos_rutas.csv)"
lista_visual = ctk.CTkLabel(ventana, text=ciudades_texto, font=("Arial", 11), text_color="gray", wraplength=700, justify="center")
lista_visual.pack(pady=(0, 15))

# ==========================
# MENÚS DESPLEGABLES
# ==========================
titulo_origen = ctk.CTkLabel(ventana, text="Ciudad de Origen", font=("Arial", 15, "bold"))
titulo_origen.pack(pady=(10, 5))

combo_origen = ctk.CTkComboBox(ventana, values=lista_ciudades, width=250, state="readonly", command = actualizar_destinos)
combo_origen.set("Selecciona ciudad de origen")
combo_origen.pack()

titulo_destino = ctk.CTkLabel(ventana, text="Ciudad de Destino", font=("Arial", 15, "bold"))
titulo_destino.pack(pady=(20, 5))

combo_destino = ctk.CTkComboBox(ventana, values=lista_ciudades, width=250, state="readonly")
combo_destino.set("Selecciona ciudad de destino")
combo_destino.pack()

# ==========================
# BOTÓN Y RESULTADO
# ==========================
boton_calcular = ctk.CTkButton(ventana, text="Calcular Ruta", command=calcular_ruta, width=200)
boton_calcular.pack(pady=25)

titulo_resultado = ctk.CTkLabel(ventana, text="Resultado", font=("Arial", 15, "bold"))
titulo_resultado.pack()

resultado = ctk.CTkLabel(ventana, text="Seleccione origen y destino", font=("Arial", 14), justify="center")
resultado.pack(pady=15)

# ==========================
# funcion para cerrar la aplicación de forma segura
# ==========================
def cerrar_aplicacion():
    plt.close('all')      # Cierra las ventanas de Matplotlib que queden abiertas
    ventana.quit()        # Detiene el ciclo principal de CustomTkinter
    ventana.destroy()     # Destruye la ventana de forma segura

# Le dice a la x de la ventana que use nuestra función de cierre limpio
ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
ventana.mainloop()
