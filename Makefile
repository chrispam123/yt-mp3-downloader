# =============================================================================
# YT-MP3 Downloader - Makefile
# Uso: make <comando>
# =============================================================================

# .PHONY le dice a Make que estos nombres son comandos, no archivos.
# Sin esto, si existiera un archivo llamado "install", Make se confundiría.
.PHONY: help install update run clean lint

# El primer target es el que se ejecuta cuando escribes "make" sin argumentos.
# Lo usamos para mostrar ayuda, que es la práctica más profesional.
help:
	@echo ""
	@echo "  YT-MP3 Downloader — Comandos disponibles"
	@echo "  ========================================="
	@echo "  make install   — Crea el entorno virtual e instala dependencias"
	@echo "  make update    — Recompila requirements.txt y actualiza dependencias"
	@echo "  make run       — Ejecuta el script descargador"
	@echo "  make clean     — Elimina el entorno virtual y archivos temporales"
	@echo ""

# Instala todo lo necesario para que el proyecto funcione.
# Cualquier persona que clone el repo solo necesita ejecutar este comando.
install:
	@echo "→ Creando entorno virtual..."
	python3 -m venv .venv
	@echo "→ Instalando dependencias..."
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install pip-tools
	.venv/bin/pip-sync requirements.txt
	@echo "✓ Entorno listo. Actívalo con: source .venv/bin/activate"

# Recompila las dependencias cuando añades algo nuevo a requirements.in.
# El flujo correcto es: editas requirements.in → ejecutas make update → commiteas.
update:
	@echo "→ Recompilando dependencias..."
	.venv/bin/pip-compile requirements.in
	.venv/bin/pip-sync requirements.txt
	@echo "✓ Dependencias actualizadas"

# Lanza el script principal.
# Usamos .venv/bin/python para asegurarnos de usar el Python del entorno virtual,
# independientemente de si el usuario tiene el entorno activado o no.
run:
	@echo "→ Iniciando YT-MP3 Downloader..."
	cd src && ../.venv/bin/python cli.py

# Limpia todos los archivos generados automáticamente.
# Útil para empezar desde cero o solucionar problemas raros de entorno.
clean:
	@echo "→ Eliminando entorno virtual y caché..."
	rm -rf .venv
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✓ Limpieza completada"
