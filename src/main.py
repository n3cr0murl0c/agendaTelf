"""
API REST para la Agenda Telefónica usando FastAPI

Esta API proporciona endpoints para gestionar una agenda telefónica,
permitiendo registrar, consultar, listar y eliminar contactos.

Endpoints disponibles:
- GET /: Información de la API
- POST /contactos/: Registrar un nuevo contacto
- GET /contactos/: Listar todos los contactos
- GET /contactos/{nombre}: Consultar un contacto específico
- DELETE /contactos/{nombre}: Eliminar un contacto
- GET /estadisticas/: Obtener estadísticas de la agenda
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import uvicorn

from src.agenda import AgendaTelefonica, ContactoInvalidoError

# ============================================================================
# CONFIGURACIÓN DE FASTAPI
# ============================================================================

app = FastAPI(
    title="Agenda Telefónica API",
    description="""
    ## 📱 API REST para Gestión de Agenda Telefónica
    
    Esta API permite gestionar una agenda de contactos telefónicos con las siguientes funcionalidades:
    
    ### Funcionalidades:
    * **Registrar** contactos con validación de datos
    * **Consultar** contactos por nombre
    * **Listar** todos los contactos ordenados alfabéticamente
    * **Eliminar** contactos existentes
    * **Estadísticas** de la agenda
    
    ### Validaciones:
    * **Nombres**: Solo letras, espacios y caracteres especiales (á, é, í, ó, ú, ñ)
    * **Teléfonos**: Entre 7 y 15 dígitos, se permiten guiones y espacios
    
    ### Desarrollado por:
    * @n3cr0murl0c
    """,
    version="1.0.0",
    contact={
        "name": "Equipo de Desarrollo",
        "email": "equipo@agenda-telefonica.com",
    },
    license_info={
        "name": "MIT",
    },
)

# Instancia global de la agenda (en producción usar base de datos)
agenda = AgendaTelefonica()


# ============================================================================
# CONFIGURACIÓN OPENAPI PERSONALIZADA
# ============================================================================


def custom_openapi():
    """Genera esquema OpenAPI personalizado con información extendida"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Agenda Telefónica API",
        version="1.0.0",
        description="""
        ## 📱 API REST para Gestión de Agenda Telefónica
        
        API completa para gestionar contactos telefónicos con validaciones robustas.
        
        ### Características:
        - ✅ Registro con validación de datos
        - 🔍 Búsqueda case-insensitive
        - 📋 Listado ordenado alfabéticamente
        - 🗑️ Eliminación segura
        - 📊 Estadísticas en tiempo real
        
        ### Tecnologías:
        - FastAPI 0.104+
        - Pydantic v2
        - Python 3.9+
        """,
        routes=app.routes,
        contact={
            "name": "Equipo 9",
            "email": "",
            "url": "https://github.com/n3cr0murl0c",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        servers=[
            {"url": "http://localhost:8000", "description": "Servidor de desarrollo"},
            {"url": "https://api.agenda-telefonica.com", "description": "Producción"},
        ],
        tags=[
            {"name": "Root", "description": "Información general de la API"},
            {
                "name": "Contactos",
                "description": "Operaciones CRUD para gestión de contactos",
            },
            {
                "name": "Estadísticas",
                "description": "Métricas y estadísticas de la agenda",
            },
        ],
    )

    # Agregar información de seguridad (si se implementa en el futuro)
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ============================================================================
# MODELOS PYDANTIC (SCHEMAS)
# ============================================================================


class ContactoCreate(BaseModel):
    """
    Modelo para crear un nuevo contacto

    Attributes:
        nombre: Nombre completo del contacto (solo letras y espacios)
        telefono: Número de teléfono (7-15 dígitos)
    """

    nombre: str = Field(
        min_length=1,
        max_length=100,
        description="Nombre del contacto (solo letras y espacios)",
    )
    telefono: str = Field(
        min_length=7, max_length=20, description="Número de teléfono (7-15 dígitos)"
    )

    @field_validator("nombre")
    @classmethod
    def validar_nombre_no_vacio(cls, v: str) -> str:
        """Valida que el nombre no esté vacío después de strip"""
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

    @field_validator("telefono")
    @classmethod
    def validar_telefono_no_vacio(cls, v: str) -> str:
        """Valida que el teléfono no esté vacío después de strip"""
        if not v.strip():
            raise ValueError("El teléfono no puede estar vacío")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [{"nombre": "María García", "telefono": "0987-654-321"}]
        }
    }


