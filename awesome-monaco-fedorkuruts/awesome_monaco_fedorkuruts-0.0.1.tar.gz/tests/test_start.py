from unittest.mock import patch
from src import main


def replace_files(folder, file):
    from tests.case import start, end, abbreviations
    from awesome_monaco_FEDORKURUTS.brains.config import RACERS, START, END
    if file == RACERS:
        text = abbreviations.strip().split("\n")
        return text
    elif file == START:
        text = start.strip().split("\n")
        return text
    elif file == END:
        text = end.strip().split("\n")
        return text
    else:
        raise AttributeError


@patch('sys.argv',
       ['start.py', '--files', 'C:\\Users\\Asus\\PycharmProjects\\monaco\\storage', '--driver', 'Sergey Sirotkin'])
@patch('brains.build_data.read_file', replace_files)
def test_main_driver(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out.split("\n") == ['DNF | Sergey Sirotkin WILLIAMS MERCEDES | INVALID TIME',
                                        '_________________________________________________________________',
                                        '']



@patch('sys.argv',
       ['start.py', '--files', 'folder_of_storage', '--asc'])
@patch('brains.build_data.read_file', replace_files)
def test_main_asc(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out.split("\n") == ['1.  | Sebastian Vettel FERRARI                   | 0:01:04.415000',
                                        '2.  | Valtteri Bottas MERCEDES                   | 0:01:12.434000',
                                        '3.  | Stoffel Vandoorne MCLAREN RENAULT          | 0:01:12.463000',
                                        '4.  | Kimi R?ikk?nen FERRARI                     | 0:01:12.639000',
                                        '5.  | Fernando Alonso MCLAREN RENAULT            | 0:01:12.657000',
                                        '6.  | Charles Leclerc SAUBER FERRARI             | 0:01:12.829000',
                                        '7.  | Sergio Perez FORCE INDIA MERCEDES          | 0:01:12.848000',
                                        '8.  | Romain Grosjean HAAS FERRARI               | 0:01:12.930000',
                                        '9.  | Pierre Gasly SCUDERIA TORO ROSSO HONDA     | 0:01:12.941000',
                                        '10. | Carlos Sainz RENAULT                       | 0:01:12.950000',
                                        '_________________________________________________________________',
                                        '11. | Nico Hulkenberg RENAULT                    | 0:01:13.065000',
                                        '12. | Brendon Hartley SCUDERIA TORO ROSSO HONDA  | 0:01:13.179000',
                                        '13. | Marcus Ericsson SAUBER FERRARI             | 0:01:13.265000',
                                        '14. | Lance Stroll WILLIAMS MERCEDES             | 0:01:13.323000',
                                        '15. | Kevin Magnussen HAAS FERRARI               | 0:01:13.393000',
                                        'DNF | Lewis Hamilton MERCEDES                    | INVALID TIME',
                                        'DNF | Esteban Ocon FORCE INDIA MERCEDES          | INVALID TIME',
                                        'DNF | Sergey Sirotkin WILLIAMS MERCEDES          | INVALID TIME',
                                        'DNF | Daniel Ricciardo RED BULL RACING TAG HEUER | INVALID TIME',
                                        '']


@patch('sys.argv',
       ['start.py', '--files', 'folder_of_storage', '--desc'])
@patch('brains.build_data.read_file', replace_files)
def test_main_desc(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out.split("\n") == ['DNF | Daniel Ricciardo RED BULL RACING TAG HEUER | INVALID TIME',
                                        'DNF | Sergey Sirotkin WILLIAMS MERCEDES          | INVALID TIME',
                                        'DNF | Esteban Ocon FORCE INDIA MERCEDES          | INVALID TIME',
                                        'DNF | Lewis Hamilton MERCEDES                    | INVALID TIME',
                                        '15. | Kevin Magnussen HAAS FERRARI               | 0:01:13.393000',
                                        '14. | Lance Stroll WILLIAMS MERCEDES             | 0:01:13.323000',
                                        '13. | Marcus Ericsson SAUBER FERRARI             | 0:01:13.265000',
                                        '12. | Brendon Hartley SCUDERIA TORO ROSSO HONDA  | 0:01:13.179000',
                                        '11. | Nico Hulkenberg RENAULT                    | 0:01:13.065000',
                                        '_________________________________________________________________',
                                        '10. | Carlos Sainz RENAULT                       | 0:01:12.950000',
                                        '9.  | Pierre Gasly SCUDERIA TORO ROSSO HONDA     | 0:01:12.941000',
                                        '8.  | Romain Grosjean HAAS FERRARI               | 0:01:12.930000',
                                        '7.  | Sergio Perez FORCE INDIA MERCEDES          | 0:01:12.848000',
                                        '6.  | Charles Leclerc SAUBER FERRARI             | 0:01:12.829000',
                                        '5.  | Fernando Alonso MCLAREN RENAULT            | 0:01:12.657000',
                                        '4.  | Kimi R?ikk?nen FERRARI                     | 0:01:12.639000',
                                        '3.  | Stoffel Vandoorne MCLAREN RENAULT          | 0:01:12.463000',
                                        '2.  | Valtteri Bottas MERCEDES                   | 0:01:12.434000',
                                        '1.  | Sebastian Vettel FERRARI                   | 0:01:04.415000',
                                        '']


# @patch('sys.argv',
#        ['start.py', '--files', 'folder_of_storage'])
# @patch('brains.build_data.read_file', replace_files)
# def test_main_negative_(capsys):
#     main()
#     captured = capsys.readouterr()
#     assert captured.out.split("\n") == "d"