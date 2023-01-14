import yaml
from tensorflow import keras

from vqa.src import root_dir
from vqa.src.image_extraction import ImageExtraction
from vqa.src.question_extraction import QuestionExtraction
from vqa.src.transformer import TransformerModel, TransformerDecoderBlock, TransformerEncoderBlock

class Model():
    def __init__(self) -> None:
        self.ROOT_dir = root_dir.find_ROOT_dir()
        self.config  = yaml.load(open(f"{self.ROOT_dir}/storage/config.yml"), Loader = yaml.loader.SafeLoader)
        
        self.image_extraction = ImageExtraction()
        self.question_extraction = QuestionExtraction()
        self.encoder = TransformerEncoderBlock(embed_dim=self.config["EMBED_DIM"], dense_dim=self.config["FF_DIM"], num_heads=6)
        self.decoder = TransformerDecoderBlock(embed_dim=self.config["EMBED_DIM"], ff_dim=self.config["FF_DIM"], num_heads=6)
        self.transformer_model = TransformerModel(encoder=self.encoder, decoder=self.decoder)
        
    def compile(self):
        cross_entropy = keras.losses.SparseCategoricalCrossentropy(
            from_logits=False, reduction="none"
        )
        self.transformer_model.compile(optimizer=keras.optimizers.legacy.Adam(0.0001), loss=cross_entropy)

    def load(self):
        self.transformer_model.load_weights(f"{self.ROOT_dir}/storage/best.ckpt")
