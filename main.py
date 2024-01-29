import tkinter as tk
from tkinter import ttk
import logging
import multiprocessing
from apolo11.python.utils.Utils import run_simulation, run_reports

# Configuración básica de logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_simulation_process(stop_flag):
    global stop_execution_flag
    try:
        run_simulation(stop_flag)
    except KeyboardInterrupt:
        logging.info("\nSimulation process interrupted. Exit...")


def run_reports_process():
    global stop_execution_flag
    run_reports()


def main():
    # Multiprocessing managers for communication
    manager = multiprocessing.Manager()
    stop_execution_flag = manager.Value('b', False)

    def ejecutar_simulacion():
        global stop_execution_flag
        stop_execution_flag = manager.Value('b', False)
        simulation_process = multiprocessing.Process(target=run_simulation_process, args=(stop_execution_flag,))
        simulation_process.start()
        label.config(text="Simulation running.")
        logging.info("Simulation started.")

    def ejecutar_reportes():
        global stop_execution_flag
        stop_execution_flag = manager.Value('b', False)
        reports_process = multiprocessing.Process(target=run_reports_process)
        reports_process.start()
        label.config(text="Reports running.")
        logging.info("Reports started.")

    def detener_ejecucion():
        global stop_execution_flag
        stop_execution_flag.value = True
        label.config(text="Execution stopping...")
        logging.warning("Execution stopping.")

    def salir():
        global popup
        popup.destroy()
        logging.info("Application closed.")

    def mostrar_menu():
        global popup
        global label

        popup = tk.Tk()
        popup.title("Interactive menu")
        popup.geometry("300x250")  # Tamaño de la ventana

        style = ttk.Style()

        # Establecer el color de fondo del botón "Salir" en rojo
        style.configure("TButton", padding=(10, 5, 10, 5), font='Helvetica 10')
        style.map("TButton", background=[('active', 'red')])

        label = tk.Label(popup, text="Please select an option:")
        label.pack(pady=10)

        btn_simulacion = ttk.Button(popup, text="EXECUTE SIMULATION", command=ejecutar_simulacion)
        btn_simulacion.pack(pady=5)

        btn_reportes = ttk.Button(popup, text="EXECUTE REPORTS", command=ejecutar_reportes)
        btn_reportes.pack(pady=5)

        btn_detener = ttk.Button(popup, text="STOP EXECUTION", command=detener_ejecucion, style="TButton")
        btn_detener.pack(pady=5)

        btn_salir = ttk.Button(popup, text="EXIT", command=salir, style="TButton")
        btn_salir.pack(pady=5)

        popup.mainloop()

    # Call freeze_support to enable the proper process spawning on Windows
    multiprocessing.freeze_support()
    
    mostrar_menu()


if __name__ == "__main__":
    main()
