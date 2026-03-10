# YT-MP3 Downloader

Herramienta de línea de comandos para descargar el audio de vídeos de YouTube
y convertirlos automáticamente a MP3. Desarrollada con Python, yt-dlp y ffmpeg.

## Requisitos del sistema

Este proyecto tiene dos tipos de dependencias: las del sistema operativo y las
de Python. Las primeras debes instalarlas manualmente una sola vez en cada
máquina, porque son programas del sistema que no pueden gestionarse con pip.
Las segundas las gestiona automáticamente el Makefile.

En Ubuntu o Debian, instala las dependencias del sistema con estos comandos:

    sudo apt update
    sudo apt install git python3 python3-pip python3-venv ffmpeg -y

Esto instala Git para el control de versiones, Python 3 con pip y venv para
gestionar el entorno del proyecto, y ffmpeg que es el programa que realiza
la conversión del audio descargado al formato MP3. Sin ffmpeg instalado
en el sistema, la conversión fallará aunque el resto del proyecto esté
correctamente configurado.

Puedes verificar que todo quedó bien instalado con:

    git --version
    python3 --version
    ffmpeg -version

## Instalación

Una vez tienes las dependencias del sistema, clona el repositorio y deja
que el Makefile haga el resto:

    git clone git@github.com:TU_USUARIO/yt-mp3-downloader.git
    cd yt-mp3-downloader
    make install

El comando `make install` crea el entorno virtual de Python, instala pip-tools,
y sincroniza todas las dependencias con las versiones exactas definidas en
requirements.txt. Esto garantiza que tu entorno es idéntico al de cualquier
otra persona que haya clonado el proyecto.

Luego copia el archivo de configuración de ejemplo:

    cp .env.example .env

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

`DOWNLOAD_DIR` define la carpeta donde se guardan los MP3. Por defecto es `downloads/`.
`AUDIO_QUALITY` controla la calidad del MP3 de 0 (mejor calidad) a 9 (menor calidad). Por defecto es `2`.

## Estructura del proyecto

    yt-mp3-downloader/
    ├── src/
    │   ├── cli.py          # Punto de entrada: interfaz de línea de comandos
    │   ├── downloader.py   # Lógica de descarga con yt-dlp
    │   └── converter.py    # Utilidades de conversión y verificación de ffmpeg
    ├── downloads/          # MP3 generados (ignorado por git)
    ├── scripts/            # Scripts de utilidad para el proyecto
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

Si necesitas añadir una nueva librería de Python al proyecto, edita
`requirements.in` añadiendo el nombre del paquete, ejecuta `make update`
para que pip-tools recalcule el árbol completo de dependencias, y commitea
ambos archivos juntos en el mismo commit. Nunca edites `requirements.txt`
a mano.

## Autor
mzk
