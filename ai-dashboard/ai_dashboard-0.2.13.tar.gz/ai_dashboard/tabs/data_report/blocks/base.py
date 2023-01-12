import io
import requests
import numpy as np


class BaseBlock:
    """
    blocks do not communicate with the report app directly, but instead return a dict
    """

    block = {}
    upload = False

    def __call__(self, report_client=None):
        self.postprocess(report_client)
        return self.block

    def postprocess(self, report_client=None):
        """
        code for postprocessing the block that involves the client, e.g. uploading images to the report app
        """
        pass

    def _paragraph(self, content, exclude_appblock=False):
        if exclude_appblock:
            return {
                "type": "paragraph",
                "content": self.preprocess_text_contents(content),
            }
        return {
            "type": "appBlock",
            # "attrs" : {"id": str(uuid.uuid4())},
            "content": [
                {"type": "paragraph", "content": self.preprocess_text_contents(content)}
            ],
        }

    def preprocess_text_contents(self, content):
        """for processing text contents"""
        if isinstance(content, str):
            # allows for simple text input into paragraph
            return [{"type": "text", "text": content}]
        elif isinstance(content, (float, int, np.generic)):
            return [{"type": "text", "text": str(content)}]
        elif isinstance(content, dict):
            if content["type"] == "text":
                return [content]
            else:
                raise TypeError(f"This only accepts 'text' type, not {content['type']}")
        elif isinstance(content, list):
            content_list = []
            for c in content:
                processed_c = self.preprocess_text_contents(c)
                if not isinstance(processed_c, list):
                    processed_c = [processed_c]
                content_list += processed_c
            return content_list
        elif callable(content):
            return self.preprocess_text_contents(content())
        else:
            print(type(content))
            return [content]

    def postprocess_blocks(self, blocks, report_client=None):
        if isinstance(blocks, list):
            processed_blocks = []
            for b in blocks:
                processed_b = self.postprocess_block(b, report_client=report_client)
                processed_blocks.append(processed_b)
            return processed_blocks
        else:
            raise TypeError("'blocks' has to be of type list.")

    def postprocess_block(self, block, report_client=None):
        if isinstance(block, str):
            # if we input just a string it needs to output a paragraph block
            return self._paragraph(block, exclude_appblock=True)
        elif isinstance(block, (float, int, np.generic)):
            # to convert all edge case types to paragraph block
            return self._paragraph(str(block), exclude_appblock=True)
        elif isinstance(block, dict):
            # this is necessary to nest blocks that are already dictionaries within layout blocks
            input_block = block
            if block["type"] == "appBlock":
                input_block = block["content"][0]
            return input_block
        elif callable(block):
            return self.postprocess_block(
                block(report_client=report_client), report_client=report_client
            )
        else:
            print("this type got through", type(block))
            return block

    def _get_content_bytes(self, content):
        if isinstance(content, str):
            if "http" in content and "/":
                # online image
                content_bytes = io.BytesIO(requests.get(content).content).getvalue()
            else:
                # local filepath
                content_bytes = io.BytesIO(open(content, "rb").read()).getvalue()
        elif isinstance(content, bytes):
            content_bytes = content
        elif isinstance(content, io.BytesIO):
            content_bytes = content.getvalue()
        else:
            raise TypeError("'content' needs to be of type str, bytes or io.BytesIO.")
        return content_bytes


class BaseMark(BaseBlock):
    def preprocess_mark(self, content, mark, nested=False):
        """
        test cases:
        ItalicMark("test")
        ItalicMark(UnderlinMark("test"))
        ItalicMark([UnderlinMark("test"), "test2])
        [ItalicMark("test), "test2"]
        """
        if isinstance(content, str):
            # just handles simple plain text
            output = {"type": "text", "text": content, "marks": mark}
            return output if nested else [output]
        elif isinstance(content, (float, int, np.generic)):
            output = {"type": "text", "text": str(content), "marks": mark}
            return output if nested else [output]
        elif isinstance(content, dict):
            # this should append mark to an existing mark
            if "marks" in content:
                content["marks"] += mark
            return content
        elif isinstance(content, list):
            # this should output a list of {text, (marks)}
            content_list = []
            for c in content:
                processed_c = self.preprocess_mark(c, mark, nested=True)
                if not isinstance(processed_c, list):
                    processed_c = [processed_c]
                content_list += processed_c
            return content_list
        elif "blocks.marks" in str(type(content)):
            # this should call/activate a Mark, this check is kind of inefficient
            return self.preprocess_mark(content(), mark, nested=nested)
        else:
            output = {"type": "text", "text": content, "marks": mark}
            return output if nested else [output]
