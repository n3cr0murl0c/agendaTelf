# 📱 Agenda Telefónica API - Guía Rápida

## 🎯 ¿Qué hace esta API?

Esta API REST permite gestionar una agenda telefónica de forma simple y eficiente.

**Funcionalidades principales:**

- ✅ **Registrar** contactos nuevos
- 🔍 **Buscar** contactos por nombre
- 📋 **Listar** todos los contactos
- 🗑️ **Eliminar** contactos
- 📊 Ver **estadísticas** de la agenda

---

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar la API

```bash
uvicorn src.main:app --reload
```

### 3. Abrir en el navegador

```
http://localhost:8000/docs
```

---

## 📖 ¿Cómo funciona la API?

### 🟢 Endpoint 1: Registrar un contacto

**Qué hace:** Guarda un nuevo contacto en la agenda

**Método:** `POST /contactos/`

**Ejemplo con curl:**

```bash
curl -X POST "http://localhost:8000/contactos/" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "telefono": "0998765432"
  }'
```

**Respuesta:**

```json
{
  "mensaje": "Contacto registrado exitosamente",
  "nombre": "Juan Pérez",
  "telefono": "0998765432"
}
```

**Validaciones:**

- ✅ El nombre solo puede tener letras y espacios
- ✅ El teléfono debe tener entre 7 y 15 dígitos
- ❌ No se permiten nombres duplicados

---

### 🔵 Endpoint 2: Listar todos los contactos

**Qué hace:** Muestra todos los contactos guardados (ordenados alfabéticamente)

**Método:** `GET /contactos/`

**Ejemplo con curl:**

```bash
curl -X GET "http://localhost:8000/contactos/"
```

**Respuesta:**

```json
[
  {
    "nombre": "Ana García",
    "telefono": "0991234567"
  },
  {
    "nombre": "Juan Pérez",
    "telefono": "0998765432"
  },
  {
    "nombre": "María López",
    "telefono": "0987654321"
  }
]
```

---

### 🔵 Endpoint 3: Buscar un contacto específico

**Qué hace:** Busca un contacto por su nombre exacto

**Método:** `GET /contactos/{nombre}`

**Ejemplo con curl:**

```bash
curl -X GET "http://localhost:8000/contactos/Juan%20Pérez"
```

**Respuesta si existe:**

```json
{
  "nombre": "Juan Pérez",
  "telefono": "0998765432"
}
```

**Respuesta si NO existe:**

```json
{
  "detail": "El contacto 'Juan Pérez' no existe en la agenda"
}
```

---

### 🔴 Endpoint 4: Eliminar un contacto

**Qué hace:** Elimina un contacto de la agenda

**Método:** `DELETE /contactos/{nombre}`

**Ejemplo con curl:**

```bash
curl -X DELETE "http://localhost:8000/contactos/Juan%20Pérez"
```

**Respuesta:**

```json
{
  "mensaje": "Contacto eliminado exitosamente",
  "nombre": "Juan Pérez",
  "telefono": "0998765432"
}
```

---

### 📊 Endpoint 5: Ver estadísticas

**Qué hace:** Muestra cuántos contactos hay en la agenda

**Método:** `GET /estadisticas/`

**Ejemplo con curl:**

```bash
curl -X GET "http://localhost:8000/estadisticas/"
```

**Respuesta:**

```json
{
  "total_contactos": 3,
  "mensaje": "La agenda tiene 3 contacto(s)"
}
```

---

## 🧪 Probar la API desde el navegador

### Opción 1: Swagger UI (Recomendado)

1. Abre: `http://localhost:8000/docs`
2. Verás una interfaz interactiva
3. Puedes probar cada endpoint directamente
4. Click en "Try it out" para ejecutar peticiones

### Opción 2: ReDoc

1. Abre: `http://localhost:8000/redoc`
2. Documentación más formal y detallada
3. Ideal para lectura

---

## ✅ Ejemplos de Validaciones

### ✅ VÁLIDO - Nombre correcto

```json
{
  "nombre": "María José",
  "telefono": "0998765432"
}
```

### ✅ VÁLIDO - Nombre con tildes y ñ

```json
{
  "nombre": "José Núñez",
  "telefono": "099-876-5432"
}
```

### ✅ VÁLIDO - Teléfono con guiones

```json
{
  "nombre": "Ana García",
  "telefono": "099-876-5432"
}
```

### ❌ INVÁLIDO - Nombre con números

```json
{
  "nombre": "Juan123",
  "telefono": "0998765432"
}
```

**Error:** "Nombre inválido. Debe contener solo letras y espacios"

### ❌ INVÁLIDO - Teléfono muy corto

```json
{
  "nombre": "Juan Pérez",
  "telefono": "12345"
}
```

**Error:** "Teléfono inválido. Debe contener entre 7-15 dígitos"

### ❌ INVÁLIDO - Contacto duplicado

```json
{
  "nombre": "Juan Pérez",
  "telefono": "0991234567"
}
```

**Error:** "El contacto 'Juan Pérez' ya existe en la agenda"

---

## 🐍 Usar la API desde Python

### Ejemplo completo:

