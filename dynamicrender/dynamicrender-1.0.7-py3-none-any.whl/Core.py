from dynamicadaptor.Message import RenderMessage
from PIL import Image
import asyncio

from .DynHeader import DynHeaderRender, DynFooterRender
from .DynText import DynTextRender
from .DynMajor import DynMajorRender
from .DynForward import DyForwardRender
from .DynAdditional import DynAdditionalRender
from .Tools import merge_pictures
from .DynConfig import ConfigInit, Optional, Union

class DyRender(ConfigInit):
    def __init__(self, data_path: Optional[str] = None, font_path: Union[None, str, dict] = None):
        super().__init__(data_path, font_path)

    async def dyn_render(self, message: RenderMessage) -> Image.Image:
        """the renderer's entry function

        Parameters
        ----------
        message : RenderMessage

        Returns
        -------
        Image.Image

        """
        head_task = DynHeaderRender(
            self.static_path, self.dyn_color, self.dyn_font, self.dy_size)
        tasks = [head_task.run(message.header)]
        if message.text is not None:
            text_task = DynTextRender(
                self.static_path, self.dyn_color, self.dyn_font, self.dy_size)
            tasks.append(text_task.run(message.text))
        if message.major is not None:
            major_task = DynMajorRender(
                self.static_path, self.dyn_color, self.dyn_font, self.dy_size)
            tasks.append(major_task.run(message.major))
        if message.forward is not None:
            forward_task = DyForwardRender(
                self.static_path, self.dyn_color, self.dyn_font, self.dy_size)
            tasks.append(forward_task.dyn_forward_render(message.forward))
        if message.additional is not None:
            additional_task = DynAdditionalRender(
                self.static_path, self.dyn_color, self.dyn_font, self.dy_size)
            tasks.append(additional_task.run(message.additional))
        footer_task = DynFooterRender(self.static_path, self.dyn_color, self.dyn_font, self.dy_size)
        tasks.append(footer_task.run(message.message_id))
        result = await asyncio.gather(*tasks)
        return await merge_pictures(result)
