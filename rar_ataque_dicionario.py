import subprocess
import time

SEVEN_ZIP_PATH = r"C:\Program Files\7-Zip\7z.exe"  # Caminho completo para o executável 7z

def dictionary_attack(rar_path, dictionary_path):
    """Tenta descompactar o arquivo RAR usando um ataque de dicionário com o 7z via subprocess."""
    last_print_time = time.time()  # Armazena o tempo inicial
    with open(dictionary_path, 'r', encoding='utf-8') as file:
        for password in file:
            password = password.strip()  # Remove espaços em branco e novas linhas
            try:
                # Chama o 7z via subprocess, especificando o caminho completo
                result = subprocess.run(
                    [SEVEN_ZIP_PATH, 'x', '-p{}'.format(password), '-y', rar_path],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                # Verifica se a senha foi bem-sucedida verificando a saída
                if 'Everything is Ok' in result.stdout:
                    print(f"Senha encontrada: {password}")
                    return password
            except subprocess.CalledProcessError as e:
                pass  # Senha incorreta, continua tentando

            current_time = time.time()
            if current_time - last_print_time >= 15:
                print(f"Última senha testada: {password}")
                last_print_time = current_time  # Atualiza o tempo da última impressão

    print("Senha não encontrada.")
    return None

if __name__ == "__main__":
    rar_path = input("Digite o caminho do arquivo RAR protegido por senha: ")
    dictionary_path = input("Digite o caminho do arquivo de texto com o dicionário de senhas: ")

    result = dictionary_attack(rar_path, dictionary_path)
    if result:
        print(f"A senha do RAR é: {result}")
    else:
        print("Não foi possível descriptografar o RAR com o dicionário fornecido.")