```python
import requests

# URL base de la API
BASE_URL = "http://localhost:8000"

# 1. Registrar un contacto
def registrar_contacto(nombre, telefono):
    response = requests.post(
        f"{BASE_URL}/contactos/",
        json={"nombre": nombre, "telefono": telefono}
    )
    print(response.json())

# 2. Listar todos los contactos
def listar_contactos():
    response = requests.get(f"{BASE_URL}/contactos/")
    contactos = response.json()
    for contacto in contactos:
        print(f"{contacto['nombre']}: {contacto['telefono']}")

# 3. Buscar un contacto
def buscar_contacto(nombre):
    response = requests.get(f"{BASE_URL}/contactos/{nombre}")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Contacto no encontrado")

# 4. Eliminar un contacto
def eliminar_contacto(nombre):
    response = requests.delete(f"{BASE_URL}/contactos/{nombre}")
    print(response.json())

# 5. Ver estadísticas
def ver_estadisticas():
    response = requests.get(f"{BASE_URL}/estadisticas/")
    print(response.json())

# Usar las funciones
if __name__ == "__main__":
    # Registrar contactos
    registrar_contacto("Juan Pérez", "0998765432")
    registrar_contacto("María García", "0987654321")

    # Listar todos
    print("\n--- Todos los contactos ---")
    listar_contactos()

    # Buscar uno específico
    print("\n--- Buscar contacto ---")
    buscar_contacto("Juan Pérez")

    # Ver estadísticas
    print("\n--- Estadísticas ---")
    ver_estadisticas()

    # Eliminar un contacto
    print("\n--- Eliminar contacto ---")
    eliminar_contacto("Juan Pérez")

    # Listar de nuevo
    print("\n--- Contactos después de eliminar ---")
    listar_contactos()
```

---

## 🧪 Ejecutar las Pruebas

### Ejecutar todas las pruebas:

```bash
pytest tests/ -v
```

### Ver cobertura de pruebas:

```bash
coverage run -m pytest tests/
coverage report -m
coverage html
```

### Verificar estilo de código:

```bash
flake8 src/ tests/
```

---

## 📊 Flujo de Trabajo Completo

```
1. Cliente hace petición → 2. FastAPI recibe → 3. Valida datos
                                                      ↓
                                                      ✅ Válido
                                                      ↓
4. Cliente recibe respuesta ← 5. Retorna respuesta ← 6. Ejecuta lógica
                                                      (agenda.py)
```

### Ejemplo paso a paso:

1. **Cliente** envía: `POST /contactos/ {"nombre": "Juan", "telefono": "099..."}`
2. **FastAPI** recibe la petición en el endpoint `crear_contacto()`
3. **Pydantic** valida el modelo `ContactoCreate`
4. **Lógica** llama a `agenda.registrar_contacto()`
5. **Validaciones** internas verifican nombre y teléfono
6. **Respuesta** se envía de vuelta al cliente

---

## 🔍 Códigos de Estado HTTP

| Código  | Significado           | Cuándo ocurre                             |
| ------- | --------------------- | ----------------------------------------- |
| **200** | OK                    | Operación exitosa (consulta, eliminación) |
| **201** | Created               | Contacto registrado exitosamente          |
| **400** | Bad Request           | Datos inválidos o contacto duplicado      |
| **404** | Not Found             | Contacto no encontrado                    |
| **500** | Internal Server Error | Error del servidor                        |

---

## 📂 Estructura de Archivos

```
agenda-telefonica/
├── src/
│   ├── __init__.py          # Inicialización del paquete
│   ├── agenda.py            # Lógica de negocio (clase AgendaTelefonica)
│   └── main.py              # API FastAPI (endpoints)
├── tests/
│   ├── test_registro_consulta.py  # Pruebas de registro y consulta
│   └── test_eliminar.py           # Pruebas de eliminación
├── requirements.txt         # Dependencias de producción
└── README.md               # Este archivo
```

---

## 🛠️ Tecnologías Utilizadas

- **FastAPI**: Framework web moderno para crear APIs
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI
- **Pytest**: Framework de pruebas
- **Coverage**: Análisis de cobertura

---

## 💡 Consejos Útiles

### Para desarrollo:

- Usa `--reload` para que el servidor se reinicie automáticamente
- Revisa la documentación en `/docs` antes de hacer peticiones
- Usa `pytest -v` para ver más detalles de las pruebas

### Para debugging:

- Revisa los logs en la terminal donde corre uvicorn
- Usa `print()` en la lógica para ver qué pasa
- FastAPI muestra errores muy claros en `/docs`

### Atajos útiles:

```bash
# Ejecutar servidor
uvicorn src.main:app --reload

# Ejecutar pruebas con detalles
pytest -v

# Ver cobertura y abrir reporte
coverage run -m pytest && coverage html && open htmlcov/index.html
```

---

## ❓ Preguntas Frecuentes

**P: ¿Por qué dice "contacto no encontrado"?**  
R: Los nombres son case-sensitive. "juan" ≠ "Juan"

**P: ¿Los datos se guardan en una base de datos?**  
R: No, se guardan en memoria (se pierden al reiniciar)

**P: ¿Puedo usar espacios en los nombres?**  
R: Sí, "Juan Pérez" es válido

**P: ¿Puedo usar guiones en teléfonos?**  
R: Sí, "099-876-5432" es válido

**P: ¿Cuántos contactos puedo registrar?**  
R: Ilimitados (limitado solo por la memoria RAM)

---

## 📞 Soporte

Si tienes problemas, verifica:

1. ¿Instalaste todas las dependencias? (`pip install -r requirements.txt`)
2. ¿El servidor está corriendo? (`uvicorn src.main:app --reload`)
3. ¿La URL es correcta? (`http://localhost:8000`)
4. ¿Los datos son válidos según las validaciones?

---

**Desarrollado con ❤️ para el curso de Integración Continua**
