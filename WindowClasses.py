import win32gui
import win32process
import psutil

def get_window_class_by_process_name(process_name):
    window_classes = []
    for proc in psutil.process_iter():
        if proc.name().lower() == process_name.lower():
            try:
                def enum_windows_callback(hwnd, lparam):
                    if win32gui.IsWindowVisible(hwnd):
                        _, pid = win32process.GetWindowThreadProcessId(hwnd)
                        if pid == proc.pid:
                            window_classes.append(win32gui.GetClassName(hwnd))
                    return True

                win32gui.EnumWindows(enum_windows_callback, 0)
                if window_classes:
                    return window_classes
            except (psutil.NoSuchProcess, win32gui.pywintypes.error):
                pass
    return None

if __name__ == '__main__':
    process_name = input("Введите имя процесса (с расширением .exe): ")
    window_classes = get_window_class_by_process_name(process_name)
    if window_classes:
        with open("window_classes.txt", "w", encoding="utf-8") as f:
            f.write(f"Классы окон процесса {process_name}:\n")
            for class_name in window_classes:
                f.write(f"{class_name}\n")
            f.write("\n")
        print(f"Классы окон процесса {process_name}: {window_classes} \n"
              f"Инфa записана в файл window_classes.txt")
    else:
        print(f"Процесс {process_name} не найден.")