class ContactoResponse(BaseModel):
    """
    Modelo de respuesta de un contacto

    Attributes:
        nombre: Nombre del contacto
        telefono: Teléfono del contacto
    """

    nombre: str = Field(description="Nombre del contacto")
    telefono: str = Field(description="Número de teléfono")

    model_config = {
        "json_schema_extra": {
            "examples": [{"nombre": "María García", "telefono": "0987654321"}]
        }
    }


class MensajeResponse(BaseModel):
    """
    Modelo de respuesta con mensaje de operación

    Attributes:
        mensaje: Mensaje descriptivo de la operación
        nombre: Nombre del contacto (opcional)
        telefono: Teléfono del contacto (opcional)
    """

    mensaje: str = Field(description="Mensaje de respuesta")
    nombre: Optional[str] = Field(default=None, description="Nombre del contacto")
    telefono: Optional[str] = Field(default=None, description="Teléfono del contacto")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "mensaje": "Contacto registrado exitosamente",
                    "nombre": "María García",
                    "telefono": "0987654321",
                }
            ]
        }
    }


class EstadisticasResponse(BaseModel):
    """
    Modelo de respuesta de estadísticas

    Attributes:
        total_contactos: Número total de contactos
        mensaje: Mensaje descriptivo
    """

    total_contactos: int = Field(description="Total de contactos")
    mensaje: str = Field(description="Mensaje informativo")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"total_contactos": 5, "mensaje": "La agenda tiene 5 contacto(s)"}
            ]
        }
    }


# ============================================================================
# ENDPOINTS DE LA API
# ============================================================================


@app.get(
    "/",
    tags=["Root"],
    summary="Información de la API",
    response_description="Información general de la API",
)
def read_root():
    """
    ## Endpoint raíz de la API

    Retorna información básica sobre la API y enlaces útiles.

    ### Retorna:
    - Mensaje de bienvenida
    - Versión de la API
    - Enlaces a documentación
    """
    return {
        "mensaje": "Bienvenido a la Agenda Telefónica API",
        "version": "1.0.0",
        "documentacion_interactiva": "/docs",
        "documentacion_alternativa": "/redoc",
        "endpoints": {
            "registrar_contacto": "POST /contactos/",
            "listar_contactos": "GET /contactos/",
            "consultar_contacto": "GET /contactos/{nombre}",
            "eliminar_contacto": "DELETE /contactos/{nombre}",
            "estadisticas": "GET /estadisticas/",
        },
    }


