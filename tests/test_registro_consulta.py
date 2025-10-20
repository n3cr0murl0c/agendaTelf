"""
Pruebas unitarias para funciones de registro y consulta de contactos
Desarrolladores A
"""

import pytest
from src.agenda import AgendaTelefonica


class TestRegistroContactos:
    """Pruebas para la función de registro de contactos"""

    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.agenda = AgendaTelefonica()

    def test_registrar_contacto_exitoso(self):
        """Verifica que se pueda registrar un contacto válido"""
        resultado = self.agenda.registrar_contacto("Juan Pérez", "0987654321")

        assert resultado["success"] is True
        assert "Juan Pérez" in resultado["message"]
        assert resultado["contacto"]["nombre"] == "Juan Pérez"
        assert str(resultado["contacto"]["telefono"]) == "0987654321"

    def test_registrar_contacto_con_espacios(self):
        """Verifica normalización de nombres con espacios extra"""
        resultado = self.agenda.registrar_contacto("  María  García  ", "0998765432")

        assert resultado["success"] is True
        assert resultado["contacto"]["nombre"] == "María García"

    def test_registrar_contacto_con_tildes(self):
        """Verifica que se acepten nombres con tildes y ñ"""
        resultado = self.agenda.registrar_contacto("José Muñoz", "0987654321")

        assert resultado["success"] is True
        assert resultado["contacto"]["nombre"] == "José Muñoz"

    def test_registrar_telefono_formato_internacional(self):
        """Verifica limpieza de caracteres especiales en teléfono"""
        resultado = self.agenda.registrar_contacto("Ana López", "+593 98-765-4321")

        assert resultado["success"] is True
        assert resultado["contacto"]["telefono"] == "593987654321"

    def test_registrar_telefono_con_parentesis(self):
        """Verifica limpieza de paréntesis en teléfono"""
        resultado = self.agenda.registrar_contacto("Carlos Ruiz", "(02) 2345678")

        assert resultado["success"] is True
        assert resultado["contacto"]["telefono"] == "022345678"

    def test_registrar_contacto_duplicado(self):
        """Verifica que no se permitan contactos duplicados"""
        self.agenda.registrar_contacto("Pedro Sánchez", "0987654321")

        with pytest.raises(ValueError) as excinfo:
            self.agenda.registrar_contacto("Pedro Sánchez", "0998765432")

        assert "ya existe" in str(excinfo.value)

    def test_registrar_nombre_vacio(self):
        """Verifica que no se acepte un nombre vacío"""
        with pytest.raises(ValueError) as excinfo:
            self.agenda.registrar_contacto("", "0987654321")

        assert "Nombre inválido" in str(excinfo.value)

    def test_registrar_nombre_solo_espacios(self):
        """Verifica que no se acepte un nombre con solo espacios"""
        with pytest.raises(ValueError) as excinfo:
            self.agenda.registrar_contacto("   ", "0987654321")

        assert "Nombre inválido" in str(excinfo.value)

    def test_registrar_nombre_con_numeros(self):
        """Verifica que no se acepten nombres con números"""
        with pytest.raises(ValueError) as excinfo:
            self.agenda.registrar_contacto("Juan123", "0987654321")

        assert "Nombre inválido" in str(excinfo.value)

    def test_registrar_nombre_con_caracteres_especiales(self):
        """Verifica que no se acepten nombres con caracteres especiales"""
        with pytest.raises(ValueError) as excinfo:
            self.agenda.registrar_contacto("Juan@Pérez", "0987654321")

        assert "Nombre inválido" in str(excinfo.value)

    def test_registrar_telefono_vacio(self):
        """Verifica que no se acepte un teléfono vacío"""
        with pytest.raises(ValueError) as excinfo:
            self.agenda.registrar_contacto("Juan Pérez", "")

        assert "Teléfono inválido" in str(excinfo.value)

    def test_registrar_telefono_muy_corto(self):
        """Verifica que no se acepte un teléfono menor a 7 dígitos"""
        with pytest.raises(ValueError) as excinfo:
            self.agenda.registrar_contacto("Juan Pérez", "123456")

        assert "Teléfono inválido" in str(excinfo.value)

    def test_registrar_telefono_muy_largo(self):
        """Verifica que no se acepte un teléfono mayor a 15 dígitos"""
        with pytest.raises(ValueError) as excinfo:
            self.agenda.registrar_contacto("Juan Pérez", "1234567890123456")

        assert "Teléfono inválido" in str(excinfo.value)

    def test_registrar_telefono_con_letras(self):
        """Verifica que no se acepte un teléfono con letras"""
        with pytest.raises(ValueError) as excinfo:
            self.agenda.registrar_contacto("Juan Pérez", "098abc4321")

        assert "Teléfono inválido" in str(excinfo.value)

    def test_registrar_multiples_contactos(self):
        """Verifica registro de múltiples contactos diferentes"""
        self.agenda.registrar_contacto("Juan Pérez", "0987654321")
        self.agenda.registrar_contacto("María García", "0998765432")
        self.agenda.registrar_contacto("Pedro López", "0976543210")

        assert self.agenda.contar_contactos() == 3


