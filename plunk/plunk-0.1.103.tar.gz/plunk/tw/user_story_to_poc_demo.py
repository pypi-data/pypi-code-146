import pytest
from http2py.client import HttpClient
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from streamlitfront.tests.common import select_func, send_input, compute_output
from time import sleep

DFLT_VAX = 0.8


def _factor(vax, vax_factor):
    return (
        # vax is proportion of vaxinated and vax_factor how much less
        # (compared to non-vax) a given probability would be for vaxinated):
        vax * vax_factor
        +
        # (1 - vax) is the proportion of non vaxinated folks and 1.0 means "no change"
        (1 - vax) * 1.0
    )


def r(exposed=6, infect_if_expose=1 / 5):
    return exposed * infect_if_expose


def infected(r=1.2, vax=0.8, infection_vax_factor=0.15):
    return r * _factor(vax, infection_vax_factor)


def die(
    infected, die_if_infected=0.05, vax=DFLT_VAX, death_vax_factor=0.05,
):
    return infected * die_if_infected * _factor(vax, death_vax_factor)


def death_toll(die, population=1e6):
    return int(die * population)


@pytest.mark.parametrize(
    'call_specs',
    [
        (
            [
                dict(
                    func=r,
                    inputs=dict(exposed=10, infect_if_expose=0.3,),
                    expected_result=3.0,
                ),
                dict(
                    func=infected,
                    inputs=dict(r=2, vax=0.5, infection_vax_factor=0.5),
                    expected_result=1.5,
                ),
                dict(
                    func=die,
                    inputs=dict(
                        infected=1.5,
                        die_if_infected=0.25,
                        vax=0.5,
                        death_vax_factor=0.25,
                    ),
                    expected_result=0.234375,
                ),
                dict(
                    func=death_toll,
                    inputs=dict(die=0.234375, population=2000000,),
                    expected_result=468750.0,
                ),
            ]
        )
    ],
)
def test_published_app(call_specs, surface='ui'):
    def parse_spec(spec):
        return (
            spec['func'],
            spec['inputs'],
            spec['expected_result'],
        )

    def test_api():
        print(f'Validating the API...')
        api = HttpClient(url='https://extrudeploy-api.herokuapp.com/openapi')
        for spec in call_specs:
            func, inputs, expected_result = parse_spec(spec)
            endpoint = getattr(api, func.__name__)
            api_result = endpoint(**inputs)
            print(f'Asserting that {api_result=} == {expected_result=}')
            assert api_result == expected_result
            sleep(1)
        print(f'All good with the API!')
        sleep(1)

    def test_ui():
        print(f'Validating the UI...')

        def call_ui(idx, func, inputs):
            select_func(idx, dom)
            for idx, value in enumerate(inputs.values()):
                send_input(value, idx, dom)
                sleep(1)
            return compute_output(func, dom)

        options = ChromeOptions()
        options.add_argument('--window-size=1920,1080')
        dom = Chrome(ChromeDriverManager().install(), options=options)
        dom.get('https://extrudeploy.herokuapp.com')
        try:
            for idx, spec in enumerate(call_specs):
                func, inputs, expected_result = parse_spec(spec)
                ui_result = call_ui(idx, func, inputs)
                print(f'Asserting that {ui_result=} == {expected_result=}')
                assert float(ui_result) == expected_result
                # assert ui_result == expected_result
            print(f'All good with the UI!')
            sleep(1)
        finally:
            dom.close()

    if surface == 'ui':
        test_ui()
    elif surface:
        test_api()
