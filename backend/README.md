###  Ejecutar el Cliente desde Python
Posicionarse en el directorio del cliente y ejecutar el programa python
*OJO! - El servidor debe estar arrancado*
```bash
cd C:\Users\captw\workspaces\FastAPI\Astronomy\client
python upload
```

###  Ejecutar el Server desde Python
Con el Dockerfile en su lugar, ahora puede compilar la imagen de Docker. Navegue hasta el directorio raíz del proyecto y ejecute el siguiente comando:
```bash

uvicorn app.main:app --reload
```
###  Ejecutar el Server desde DOCKER
####  Creación de la imagen de Docker
Con el Dockerfile en su lugar, ahora puede compilar la imagen de Docker. Navegue hasta el directorio raíz del proyecto y ejecute el siguiente comando:

``` bash
docker build -t fastapi-server .
```

### Ejecución del contenedor Docker
Después de compilar la imagen de Docker, puede ejecutarla como un contenedor. Use el siguiente comando para iniciar un contenedor a partir de la imagen que ha creado:

``` bash
docker run -d -p 8000:8000 -v C:/Users/captw/workspaces/Astronomy-Stars/Server/project_resp/images:/app/images fastapi-server
```

### Subir el docker a Render
``` bash
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/CaptWhite/Astronomy.git
git push -u origin main
```

### Eliminar origen de datos de Git
A veces da el error 'remote origin already exists' cuando intentamos crear un origen de git
``` bash
git remote remove origin
```