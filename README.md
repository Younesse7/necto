# necto
Python-based network utility that can be used for remote communication and network-related tasks. It offers the following key functionalities:

- **Listener**: The tool can act as a listener, waiting for incoming network connections on a specified host and port.

- **Command Execution**: It can execute shell commands on a remote host and capture the output.

- **File Upload**: It has the ability to upload files to a remote host over a network connection.

- **Basic Shell Interaction**: It can provide a basic command shell interface for interaction with a remote system.

- **Network Communication**: The tool facilitates the exchange of data and messages between systems connected via network sockets.

- **Port Binding**: It allows binding to a specific port for network communication.

- **Error Handling**: It includes basic error handling for network-related operations

usage :

python necto.py [options]





-h, --help: Display a help message.

-l, --listen: Start the tool in listener mode.

-e, --execute: Execute a command upon receiving a connection.

-c, --command: Start a command shell.

-u, --upload=<destination>: Upload a file upon receiving a connection.

-t, --target=<host>: Set the target host (required).

-p, --port=<port>: Set the target port (required).

Start in listener mode:

                 python necto.py -l -t <host> -p <port>

                 
Execute a command upon receiving a connection:

                  python necto.py -t <host> -p <port> -e "cat /etc/passwd"


                  
Start a command shell:

                    python necto.py -t <host> -p <port> -c


Upload a file upon receiving a connection:




                    python necto.py -t <host> -p <port> -u /path/to/destination/file


