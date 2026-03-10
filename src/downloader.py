"""
downloader.py
Responsabilidad: descargar el stream de audio desde una URL de YouTube.
Utiliza yt-dlp, que imita el comportamiento de un navegador para evitar bloqueos.
"""

import yt_dlp
from pathlib import Path


def build_ydl_options(output_dir: Path, audio_quality: int) -> dict:
    """
    Construye el diccionario de opciones para yt-dlp.
    
    Separamos la configuración en su propia función para que sea
    fácil de leer, testear y modificar sin tocar la lógica principal.
    """
    return {
        # Descargamos solo el mejor stream de audio disponible.
        # 'bestaudio/best' significa: primero intenta solo audio,
        # si no hay, descarga el mejor formato completo.
        "format": "bestaudio/best",

        # Le decimos a yt-dlp que después de descargar,
        # ejecute ffmpeg para convertir a mp3.
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": str(audio_quality),
        }],

        # Plantilla del nombre del archivo de salida.
        # %(title)s es el título del vídeo, %(ext)s la extensión.
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),

        # Silenciamos la salida verbose de yt-dlp para
        # controlar nosotros mismos qué mostramos al usuario.
        "quiet": True,
        "no_warnings": True,
    }


def download_audio(url: str, output_dir: Path, audio_quality: int = 2) -> dict:
    """
    Descarga el audio de una URL de YouTube y lo guarda en output_dir.

    Devuelve un diccionario con información del vídeo descargado,
    lo que permite a quien llame a esta función saber el título,
    la duración, etc. sin tener que parsear nada.

    Lanza excepciones explícitas para que la CLI pueda mostrar
    mensajes de error claros al usuario.
    """
    # Nos aseguramos de que la carpeta de destino existe.
    # exist_ok=True significa que no falla si ya existe.
    output_dir.mkdir(parents=True, exist_ok=True)

    options = build_ydl_options(output_dir, audio_quality)

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            # extract_info con download=True descarga el vídeo
            # y además devuelve un dict con todos los metadatos.
            info = ydl.extract_info(url, download=True)
            return {
                "title": info.get("title", "Desconocido"),
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "Desconocido"),
            }

    except yt_dlp.utils.DownloadError as e:
        # yt-dlp lanza DownloadError para casi todo: URL inválida,
        # vídeo privado, región bloqueada, etc. Capturamos el mensaje
        # original y lo relanzamos como un error más legible.
        raise RuntimeError(f"Error al descargar el vídeo: {e}") from e

