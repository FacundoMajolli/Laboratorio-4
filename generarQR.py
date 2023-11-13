import qrcode

def generar_qr(nombre, apellido, dni):
    # Combina la información en una cadena
    informacion = f"DNI: {dni}\nApellido: {apellido}\nNombre: {nombre}"

    # Crea un objeto QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Agrega la información al código QR
    qr.add_data(informacion)
    qr.make(fit=True)

    # Crea una imagen QR utilizando la biblioteca PIL
    imagen_qr = qr.make_image(fill_color="black", back_color="white")

    # Guarda la imagen QR en un archivo
    nombre_archivo = f"DNI_{dni}_qr.png"
    imagen_qr.save(nombre_archivo)

    print(f"Código QR generado y guardado como {nombre_archivo}")

# Ejemplo de uso
nombre = "Alejandro"
apellido = "Guiñazu"
dni = "27775770"

generar_qr(nombre, apellido, dni)
