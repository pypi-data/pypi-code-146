from dynamicadaptor.Repost import Forward
from PIL import Image
import  asyncio
from .DynAdditional import DynAdditionalRender
from .DynConfig import DynColor, DynFontPath, DynSize
from .DynHeader import DynForwardHeaderRender
from .DynMajor import DynMajorRender
from .DynText import DynTextRender
from .Tools import merge_pictures


class DyForwardRender:
    def __init__(self, static_path: str, dyn_color: DynColor, dyn_font_path: DynFontPath, dyn_size: DynSize):
        self.static_path: str = static_path
        self.dyn_color: DynColor = dyn_color
        self.dyn_font: DynFontPath = dyn_font_path
        self.dyn_size: DynSize = dyn_size

    async def dyn_forward_render(self, message: Forward) -> Image.Image:
        """the renderer's entry function

        Parameters
        ----------
        message : Forward

        Returns
        -------
        Image.Image
            
        """
        head_task = DynForwardHeaderRender(self.static_path, self.dyn_color, self.dyn_font, self.dyn_size)
        tasks = [head_task.run(message.header)]
        if message.text is not None:
            text_task = DynTextRender(self.static_path, self.dyn_color, self.dyn_font, self.dyn_size)
            tasks.append(text_task.run(message.text, "F"))
        if message.major is not None:
            major_task = DynMajorRender(self.static_path, self.dyn_color, self.dyn_font, self.dyn_size)
            tasks.append(major_task.run(message.major, "F"))
        if message.additional is not None:
            additional_task = DynAdditionalRender(self.static_path, self.dyn_color, self.dyn_font, self.dyn_size)
            tasks.append(additional_task.run(message.additional, "F"))
        result = await asyncio.gather(*tasks)
        return await merge_pictures(result)
