import requests


def buscar_avatar(usuario):
    """
    :param usuario: busca um usuario no git hub
    :return: str com o id e com o avatar
    """

    url = f'https://api.github.com/users/{usuario}'
    busca = requests.get(url)
    return f"O id do usuario é: {busca.json()['id']}\n" \
           f"E o seu avatar é {busca.json()['avatar_url']} "


if __name__ == '__main__':
    print(buscar_avatar(input('Qual o usuário:')))
