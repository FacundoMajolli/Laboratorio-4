import cv2
import numpy as np
import pandas as pd
from datetime import datetime
import threading
import keyboard
import os
import sys

# Verificar si el archivo Excel ya existe
archivo_excel = 'qr_data.xlsx'
if os.path.exists(archivo_excel):
    # Si existe, carga el DataFrame desde el archivo
    df = pd.read_excel(archivo_excel, engine='openpyxl')
else:
    # Si no existe, crea un DataFrame vacío
    df = pd.DataFrame(columns=['DNI', 'Apellido', 'Nombre', 'Fecha', 'Hora'])

# Configurar la captura de video con menor resolución
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Reducir a la mitad
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Reducir a la mitad

# Variable para controlar la ejecución
escaneo_completo = False

# Variable para controlar si se cerró la cámara por Escape
camera_closed_by_escape = False

# Función para captura y procesamiento en un hilo
def captura_y_procesamiento():
    global df, escaneo_completo, camera_closed_by_escape
    while capture.isOpened():
        ret, frame = capture.read()

        qrDetector = cv2.QRCodeDetector()
        data, bbox, rectifiedImage = qrDetector.detectAndDecode(frame)

        if bbox is not None and bbox.size > 0 and len(data) > 0 and not escaneo_completo:
            print(f'Dato: {data}')

            # Obtener la fecha y hora actual
            now = datetime.now()
            fecha_hora_actual = now.strftime("%Y-%m-%d %H:%M:%S")

            # Dividir la información del código QR
            info_split = data.split('\n')
            dni, apellido, nombre = info_split[0].split(': ')[1], info_split[1].split(': ')[1], info_split[2].split(': ')[1]

            # Agregar datos al DataFrame
            nueva_fila = pd.DataFrame({'DNI': [dni], 'Apellido': [apellido], 'Nombre': [nombre], 'Fecha': [now.strftime("%Y-%m-%d")], 'Hora': [now.strftime("%H:%M:%S")]})

            # Reorganizar las columnas del DataFrame
            nueva_fila = nueva_fila[['DNI', 'Apellido', 'Nombre', 'Fecha', 'Hora']]

            # Agregar la nueva fila al DataFrame
            df = pd.concat([df, nueva_fila], ignore_index=True)

            cv2.imshow('webCam', rectifiedImage)

            # Agrega un pequeño retraso para procesar menos cuadros por segundo
            cv2.waitKey(10)
            
            # Marcar que el escaneo ha sido completado
            escaneo_completo = True

            # Cerrar la cámara después del escaneo completo
            capture.release()
            cv2.destroyAllWindows()

        else:
            cv2.imshow('webCam', frame)

        # Liberar la tecla después de procesarla
        key = cv2.waitKey(1)
        if key == 27:  # Verifica si la tecla presionada es 'ESC' (27 es el código ASCII para la tecla ESC)
            camera_closed_by_escape = True
            break

# Iniciar el hilo para captura y procesamiento
thread = threading.Thread(target=captura_y_procesamiento)
thread.start()

# Esperar a que el hilo termine antes de continuar
thread.join()

# Si la cámara se cerró por Escape, se cierra el programa sin actualizar el DataFrame
if camera_closed_by_escape:
    sys.exit()

# Guardar el DataFrame en un archivo Excel si se completó el escaneo para actualizarlo
df.iloc[:, :5].to_excel(archivo_excel, index=False, sheet_name='Sheet1', header=True, startrow=0, engine='openpyxl')

print("DataFrame actualizado:")
print(df)


