# qr_strategy.py
from abc import ABC, abstractmethod
import qrcode
from io import BytesIO
from django.core.files import File

class QRCodeStrategy(ABC):
    """
    Interfaz para definir la estrategia de generación de códigos QR.
    """

    @abstractmethod
    def generate(self, text: str) -> File:
        """
        Genera un objeto File que contiene la imagen del código QR basado en el texto dado.
        
        :param text: Texto o datos que se usarán para generar el código QR.
        :return: Un objeto File con la imagen del QR.
        """
        pass

class DefaultQRCodeStrategy(QRCodeStrategy):
    """
    Implementación por defecto de la estrategia para generar códigos QR.
    Utiliza la librería 'qrcode' para crear la imagen y la encapsula en un objeto File.
    """
    def generate(self, text: str) -> File:
        # Crear el código QR utilizando la librería qrcode
        qr = qrcode.make(text)
        # Usamos BytesIO para guardar la imagen en memoria
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        # Posicionar el puntero al inicio del buffer
        buffer.seek(0)
        # Definir un nombre para el archivo. Aquí lo generamos a partir del texto (puedes personalizarlo)
        file_name = f"{text}_qr.png"
        # Retornar un objeto File de Django, que es compatible con ImageField
        return File(buffer, name=file_name)
