import csv
import logging
from typing import Iterable, List, Optional, Generator

from pathlib import Path
from sylk_parser import SylkParser
from pyramid.request import Request
from endi_base.utils import date as date_utils
from endi_base.utils.math import convert_to_float

from endi_celery.interfaces import IAccountingFileParser
from endi_celery.parsers import BaseParser, BaseProducer, OperationData

logger = logging.getLogger(__name__)


class SlkFileParser(BaseParser):
    def stream(self) -> Generator[list, None, None]:
        for line in SylkParser(str(self.file_path)):
            yield line


class CsvFileParser(BaseParser):
    encoding = "utf-8"

    def stream(self) -> Generator[list, None, None]:
        with open(self.file_path, encoding=self.encoding) as fbuf:
            dialect = csv.Sniffer().sniff(fbuf.read())
            fbuf.seek(0)
            for line in csv.reader(fbuf, dialect):
                yield line


class OperationProducer(BaseProducer):
    def _get_num_val(self, line: List[str], index: int) -> float:
        result = 0
        if len(line) > index:
            result = line[index].strip() or 0
        return convert_to_float(result)

    def _get_label(self, line: List[str]) -> str:
        label = line[5].strip()
        label = label[:80]
        return label

    def _stream_operation(self, line) -> Optional[OperationData]:
        result = None
        if len(line) >= 6:
            if line[0].strip() not in (
                "Compte analytique de l'entrepreneur",
                "Numéro analytique",
            ):
                analytical_account = line[0].strip()
                general_account = line[1].strip()
                date = date_utils.str_to_date(line[2].strip()).date()
                if not date:
                    logger.error("This line has incorrect datas : %s" % line)
                    return None

                label = self._get_label(line)
                debit = self._get_num_val(line, index=6)
                credit = self._get_num_val(line, index=7)
                balance = 0
                result = OperationData(
                    analytical_account=analytical_account,
                    general_account=general_account,
                    date=date,
                    label=label,
                    debit=debit,
                    credit=credit,
                    balance=balance,
                )
        return result

    def stream_operations(self) -> Iterable[OperationData]:
        for line in self.parser.stream():
            data = self._stream_operation(line)
            if data is not None:
                yield data


def parser_factory(context: Path, request: Request):
    if context.suffix == ".slk":
        return SlkFileParser(context)
    elif context.suffix == ".csv":
        return CsvFileParser(context)


def producer_factory(context: IAccountingFileParser, request: Request):
    return OperationProducer(context)
