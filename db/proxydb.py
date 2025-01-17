import sqlite3
import time

class SensorDataInserterSQLite:
    def __init__(self, db_file):
        # Conexión a la base de datos SQLite
        #self.connection = sqlite3.connect(db_file)
        self.db_file = db_file
        #self.cursor = self.connection.cursor()
        print("Conectado a la base de datos SQLite")
        connection = sqlite3.connect(self.db_file)
        cursor = connection.cursor()
        # Crear la tabla si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lecturas_sensores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sensor_mq135 INTEGER NOT NULL,
                sensor_mq3 INTEGER NOT NULL
            )
        ''')
        connection.commit()

    def insertar_datos(self, fecha_valor, mq135_valor, mq4_valor):
        try:
            connection = sqlite3.connect(self.db_file)
            cursor = connection.cursor()
            # Crear la consulta SQL para insertar los datos
            sql = "INSERT INTO lecturas_sensores (fecha, sensor_mq135, sensor_mq3) VALUES (?, ?, ?)"
            values = (fecha_valor, mq135_valor, mq4_valor)
            
            # Ejecutar la consulta
            cursor.execute(sql, values)
            
            # Confirmar cambios en la base de datos
            #self.connection.commit()
            connection.commit()
            print(f"{fecha_valor} - Datos insertados: MQ-135 = {mq135_valor}, MQ-3 = {mq4_valor}")
        
        except sqlite3.Error as e:
            print(f"Error al insertar los datos: {e}")
            self.connection.rollback()
    
    def cerrar_conexion(self):
        # Cerrar cursor y conexión
        self.cursor.close()
        self.connection.close()
        print("Conexión a la base de datos cerrada")
