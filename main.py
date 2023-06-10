from server import Server
from peer import Peer

# Pasta de exemplo que foi utilizada nos testes sendo trocados por valores storage-1, storage-2 ou storage-3
# C:\Users\Bira\Projects\SD-EP-Napster\napster-p2p\storage-1

choice = input("1 -> Server, 2 -> Peer\n")
# Solicita ao usuário que escolha entre a opção "1" para iniciar o servidor ou "2" para iniciar um peer.

if choice == "1":
    # Se a escolha for "1", inicia-se o servidor. 
    # Solicita ao usuário que insira o IP do servidor e, se nenhum IP for fornecido, assume-se o valor padrão '127.0.0.1'. 
    # Em seguida, solicita o número da porta do servidor e, se nenhuma porta for fornecida, assume-se o valor padrão '1099'.
    # Cria uma instância da classe Server com o IP e a porta fornecidos e executa o método run() do servidor.
    print("Starting Server")

    s_IP = input("Enter the server IP: ")
    if s_IP == "":
        s_IP = '127.0.0.1'

    s_port = input("Enter the server port: ")
    if s_port == "":
        s_port = 1099
    else:
        s_port = int(s_port)

    server = Server(s_IP, s_port)
    server.run()

elif choice == "2":
    # Se a escolha for "2", inicia-se um peer. 
    # Solicita ao usuário que insira o IP do peer e, se nenhum IP for fornecido, assume-se o valor padrão '127.0.0.1'. 
    # Em seguida, solicita o número da porta do peer e, se nenhuma porta for fornecida, assume-se o valor padrão '0', o qual irá utilizar uma porta randomizada que não estiver sendo utilizada.
    # Solicita também o diretório de armazenamento do peer e, se nenhum diretório for fornecido, assume-se o valor padrão "C:/Users\Bira\Projects\SD-EP-Napster\napster-p2p\storage". 
    # Cria uma instância da classe Peer com o IP, a porta e o diretório de armazenamento fornecidos.
   
    print("Starting Peer")

    p_IP = input("Enter the peer IP: ")
    if p_IP == "":
        p_IP = '127.0.0.1'

    p_port = input("Enter the peer port: ")
    if p_port == "":
        p_port = 0
    else:
        p_port = int(p_port)

    p_storage = input("Enter the peer storage: ")
    if p_storage == "":
        p_storage = "C:/Users\Bira\Projects\SD-EP-Napster\napster-p2p\storage"

    peer = Peer(p_IP, p_port, p_storage)

    while True:
        # Entra em um loop infinito onde o usuário pode escolher entre diferentes ações relacionadas ao peer. 
        # Solicita ao usuário que insira a opção desejada: 
        # "1" para se registrar
        # "2" para pesquisar por um arquivo 
        # "3" para fazer o download de um arquivo
        # Com base na opção escolhida, são solicitados os parâmetros relevantes e os métodos apropriados do peer são chamados. 
        # Se uma opção inválida for fornecida, o loop é encerrado.
        choice_2 = input("1 -> JOIN, 2 -> SEARCH, 3 -> DOWNLOAD\n")

        if choice_2 == "1":
            peer.register()

        elif choice_2 == "2":
            file = input("Enter the file name: ")
            peer.search(file)

        elif choice_2 == "3":
            p_IP = input("Enter the peer IP: ")
            p_port = int(input("Enter the peer port: "))
            file = input("Enter the file name: ")
            peer.download(p_IP, p_port, file)
        
        else:
            print("Ending proccess")
            exit()

else:
    # Se a escolha inicial não for "1" nem "2", significa que a opção fornecida é inválida e o processo é encerrado.
    print("Ending proccess")
    exit()