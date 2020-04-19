import socket
import select
import errno
import sys


def client():

    ip = ''
    port = 1234

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2)

    try:
        client_socket.connect((ip, port))
    except:
        print('Enable to conect')
        sys.exit()

    print('Connected to remove host. Send message')
    sys.stdout.write('[Me] ')
    sys.stdout.flush()

    while 1:
        socket_list = [sys.stdin, client_socket]

        ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

        for sock in ready_to_read:
            if sock == client_socket:
                data = sock.recv(4096).decode('utf-8')
                if not data:
                    print('Disconnect from caht')
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] ')
                    sys.stdout.flush()
            else:

                msg = sys.stdin.readline()
                client_socket.send(msg.encode('utf-8'))
                sys.stdout.write('[Me] ')
                sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(client())
"""
HEADER_LENGTH = 10

IP = "0.0.0.0"
PORT = 1234

input_username = input("Username: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)
username = input_username.encode('utf-8')

username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    message = input(f'{input_username} > ')

    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header + message)
    #create else delete while
    try:
        while 1:
            username_header = client_socket.recv(HEADER_LENGTH)
            if not len(username_header):
                print('connection closed by the server')
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            
            print(f'{username} > {message}')

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}' .format(str(e)))
            sys.exit()
        continue
            
    except Exception as e:
        print('General error' . format(str(e)))
        sys.exit()
    
"""
