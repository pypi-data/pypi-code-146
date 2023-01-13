""" Все операции методов """
from qpi.functions import execute_method_decorator
from qpi.auth import auth_module


@execute_method_decorator('Попытка аутентификации клиента')
def auth_me(sql_shell, login, password, connection, connections_dict, users_table_name, user_name_column,
            self_qpi, *args, **kwargs):
    """ Команда на авторизацию пользователя (клиенета QDK), принимает login, password,
    connection (самое подключение с клиентом),
    connections_dict - словарь, содержащий все подключения,
    users_table_name - имя таблицы, где хранятся данные о пользователях,
    users_name_column - имя поля, в котором хранится идентификатор пользователя
    self_qpi - сам объект QPI """
    response, status = auth_module.auth_user(sql_shell, login, password, connection, users_table_name, user_name_column)
    if status:
        set_connection_auth(connections_dict, connection)
        self_qpi.after_auth_execute(connection, connections_dict, *args, **kwargs)
        return {'info': response}
    else:
        return {'status': False, 'info': response}


def set_connection_auth(connections_dict, connection, *args, **kwargs):
    """ Для подключения connection в словаре connections_dict выставить флажок об успешной аутентификации"""
    return set_connection_status(connections_dict, connection, 'auth', True)


def set_connection_unauth(connections_dict, connection, *args, **kwargs):
    """ Для подключения connection в словаре connections_dict убрать флажок об успешной аутентификации"""
    return set_connection_status(connections_dict, connection, 'auth', False)


def set_connection_subscribe(connections_dict, connection, *args, **kwargs):
    """ Для подключения connection в словаре connections_dict выставить режим подписчика"""
    return set_connection_status(connections_dict, connection, 'subscriber', True)


def set_connection_unsubscribe(connections_dict, connection, *args, **kwargs):
    """ Для подключения connection в словаре connections_dict отключить режим подписчика"""
    return set_connection_status(connections_dict, connection, 'subscriber', False)


@execute_method_decorator('Изменение статуса')
def set_connection_status(connections_dict: dict, connection: object, status: str, value, *args, **kwargs):
    """ В словаре connections_dict для ключа connection выставить ключу status значение value"""
    connections_dict[connection][status] = value
    return 'Статус ключа {} успешно изменен на {}'.format(status, value)


@execute_method_decorator
def get_methods(self_qpi, *args, **kwargs):
    """ Вернять все методы QPI"""
    return self_qpi.methods


@execute_method_decorator('Ответ на hello_word!')
def get_hello_answer(*args, **kwargs):
    return 'Hello you too!'
