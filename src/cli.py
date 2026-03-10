"""
cli.py
Responsabilidad: punto de entrada del script. Gestiona la interacción
con el usuario, lee la configuración del entorno, y coordina
el downloader y el converter.
"""

import sys
from pathlib import Path

# python-dotenv carga las variables del archivo .env
# al entorno del proceso antes de que las leamos con os.getenv.
from dotenv import load_dotenv
import os

from downloader import download_audio
from converter import check_ffmpeg, format_duration


def load_config() -> dict:
    """
    Carga la configuración desde el archivo .env.

    Centralizar la carga de configuración en una función tiene
    una ventaja enorme: cuando lleves esto a la nube, solo
    cambiarás esta función para leer de un gestor de secretos
    (como AWS Secrets Manager o Vault), sin tocar el resto del código.
    """
    # Buscamos el .env en el directorio raíz del proyecto,
    # que está un nivel arriba de src/
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)

    return {
        "download_dir": Path(os.getenv("DOWNLOAD_DIR", "downloads")),
        "audio_quality": int(os.getenv("AUDIO_QUALITY", "2")),
    }


def print_banner() -> None:
    """Muestra el encabezado del programa."""
    print("\n" + "="*50)
    print("       YT-MP3 Downloader")
    print("="*50 + "\n")


def print_success(info: dict, config: dict) -> None:
    """Muestra un resumen del archivo descargado."""
    duration = format_duration(info.get("duration", 0))
    print("\n✓ Descarga completada con éxito")
    print(f"  Título:    {info['title']}")
    print(f"  Autor:     {info['uploader']}")
    print(f"  Duración:  {duration}")
    print(f"  Guardado en: {config['download_dir'].resolve()}\n")


def main() -> None:
    """
    Función principal del script.

    Separar la lógica en main() y luego llamarla desde
    el bloque if __name__ == "__main__" es una práctica
    estándar en Python. Permite importar este módulo desde
    otros scripts o tests sin que se ejecute automáticamente.
    """
    print_banner()

    # Paso 1: verificar dependencias del sistema antes de hacer nada
    try:
        check_ffmpeg()
    except EnvironmentError as e:
        print(f"✗ Error de configuración: {e}")
        sys.exit(1)

    # Paso 2: cargar configuración del .env
    config = load_config()

    # Paso 3: pedir la URL al usuario
    url = input("Introduce la URL de YouTube: ").strip()

    # Validación básica: comprobamos que la URL tiene pinta de ser de YouTube
    if "youtube.com" not in url and "youtu.be" not in url:
        print("✗ La URL no parece ser de YouTube. Inténtalo de nuevo.")
        sys.exit(1)

    # Paso 4: descargar y convertir
    print(f"\n⟳ Descargando audio...")
    try:
        info = download_audio(
            url=url,
            output_dir=config["download_dir"],
            audio_quality=config["audio_quality"],
        )
        print_success(info, config)

    except RuntimeError as e:
        print(f"\n✗ {e}")
        sys.exit(1)


# Este bloque garantiza que main() solo se ejecuta cuando
# lanzamos este archivo directamente, no cuando lo importamos.
if __name__ == "__main__":
    main()
