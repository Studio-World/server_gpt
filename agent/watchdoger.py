import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

FOLDER_WATCH = "./data/events"  # Rota de vigia (corrigido para diretório local)

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"[++] Criado: {event.src_path}")
            run_tasks(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            print(f"[**] Modificado: {event.src_path}")
            run_tasks(event.src_path)

def run_tasks(filename):
    if filename.endswith(".zip"):
        print(f"[(WATCH_HYDES)] Extraindo zip: {filename}")
        try:
            subprocess.run(["unzip", "-o", filename, "-d", os.path.dirname(filename)])
        except Exception as e:
            print(f"Erro ao extrair zip: {e}")
    elif filename.endswith(".txt"):
        print(f"[WATCH_START] Executando script: {filename}")
        try:
            subprocess.run(["python3", filename])
        except Exception as e:
            print(f"Erro no script: {e}")

print("[1] Watchdog ativo. Escutando eventos...")
if not os.path.exists(FOLDER_WATCH):
    os.makedirs(FOLDER_WATCH)
    print(f"[0] Criado diretório vazio: {FOLDER_WATCH}")

observer = Observer()
event_handler = MyHandler()
observer.schedule(event_handler, FOLDER_WATCH, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()