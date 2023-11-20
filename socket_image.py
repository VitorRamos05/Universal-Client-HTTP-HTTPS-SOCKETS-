import socket, os

PORT = 80

try:
    url_completa = input("Digite a URL da imagem que deseja baixar: ")

    def nome_arquivo(url):
        partes = url.split('/')
        return partes[-1]

    nome = nome_arquivo(url_completa)
    
    url_part = url_completa.split('//')
    url_host = url_part[1].split('/')[0]
    url_image = '/' + '/'.join(url_part[1].split('/')[1:])
    url_request = f'GET {url_image} HTTP/1.1\r\nHost: {url_host}\r\n\r\n'
    
    sock_image = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_image.connect((url_host, PORT))
    sock_image.sendall(url_request.encode())

    tamanho = None
    image = b''

    while True:
        dados = sock_image.recv(4096)
        if not dados:
            break
        image = image + dados
        tamanho_conteudo = image.split(b'Content-Length:')
        if len(tamanho_conteudo) > 1:
            tamanho = int(tamanho_conteudo[1].split()[0])
        if tamanho is not None and len(image) >= tamanho:
            break
    sock_image.close()
    print(f'\nTamanho da Imagem: {tamanho} bytes')

    pasta = os.path.dirname(nome)
    if not os.path.exists(pasta):
        os.makedirs(pasta)
    
    end = '\r\n\r\n'.encode()
    posicao = image.find(end)
    dados_bin = image[posicao + 4:]
    cabeçalhos = image[:posicao]

    file_output = open(nome, 'wb')
    file_output.write(dados_bin)
    file_output.close()
except TimeoutError:
    print("Espirou o tempo limite.")
except ConnectionError:
    print("Conexão nao estabelecida.")
except Exception as error:
    print(f"Ocorreu um erro: {error}")
