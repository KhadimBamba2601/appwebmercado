import random

def generar_ip_aleatoria():
  """Genera una dirección IPv4 aleatoria."""
  octetos = [random.randint(0, 255) for _ in range(4)]
  return ".".join(map(str, octetos))

ip_aleatoria = generar_ip_aleatoria()
print(f"IP aleatoria generada: {ip_aleatoria}")

# Escribir la salida en un archivo
with open("ip_generada.txt", "w") as f:
    f.write(f"IP aleatoria generada: {ip_aleatoria}") 