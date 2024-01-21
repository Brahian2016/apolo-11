import tkinter as tk
from tkinter import ttk
import logging
from apolo11.python.utils.Utils import run_simulation, run_reports

# Configuración básica de logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ejecutar_simulacion():
    run_simulation()
    label.config(text="Simulación completada.")
    logging.info("Simulación completada.")

def ejecutar_reportes():
    flag: bool = run_reports()
    if flag:
        label.config(text="Reportes ejecutados.")
        logging.info("Reportes ejecutados.")
    else:
        label.config(text="No hay archivo para reportes.")
        logging.warning("No se realiza proceso.")

def salir():
    popup.destroy()
    logging.info("Aplicación cerrada.")

def mostrar_menu():
    global popup
    global label

    popup = tk.Tk()
    popup.title("Menú interactivo")
    popup.geometry("300x200")  # Tamaño de la ventana

    style = ttk.Style()

    # Establecer el color de fondo del botón "Salir" en rojo
    style.configure("TButton", padding=(10, 5, 10, 5), font='Helvetica 10')
    style.map("TButton", background=[('active', 'red')])

    label = tk.Label(popup, text="Por favor, elige una opción:")
    label.pack(pady=10)

    btn_simulacion = ttk.Button(popup, text="Ejecutar la simulación", command=ejecutar_simulacion)
    btn_simulacion.pack(pady=5)

    btn_reportes = ttk.Button(popup, text="Ejecutar reportes", command=ejecutar_reportes)
    btn_reportes.pack(pady=5)

    btn_salir = ttk.Button(popup, text="Salir", command=salir, style="TButton")
    btn_salir.pack(pady=5)

    popup.mainloop()

if __name__ == "__main__":
    mostrar_menu()
