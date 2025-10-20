"""
Módulo de gestión de agenda telefónica
Proporciona funcionalidades para registrar, consultar y eliminar contactos
"""

import re
from typing import Dict, List, Optional


class ContactoInvalidoError(Exception):
    """Excepción personalizada para contactos inválidos"""

    pass


class AgendaTelefonica:
    """Clase para gestionar una agenda telefónica"""

    def __init__(self):
        """Inicializa la agenda con un diccionario vacío"""
        self.contactos: Dict[str, str] = {}

    def _normalizar_nombre(self, nombre: str) -> str:
        """
        Normaliza el nombre eliminando espacios extra y capitalizando palabras

        Args:
            nombre: Nombre a normalizar

        Returns:
            str: Nombre normalizado
        """
        # Eliminar espacios extra y capitalizar cada palabra
        palabras = nombre.strip().split()
        return " ".join(palabra.capitalize() for palabra in palabras)

    def _limpiar_telefono(self, telefono: str) -> str:
        """
        Limpia el teléfono eliminando caracteres especiales

        Args:
            telefono: Número de teléfono a limpiar

        Returns:
            str: Teléfono solo con dígitos
        """
        # Remover todos los caracteres que no sean dígitos
        return re.sub(r"[^\d]", "", telefono)

    def validar_nombre(self, nombre: str) -> bool:
        """
        Valida que el nombre solo contenga letras y espacios

        Args:
            nombre: Nombre del contacto a validar

        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not nombre or not nombre.strip():
            return False

        # Solo letras, espacios y tildes
        patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$"
        return bool(re.match(patron, nombre.strip()))

    def validar_telefono(self, telefono: str) -> bool:
        """
        Valida que el teléfono contenga solo dígitos y tenga entre 7-15 caracteres

        Args:
            telefono: Número de teléfono a validar

        Returns:
            bool: True si es válido, False en caso contrario
        """
        if not telefono:
            return False

        # Limpiar el teléfono primero
        telefono_limpio = self._limpiar_telefono(telefono)

        if not telefono_limpio:
            return False

        # Verificar que no tenga letras después de limpiar caracteres especiales
        # Si el teléfono original tenía letras, el limpio será más corto
        telefono_sin_espacios = (
            telefono.replace(" ", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
            .replace("+", "")
        )
        if not telefono_sin_espacios.isdigit():
            return False

        # Longitud entre 7 y 15 dígitos
        return 7 <= len(telefono_limpio) <= 15

    def registrar_contacto(self, nombre: str, telefono: str) -> Dict:
        """
        Registra un nuevo contacto en la agenda

        Args:
            nombre: Nombre del contacto
            telefono: Número de teléfono del contacto

        Returns:
            Dict con success, message, mensaje y contacto

        Raises:
            ValueError: Si el nombre o teléfono no son válidos
        """
        nombre = nombre.strip()
        telefono = telefono.strip()

        # Validar nombre
        if not self.validar_nombre(nombre):
            raise ValueError("Nombre inválido. Debe contener solo letras y espacios")

        # Validar teléfono
        if not self.validar_telefono(telefono):
            raise ValueError("Teléfono inválido. Debe contener entre 7-15 dígitos")

        # Normalizar nombre
        nombre_normalizado = self._normalizar_nombre(nombre)

        # Verificar duplicados (case-insensitive)
        if nombre_normalizado in self.contactos:
            raise ValueError(
                f"El contacto '{nombre_normalizado}' ya existe en la agenda"
            )

        # Limpiar teléfono
        telefono_limpio = self._limpiar_telefono(telefono)

        # Guardar contacto
        self.contactos[nombre_normalizado] = telefono_limpio

        mensaje_texto = f"Contacto '{nombre_normalizado}' registrado exitosamente"

        return {
            "success": True,
            "message": mensaje_texto,
            "mensaje": "Contacto registrado exitosamente",  # Para compatibilidad con tests
            "contacto": {"nombre": nombre_normalizado, "telefono": telefono_limpio},
        }

    def consultar_contacto(self, nombre: str) -> Optional[Dict[str, str]]:
        """
        Consulta un contacto por nombre (case-insensitive)

        Args:
            nombre: Nombre del contacto a buscar

        Returns:
            Dict con los datos del contacto o None si no existe
        """
        if not nombre or not nombre.strip():
            return None

        # Normalizar nombre para búsqueda
        nombre_normalizado = self._normalizar_nombre(nombre)

        if nombre_normalizado in self.contactos:
            return {
                "nombre": nombre_normalizado,
                "telefono": self.contactos[nombre_normalizado],
            }

        return None

    def listar_contactos(self) -> List[Dict[str, str]]:
        """
        Lista todos los contactos de la agenda ordenados alfabéticamente

        Returns:
            Lista de diccionarios con todos los contactos
        """
        return [
            {"nombre": nombre, "telefono": telefono}
            for nombre, telefono in sorted(self.contactos.items())
        ]

    def eliminar_contacto(self, nombre: str) -> Dict:
        """
        Elimina un contacto de la agenda

        La eliminación es case-sensitive: "juan pérez" NO encontrará "Juan Pérez"
        Solo normaliza espacios extra: "  Juan   Pérez  " encontrará "Juan Pérez"

        Args:
            nombre: Nombre del contacto a eliminar

        Returns:
            Dict con mensaje, nombre y telefono del contacto eliminado

        Raises:
            ContactoInvalidoError: Si el contacto no existe
        """
        if not nombre or not nombre.strip():
            raise ContactoInvalidoError("Nombre inválido")

        # Solo normalizar espacios extra, mantener mayúsculas/minúsculas exactas
        nombre_con_espacios_normalizados = " ".join(nombre.strip().split())

        # Buscar el contacto con el nombre EXACTO (case-sensitive)
        if nombre_con_espacios_normalizados not in self.contactos:
            raise ContactoInvalidoError(
                f"El contacto '{nombre_con_espacios_normalizados}' no existe en la agenda"
            )

        telefono = self.contactos[nombre_con_espacios_normalizados]
        del self.contactos[nombre_con_espacios_normalizados]

        return {
            "mensaje": "Contacto eliminado exitosamente",
            "nombre": nombre_con_espacios_normalizados,
            "telefono": telefono,
        }

    def contar_contactos(self) -> int:
        """
        Retorna el total de contactos en la agenda

        Returns:
            int: Número total de contactos
        """
        return len(self.contactos)

    def total_contactos(self) -> int:
        """
        Alias de contar_contactos para compatibilidad con API

        Returns:
            int: Número total de contactos
        """
        return self.contar_contactos()
