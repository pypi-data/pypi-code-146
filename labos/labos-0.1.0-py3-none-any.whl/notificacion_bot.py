import requests

def mensaje_tel(mensaje: str = 'Termino de correr el script'):
    '''
    Manda un mensaje de telegram al chat que tenes con el bot 'python_scripts'.

    INPUT: 
    mensaje: str: mensaje para mandar al bot.
    '''
    api_token = '5448153732:AAGhKraJQquEqMfpD3cb4rnTcrKB6U1ViMA'
    api_url = f'https://api.telegram.org/bot{api_token}/sendMessage'
    chat_id = '1034347542'
    try:
        response = requests.post(api_url, json={'chat_id': chat_id, 'text': mensaje})
        print(response.text)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    # Se saca de BotFather
    # token = '5448153732:AAGhKraJQquEqMfpD3cb4rnTcrKB6U1ViMA'
    
    # How to get the chat_id
    # url = f'https://api.telegram.org/bot{token}/getUpdates'
    # print(requests.get(url).json())
    # chat_id = 1034347542
    
    # Prueba de si los mensajes funcionan
    mensaje_tel('Los mensajes funcionan')