class TestConsultaContactos:
    """Pruebas para la función de consulta de contactos"""

    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.agenda = AgendaTelefonica()
        # Agregar contactos de prueba
        self.agenda.registrar_contacto("Juan Pérez", "0987654321")
        self.agenda.registrar_contacto("María García", "0998765432")
        self.agenda.registrar_contacto("José Muñoz", "0976543210")

    def test_consultar_contacto_existente(self):
        """Verifica consulta de un contacto que existe"""
        contacto = self.agenda.consultar_contacto("Juan Pérez")

        assert contacto is not None
        assert contacto["nombre"] == "Juan Pérez"
        assert contacto["telefono"] == "0987654321"

    def test_consultar_contacto_normaliza_nombre(self):
        """Verifica que la búsqueda normalice el nombre"""
        contacto = self.agenda.consultar_contacto("  juan pérez  ")

        assert contacto is not None
        assert contacto["nombre"] == "Juan Pérez"

    def test_consultar_contacto_case_insensitive(self):
        """Verifica que la búsqueda no distinga mayúsculas"""
        contacto = self.agenda.consultar_contacto("JUAN PÉREZ")

        assert contacto is not None
        assert contacto["nombre"] == "Juan Pérez"

    def test_consultar_contacto_inexistente(self):
        """Verifica consulta de un contacto que no existe"""
        contacto = self.agenda.consultar_contacto("Pedro Sánchez")

        assert contacto is None

    def test_consultar_nombre_vacio(self):
        """Verifica que retorne None con nombre vacío"""
        contacto = self.agenda.consultar_contacto("")

        assert contacto is None

    def test_consultar_nombre_solo_espacios(self):
        """Verifica que retorne None con solo espacios"""
        contacto = self.agenda.consultar_contacto("   ")

        assert contacto is None

    def test_consultar_todos_los_contactos(self):
        """Verifica que se puedan consultar todos los contactos agregados"""
        assert self.agenda.consultar_contacto("Juan Pérez") is not None
        assert self.agenda.consultar_contacto("María García") is not None
        assert self.agenda.consultar_contacto("José Muñoz") is not None


class TestListarContactos:
    """Pruebas para la función de listar contactos"""

    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.agenda = AgendaTelefonica()

    def test_listar_agenda_vacia(self):
        """Verifica que una agenda vacía retorne lista vacía"""
        contactos = self.agenda.listar_contactos()

        assert contactos == []
        assert len(contactos) == 0

    def test_listar_un_contacto(self):
        """Verifica listado con un solo contacto"""
        self.agenda.registrar_contacto("Juan Pérez", "0987654321")
        contactos = self.agenda.listar_contactos()

        assert len(contactos) == 1
        assert contactos[0]["nombre"] == "Juan Pérez"
        assert contactos[0]["telefono"] == "0987654321"

    def test_listar_multiples_contactos(self):
        """Verifica listado con múltiples contactos"""
        self.agenda.registrar_contacto("Juan Pérez", "0987654321")
        self.agenda.registrar_contacto("María García", "0998765432")
        self.agenda.registrar_contacto("Pedro López", "0976543210")

        contactos = self.agenda.listar_contactos()

        assert len(contactos) == 3

    def test_listar_orden_alfabetico(self):
        """Verifica que los contactos estén ordenados alfabéticamente"""
        self.agenda.registrar_contacto("Zulma Torres", "0987654321")
        self.agenda.registrar_contacto("Ana Martínez", "0998765432")
        self.agenda.registrar_contacto("Mario Gómez", "0976543210")

        contactos = self.agenda.listar_contactos()

        assert contactos[0]["nombre"] == "Ana Martínez"
        assert contactos[1]["nombre"] == "Mario Gómez"
        assert contactos[2]["nombre"] == "Zulma Torres"

    def test_listar_estructura_datos(self):
        """Verifica que cada contacto tenga la estructura correcta"""
        self.agenda.registrar_contacto("Juan Pérez", "0987654321")
        contactos = self.agenda.listar_contactos()

        assert "nombre" in contactos[0]
        assert "telefono" in contactos[0]
        assert len(contactos[0]) == 2


class TestValidaciones:
    """Pruebas para funciones de validación"""

    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.agenda = AgendaTelefonica()

    def test_validar_nombre_correcto(self):
        """Verifica validación de nombres correctos"""
        assert self.agenda.validar_nombre("Juan Pérez") is True
        assert self.agenda.validar_nombre("María José") is True
        assert self.agenda.validar_nombre("José Muñoz") is True

    def test_validar_nombre_incorrecto(self):
        """Verifica validación de nombres incorrectos"""
        assert self.agenda.validar_nombre("") is False
        assert self.agenda.validar_nombre("   ") is False
        assert self.agenda.validar_nombre("Juan123") is False
        assert self.agenda.validar_nombre("Juan@Pérez") is False

    def test_validar_telefono_correcto(self):
        """Verifica validación de teléfonos correctos"""
        assert self.agenda.validar_telefono("0987654321") is True
        assert self.agenda.validar_telefono("1234567") is True
        assert self.agenda.validar_telefono("123456789012345") is True
        assert self.agenda.validar_telefono("+593 98-765-4321") is True

    def test_validar_telefono_incorrecto(self):
        """Verifica validación de teléfonos incorrectos"""
        assert self.agenda.validar_telefono("") is False
        assert self.agenda.validar_telefono("123456") is False
        assert self.agenda.validar_telefono("1234567890123456") is False
        assert self.agenda.validar_telefono("098abc4321") is False


class TestContadorContactos:
    """Pruebas para la función de contar contactos"""

    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.agenda = AgendaTelefonica()

    def test_contar_agenda_vacia(self):
        """Verifica conteo en agenda vacía"""
        assert self.agenda.contar_contactos() == 0

    def test_contar_despues_de_agregar(self):
        """Verifica conteo después de agregar contactos"""
        self.agenda.registrar_contacto("Juan Pérez", "0987654321")
        assert self.agenda.contar_contactos() == 1

        self.agenda.registrar_contacto("María García", "0998765432")
        assert self.agenda.contar_contactos() == 2

        self.agenda.registrar_contacto("Pedro López", "0976543210")
        assert self.agenda.contar_contactos() == 3
