import os
import sys
import shutil
import winreg
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def elevate_privileges():
    if not is_admin():
        script = os.path.abspath(sys.argv[0])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)
        sys.exit(0)

def remove_from_startup():
    print("Removing from startup...")
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_ALL_ACCESS) as reg_key:
            try:
                winreg.DeleteValue(reg_key, "DriverUpdateService")
                print("✓ Removed from startup registry")
            except FileNotFoundError:
                print("✓ Startup entry not found (already removed)")
    except Exception as e:
        print(f"✗ Error removing startup: {e}")

def remove_backdoor_files():
    print("Removing backdoor files...")
    
    # Файлы для удаления
    backdoor_files = [
        os.path.join(os.environ['SystemRoot'], 'System32', 'WindowsDriverUpdate.exe'),
        os.path.join(os.environ['SystemRoot'], 'System32', 'автоматическое обновление драйверов.exe'),
        os.path.join(os.path.expanduser("~"), 'Downloads', 'WindowsDriverUpdate.exe'),
        os.path.abspath("WindowsDriverUpdate.exe")  # В текущей директории
    ]
    
    for file_path in backdoor_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"✓ Removed: {file_path}")
            except Exception as e:
                print(f"✗ Error removing {file_path}: {e}")
        else:
            print(f"✓ Not found: {file_path}")

def kill_backdoor_process():
    print("Killing backdoor processes...")
    try:
        # Ищем процессы бэкдора
        processes = ["WindowsDriverUpdate.exe", "автоматическое обновление драйверов.exe"]
        
        for proc in processes:
            result = subprocess.run(f'taskkill /f /im "{proc}"', shell=True, capture_output=True, text=True)
            if "SUCCESS" in result.stdout or "terminated" in result.stdout:
                print(f"✓ Killed process: {proc}")
            else:
                print(f"✓ Process not running: {proc}")
                
    except Exception as e:
        print(f"✗ Error killing processes: {e}")

def clean_temp_files():
    print("Cleaning temporary files...")
    try:
        temp_dirs = [
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', ''),
            os.path.join(os.environ['SystemRoot'], 'Temp'),
            os.path.join(os.path.expanduser("~"), 'AppData', 'Local', 'Temp')
        ]
        
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.lower().endswith(('.exe', '.py', '.pyc')):
                            try:
                                file_path = os.path.join(root, file)
                                if "backdoor" in file.lower() or "windowsdriverupdate" in file.lower():
                                    os.remove(file_path)
                                    print(f"✓ Removed temp file: {file}")
                            except:
                                pass
                                
        print("✓ Temporary files cleaned")
    except Exception as e:
        print(f"✗ Error cleaning temp files: {e}")

def reset_windows_firewall():
    print("Resetting Windows Firewall...")
    try:
        # Удаляем правила бэкдора если есть
        subprocess.run('netsh advfirewall firewall delete rule name="Backdoor"', shell=True, capture_output=True)
        subprocess.run('netsh advfirewall firewall delete rule name="WindowsDriverUpdate"', shell=True, capture_output=True)
        print("✓ Firewall rules reset")
    except Exception as e:
        print(f"✗ Error resetting firewall: {e}")

def main():
    print("=" * 50)
    print("    Backdoor Cleanup Tool - Rudeps Research")
    print("=" * 50)
    print()
    
    if not is_admin():
        print("Requesting administrator privileges...")
        elevate_privileges()
        return
    
    print("WARNING: This will remove all backdoor components!")
    confirm = input("Continue? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("Cleanup cancelled.")
        return
    
    print("\nStarting cleanup process...\n")
    
    # Выполняем очистку
    kill_backdoor_process()
    print()
    
    remove_from_startup()
    print()
    
    remove_backdoor_files()
    print()
    
    clean_temp_files()
    print()
    
    reset_windows_firewall()
    print()
    
    print("=" * 50)
    print("CLEANUP COMPLETED!")
    print("All backdoor components have been removed.")
    print("=" * 50)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()