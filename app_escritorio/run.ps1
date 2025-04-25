# Script para iniciar la aplicación
$env:PYTHONPATH = "."
$env:PYTHONUNBUFFERED = "1"

# Verificar si Python está instalado
try {
    python --version
} catch {
    Write-Host "Error: Python no está instalado o no está en el PATH"
    exit 1
}

# Verificar si las dependencias están instaladas
try {
    python -c "import PyQt6" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Instalando dependencias..."
        pip install -r requirements.txt
    }
} catch {
    Write-Host "Error al verificar/instalar dependencias"
    exit 1
}

# Iniciar la aplicación
Write-Host "Iniciando la aplicación..."
python main.py 