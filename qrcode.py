import cv2
import numpy as np
import pandas as pd
from datetime import datetime

# Crear un DataFrame para almacenar los datos
df = pd.DataFrame(columns=['QR_Data', 'Fecha', 'Hora'])

capture = cv2.VideoCapture(0)

while capture.isOpened():
    ret, frame = capture.read()

    qrDetector = cv2.QRCodeDetector()
    data, bbox, rectifiedImage = qrDetector.detectAndDecode(frame)

    if len(data) > 0:
        print(f'Dato: {data}')

        # Obtener la fecha y hora actual
        now = datetime.now()
        fecha_hora_actual = now.strftime("%Y-%m-%d %H:%M:%S")

        # Agregar datos al DataFrame
        new_data = pd.DataFrame({'QR_Data': [data], 'Fecha': [now.strftime("%Y-%m-%d")], 'Hora': [now.strftime("%H:%M:%S")]})
        df = pd.concat([new_data, df], ignore_index=True)

        # Guardar el DataFrame en un archivo Excel
        df.to_excel('qr_data.xlsx', index=False)

        cv2.imshow('webCam', rectifiedImage)

        # Agrega un pequeño retraso para permitir ver la imagen
        cv2.waitKey(200)

    else:
        cv2.imshow('webCam', frame)

    # Liberar la tecla después de procesarla
    key = cv2.waitKey(1)
    if key == ord('s'):
        break

capture.release()
cv2.destroyAllWindows()
