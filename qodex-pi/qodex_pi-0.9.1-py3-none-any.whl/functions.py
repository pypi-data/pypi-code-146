""" Содержить все функции для функционирования QPI """
import socket
from traceback import format_exc


def create_server(my_ip, my_port):
    """ Создать и вернуть сервер"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((my_ip, my_port))
    server.listen(10)
    return server


def execute_method_decorator(success_response=None):
    # Декоратор, оборачивающий выполнение метода
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                # Выполнить метод, передав ему все аргументы
                method_response = func(*args, **kwargs)
                operated_method_response = operate_method_response(method_response, success_response)
                operated_method_response['method_str'] = func.__name__      # Добавить имя метода
                return operated_method_response
            except:
                return {'status': False, 'info': format_exc()}
        return wrapper
    return decorator


def operate_method_response(response, success_reponse, *args, **kwargs):
    """ Обрабатывает ответ от вызвываемого метода ядра или супер-метода """
    return {'status': try_extract_key(array=response, key='status', default_value=True),
            'info': try_extract_key(array=response, key='info', default_value=success_reponse)}


def try_extract_key(array, key, default_value):
    """ Пытается извлечь из ответа array значение ключа key. При неудаче возвращает значение default_value """
    try:
        return array[key]
    except (KeyError, TypeError) as e:
        return default_value


def expand_kwargs(values, *args, **kwargs):
    """ Расширяет заданный юзером словарь с параметрами для выполнения команд своими (так, например, можно в выполняющую
    команду передать даныне о соединении connection, или же вообще о всем словаре соединений connections_dict) """
    for key, value in kwargs.items():
        values[key] = value


def extract_core_support_methods(core, *args, **kwargs):
    """ Извлечь словарь открытых для API методов от Core"""
    try:
        methods = core.get_api_support_methods()
        return methods
    except AttributeError:
        return {}


def no_method_operation(command, qpi_name, *args, **kwargs):
    """ Функция вызывается, если для указанной операции не найден соответствующий метод класса ядра """
    return {'status': False, 'info': 'Метод {} не поддерживается на стороне {}'.format(command, qpi_name)}
