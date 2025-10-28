"""
Módulo de utilidades para la aplicación.
Contiene funciones auxiliares utilizadas en diferentes partes de la aplicación.
"""
import re
from datetime import datetime

def validar_correo(correo):
    """
    Valida que un correo electrónico tenga un formato válido.
    
    Args:
        correo (str): Correo electrónico a validar
        
    Returns:
        bool: True si el correo es válido, False en caso contrario
    """
    # expresión regular para validar el correo
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(patron, correo))

def formatear_duracion(minutos):
    horas = minutos // 60
    minutos_restantes = minutos % 60
    return f"{horas:02d}:{minutos_restantes:02d}"

def generar_slug(texto):
    """
    Genera un slug a partir de un texto.
    Un slug es una versión de texto amigable para URLs.
    
    Args:
        texto (str): Texto a convertir en slug
        
    Returns:
        str: Slug generado
    """
    # Convertir a minúsculas
    slug = texto.lower()
    
    # Reemplazar espacios con guiones
    slug = re.sub(r'[\s_]+', '-', slug)
    # Eliminar caracteres no alfanuméricos (excepto guiones)
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    # Reemplazar múltiples guiones con uno solo
    slug = re.sub(r'[-]+', '-', slug)
    # Eliminar guiones al inicio y final
    slug = slug.strip('-')
    return slug

def obtener_año_actual():
    """
    Obtiene el año actual.
    
    Returns:
        int: Año actual
    """
    return datetime.now().year

def validar_año(año):
    """
    Valida que un año sea válido (no futuro y no muy antiguo).
    
    Args:
        año (int): Año a validar
        
    Returns:
        bool: True si el año es válido, False en caso contrario
    """
    año_actual = obtener_año_actual()
    return 1900 <= año <= año_actual

