# necto
tool for connection 

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


