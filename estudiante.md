# Taller 2 - API de Películas

## Información del Estudiante

- **Nombre:** Andres Esteban Vasquez Peña
- **Materia:** Lenguaje de Programación 3
- **Taller:** Taller 2

---

## Descripción del Proyecto

Este proyecto consiste en una API RESTful desarrollada con FastAPI y SQLModel para gestionar una base de datos de películas. La API permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre tres modelos principales: **Usuarios**, **Películas** y **Favoritos**.

La aplicación está completamente probada, con una suite de 24 tests unitarios y de integración que garantizan su correcto funcionamiento. Además, incluye características avanzadas como paginación, validación de datos y un sistema de logging de peticiones.

## Estructura del Proyecto

La estructura del proyecto sigue las mejores prácticas para aplicaciones FastAPI, separando la lógica en diferentes módulos:

```
lp3-taller2/
├── app/
│   ├── routers/         # Endpoints de la API
│   ├── config.py        # Configuración de la aplicación
│   ├── database.py      # Lógica de la base de datos
│   ├── models.py        # Modelos de datos (tablas)
│   └── schemas.py       # Esquemas de validación (Pydantic)
├── tests/
│   └── test_api.py      # Pruebas automatizadas
├── main.py              # Punto de entrada de la aplicación
├── requirements.txt     # Dependencias
└── ...
```

## Instalación y Puesta en Marcha

1.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Cargar datos iniciales (opcional pero recomendado):**
    Para probar la API con datos de ejemplo, ejecuta:
    ```bash
    sqlite3 peliculas.db < init_db.sql
    ```

3.  **Ejecución del servidor de desarrollo:**
    ```bash
    uvicorn main:app --reload
    ```

## ¿Cómo Probar la Aplicación?

Una vez que el servidor está en marcha, puedes verificar que todo funciona de las siguientes maneras.

### 1. Pruebas con el Navegador (Recomendado)

FastAPI genera una documentación interactiva que es ideal para probar.

1.  Abre tu navegador y ve a: **http://127.0.0.1:8000/docs**
2.  Desde esta interfaz (Swagger UI), puedes desplegar cada endpoint y hacer clic en **"Try it out"** para ejecutar peticiones.

    *   **Listar usuarios:** Ve a `GET /api/usuarios/` y haz clic en "Execute". Deberías ver la lista de usuarios.
    *   **Ver favoritos de un usuario:** Ve a `GET /api/usuarios/{usuario_id}/favoritos`, introduce `1` como `usuario_id` y haz clic en "Execute". Verás las películas favoritas del primer usuario.

### 2. Pruebas desde la Consola (con `curl`)

También puedes usar una herramienta de línea de comandos como `curl` para interactuar con la API.

*   **Listar todas las películas:**
    ```bash
    curl -X GET "http://127.0.0.1:8000/api/peliculas/"
    ```

*   **Crear un nuevo usuario:**
    ```bash
    curl -X POST "http://127.0.0.1:8000/api/usuarios/" \
    -H "Content-Type: application/json" \
    -d '{"nombre": "Usuario de Consola", "correo": "consola@example.com"}'
    ```

### 3. Pruebas Automatizadas

El proyecto incluye una suite de pruebas completa que puedes ejecutar con `pytest`. Esto verifica automáticamente que todos los endpoints funcionen como se espera.

```bash
pytest
```

Un resultado exitoso mostrará `24 passed`, confirmando la robustez de la aplicación.

## Sugerencias de Mejora Implementadas

A continuación se listan las sugerencias del `README.md` original, marcando las que se han implementado en este proyecto.

- [ ] 1. **Autenticación y autorización**: Implementar JWT o OAuth2.
- [x] 2. **Paginación**: Añadir soporte para paginación en las listas.
- [x] 3. **Validación de datos**: Implementar validación robusta de datos de entrada.
- [x] 4. **Tests unitarios e integración**: Desarrollar pruebas automatizadas.
- [ ] 5. **Base de datos en producción**: Migrar a PostgreSQL o MySQL.
- [ ] 6. **Docker**: Contenerizar la aplicación.
- [x] 7. **Registro (logging)**: Implementar un sistema de registro de peticiones.
- [ ] 8. **Caché**: Añadir caché para mejorar la velocidad de respuesta.
- [ ] 9. **Sistema de valoraciones**: Permitir a los usuarios calificar películas.
- [ ] 10. **Recomendaciones inteligentes**: Desarrollar un algoritmo de recomendación avanzado.
- [ ] 11. **Integración con APIs externas**: Conectar con APIs como TMDB u OMDB.
- [ ] 12. **Listas personalizadas**: Permitir a los usuarios crear listas temáticas.

