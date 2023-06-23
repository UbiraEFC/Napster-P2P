Sistema Peer-to-Peer para Transferência de Arquivos de Vídeo Gigantes
=====================================================================

Este projeto consiste na implementação de um sistema peer-to-peer (P2P) que permite a transferência de arquivos de vídeo gigantes entre peers, intermediados por um servidor centralizado. O sistema utiliza o protocolo TCP (Transmission Control Protocol) para comunicação entre os componentes.

Descrição da Atividade
----------------------

O sistema P2P permite que os peers atuem tanto como provedores de informações, fornecendo arquivos de vídeo, quanto como receptores desses arquivos. Cada peer pode registrar-se no servidor central, informando suas informações de identificação e os arquivos disponíveis para compartilhamento. Os peers podem pesquisar arquivos específicos no servidor e obter uma lista de peers que possuem esses arquivos.

Quando um peer deseja baixar um arquivo de vídeo específico, ele envia uma requisição para o servidor contendo o nome do arquivo desejado. O servidor realiza uma busca pelo nome do arquivo e responde ao peer com uma lista de peers que possuem o arquivo solicitado. O peer pode então escolher um dos peers da lista e enviar uma requisição direta para baixar o arquivo.

Após a confirmação do peer provedor, o arquivo é transferido diretamente do peer provedor para o peer solicitante. Uma vez que o arquivo é recebido pelo peer solicitante, ele pode ser salvo em uma pasta local e visualizado utilizando um software externo de reprodução de vídeo.

Componentes do Projeto
----------------------

O projeto é dividido em dois arquivos principais:

### server.py

O arquivo `server.py` contém a implementação da classe `Server` e suas funções relacionadas. A classe `Server` representa o servidor central do sistema P2P e é responsável por gerenciar as conexões dos peers, processar suas solicitações e manter um registro dos arquivos disponíveis em cada peer. As principais funções do servidor incluem:

-   `run()`: inicia o servidor, aguardando conexões de peers.
-   `peer_handler()`: lida com as solicitações recebidas dos peers, como registro, busca e download de arquivos.
-   Funções auxiliares para processar as solicitações dos peers e manter o registro de arquivos.

### peer.py

O arquivo `peer.py` contém a implementação da classe `Peer` e suas funções relacionadas. A classe `Peer` representa um peer no sistema P2P e é responsável por interagir com o servidor central e outros peers. As principais funções do peer incluem:

-   `register()`: registra o peer no servidor central, informando suas informações de identificação e os arquivos disponíveis.
-   `search()`: realiza busca por arquivos no servidor, obtendo uma lista de peers que possuem o arquivo desejado.
-   `download()`: baixa arquivos de outros peers selecionados.
-   `listen()`: ouve conexões de outros peers para receber solicitações de download.
-   Funções auxiliares para obter a lista de arquivos disponíveis, enviar arquivos e atualizar o servidor.

Como Executar
-------------

Para executar o sistema, é necessário ter o Python instalado em sua máquina. Siga os passos abaixo:

1.  Faça o download dos arquivos `server.py` e `peer.py` para uma pasta local.

2.  Abra um terminal ou prompt de comando e navegue até a pasta onde os arquivos foram salvos.

3.  Para iniciar o servidor, execute o seguinte comando:

    `py server.py`

4.  Para iniciar um peer, execute o seguinte comando:


    `py peer.py`

    Certifique-se de executar o comando do passo 4 em terminais ou prompts de comando separados para cada peer.

Considerações Finais
--------------------

Este projeto proporcionou a implementação de um sistema P2P para transferência eficiente e segura de arquivos de vídeo gigantes entre peers. Superamos desafios como o gerenciamento de threads e o envio de arquivos grandes, utilizando conceitos avançados de programação.

Agradecemos pela oportunidade de trabalhar neste projeto e estamos abertos a sugestões e melhorias. Sinta-se à vontade para contribuir, fornecer feedback e utilizar este sistema para suas necessidades de transferência de arquivos P2P.

Divirta-se explorando o mundo do compartilhamento de arquivos com o nosso sistema P2P!
