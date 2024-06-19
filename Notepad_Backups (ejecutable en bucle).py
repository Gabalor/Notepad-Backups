import pyautogui
import pygetwindow as gw
import pyperclip
import time
from datetime import datetime
import re

def sanitize_filename(filename):
    # Reemplaza caracteres no permitidos en nombres de archivos por guiones bajos
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def save_notepad_backup(window, counter):
    try:
        # Activar la ventana de Notepad
        window.activate()
        time.sleep(1)  # Esperar un segundo para asegurarse de que la ventana esté activa

        # Verificar que la ventana activa es Notepad
        active_window = gw.getActiveWindow()
        if active_window.title != window.title:
            print(f"Failed to activate window: {window.title}")
            return

        pyautogui.hotkey('ctrl', 'a')  # Seleccionar todo el texto
        pyautogui.hotkey('ctrl', 'c')  # Copiar al portapapeles
        time.sleep(0.5)  # Esperar para asegurar que la copia se complete
        clipboard_content = pyperclip.paste()  # Obtener el contenido del portapapeles
        clipboard_content = clipboard_content.replace('\r\n', '\n')  # Normalizar saltos de línea a solo '\n' 

        # Generar un nombre de archivo con la fecha y hora actuales y el título de la ventana
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        window_title = window.title

        if not window_title:
            window_title = f"Untitled_{counter}"
        else:
            window_title = sanitize_filename(window_title)

        file_name = f"Backup_{window_title}_{timestamp}.txt"
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(clipboard_content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    counter = 1
    try:
        while True:
            notepad_windows = gw.getWindowsWithTitle('Notepad')
            for window in notepad_windows:
                # Print window title for debugging
                print(f"Processing window: {window.title}")
                save_notepad_backup(window, counter)
                counter += 1
                time.sleep(1)  # Añadir una pausa entre el procesamiento de ventanas
            counter = 1  # Reiniciar el contador
            time.sleep(10)  # Tiempo a esperar antes de hacer el próximo respaldo
    except KeyboardInterrupt:
        print("Interrupted by user")
