from src.cli_report.report import main
from unittest.mock import patch, mock_open

start_log = ('SVF2018-05-24_12:02:58.917\n'
             'VBM2018-05-24_12:00:00.000')
end_log = ('VBM2018-05-24_12:01:12.434\n'
           'SVF2018-05-24_12:04:03.332')
abbreviations_txt = ('SVF_Sebastian Vettel_FERRARI\n'
                     'VBM_Valtteri Bottas_MERCEDES')


def test_mock_open_file():
    with patch("builtins.open", mock_open(read_data=start_log)) as mock_file:
        assert open('start.log').readlines() == ['SVF2018-05-24_12:02:58.917\n', 'VBM2018-05-24_12:00:00.000']
        mock_file.assert_called_once_with('start.log')
    with patch("builtins.open", mock_open(read_data=end_log)) as mock_file:
        assert open('end.log').readlines() == ['VBM2018-05-24_12:01:12.434\n', 'SVF2018-05-24_12:04:03.332']
        mock_file.assert_called_once_with('end.log')
    with patch("builtins.open", mock_open(read_data=abbreviations_txt)) as mock_file:
        assert open('abbreviations.txt').readlines() == ['SVF_Sebastian Vettel_FERRARI\n',
                                                         'VBM_Valtteri Bottas_MERCEDES']
        mock_file.assert_called_once_with('abbreviations.txt')


def test_main_function(tmpdir, capsys):
    start_log_path = tmpdir.join("start.log")
    start_log_path.write(start_log)
    end_log_path = tmpdir.join("end.log")
    end_log_path.write(end_log)
    abbreviations_txt_path = tmpdir.join("abbreviations.txt")
    abbreviations_txt_path.write(abbreviations_txt)
    assert start_log_path.read() == start_log
    assert end_log_path.read() == end_log
    assert abbreviations_txt_path.read() == abbreviations_txt
    folder_path = str(tmpdir)
    with patch("sys.argv", ['main', '--files', folder_path]):
        main()
    captured = capsys.readouterr()
    assert captured.out == ("Sebastian Vettel     | FERRARI                   | 1:04.415\n"
                            "Valtteri Bottas      | MERCEDES                  | 1:12.434\n")
    with patch("sys.argv", ['main', '--files', folder_path, '--desc']):
        main()
    captured = capsys.readouterr()
    assert captured.out == ("Valtteri Bottas      | MERCEDES                  | 1:12.434\n"
                            "Sebastian Vettel     | FERRARI                   | 1:04.415\n")
    with patch("sys.argv", ['main', '--files', folder_path, '--driver', 'Valtteri Bottas']):
        main()
    captured = capsys.readouterr()
    assert captured.out == "Valtteri Bottas      | MERCEDES                  | 1:12.434\n"


if __name__ == '__main__':
    main()

