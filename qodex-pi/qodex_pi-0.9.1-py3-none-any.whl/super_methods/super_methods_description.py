""" Содержит супер-методы, - методы, которые являются общими для всех наследников QPI """
from qpi.super_methods import operations


super_methods = {
    'subscribe':
        {'args': (),
         'kwargs': {},
         'description': 'Подписаться на обновления состояния QPI',
         'method': operations.set_connection_subscribe,
         'active': True},
    'unsubscribe':
        {'args': (),
         'kwargs': {},
         'description': 'Отписаться от обновлений состояния QPI',
         'method': operations.set_connection_unsubscribe,
         'active': True},
    'get_methods':
        {'args': (),
         'kwargs': {},
         'description': 'Получить все поддреживаемые методы QPI (супер-методы и методы ядра)',
         'method': operations.get_methods,
         'active': True},
    'hello_world':
        {'args': (),
         'kwargs': {},
         'description': 'Тестовый метод, в случае успешного выполнения, отправляет в ответ "Hello you too!"',
         'method': operations.get_hello_answer,
         'active': True},
    'auth_me':
        {'args': (),
         'kwargs': {},
         'description': 'Метод авторизации клиента на доступ к остальным методам',
         'method': operations.auth_me,
         'active': True},

}
