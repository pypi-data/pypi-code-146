""" Модуль аутентификации пользователя. Аутенификаия проходит путем сравнения заданного логина/пароля (login/password)
с логином паролем, хранимыми в таблице tablename;
В таблице должны присутствовать поле <login_name> и <password_name>, задаваемые пользователем.
Для работы с БД используется служебный фреймворк WSQLuse (sqlhsell).
Так же передается словарь (conn_dict), в котором ключем является подключение к сокету (connection) а значением
еще один словарь с разными парами ключ-значение, в частности, ключ auth, принимающий True или False и отвечающий
на вопрос, аутентифицирован пользователь или нет. """
import hashlib


def auth_user(sqlshell, login, password, connection, users_table_name='users', user_name_column='username'):
    response = auth_user_from_db(sqlshell, users_table_name, user_name_column, login, password)
    response = check_if_auth_succes(response)
    if type(response) == int:
        ip = connection.getpeername()[0]
        user_id = save_conn_ip(sqlshell, users_table_name, user_name_column, login, ip)['info'][0][0]
        return user_id, True
    else:
        return 'Wrong password or login!', False


def set_disconnect_status(sqlshell, users_tablename, ip):
    command = "UPDATE {} set connected=False where last_ip='{}'".format(users_tablename, ip)
    sqlshell.try_execute(command)


def save_conn_ip(sqlshell, tablename, login_name, login, ip):
    command = "UPDATE {} SET last_ip='{}', connected=True".format(tablename, ip)
    command += " where {}='{}'".format(login_name, login)
    user_id = sqlshell.try_execute(command)
    print('user_id', user_id)
    return user_id


def check_if_auth_succes(response):
    # Проверяет прошла аутентификация юзера в БД успешно
    if len(response) == 0 or response[0][0] is None:
        return False
    else:
        response = response[0][0]
        return response


def auth_user_from_db(sqlshell, tablename, login_name, login, password):
    # Аутентификация юзера, путем проверки в БД (через sqlshell) наличие логина (login) и совпадающего
    # пароля (password)
    command = "SELECT id ".format(password)
    command += "FROM {} ".format(tablename)
    command += "where {}='{}' and password=crypt('{}', password)".format(login_name, login, password)
    response = sqlshell.try_execute_get(command)
    return response
