def write(url):
    with open("shell.py", "w") as f:
        f.write(f"""
import socket\n
""")
        f.write(f"HOST = '{url}'")
        f.write("""
PORT = 4444        # The port used by the server
""")
        f.write("""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
print('Received', repr(data))
        """)
