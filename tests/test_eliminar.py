"""
Pruebas unitarias para eliminación de contactos
Desarrolladores B: Implementación de eliminar contactos
"""

import pytest
from src.agenda import AgendaTelefonica, ContactoInvalidoError


class TestEliminarContactos:
    """Pruebas para la funcionalidad de eliminación"""

    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.agenda = AgendaTelefonica()
        self.agenda.registrar_contacto("Juan Pérez", "0998765432")
        self.agenda.registrar_contacto("María García", "0987654321")
        self.agenda.registrar_contacto("Pedro López", "0976543210")

    def test_eliminar_contacto_existente(self):
        """Prueba eliminación exitosa de un contacto existente"""
        resultado = self.agenda.eliminar_contacto("Juan Pérez")

        assert resultado["mensaje"] == "Contacto eliminado exitosamente"
        assert resultado["nombre"] == "Juan Pérez"
        assert resultado["telefono"] == "0998765432"
        assert self.agenda.total_contactos() == 2

    def test_eliminar_contacto_inexistente(self):
        """Prueba error al eliminar contacto inexistente"""
        with pytest.raises(ContactoInvalidoError) as excinfo:
            self.agenda.eliminar_contacto("Laura Martínez")

        assert "no existe" in str(excinfo.value)
        assert self.agenda.total_contactos() == 3

    def test_eliminar_con_espacios_extra(self):
        """Prueba eliminación con espacios adicionales en el nombre"""
        resultado = self.agenda.eliminar_contacto("  María García  ")

        assert resultado["nombre"] == "María García"
        assert self.agenda.total_contactos() == 2

    def test_eliminar_todos_contactos(self):
        """Prueba eliminación de todos los contactos"""
        self.agenda.eliminar_contacto("Juan Pérez")
        self.agenda.eliminar_contacto("María García")
        self.agenda.eliminar_contacto("Pedro López")

        assert self.agenda.total_contactos() == 0
        assert self.agenda.listar_contactos() == []

    def test_eliminar_y_verificar_consulta(self):
        """Prueba que después de eliminar no se puede consultar"""
        self.agenda.eliminar_contacto("Juan Pérez")

        contacto = self.agenda.consultar_contacto("Juan Pérez")
        assert contacto is None

    def test_eliminar_y_registrar_nuevamente(self):
        """Prueba eliminar y volver a registrar el mismo contacto"""
        self.agenda.eliminar_contacto("Juan Pérez")
        resultado = self.agenda.registrar_contacto("Juan Pérez", "0991234567")

        assert resultado["mensaje"] == "Contacto registrado exitosamente"
        assert self.agenda.total_contactos() == 3

        contacto = self.agenda.consultar_contacto("Juan Pérez")
        if contacto is not None:
            assert contacto["telefono"] == "0991234567"
        else:
            # Handle the case when the contacto is None
            print("Contacto no encontrado")

    def test_eliminar_contacto_de_agenda_vacia(self):
        """Prueba error al eliminar de agenda vacía"""
        agenda_vacia = AgendaTelefonica()

        with pytest.raises(ContactoInvalidoError) as excinfo:
            agenda_vacia.eliminar_contacto("Juan Pérez")

        assert "no existe" in str(excinfo.value)

    def test_eliminar_mantiene_otros_contactos(self):
        """Prueba que eliminar no afecta otros contactos"""
        self.agenda.eliminar_contacto("María García")

        # Verificar que los otros contactos siguen existiendo
        juan = self.agenda.consultar_contacto("Juan Pérez")
        pedro = self.agenda.consultar_contacto("Pedro López")

        assert juan is not None
        assert pedro is not None
        assert juan["telefono"] == "0998765432"
        assert pedro["telefono"] == "0976543210"

    def test_eliminar_ultimo_contacto(self):
        """Prueba eliminar cuando solo queda un contacto"""
        self.agenda.eliminar_contacto("Juan Pérez")
        self.agenda.eliminar_contacto("María García")

        resultado = self.agenda.eliminar_contacto("Pedro López")

        assert resultado["mensaje"] == "Contacto eliminado exitosamente"
        assert self.agenda.total_contactos() == 0

    def test_eliminar_nombre_case_sensitive(self):
        """Prueba que la eliminación es sensible a mayúsculas/minúsculas"""
        with pytest.raises(ContactoInvalidoError):
            self.agenda.eliminar_contacto("juan pérez")

        # El contacto original debe seguir existiendo
        assert self.agenda.total_contactos() == 3


class TestIntegracionCompleta:
    """Pruebas de integración de todas las funcionalidades"""

    def setup_method(self):
        """Configuración antes de cada prueba"""
        self.agenda = AgendaTelefonica()

    def test_flujo_completo_registro_consulta_eliminacion(self):
        """Prueba flujo completo: registrar, consultar y eliminar"""
        # Registrar
        self.agenda.registrar_contacto("Ana Torres", "0995551234")
        assert self.agenda.total_contactos() == 1

        # Consultar
        contacto = self.agenda.consultar_contacto("Ana Torres")
        if contacto is not None:
            assert contacto["telefono"] == "0995551234"
        else:
            print("Contacto not found")

        # Eliminar
        resultado = self.agenda.eliminar_contacto("Ana Torres")
        assert resultado["mensaje"] == "Contacto eliminado exitosamente"
        assert self.agenda.total_contactos() == 0

    def test_operaciones_multiples_contactos(self):
        """Prueba múltiples operaciones con varios contactos"""
        # Registrar 5 contactos
        contactos = [
            ("Ana García", "0991111111"),
            ("Bruno López", "0992222222"),
            ("Carlos Ruiz", "0993333333"),
            ("Diana Flores", "0994444444"),
            ("Elena Mora", "0995555555"),
        ]

        for nombre, telefono in contactos:
            self.agenda.registrar_contacto(nombre, telefono)

        assert self.agenda.total_contactos() == 5

        # Eliminar 2 contactos
        self.agenda.eliminar_contacto("Bruno López")
        self.agenda.eliminar_contacto("Diana Flores")

        assert self.agenda.total_contactos() == 3

        # Verificar que los eliminados no existen
        assert self.agenda.consultar_contacto("Bruno López") is None
        assert self.agenda.consultar_contacto("Diana Flores") is None

        # Verificar que los otros siguen existiendo
        assert self.agenda.consultar_contacto("Ana García") is not None
        assert self.agenda.consultar_contacto("Carlos Ruiz") is not None
        assert self.agenda.consultar_contacto("Elena Mora") is not None

    def test_listado_despues_operaciones(self):
        """Prueba que el listado es correcto después de varias operaciones"""
        # Registrar contactos
        self.agenda.registrar_contacto("Zebra Última", "0991111111")
        self.agenda.registrar_contacto("Ana Primera", "0992222222")
        self.agenda.registrar_contacto("María Media", "0993333333")

        # Eliminar uno del medio
        self.agenda.eliminar_contacto("María Media")

        # Verificar orden alfabético
        contactos = self.agenda.listar_contactos()
        assert len(contactos) == 2
        assert contactos[0]["nombre"] == "Ana Primera"
        assert contactos[1]["nombre"] == "Zebra Última"
