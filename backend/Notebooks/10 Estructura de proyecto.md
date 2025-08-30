## Estructura base de un proyecto FastAPI Server - RESP
Aquí tienes una estructura base de un proyecto FastAPI que puede servir para desarrollar un servidor REST (Resp) robusto, organizado y escalable. Esta estructura es modular y sigue buenas prácticas de arquitectura:

### 📁 Estructura del proyecto
``` bash
my_fastapi_project/
│
├── app/                        # Código principal de la aplicación
│   ├── __init__.py
│   ├── main.py                # Punto de entrada de la app (FastAPI instance)
│   ├── config.py              # Configuraciones del proyecto
│   ├── dependencies.py        # Dependencias comunes (auth, DB, etc.)
│
│   ├── api/                   # Rutas organizadas por módulos
│   │   ├── __init__.py
│   │   ├── routes/           
│   │   │   ├── __init__.py
│   │   │   ├── users.py       # Rutas de usuarios
│   │   │   ├── items.py       # Rutas de ítems, por ejemplo
│
│   ├── models/                # Modelos ORM (p. ej. SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── item.py
│
│   ├── schemas/               # Pydantic schemas (validación y serialización)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── item.py
│
│   ├── services/              # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── item_service.py
│
│   ├── db/                    # Conexión y utilidades de base de datos
│   │   ├── __init__.py
│   │   ├── session.py
│   │   ├── base.py
│
├── tests/                     # Pruebas unitarias y de integración
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_items.py
│
├── .env                       # Variables de entorno
├── requirements.txt           # Dependencias del proyecto
├── alembic/                   # Migraciones de base de datos (si usas Alembic)
├── README.md
```

### 🧠 Explicación de los componentes clave
- main.py: instancia FastAPI, incluye routers, middlewares, eventos de startup/shutdown.
- config.py: configuración centralizada (lectura de variables desde .env con pydantic.BaseSettings).
- models/: define entidades para la base de datos (por ejemplo, usando SQLAlchemy).
- schemas/: define los datos que se reciben/envían con Pydantic.
- api/routes/: define endpoints, importando servicios y modelos.
- services/: contiene lógica que no pertenece al controlador ni al modelo (patrón de servicios).
- db/: configura conexión a base de datos, instancias de sesión, etc.
- tests/: pruebas con pytest.

### 🚀 Ejemplo de arranque básico (main.py)
``` python
from fastapi import FastAPI
from app.api.routes import users, items

app = FastAPI(title="Mi API REST con FastAPI")

# Incluir rutas
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(items.router, prefix="/items", tags=["items"])

@app.get("/")
def root():
    return {"message": "Servidor activo"}
```

### 📦 requirements.txt ejemplo
- fastapi
- uvicorn[standard]
- [sqlalchemy](https://www.sqlalchemy.org/)   the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.       
- [pydantic](https://docs.pydantic.dev/latest/)  Pydantic is the most widely used data validation library for Python
- python-dotenv
- [alembic](https://alembic.sqlalchemy.org/)   is a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python

### 📦 Ejemplo de proyecto base - base-project
ejecutar el servidor con:
``` bash
uvicorn app.main:app --reload
```

desde el navegador
```
http://127.0.0.1:8000/
http://127.0.0.1:8000/users
http://127.0.0.1:8000/items
```

