Configurar un usuario de despliegue con acceso solo por clave pública es una excelente práctica de seguridad. Aquí te explico los pasos detallados para hacerlo.

-----

### Paso 1: Crear el usuario `deploy`

Lo primero es crear el usuario. Por seguridad, le asignaremos un *shell* que no permite el inicio de sesión interactivo. Así, nadie podrá usar este usuario para conectarse al servidor con un shell regular, lo que solo permitirá las conexiones automatizadas (como las de despliegue).

```bash
sudo useradd -m -s /usr/sbin/nologin deploy
```
  * `useradd`: El comando para crear el usuario.
  * `-m`: Crea el directorio *home* del usuario (`/home/deploy`).
  * `-s /usr/sbin/nologin`: Asigna un *shell* que impide los inicios de sesión.

-----

### Paso 2: Configurar el acceso por clave SSH

Ahora, necesitas configurar el directorio donde se almacenarán las claves públicas. SSH es muy estricto con los permisos de estos archivos, así que es importante hacer los pasos en el orden correcto.

```bash
# Cambia temporalmente al usuario 'deploy' para crear el directorio .ssh
sudo -i -u deploy

# Crea el directorio y el archivo de claves
mkdir ~/.ssh
chmod 700 ~/.ssh
touch ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# Sal del usuario 'deploy' para volver al tuyo
exit
```

-----

### Paso 3: Copiar la clave pública

Ahora, copia tu clave pública (la que tienes en tu máquina local, usualmente en `~/.ssh/id_rsa.pub`) al archivo `authorized_keys` que acabas de crear.

Puedes hacerlo de dos maneras:

**Opción 1: Usando `ssh-copy-id` (la forma más fácil)**
Este comando hace todo el trabajo por ti. Solo necesitas acceso con otro usuario en el servidor.

```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub deploy@<tu_servidor>
```

**Opción 2: Copiar y pegar manualmente**
Si prefieres hacerlo a mano, primero copia tu clave desde tu máquina local.

```bash
cat ~/.ssh/id_rsa.pub
```

Luego, en el servidor, edita el archivo `authorized_keys` y pega la clave completa en una sola línea.

```bash
sudo nano /home/deploy/.ssh/authorized_keys
```

-----

### Paso 4: Probar la conexión y deshabilitar la contraseña

Ahora que la clave está en el servidor, puedes probar la conexión. Si todo está correcto, deberías poder conectarte sin que te pida contraseña.

```bash
ssh deploy@<tu_servidor>
```

Si la conexión funciona, ¡genial\! Es hora de deshabilitar la autenticación por contraseña para este usuario. Esto es crucial para la seguridad, ya que **evita por completo** que alguien intente iniciar sesión con una contraseña.

Abre el archivo de configuración del demonio de SSH:

```bash
sudo nano /etc/ssh/sshd_config
```

Agrega estas líneas al final del archivo:

```
Match User deploy
  PasswordAuthentication no
```

Guarda y cierra el archivo. Finalmente, reinicia el servicio SSH para aplicar los cambios:

```bash
sudo systemctl restart sshd
```

¡Listo\! El usuario `deploy` ahora solo acepta conexiones a través de claves SSH, garantizando una configuración más segura para tus despliegues.