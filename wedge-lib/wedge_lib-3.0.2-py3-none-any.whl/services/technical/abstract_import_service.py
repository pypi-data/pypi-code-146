from abc import abstractmethod

from django.conf import settings
from w.services.abstract_service import AbstractService
from w.services.imports.models.import_report import ImportReport, ImportRowError
from w.services.technical.csv_service import CsvService
from w.services.technical.excel_service import ExcelService
from w.services.technical.filesystem_service import FilesystemService
from w.services.technical.models.csv_options import CsvOptions


class AbstractImportService(AbstractService):
    sheet_name = None
    _filename = None
    _context = None

    @classmethod
    def import_file(cls, filename, context=None, delimiter=",") -> ImportReport:
        """
        Import filename

        Args:
            filename(str): csv or excel file
            context(dict): context to use for subsequent methods
            delimiter(str): if csv delimiter different from comma

        Returns:
            Tuple[list, ImportReport]
        """
        FilesystemService.check_file_exists(filename)
        cls._filename = filename
        cls._context = context
        data = cls._load_data(filename, cls._list_mapping_columns(), delimiter)
        return cls.import_data(data)

    @classmethod
    def import_data(cls, data) -> ImportReport:
        """
        Import data

        Args:
            data(list): data to import

        Returns:
            Tuple[list, ImportReport]: validation_errors, import_report
        """
        validated_datas, validation_errors = cls._validate(data)
        cls._import(validated_datas)
        return cls._get_import_report(validation_errors)

    @classmethod
    def _get_import_report(cls, validation_errors) -> ImportReport:
        """
        Get import report

        Args:
            validation_errors:

        Returns:
            ImportReport
        """
        report = ImportReport(nb_total=len(validation_errors))
        mapping = cls._list_mapping_attributes()
        for idx, error in enumerate(validation_errors):
            if error:
                report.nb_ignored += 1
                report.nb_errors += len(error.keys())
                report.errors.append(
                    ImportRowError(
                        num_row=idx + 1,
                        errors=[
                            f"{mapping[attr]}: {msg[0]}" for attr, msg in error.items()
                        ],
                    )
                )
            else:
                report.nb_imported += 1
        return report

    @staticmethod
    def get_example_dir(relative=True):
        """get import example directory"""
        example_dir = "core/media/imports/examples"
        if relative:
            return example_dir
        return f"{settings.ROOT_DIR}/{example_dir}"

    @classmethod
    def _load_data(cls, filename, mapping_columns, delimiter):
        """
        Load data from csv or excel file
        Args:
            filename(str): csv or excel file

        Returns:
            list

        Raises:
            RuntimeError:
        """
        filename = FilesystemService.get_path(filename)
        if CsvService.is_csv(filename):
            options = CsvOptions(mapping_columns, delimiter)
            return CsvService.load(filename, options)
        if ExcelService.is_excel(filename):
            return ExcelService.load(filename, mapping_columns, cls.sheet_name)
        raise RuntimeError(f"Format {filename.name} not supported")

    @classmethod
    def _list_mapping_attributes(cls) -> dict:
        """
        List mapping from attributes to csv/excel columns

        Returns:
            dict: {<import header label>: <wanted attribut>, ...}
        """
        return {v: k for k, v in cls._list_mapping_columns().items()}

    @classmethod
    @abstractmethod
    def _list_mapping_columns(cls) -> dict:
        """
        List mapping columns from csv/excel to wanted attributes

        Returns:
            dict: {<import header label>: <wanted attribut>, ...}
        """
        pass

    @classmethod
    @abstractmethod
    def _validate(cls, data) -> tuple:
        """
        Validate data

        Args:
            data(list): data to validate

        Returns:
            tuple: validated_data, validation_errors
        """
        pass

    @classmethod
    @abstractmethod
    def _import(cls, data) -> None:
        """
        Import data

        Args:
            data([dict]): datas to  import

        Returns:
            None
        """
        pass
