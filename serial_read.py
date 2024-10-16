import serial
import time
import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib.pyplot as plt
from collections import deque
from proxydb import SensorDataInserterSQLite
# Configurar el puerto serial
arduino_port = 'COM6'  # Cambia esto según tu puerto
baud_rate = 9600  # Velocidad de transmisión (baud rate)
timeout = 1  # Tiempo de espera en segundos para la lectura
ser = serial.Serial(arduino_port, baud_rate, timeout=timeout)

# Buffer para los datos (almacenará los últimos 100 valores)
data_buffer = deque(maxlen=100)

def main(page: ft.Page):
    inserter = SensorDataInserterSQLite(db_file="sensores.db")
    # Configuración inicial de la ventana
    page.title = "Gráfica de Datos en Tiempo Real"
    page.window_width = 800
    page.window_height = 600
    
    # Crear una figura de matplotlib
    fig, ax = plt.subplots()
    line, = ax.plot([], [], label="Datos del sensor")
    ax.set_xlim(0, 100)  # Eje X de 0 a 100
    ax.set_ylim(0, 1023)  # Eje Y ajustado para un valor de 10 bits (0 a 1023)

    # Inicializar la gráfica en la app de Flet
    chart = MatplotlibChart(fig, expand=True)

    # Agregar el gráfico a la página
    page.add(chart)

    def update_chart():
        # Actualizar la gráfica con los nuevos datos
        line.set_xdata(range(len(data_buffer)))  # Actualizar los valores del eje X
        line.set_ydata(data_buffer)  # Actualizar los valores del eje Y
        ax.relim()  # Recalcular límites de los datos
        ax.autoscale_view()  # Ajustar la vista de la gráfica
        chart.update()  # Actualizar la gráfica en Flet

    def read_serial_data():
        try:
            print(f"Conectado al puerto {arduino_port}")
            time.sleep(2)  # Esperar a que el Arduino se inicialice
            while True:
                if ser.in_waiting > 0:  # Verificar si hay datos disponibles
                    data = ser.readline().decode('utf-8').strip()  # Leer y decodificar los datos
                    if data.isdigit():  # Verificar que los datos sean números
                        data_buffer.append(int(data))  # Agregar los datos al buffer
                        print(f"Datos recibidos: {data}")  # Imprimir datos recibidos
                        mq135_valor = 300  # Ejemplo de valor del sensor MQ-135
                        mq4_valor = 200    # Ejemplo de valor del sensor MQ-4
                        fecha_valor = time.ctime()
                        inserter.insertar_datos(fecha_valor, mq135_valor, mq4_valor)
                        update_chart()  # Actualizar la gráfica en tiempo real
        except serial.SerialException as e:
            print(f"Error de conexión: {e}")
        finally:
            if ser.is_open:
                ser.close()  # Cerrar el puerto serial si está abierto
                print("Conexión serial cerrada")

    # Iniciar el proceso de lectura serial en otro hilo
    page.add(ft.ElevatedButton("Iniciar Lectura Serial", on_click=lambda _: read_serial_data()))

# Correr la aplicación Flet
ft.app(target=main)
