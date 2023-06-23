import socket
import os
import sys
from threading import Thread

class Peer:
    def __init__(self, IP, port, storage, s_IP = '127.0.0.1', s_port = 1099 ):
    # A classe Peer é definida. O método __init__ é o construtor da classe e inicializa os atributos
        
        # IP, storage, port, s, s_IP e s_port. 
        self.IP = IP
        self.storage = storage

         # É criado um socket s e o IP é vinculado a uma porta aleatória ou alguma que tenha sido passada por parametro.
        self.s = socket.socket()
        self.s.bind((self.IP, port)) 

        # O socket começa a ouvir por conexões.
        self.s.listen(2)

        # A porta real em que o socket está ouvindo é obtida e armazenada no atributo port. 
        self.port = self.s.getsockname()[1]

        print("Peer started at IP: " + self.IP + " Port: " + str(self.port))

        # O IP e a porta do servidor (server IP e server port) também são armazenados nos atributos s_IP e s_port, respectivamente
        self.s_IP = s_IP
        self.s_port = s_port

        # Em seguida, cria uma nova thread com o método peer_handler() do peer como alvo e inicia a thread.
        t = Thread(target = self.peer_handler, args = ())
        t.start()

    def peer_handler(self):
    # O método listen fica em um loop infinito, aguardando conexões. Quando uma conexão é estabelecida.
        while True:

            # O socket é aceito e uma mensagem é recebida do cliente. A mensagem é dividida em palavras separadas.
            c, addr = self.s.accept()
            data = c.recv(1024).decode()
            data = data.split()

            # Se a primeira palavra da mensagem for "DOWNLOAD", isso indica que o peer está solicitando um arquivo específico. 
            if data[0] == "DOWNLOAD":

                # O nome do arquivo é extraído da mensagem e uma mensagem é impressa indicando o peer que fez a solicitação e o arquivo solicitado. 
                file = data[1]
                print("Peer {}:{} solicitou arquivo {}".format(addr[0], addr[1], file))

                # O método send_file é chamado para enviar o arquivo solicitado para o peer. 
                self.send_file(c, file)

            # A conexão é fechada após a verificação.
            c.close()

    def register(self):
        try:
        # O método register cria um novo socket s e se conecta ao servidor usando o IP e a porta do servidor armazenados nos atributos s_IP e s_port. 
            s = socket.socket()
            s.connect((self.s_IP, self.s_port))
                
            # É criada uma string files contendo os nomes de arquivos disponíveis no peer. 
            files = ' '.join(self.get_my_files()).replace('[', '').replace(']', '').replace('"', '').replace(',', '').replace("'", '')
            data = "JOIN {} {} {}".format(self.IP, str(self.port), files)

            # A string é enviada ao servidor junto com o IP, a porta e a mensagem "JOIN". 
            s.send(data.encode())
            response = s.recv(1024).decode()

            # A resposta do servidor é recebida e, se for "JOIN_OK", uma mensagem é impressa indicando que o peer se registrou com sucesso junto com o IP, a porta e os arquivos disponíveis. 
            if response == "JOIN_OK":
                print("Sou peer {}:{} com arquivos {}".format(self.IP, self.port, files))

            s.close()
        except:
            print("Error to conect with server")
            sys.exit()

            

    def search(self, file):
        try:
        # O método search cria um novo socket s e se conecta ao servidor usando o IP e a porta do servidor armazenados nos atributos s_IP e s_port. 
            s = socket.socket()
            s.connect((self.s_IP, self.s_port))

            # É criada uma mensagem data contendo o comando "SEARCH" seguido pelo nome do arquivo a ser pesquisado. 
            data = "SEARCH {}".format(file)
            s.send(data.encode())

            # A resposta do servidor é recebida e convertida para um dicionário usando a função eval(). 
            response = eval(s.recv(1024).decode())

            # Os pares chave-valor relevantes são extraídos do dicionário. 
            matching_peers = response['matching_peers']
            response = response['response']

            # Se a resposta for "SEARCH_OK", a lista de peers compatíveis é formatada em uma string e impressa na tela.
            if response == "SEARCH_OK":
                data = ' '.join(matching_peers).replace('[', '').replace(']', '').replace('"', '').replace(',', '').replace("'", '')
                if data == "":
                    print("nenhum peer encontrado com arquivo solicitado")
                else:
                    print("peers com arquivo solicitado: {}".format(data))

            s.close()

        except:
            print("Error to conect with server")
            

    def get_my_files(self):
    # O método get_my_files retorna uma lista de nomes de arquivos presentes no diretório de armazenamento do peer.
        try:
            file_names = []

            for file in os.listdir(self.storage):
                file_names.append(file)

            return file_names
        
        except:
            print("Error to get files")
            sys.exit()
    
    def download(self, p_IP, p_port, file):
        try:
        # O método download cria um novo socket s e se conecta ao peer do qual se deseja fazer o download usando o IP e a porta fornecidos. 
            s = socket.socket()
            s.connect((p_IP, p_port))

            # É criada uma mensagem data contendo o comando "DOWNLOAD" seguido pelo nome do arquivo a ser baixado. 
            data = "DOWNLOAD {}".format(file)

            # A mensagem é enviada ao peer. A resposta do peer é recebida e armazenada. 
            s.send(data.encode())
            response = s.recv(1024).decode()

            # O método receive_file é chamado para receber o arquivo do peer.
            self.receive_file(s, response, file)

            s.close()
        except:
           print("Error to conect with peer")
            

    def send_file(self, c, file):
    # O método send_file é responsável por enviar o arquivo solicitado para o peer que fez a solicitação. 
        try:
            # O arquivo é aberto em modo de leitura binária e é lido em blocos de 1024 bytes. 
            with open(os.path.join(self.storage, file), 'rb') as f:
                c.send("DOWNLOAD_OK".encode())
                data = f.read(1024)

                # Enquanto houver dados no arquivo, esses dados são enviados ao peer através do socket c. 
                while data:
                    c.send(data)
                    data = f.read(1024)

        # Se ocorrer uma exceção durante o processo de envio do arquivo, uma mensagem "DOWNLOAD_FAIL" é enviada ao peer. 
        except:
            c.send("DOWNLOAD_FAIL".encode())

        c.close()
    
    def receive_file(self, s, response, file):
    # O método receive_file é responsável por receber o arquivo enviado por um peer durante o processo de download. 
        # Se a resposta do peer for "DOWNLOAD_OK"
        if response == "DOWNLOAD_OK":

            # O arquivo é aberto em modo de escrita binária e os dados recebidos do peer são gravados no arquivo em blocos de 1024 bytes. 
            with open(os.path.join(self.storage, file), 'wb') as f:
                data = s.recv(1024)

                while data:
                    f.write(data)
                    data = s.recv(1024)

            # Após a conclusão do download, uma mensagem é impressa indicando que o arquivo foi baixado com sucesso na pasta de armazenamento do peer. 
            print("Arquivo {} baixado com sucesso na pasta {}".format(file, self.storage))

            # O método update também é chamado para atualizar os arquivos disponíveis no servidor. 
            self.update()

        # Se a resposta do peer não for "DOWNLOAD_OK", uma mensagem de falha é impressa.    
        else:
            print("Falha ao receber arquivo {}".format(file))

        s.close()

    def update(self):
    # O método update é responsável por atualizar os arquivos disponíveis no servidor. 

        # Um novo socket s é criado e conectado ao servidor. 
        s = socket.socket()
        s.connect((self.s_IP, self.s_port))

        # Uma string files é criada com os nomes dos arquivos disponíveis no peer e formatada adequadamente.
        files = ' '.join(self.get_my_files()).replace('[', '').replace(']', '').replace('"', '').replace(',', '').replace("'", '')
        
        # Uma mensagem data é criada contendo o comando "UPDATE" seguido pelo IP, a porta e a lista de arquivos.
        data = "UPDATE {} {} {}".format(self.IP, str(self.port), files)

        # A mensagem é enviada ao servidor. A resposta do servidor é recebida
        s.send(data.encode())
        response = s.recv(1024).decode()

        # Se for "UPDATE_OK", a conexão é fechada. 
        if response == "UPDATE_OK":
            s.close()

        # Caso contrário, uma mensagem de falha é impressa.
        else:
            print("Falha ao atualizar arquivos")
            s.close()

    def run(self):
            # Entra em um loop infinito onde o usuário pode escolher entre diferentes ações relacionadas ao peer. 
            while True:

                    # Solicita ao usuário que insira a opção desejada: 
                    # "1" para se registrar
                    # "2" para pesquisar por um arquivo 
                    # "3" para fazer o download de um arquivo
                    choice = input("1 -> JOIN, 2 -> SEARCH, 3 -> DOWNLOAD\n")

                    # Com base na opção escolhida, são solicitados os parâmetros relevantes e os métodos apropriados do peer são chamados.

                    if choice == "1":
                        peer.register()

                    elif choice == "2":
                        file = input("Enter the file name: ")
                        peer.search(file)

                    elif choice == "3":
                        p_IP = input("Enter the peer IP: ")
                        while True:
                            p_port = input("Enter the peer port: ")
                            if p_port.isdigit():
                                p_port = int(p_port)
                                break
                            else:
                                print("The peer port should be an integer.")

                        file = input("Enter the file name: ")
                        peer.download(p_IP, p_port, file)
                    
                    else:
                        # Se uma opção inválida for fornecida, o loop é encerrado.
                        print("Ending proccess")
                        sys.exit()   

p_IP = input("Enter the peer IP: ")
if p_IP == "":
    p_IP = '127.0.0.1'

while True:
    p_port_input = input("Enter the peer port: ")
    if p_port_input == "":
        p_port = 0
        break
    elif p_port_input.isdigit():
        p_port = int(p_port_input)
        break
    else:
        print("The peer port should be either an integer or empty.")

while True:
    # Solicita ao usuário que insira o caminho para a pasta de armazenamento do peer.
    p_storage = input("Enter the peer storage: ")
    if p_storage != "":
        break

peer = Peer(p_IP, p_port, p_storage)
peer.run()

