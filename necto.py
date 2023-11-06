import socket
import sys
import threading
import getopt
import subprocess as sb

listener = False
command = False
exec_cmd = ""
host = ""
upload_dir = ""
port = 0

def help():
    print("Usage: netcat.py -t target_host -p port")
    print("-l --listen                  - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run     - execute the given file upon receiving a connection")
    print("-c --command                 - initialize a command shell")
    print("-u --upload=destination      - upon receiving a connection, upload a file and write to [destination]")
    print("")
    print("Examples:")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -c")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("netcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    print("echo 'ABC' | ./netcat.py -t 192.168.0.1 -p 135")

def main():
    global listener
    global command
    global exec_cmd
    global upload_dir
    global host
    global port

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print(str(err))
        help()

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
        elif opt in ("-l", "--listen"):
            listener = True
        elif opt in ("-e", "--execute"):
            exec_cmd = arg
        elif opt in ("-c", "--command"):
            command = True
        elif opt in ("-u", "--upload"):
            upload_dir = arg
        elif opt in ("-t", "--target"):
            host = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        else:
            assert False, "Unhandled Option"

    if not listener and len(host) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)

    if listener:
        server_loop()

def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        if len(buffer):
            client.send(buffer.encode())

        while True:
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(1024)
                recv_len = len(data)
                response += data.decode()

                if recv_len < 1024:
                    break

            print(response)

            buffer = input("")
            buffer += "\n"
            client.send(buffer.encode())

    except Exception as e:
        print(e)

def server_loop():
    global host

    if not len(host):
        host = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    command = command.rstrip()
    try:
        output = sb.check_output(command, stderr=sb.STDOUT, shell=True)
        return output
    except Exception as e:
        return str(e).encode()

def client_handler(client_socket):
    global upload_dir
    global exec_cmd
    global command

    if len(upload_dir):
        file_buffer = ""

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file_buffer += data

        try:
            with open(upload_dir, "wb") as file:
                file.write(file_buffer)
            client_socket.send("Upload done :)\n".encode())
        except Exception as e:
            client_socket.send(f"Upload failed: {str(e)}\n".encode())

    if len(exec_cmd):
        output = run_command(exec_cmd)
        client_socket.send(output)

    if command:
        while True:
            client_socket.send(b"Shell> ")
            cmd_buffer = b""
            while b"\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            response = run_command(cmd_buffer.decode())
            client_socket.send(response)

if __name__ == "__main__":
    main()
