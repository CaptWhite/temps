## Middleware LogRequest

Middleware personalizado en FastAPI que sirve para registrar (loggear) cada solicitud HTTP que llega a la aplicación. Vamos línea por línea para entender su funcionamiento:

📌 Código explicado:
``` python
class LogRequestMiddleware(BaseHTTPMiddleware):
```

Crea una clase LogRequestMiddleware que hereda de BaseHTTPMiddleware, un componente de starlette.middleware.base.

Esto te permite interceptar las solicitudes antes y después de que lleguen al endpoint correspondiente.

``` python
async def dispatch(self, request: Request, call_next):
```
- dispatch es el método principal que se ejecuta en cada solicitud.
- request: el objeto de solicitud HTTP (Request de FastAPI).
- call_next: una función que permite pasar la solicitud al siguiente middleware o al endpoint final.

``` python
         body = await request.body()
```

Lee el cuerpo (body) completo de la solicitud como bytes.

⚠️ Esto es importante: solo puedes leer el body una vez, así que si no lo vuelves a poner, podría no estar disponible en el endpoint más adelante.

``` python
        print(f"Solicitud: {request.method} {request.url}")
```
Imprime en consola el método (GET, POST, etc.) y la URL de la solicitud.

``` python
        print(f"Cuerpo: {body}")  # Decodificar si es necesario
```
Está comentado, pero si lo activas, también imprimiría el cuerpo de la solicitud.

Puedes decodificarlo si es texto con: body.decode("utf-8").

``` python
        response = await call_next(request)
        return response
```

- Llama al siguiente paso en la cadena de procesamiento (otro middleware o el endpoint).
- Retorna la respuesta generada por el sistema.

### 🧪 Activación del middleware
``` python
app.add_middleware(LogRequestMiddleware)
```

Esta línea está comentada. Para que el middleware funcione, deberías descomentarla e incluirla donde creas la instancia de la app FastAPI:

``` python
app = FastAPI()
app.add_middleware(LogRequestMiddleware)
```

### ✅ ¿Para qué sirve?
- Logging/debugging: ver qué solicitudes están llegando al servidor.
- Auditar el tráfico HTTP.
- Análisis de patrones de uso.
- Verificar si los datos están siendo correctamente enviados.

