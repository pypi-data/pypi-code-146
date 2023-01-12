import klsframe.cli.cli as cli


def test_prompt_form_simple():
    form = cli.PromptForm(title='Test 1', desc='Just a test. Or not. I don\'t care')
    form.add_field('nombre', nullable=False)
    form.add_field('apellidos', nullable=False)
    res = form.fill_in()
    print(res)
    assert res == form.last_result
    assert 'nombre' in res and 'apellidos' in res
    print('[OK] Test prompt_form_simple_test succeeded\n\n')


def test_prompt_form_advanced():
    form = cli.PromptForm(title='Test 2', desc='Just a test. Or not. I don\'t care')
    form.add_string_field(name='Nombre', description='Nombre del titular de la cuenta', example='Pedro')
    form.add_string_field(name='Apellidos', description='Apellidos del titular de la cuenta', example='Pérez')
    form.add_numeric_field(name='Edad', description='Edad en años del titular de la cuenta', example='12',
                           decimal_digits=0, min_val=1, max_val=99)
    form.add_list_field(name='hobbies', description="Top-3 hobbies", max_size=3)
    form.add_list_field(name='fav num', description='Top-3 Favorite numbers', ltype='number', allow_repeated=False,
                        fixed_size=3)
    # form.show_info()
    res = form.fill_in(compact_mode=True, confirm=True)
    print(res)
    assert res == form.last_result
    print('[OK] Test prompt_form_advanced_test succeeded\n\n')


def test_confirm():
    print(cli.confirm_yes_no("Delete all assets", default=False, allow_empty=False, shortened=False))
    print(cli.confirm_yes_no("Exit", default=True, allow_empty=True, shortened=True))
    print(cli.confirm_yes_no("Eres tonoto?"))


def test_safe_input():
    age1 = input("Age")
    age2 = cli.safe_string_input("Age", )


def test_menu_1():
    def cagar():
        print('prffrfffrf')

    def comer():
        print('ñamñam')

    def dormir():
        print('zZzzZZZzZzzZZz')

    men = cli.Menu(allowcustom=True)
    men.add_entry('cagar', 'Ir al trono', cagar)
    men.add_entry('comer', 'Monchear', comer)
    men.add_entry('dormir', 'Sobarla', dormir)
    print(men.open())


def test_menu_2():
    dict_port_listing = {"Por defecto (no se especifican puertos)": "",
                         "Todos los puertos": "-p-",
                         "1000 puertos comunes": "--top-ports 1000"}
    menu1 = cli.Menu(allowcustom=True)
    menu1.add_entries(dict_port_listing)
    print(menu1.open())


def test_menu_3():
    menu_options1 = [
        {'value': '', 'description': 'Por defecto (no se especifican puertos)'},
        {'value': '-p-', 'description': 'Todos los puertos'},
        {'value': '--top-ports 1000', 'description': '1000 puertos comunes'}
    ]

    def input_port():
        prompt = f"Introduce tu propia seleccion de puertos, separados por espacio (23 80 443) o un rango (0-1024)"
        range_regex = '^[0-9]{1,5}-[0-9]{1,5}$'
        listing_regex = '^(([0-9]{1,5})+[ ]?)+$'
        return cli.safe_string_input(validations=[range_regex, listing_regex], allow_empty=False, prompt=prompt)

    menu2 = cli.Menu(allowcustom=True, customprompt=input_port)
    menu2.add_entries(menu_options1)
    print(menu2.open())


def test_menu_4():
    data = ["Por defecto (no se especifican puertos)", "Todos los puertos", "1000 puertos comunes"]
    menu1 = cli.Menu(title='Test 4', desc='Just a dummy test. [Implicit options: (-T3, -vvv)]', allowcustom=True)
    menu1.add_entries(data)
    print(menu1.open(verbose=True))


def test_menu_5():
    data = [{'tipo': 'tcp', 'desc': 'TCP SYN scan top ports', 'params': '-Pn -n -sS --stats-every 15s'},
            {'tipo': 'tcp', 'desc': 'TCP SYN scan ALL ports', 'params': '-p- -Pn -n -sS --stats-every 15s'}]
    menu1 = cli.Menu(title='Test 4', desc='Just a dummy test. [Implicit options: (-T3, -vvv)]', allowcustom=True)
    menu1.add_entries(data)
    print(menu1.open(verbose=True))


def test_safe_list_input_1():
    print(cli.safe_list_input(sep='new-line', max_size=5, fixed_size=3, ltype='number', allow_repeated=False,
                              prompt='Dime 3 numeros del 1 al 10', min_val=1, max_val=10))


def test_continue_or_exit():
    print("hola?")
    cli.continue_or_exit()
    print("adios!")


if __name__ == '__main__':
    # test_confirm()
    # test_prompt_form_simple()
    # test_prompt_form_advanced()
    # test_dict_to_table()
    # pyautogui.prompt(text="Apellido", title="field 1/3", default="mondongo")
    print(test_menu_5())
