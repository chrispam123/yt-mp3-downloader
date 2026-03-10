"""
converter.py
Responsabilidad: verificar que las dependencias del sistema están disponibles
y exponer utilidades relacionadas con la conversión de audio.

Por ahora la conversión real la hace yt-dlp + ffmpeg juntos en el downloader,
pero este módulo centraliza todo lo relacionado con ffmpeg para
que sea fácil extenderlo en el futuro.
"""

import shutil


def check_ffmpeg() -> None:
    """
    Verifica que ffmpeg está instalado y accesible en el PATH del sistema.

    shutil.which() busca un ejecutable en el PATH, igual que el comando
    'which ffmpeg' en la terminal. Si devuelve None, el programa no existe.

    Lanzamos un error temprano con un mensaje útil en lugar de dejar
    que el proceso falle más adelante con un error críptico de yt-dlp.
    Esto se llama 'fail fast': mejor fallar pronto y con claridad
    que fallar tarde y con confusión.
    """
    if shutil.which("ffmpeg") is None:
        raise EnvironmentError(
            "ffmpeg no está instalado o no está en el PATH del sistema.\n"
            "En Ubuntu/Debian puedes instalarlo con: sudo apt install ffmpeg -y"
        )


def format_duration(seconds: int) -> str:
    """
    Convierte una duración en segundos a formato legible mm:ss o hh:mm:ss.
    Función de utilidad para mostrar información al usuario en la CLI.
    """
    minutes, secs = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"
