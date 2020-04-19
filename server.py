import socket
import select
import sys

HEADER_LENGTH = 10
IP = "0.0.0.0"
PORT = 1234
RECV_BUFFER = 4096
SOCKET_LIST = []

def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((IP, PORT))
    server_socket.listen(5)

    SOCKET_LIST.append(server_socket)
    
    print('Server started on port ' + str(PORT))


    while 1:

        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

        for sock in ready_to_read:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print('Client (%s, %s) connected' % addr)

                broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)

            else:
                try:
                    data = sock.recv(RECV_BUFFER).decode('utf-8')

                    if data:
                        
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)

                    else:

                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()


def broadcast(server_socket, sock, message):
    for socket in SOCKET_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message.encode('utf-8'))
            except:
                socket.close()

                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
    
    
    
if __name__ == '__main__':
    sys.exit(server())
    
"""server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

server_socket.listen(3)
sockets_list = [server_socket]
clients = {}

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        
        message_length = int(message_header.decode("utf-8").strip())
        
        return {'header': message_header, 'data': client_socket.recv(message_length)} 
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)

            clients[client_socket] = user

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")

        else:
            message = receive_message(notified_socket)
            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f"Recieved message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])


    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
"""
