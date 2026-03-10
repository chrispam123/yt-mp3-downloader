#YT-MP3 downloader

Herramienta de línea de comandos para descargar el audio de vídeos de YouTube
y convertirlos automáticamente a MP3. Desarrollada con Python, yt-dlp y ffmpeg.

## Requisitos del sistema

Antes de instalar el proyecto, necesitas tener estos programas en tu máquina.
Son dependencias del sistema operativo, no de Python, por lo que se instalan
con el gestor de paquetes del sistema.Cada usuario tiene que hacerlo

- Python 3.10 o superior
- ffmpeg

En Ubuntu/Debian puedes instalar ffmpeg con:

    sudo apt install ffmpeg -y

## Instalación

Clona el repositorio y deja que el Makefile haga el resto. El comando
`make install` crea el entorno virtual, instala pip-tools y sincroniza
todas las dependencias con las versiones exactas del requirements.txt:

    git clone git@github.com:TU_USUARIO/yt-mp3-downloader.git
    cd yt-mp3-downloader
    make install

Luego copia el archivo de configuración de ejemplo y ajústalo si lo necesitas en tu entorno yo no he usado 

    cp .env.example .env

Por defecto los MP3 se guardan en la carpeta `downloads/` del proyecto
y la calidad de audio es 2 (en una escala de 0 mejor a 9 peor).

## Uso

Con el entorno instalado, ejecuta:

    make run

El script te pedirá la URL del vídeo de YouTube y hará el resto automáticamente.
El archivo MP3 quedará guardado en la carpeta `downloads/` con el título
del vídeo como nombre de archivo.

## Configuración

El comportamiento del script se controla mediante variables de entorno
definidas en el archivo `.env`. Este archivo nunca se sube a git porque
puede contener valores específicos de tu máquina. El archivo `.env.example`
sirve como plantilla documentada de todas las variables disponibles.

- `DOWNLOAD_DIR` define la carpeta donde se guardan los MP3. Por defecto es `downloads/`.
- `AUDIO_QUALITY` controla la calidad del MP3 de 0 (mejor calidad) a 9 (menor calidad). Por defecto es `2`.

## Estructura del proyecto

    yt-mp3-downloader/
    ├── src/
    │   ├── cli.py          # Punto de entrada: interfaz de línea de comandos
    │   ├── downloader.py   # Lógica de descarga con yt-dlp
    │   └── converter.py    # Utilidades de conversión y verificación de ffmpeg
    ├── downloads/          # MP3 generados (ignorado por git)
    ├── .env.example        # Plantilla de configuración
    ├── requirements.in     # Dependencias de alto nivel (editado a mano)
    ├── requirements.txt    # Dependencias pinadas (generado por pip-compile)
    ├── Makefile            # Automatización de comandos del proyecto
    └── pyproject.toml      # Metadatos del proyecto

## Comandos disponibles

    make install   Crea el entorno virtual e instala todas las dependencias
    make run       Ejecuta el script descargador
    make update    Recompila requirements.txt cuando añades nuevas dependencias
    make clean     Elimina el entorno virtual y archivos temporales generados

## Flujo de desarrollo

Este proyecto sigue un flujo de ramas estructurado para mantener `main`
siempre estable. Nunca se hace push directamente a `main` ni a `develop`.

Cada cambio sigue este ciclo: crear una rama desde `develop` con un nombre
descriptivo, trabajar en ella con commits atómicos, abrir un Pull Request
hacia `develop`, revisar y fusionar, y borrar la rama una vez fusionada.
Periódicamente, `develop` se fusiona a `main` como una nueva versión estable.

## Añadir nuevas dependencias

Si necesitas añadir una nueva librería de Python al proyecto, el flujo
correcto es editar `requirements.in` añadiendo el nombre del paquete,
ejecutar `make update` para que pip-tools recalcule el árbol completo
de dependencias, y commitear ambos archivos juntos en el mismo commit.
Nunca edites `requirements.txt` a mano.

## Autor

Mzk
