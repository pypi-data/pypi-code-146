from ..constants import (
    ConstantInputter,
    NullDeserializer,
    NullProcessor,
    NullSerializer,
)
from ..crawler import HTTPCrawler
from ..file import FileInputter
from ..gzip import GzipDeserializer, GzipSerializer
from ..json import JSONDeserializer, JSONSerializer
from ..python import PythonProcessor
from ..scraper import (
    CSSSelectorScraper,
    MixedHTMLScraper,
    SingleXPathScraper,
    XPathScraper,
)
from ..sql import SQLInputter, SQLOutputter
from ..sqs_s3 import SQSS3Inputter, SQSS3Outputter
from ..stdio import StdinInputter, StdoutOutputter
from .searcher import DirectiveSearcher

DefaultSearcher = DirectiveSearcher.create()

DefaultSearcher.add_inputter(ConstantInputter)
DefaultSearcher.add_inputter(StdinInputter)
DefaultSearcher.add_inputter(FileInputter)
DefaultSearcher.add_inputter(SQSS3Inputter)
DefaultSearcher.add_inputter(SQLInputter)

DefaultSearcher.add_processor(HTTPCrawler)
DefaultSearcher.add_processor(XPathScraper)
DefaultSearcher.add_processor(SingleXPathScraper)
DefaultSearcher.add_processor(MixedHTMLScraper)
DefaultSearcher.add_processor(CSSSelectorScraper)
DefaultSearcher.add_processor(NullProcessor)
DefaultSearcher.add_processor(PythonProcessor)

DefaultSearcher.add_serializer(GzipSerializer)
DefaultSearcher.add_serializer(NullSerializer)
DefaultSearcher.add_serializer(JSONSerializer)

DefaultSearcher.add_outputter(StdoutOutputter)
DefaultSearcher.add_outputter(SQSS3Outputter)
DefaultSearcher.add_outputter(SQLOutputter)

DefaultSearcher.add_deserializer(GzipDeserializer)
DefaultSearcher.add_deserializer(NullDeserializer)
DefaultSearcher.add_deserializer(JSONDeserializer)
