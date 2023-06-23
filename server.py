import socket
import sys
from threading import Thread

class Server:
    def __init__(self, IP, port):
    # A classe Server tem um construtor que recebe um endereço IP e uma porta. 
        self.IP = IP
        self.port = port
        
        # Um socket s é criado e vinculado ao endereço IP e porta fornecidos.
        self.s = socket.socket()
        self.s.bind((self.IP, self.port))
        self.s.listen(5)

        # O atributo peers é um dicionário vazio que será usado para armazenar informações sobre os peers que se conectam ao servidor.
        self.peers = {}

        print("Server started at IP: " + self.IP + " Port: " + str(self.port))

    def run(self):
        while True:
        # O método run é executado em um loop infinito. 

            # Ele aguarda e aceita uma conexão de cliente usando o socket.
            c, addr = self.s.accept()

            # Em seguida, cria uma nova thread para manipular a conexão com o peer. 
            # Essa thread chama o método peer_handler passando o socket da conexão e o endereço do peer como argumentos.
            t = Thread(target = self.peer_handler, args = (c, addr))
            t.start()

    def peer_handler(self, c, addr):
        try:
        # O método peer_handler é responsável por lidar com a comunicação com os peers.
            request = c.recv(1024).decode()
            data = request.split()

            # Se a primeira parte da mensagem for "JOIN", significa que um peer está se registrando no servidor. 
            if data[0] == "JOIN":

                # Os detalhes do peer, incluindo o endereço IP, porta e lista de arquivos, são extraídos da mensagem e armazenados no dicionário peers. 
                files = ' '.join(data[3:]).replace('[', '').replace(']', '').replace('"', '').replace(',', '').replace("'", '')
                self.peers[data[2]] = (data[1], data[2], data[3:])
                print('Peer {}:{} adicionado com arquivos {}'.format(data[1], data[2], files))

                # Uma mensagem de confirmação "JOIN_OK" é enviada de volta ao peer e a conexão é fechada.
                response = 'JOIN_OK'
                c.send("{}".format(response).encode())
                c.close()

            # Se a primeira parte da mensagem recebida for "SEARCH", significa que um peer está solicitando uma busca por um arquivo específico. 
            elif data[0] == "SEARCH":
                # O nome do arquivo é extraído da mensagem, juntamente com o endereço IP e porta do peer que enviou a solicitação. 
                data = data[1]
                p_IP = addr[0]
                p_port = addr[1]
                print('Peer {}:{} solicitou arquivo {}'.format(p_IP, p_port, data))
                response = "SEARCH_OK"
                matching_peers = []

                # O servidor itera sobre os dados de cada peer registrado (peers.values()) e verifica se o arquivo solicitado está presente em algum dos peers cadastrados. 
                for peer_data in self.peers.values():
                    files = peer_data[2]

                    # Se houver uma correspondência, o endereço IP e porta desse peer são adicionados a uma lista de peers compatíveis (matching_peers). 
                    if data in files:
                        peer = peer_data[0] + ":" + peer_data[1]
                        matching_peers.append(peer)  

                # Os dados de resposta, contendo os peers compatíveis e a mensagem de resposta, são enviados de volta ao peer que fez a solicitação e a conexão é fechada.
                response_data = {
                    "matching_peers": matching_peers,
                    "response": response
                }
                c.send(str(response_data).encode())
                c.close()
            
            # Se a primeira parte da mensagem recebida for "UPDATE", significa que um peer está atualizando suas informações no servidor. 
            elif data[0] == "UPDATE":
                
                # Os detalhes atualizados do peer, incluindo o endereço IP, porta e lista de arquivos, são extraídos da mensagem e atualizados no dicionário peers. 
                array = data[3:]
                self.peers[data[2]] = (data[1], data[2], array)

                # Uma mensagem de confirmação "UPDATE_OK" é enviada de volta ao peer e a conexão é fechada.
                response = 'UPDATE_OK'
                c.send("{}".format(response).encode())
                c.close()
        
        except Exception as e:
            print("Internal server error: {}",e)
            c.close()
            sys.exit()


s_IP = input("Enter the server IP: ")
if s_IP == "":
        s_IP = '127.0.0.1'

while True:
    s_port_input = input("Enter the server port: ")
    if s_port_input == "":
        s_port = 1099
        break
    elif s_port_input.isdigit():
        s_port = int(s_port_input)
        break
    else:
        print("The server port should be either an integer or empty.")
    
server = Server(s_IP, s_port)
server.run()