@app.post(
    "/contactos/",
    response_model=MensajeResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Contactos"],
    summary="Registrar un nuevo contacto",
    response_description="Contacto registrado exitosamente",
)
def crear_contacto(contacto: ContactoCreate):
    """
    ## Registra un nuevo contacto en la agenda

    ### Validaciones:
    - **Nombre**: Solo letras, espacios y caracteres especiales (á, é, í, ó, ú, ñ)
    - **Teléfono**: Entre 7 y 15 dígitos, se permiten guiones y espacios
    - **No duplicados**: No se pueden registrar contactos con el mismo nombre

    ### Parámetros:
    - **nombre**: Nombre del contacto (requerido)
    - **telefono**: Número de teléfono (requerido)

    ### Retorna:
    - **201 Created**: Contacto registrado exitosamente
    - **400 Bad Request**: Datos inválidos o contacto duplicado

    ### Ejemplo de uso:
    ```json
    {
        "nombre": "Juan Pérez",
        "telefono": "0998765432"
    }
    ```
    """
    try:
        resultado = agenda.registrar_contacto(contacto.nombre, contacto.telefono)
        # Adaptar respuesta al formato esperado por la API
        return {
            "mensaje": resultado["message"],
            "nombre": resultado["contacto"]["nombre"],
            "telefono": resultado["contacto"]["telefono"],
        }
    except (ContactoInvalidoError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get(
    "/contactos/",
    response_model=List[ContactoResponse],
    tags=["Contactos"],
    summary="Listar todos los contactos",
    response_description="Lista de contactos ordenados alfabéticamente",
)
def listar_contactos():
    """
    ## Lista todos los contactos de la agenda

    Los contactos se retornan ordenados alfabéticamente por nombre.

    ### Retorna:
    - **200 OK**: Lista de contactos (puede estar vacía)

    ### Ejemplo de respuesta:
    ```json
    [
        {
            "nombre": "Ana García",
            "telefono": "0991234567"
        },
        {
            "nombre": "Juan Pérez",
            "telefono": "0998765432"
        }
    ]
    ```
    """
    return agenda.listar_contactos()


@app.get(
    "/contactos/{nombre}",
    response_model=ContactoResponse,
    tags=["Contactos"],
    summary="Consultar un contacto específico",
    response_description="Datos del contacto encontrado",
)
def consultar_contacto(nombre: str):
    """
    ## Consulta un contacto específico por nombre

    Busca un contacto por su nombre exacto (case-sensitive).

    ### Parámetros:
    - **nombre**: Nombre del contacto a buscar (en la URL)

    ### Retorna:
    - **200 OK**: Contacto encontrado
    - **404 Not Found**: Contacto no existe

    ### Ejemplo de uso:
    ```
    GET /contactos/Juan%20Pérez
    ```

    ### Ejemplo de respuesta:
    ```json
    {
        "nombre": "Juan Pérez",
        "telefono": "0998765432"
    }
    ```
    """
    contacto = agenda.consultar_contacto(nombre)

    if contacto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El contacto '{nombre}' no existe en la agenda",
        )

    return contacto


@app.delete(
    "/contactos/{nombre}",
    response_model=MensajeResponse,
    tags=["Contactos"],
    summary="Eliminar un contacto",
    response_description="Contacto eliminado exitosamente",
)
def eliminar_contacto(nombre: str):
    """
    ## Elimina un contacto de la agenda

    Elimina permanentemente un contacto por su nombre.

    ### Parámetros:
    - **nombre**: Nombre del contacto a eliminar (en la URL)

    ### Retorna:
    - **200 OK**: Contacto eliminado exitosamente
    - **404 Not Found**: Contacto no existe

    ### Ejemplo de uso:
    ```
    DELETE /contactos/Juan%20Pérez
    ```

    ### Ejemplo de respuesta:
    ```json
    {
        "mensaje": "Contacto eliminado exitosamente",
        "nombre": "Juan Pérez",
        "telefono": "0998765432"
    }
    ```
    """
    try:
        resultado = agenda.eliminar_contacto(nombre)
        # Adaptar respuesta al formato esperado por la API
        return {
            "mensaje": resultado["message"],
            "nombre": resultado["contacto"]["nombre"],
            "telefono": resultado["contacto"]["telefono"],
        }
    except (ContactoInvalidoError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@app.get(
    "/estadisticas/",
    response_model=EstadisticasResponse,
    tags=["Estadísticas"],
    summary="Obtener estadísticas de la agenda",
    response_description="Estadísticas de la agenda",
)
def obtener_estadisticas():
    """
    ## Obtiene estadísticas generales de la agenda

    Retorna información sobre el número total de contactos registrados.

    ### Retorna:
    - **200 OK**: Estadísticas de la agenda

    ### Ejemplo de respuesta:
    ```json
    {
        "total_contactos": 5,
        "mensaje": "La agenda tiene 5 contacto(s)"
    }
    ```
    """
    total = agenda.total_contactos()
    return {"total_contactos": total, "mensaje": f"La agenda tiene {total} contacto(s)"}


# ============================================================================
# MANEJO DE ERRORES GLOBAL
# ============================================================================


@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Manejador personalizado para errores 404"""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Recurso no encontrado",
            "mensaje": "La ruta solicitada no existe",
            "documentacion": "/docs",
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Manejador personalizado para errores 500"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Error interno del servidor",
            "mensaje": "Ha ocurrido un error inesperado",
        },
    )


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    """
    Ejecuta el servidor de desarrollo

    Uso:
        python -m src.main

    O mejor aún:
        uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
    """
    uvicorn.run(
        "src.main:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )
