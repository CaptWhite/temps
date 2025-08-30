
## Middleware CORS
### 📌 ¿Qué es CORS?
CORS es un mecanismo de seguridad en los navegadores que restringe las solicitudes HTTP entre diferentes orígenes (dominios, puertos o protocolos distintos).

Por ejemplo: si tu frontend corre en http://localhost:3000 y tu API en http://localhost:8000, CORS puede bloquear las peticiones a menos que lo permitas explícitamente.

🧩 Explicación del código línea por línea:
``` python
app.add_middleware(
    CORSMiddleware,
```

- Añade el middleware CORSMiddleware a la aplicación FastAPI. Este se ejecuta en cada solicitud para verificar si cumple con las reglas CORS.

```python
    allow_origins=["*"],  # Reemplaza con el origen de tu frontend
```

Permite solicitudes desde cualquier origen (*).
⚠️ Esto es útil para desarrollo, pero no es seguro en producción. Se recomienda reemplazarlo con algo como:

``` python
allow_origins=["https://mi-frontend.com"]
```

``` python
    allow_credentials=True,
```
- Permite el uso de cookies, encabezados Authorization o cualquier otra credencial en solicitudes CORS.
- Requiere que allow_origins no sea "*", según las reglas del navegador (de lo contrario no funcionará correctamente).

``` python
    allow_methods=["*"],
```
- Permite todos los métodos HTTP en solicitudes CORS (GET, POST, PUT, DELETE, etc.).

``` python
    allow_headers=["*"],
```
- Permite **todos los encabezados** personalizados en las solicitudes.

### ✅ ¿Cuándo usar esto?
Cuando tu API FastAPI será llamada desde un frontend (por ejemplo, en React, Vue, Angular).

Evita errores como:
``` pgsql
Access to fetch at 'http://localhost:8000/...' from origin 'http://localhost:3000' has been blocked by CORS policy
```

### 🔒 Recomendación para producción
En producción, configura CORS con más cuidado:

``` python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mi-frontend.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
```

###  Configuración para producción  (por ejemplo: localhost:3000, Vite, etc.)
``` python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Origen exacto del frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)
```








Preguntar a ChatGPT
