import time
from dataclasses import dataclass

from .interfaces.deserializer import Deserializer
from .interfaces.inputter import Inputter
from .interfaces.outputter import Outputter
from .interfaces.processor import Processor
from .interfaces.serializer import Serializer


@dataclass
class Task:
    name: str
    inputter: Inputter
    processor: Processor
    outputter: Outputter
    deserializer: Deserializer
    serializer: Serializer

    def do(self) -> None:
        context = self.inputter.read()
        deserialized_body = self.deserializer.deserialize(context.body)

        for result in self.processor.process(
            deserialized_body, context=context
        ):
            job_name = self.name
            class_name = self.processor.__class__.__name__
            metadatakey = f"processed_time_{job_name}_{class_name}"
            timestamp = int(time.time())
            context.add_metadata(**{metadatakey: timestamp})

            serialized_result = self.serializer.serialize(result)
            self.outputter.write(serialized_result, context=context)

        self.inputter.done()
