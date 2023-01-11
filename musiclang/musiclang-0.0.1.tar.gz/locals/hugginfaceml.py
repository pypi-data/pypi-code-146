
from pathlib import Path


TOKENIZE = True
TRAIN = False
PREDICT = True

vocab_size = 200
paths = [str(x) for x in Path("locals/dataset_score/").glob("**/*.txt")]

# Clean all files in path
import os
for file in paths:
    os.makedirs('locals/dataset_score_clean', exist_ok=True)
    with open(file, 'r') as f:
        data = f.read()
        data = data.replace('\n', '')
        data = data.replace(' ', '')
        data = data.replace('\t', '')

    with open(os.path.join('locals/dataset_score_clean', file.split('/')[-1]), 'w') as f:
        f.write(data)




paths = [str(x) for x in Path("locals/dataset_score_clean/").glob("**/*.txt")]


if TOKENIZE:
    from tokenizers import ByteLevelBPETokenizer

    # Initialize a tokenizer
    tokenizer = ByteLevelBPETokenizer()
    # Customize training
    tokenizer.train(files=paths, vocab_size=vocab_size, min_frequency=2, special_tokens=[
        "<s>",
        "</s>",
        "<unk>",
        "<mask>",
    ])

    # Save files to disk
    tokenizer.save_model("./locals/huggin")

if TRAIN:
    from tokenizers.implementations import ByteLevelBPETokenizer
    from tokenizers.processors import BertProcessing


    # Encoding(num_tokens=7, ...)
    # tokens: ['<s>', 'Mi', 'Ġestas', 'ĠJuli', 'en', '.', '</s>']

    from torch.utils.data import Dataset
    import torch

    class MusicLangDataset(Dataset):
        def __init__(self, evaluate: bool = False):
            tokenizer = ByteLevelBPETokenizer(
                "./locals/huggin/vocab.json",
                "./locals/huggin/merges.txt",
            )
            tokenizer._tokenizer.post_processor = BertProcessing(
                ("</s>", tokenizer.token_to_id("</s>")),
                ("<s>", tokenizer.token_to_id("<s>")),
            )
            tokenizer.enable_truncation(max_length=512)
            # or use the RobertaTokenizer from `transformers` directly.

            self.examples = []

            src_files = Path("./locals/dataset_score_clean/").glob("*.txt") if evaluate else Path("./locals/dataset_score_clean/").glob("*.txt")
            for src_file in src_files:
                print("🔥", src_file)
                lines = [src_file.read_text(encoding="utf-8")]
                self.examples += [x.ids for x in tokenizer.encode_batch(lines)]

        def __len__(self):
            return len(self.examples)

        def __getitem__(self, i):
            # We’ll pad at the batch level.
            return torch.tensor(self.examples[i])

    from transformers import RobertaConfig

    config = RobertaConfig(
        vocab_size=vocab_size,
        max_position_embeddings=514,
        num_attention_heads=12,
        num_hidden_layers=6,
        type_vocab_size=1,
    )

    from transformers import RobertaTokenizerFast

    tokenizer = RobertaTokenizerFast.from_pretrained("locals/huggin", max_len=512)

    # As we are training from scratch, we only initialize from a config, not from an existing pretrained model or checkpoint.
    from transformers import RobertaForMaskedLM

    model = RobertaForMaskedLM(config=config)

    model.num_parameters()

    dataset = MusicLangDataset()

    """
    Like in the run_language_modeling.py script, we need to define a data_collator.
    
    This is just a small helper that will help us batch different samples of the dataset together into an object that PyTorch knows how to perform backprop on.
    
    """
    from transformers import DataCollatorForLanguageModeling

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm=True, mlm_probability=0.15
    )

    from transformers import Trainer, TrainingArguments

    training_args = TrainingArguments(
        output_dir="./locals/musiclang",
        overwrite_output_dir=True,
        num_train_epochs=30,
        per_gpu_train_batch_size=64,
        save_steps=10,
        save_total_limit=2,
        prediction_loss_only=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )

    trainer.train()
    trainer.save_model("./locals/ml_musiclang")



if PREDICT:
    from transformers import pipeline

    fill_mask = pipeline(
        "fill-mask",
        model="./locals/ml_musiclang",
        tokenizer="./locals/huggin"
    )

    result = fill_mask("(I%I.<mask>")
    print(result)