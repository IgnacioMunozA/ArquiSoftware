import os
import threading

def ejecutar_script(script):
    ruta_script = os.path.join('services', script)
    os.system(f'python3 {ruta_script}')

# Directorio que contiene los scripts
directorio = 'services'

# Obtener la lista de archivos en el directorio
archivos = os.listdir(directorio)

# Filtrar solo los archivos con extensión .py
scripts = [archivo for archivo in archivos if archivo.endswith('.py')]

# Crear un hilo para cada script
threads = []
for script in scripts:
    thread = threading.Thread(target=ejecutar_script, args=(script,))
    threads.append(thread)

# Iniciar todos los hilos
for thread in threads:
    thread.start()

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

print("Todos los scripts han sido ejecutados.")
