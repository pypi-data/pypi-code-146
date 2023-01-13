from qsct.main import QSCT
from qpi import functions
from qpi import my_exceptions
from qpi.auth import auth_module
from qpi.super_methods import super_methods_description
import threading
from time import sleep
from traceback import format_exc
from _thread import allocate_lock


class QPI(QSCT):
    """" Серверное API, создается на передаеваемом my_ip, my_port и ждет клиентов. Клиентов обрабатывает в
    ассинхронном режиме. От клиентов ожидает данные вида:
        {'какая-то команда':{'какие то доп.ключи: 'какие то доп.значения'}
    Однако, он эти команды не исполняет, пока клиент не пройдет авторизацию (если только сервер не работает
    в режиме without_auth=True, тогда сервер выполняет команды клиента без аутентификации и авторизации.
    Для проведения авторизации необходим модуль wsqluse, который является фреймворком для работы с БД.
    core - экземпляр программы, к которой прикручен этот QPI.
    mark_disconnect - если True, отметить информацию об отключении клиента.
    assync_operating - принимать и выполнять команды клиентов ассинхронно.
    users_table_name - имя таблицы, в котором хранятся все данные о юзерах API.
    user_column_name - имя поля в таблице users_table_name, которое отвечает за
    идентификатор пользователя"""

    def __init__(self, my_ip, my_port, core=None,
                 without_auth=False,
                 mark_disconnect=True,
                 debug=False,
                 sql_shell=None,
                 assync_operating=True,
                 users_table_name=None,
                 user_column_name=None, name="QPI",
                 auto_start=True):
        super().__init__(debug=debug)
        self.assync_operating = assync_operating
        self.without_auth = without_auth
        self.mark_disconnect = mark_disconnect
        self.users_table_name = users_table_name
        self.user_column_name = user_column_name
        self.name = name
        self.server = functions.create_server(my_ip, my_port)
        self.connections_dict = {}
        self.sql_shell = sql_shell
        self.my_ip = my_ip
        self.my_port = my_port
        self.methods = super_methods_description.super_methods
        self.methods.update(functions.extract_core_support_methods(core))
        if not without_auth and not sql_shell:
            raise my_exceptions.NoSQLshellSupplied
        if auto_start:
            threading.Thread(target=self.launch_mainloop, args=()).start()

    def launch_mainloop(self):
        """Слушает сокет, получив подключение вызывает параллельную обработку каждого соеднинения"""
        print('\n[{}] Waiting for new connections on {}:{}'.format(self.name,
                                                                   self.my_ip,
                                                                   self.my_port))
        while True:
            conn, addr = self.server.accept()
            # Добавить соединение (в виде ключа словаря) в список self.connections, для дальнейшей работы
            # self.without_auth = по умолчанию False, если при создании экз. WServer передать значение True, то
            # парольная авторизация для клиентов WClient будет не затребована.
            self.connections_dict[conn] = {'auth': self.without_auth,
                                           'subscriber': False}
            print('\n[{}] Got a new connection! Dispatching...'.format(self.name))
            # Вывести обслуживание соединения в отдельный поток
            threading.Thread(target=self.dispatcher, args=(conn, )).start()

    def dispatcher(self, conn, *arg, **kwargs):
        """" Обслуживание подключния, получает соединение с клиентом (conn), а так-же словарь,
        вида {conn: {'some_key':'some_value'}}, где словарь-значение ключа conn - это ассоциативных массив,
        хранящий параметры и разную информацию о подключении (например, статус аутентификации).
        Вызывается параллельно основному потоку для достижения ассинхронности обрабатываемых подключений"""
        ip = conn.getpeername()[0]
        self.show_print('\nЕсть клиент. Ip:', ip, debug=True)
        while True:
            try:
                self.show_print('\tWaiting for commands from client...', debug=True)
                command = self.get_data(conn)
                if not command:
                    self.show_print('\t\tConnection was lost', debug=True)
                    conn.close()
                    self.connections_dict.pop(conn)
                    if self.mark_disconnect and self.sql_shell and self.users_table_name and self.user_column_name:
                        auth_module.set_disconnect_status(self.sql_shell, self.users_table_name, ip)
                    break
                self.show_print('\tПолучена команда:', command, debug=True)
                #sleep(1)
                # Для каждой команды от клиента так-же запускается по паралелльному потоку для выполнения ее
                #threading.Thread(target=self.command_execute_queue, args=(conn, command)).start()
                self.command_execute_queue(conn, command)
            except ConnectionResetError:
                self.show_print(format_exc())
                self.connections_dict.pop(conn)
                break

    def broadcast_sending(self, data, only_subscribers=True):
        """ Рассылает данные data по всем подключенным клиентам self.connections (список,содержащий словари,
        где ключом является connection (возвращаемый методом server.accept()), а значением - разная информация о
        соединении, не играющая роль в этом контексте """
        #zombie_connections = []         # Неактивные подключения
        for connection_key, connections_details in self.connections_dict.items():
            if (only_subscribers and connections_details['subscriber']) \
                    or not only_subscribers:
                #@try:
                threading.Thread(target=self.send_data, args=(connection_key, data)).start()
                print("AC", threading.active_count())
                #except BrokenPipeError:
                    # Если подключение не активно, добавить в список для удаления
                    # (сразу удалять во время перебора словаря нельзя)
                #    zombie_connections.append(connection_key)
                #except:
                #    zombie_connections.append(connection_key)
        # В новом цикле перебрать все неактивные подключения и удалить их
        #for zombie in zombie_connections:
        #    self.connections_dict.pop(zombie)

    def command_execute_queue(self, connection, command):
        """ Функция, синхронизирующая паралелльные потоки выполнения методов.
        (В одно время может выполняться только 1 метод (actA) от 1 клиента (clientA):
        если во время обработки метода actA (в это время статус self.status_ready - негативный),
        clientB отправит запрос на выполнение какой-либо команды actB, то actB не будет выполнена,
        пока не завершится выполнение actA, и флаг self.status_ready не станет позитивным."""
        while True:
            if self.assync_operating or self.status_ready:
                self.status_ready = False
                try:
                    response = self.operate_command(command, connection)
                    self.send_response(connection, response)
                    self.status_ready = True
                    break
                except:
                    self.status_ready = True
            else:
                print('Ожидание освобождения. Поток занят... ')
                sleep(0.2)

    def send_response(self, conn, response):
        """Отправить ответ клиенту по получению от него комманды"""
        print('\nSending response', response)
        self.send_data(conn, response)

    def operate_command(self, command, connection, *args, **kwargs):
        """ Выполнить операции над командой command от клиента connection """
        response = self.check_auth(command, connection)
        return response

    def check_auth(self, command, connection, *args, **kwargs):
        """ Выполняет передававемую команду и возвращает ответ"""
        if self.connections_dict[connection]['auth'] or command['method'] == 'auth_me':
            # Если подключение авторизованное (или сервер работает в режиме no_auth)
            response = self.execute_command(command['method'], command['data'], connection)  # Выполнить пользовательские команды
        else:
            response = {'status': False, 'info': "Вы должны сначала авторизоваться! Комманда {'auth_me': "
                                                 "{'login':..., 'password'=...}} "}
        return response

    def execute_command(self, comm, values, conn, *args, **kwargs):
        """ Основаня команда по выполнению команд от клиента.
        Получает:
        comm - команду, values - доп.инфо (в виде словаря). {'command': {'key1':'value1', 'key2':'value2'}};
        conn - соединение с клиентом."""
        functions.expand_kwargs(values, connections_dict=self.connections_dict, connection=conn,
                                users_table_name=self.users_table_name, user_name_column=self.user_column_name,
                                sql_shell=self.sql_shell, self_qpi=self, methods_dict=self.methods, command=comm,
                                qpi_name=self.name)
        try:
            method = self.methods[comm]['method']
        except KeyError:
            method = functions.no_method_operation
        response_dict = {}
        try:
            response = method(**values, **kwargs)
            response_dict['status'] = True
            response_dict['info'] = response
            response_dict['core_method'] = comm
        except:
            response_dict['status'] = False
            response_dict['info'] = format_exc()
        return response_dict

    def after_auth_execute(self, *args, **kwargs):
        """ Команды, которые должны быть выполнены после авторизации пользователя"""
        pass
