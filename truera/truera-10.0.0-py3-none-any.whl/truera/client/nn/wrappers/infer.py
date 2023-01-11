"""
Helpers for inferring wrapper parameters. Putting all of the logic here so that
the dispatch in quick.py does not grow too big.
"""

from inspect import BoundArguments
from inspect import Parameter
from inspect import Signature
import random
import re
import sys
from typing import Any, Dict, Iterable

import torch

from truera.client.nn.wrappers.torch import Torch
from truera.client.util.func_utils import overload
from truera.client.util.func_utils import retab
from truera.client.util.func_utils import Undispatch
from truera.client.util.python_utils import caller_frame
from truera.client.util.python_utils import copy_bindings
from truera.client.util.python_utils import import_optional
from truera.client.util.type_utils import annotation_isinstance
from truera.client.util.type_utils import eval_type
from truera.client.util.type_utils import Exemplified
from truera.client.util.type_utils import Intersection
from truera.client.util.type_utils import Not
from truera.client.util.type_utils import Optional
from truera.client.util.type_utils import RegexTypeMatch
from truera.client.util.type_utils import Union

# TODO(piotrm): wrapping issues with some huggingface models:
# model loading problems
#   - layoutlm-base-uncased
# audio models
#   - anything with Wav2Vec2
# "not a string" error ???
#   - google/reformer-enwik8
# non-fast tokenizer gets loaded even if fast is available
#   - many examples, see quick_test_results.ipynb
# "object of type 'NoneType' has no len()"
#   - google.tapas-* models

trulens_nn_models = import_optional(
    "trulens.nn.models", "neural networks explanations"
)

transformers = import_optional("transformers", "huggingface model wrapping")

TTorchModel = 'torch.nn.Module'
TTF2Model = 'keras.engine.training.Model'

# pytorch models, tensorflow 2 models
TModel = Union(TTorchModel, TTF2Model)


def Hugs(typ: type) -> type:
    return Exemplified(base_module="transformers.models", type=typ)


# Huggingface (text?) tokenizers
THugsTokenizer = Hugs(
    Union(
        'transformers.PreTrainedTokenizer',
        'transformers.PreTrainedTokenizerFast'
    )
)

# Huggingface sequence classifiers
THugsClassifier = Hugs(
    Intersection(
        TModel,
        RegexTypeMatch(
            name="hugs_sequence_classifier",
            pattern="transformers\..+ForSequenceClassification"
        )
    )
)

# Huggingface audio sequence classifiers
THugsAudioClassifier = Hugs(
    Intersection(
        THugsClassifier,
        RegexTypeMatch(
            name="hugs_audio_sequence_classifier",
            pattern=
            "transformers\..+(UniSpeech|Audio|WavLM|Wav2Vec2).*ForSequenceClassification"
        )
    )
)

# Huggingface text sequence classifiers
THugsTextClassifier = Hugs(
    Intersection(THugsClassifier, Not(THugsAudioClassifier))
)

# Huggingface text classifiers in the pytorch api
TTorchHugsTextClassifier = Hugs(Intersection(TTorchModel, THugsTextClassifier))

# Huggingface text classifiers in the tensorflow api
TTFHugsTextClassifier = Hugs(Intersection(TTF2Model, THugsTextClassifier))


class Inferred(Optional):
    """
    Optional arguments designated to be inferred. This distinguishes arguments
    that will need to be inferred from those that can remain as their default
    value. If an optional value cannot be inferred, that is a warning. But if an
    `Inferred` value cannot be inferred, that is an error.
    """

    pass


class InferException(Exception):
    pass


def infer_defaults(config_factory, overloads_static=False):
    """
    Create a post-bind handler method for overload that infers `Inferred`
    arguments that have their default value. Config factory is needed to lookup
    the cache object from the bindings that the caller setting up the handler
    expects.

    If overload_static is True, the produced handler expects to be processing
    bindings of static methods (or "functions") that do not get "self".
    Otherwise pre-self-bound bindings are expected and self is removed from them
    before inferring methods are called.
    """

    # Caller's globals are required if __future__.annotation is enabled to be
    # able to evaluate names to types.
    _globals = caller_frame().f_globals

    def handler(sig: Signature, bindings: BoundArguments) -> BoundArguments:
        infer_bindings = copy_bindings(bindings)
        infer_bindings.apply_defaults()

        # Get the Infer object with the given cache.
        inf = Infer(config_factory(infer_bindings))

        # Self is bound to something that the infer methods do not expect, get
        # rid of it before calling infer method.
        if not overloads_static:
            del infer_bindings.arguments['self']

        # Will collect the required and inferrable arguments from the bindings.
        required_args = {}
        to_infer_args = {}

        # For each argument,
        for name, val in infer_bindings.arguments.items():
            param = sig.parameters[name]
            annot = param.annotation
            kind = param.kind

            # Determine whether the argument is Optional and Inferred. Inference
            # errors are treated slightly differently for these two.
            is_optional = False
            is_inferred = False
            if annot is not Parameter.empty:
                annot_type = eval_type(annot, globals=_globals)
                if annotation_isinstance(
                    annot_type, Optional, globals=_globals
                ):
                    is_optional = True

                    # Note that Inferred is a subtype of Optional.
                    is_inferred = annotation_isinstance(
                        annot_type, Inferred, globals=_globals
                    )

            # If does not have default value and is not annotated optional, it
            # is a required argument.
            if param.default is Parameter.empty and not is_optional and not kind in [
                Parameter.VAR_KEYWORD, Parameter.VAR_POSITIONAL
            ]:
                required_args[name] = val

            # If it is annotated optional, mark it to be inferred. Dict value
            # indicates that it is an Inferred type whose inference is required.
            elif is_optional and val == param.default:
                to_infer_args[name] = is_inferred

        # Infer each inferrable argument.
        for name, inference_required in to_infer_args.items():
            try:
                val = inf.get_or_infer(name, required=required_args)
                bindings.arguments[name] = val

            except Exception as e:
                if inference_required:
                    # If the argument was of Inferred type, a failure to infer is an error.
                    raise InferException(
                        f"Could not infer value for {name} .\n\n{e}"
                    ) from None
                else:
                    # But if it was just an optional type, the failure is a warning.
                    print(f"WARNING: {e}")

        return bindings

    return handler


# Create an overload decorator that infers optional arguments, specialized to
# Infer method calls (self is Infer instance).
def _config_factory(bindings):
    self: Infer = bindings.arguments['self']
    return self.conf


_overload = overload(post_bind_handlers=[infer_defaults(_config_factory)])


def gen_name(base: str, name: str = None):
    if name is not None:
        return name

    return f"__{base}__{nonce()}"


def nonce() -> str:
    return str(random.randint(0, sys.maxsize))


class Infer:

    def __init__(self, conf: dict):
        assert conf is not None

        self.conf = conf

    def infer(self, params: Iterable, required: dict) -> None:
        for k in params:
            v = self.conf.get(k)
            if v is None:
                self.get_or_infer(k, **required)

    def get_or_infer(self, param: str, required: dict) -> Any:

        val = self.conf.get(param)
        if val is not None:
            return val

        if hasattr(Infer.Inferences, param):
            inference = getattr(Infer.Inferences, param)

            val = inference(self, **required)

            self.conf[param] = val

            return val

        else:
            raise InferException(
                f"No inference implemented for parameter {param}."
            )

    class Inferences:
        # Seperated out into different class since the names of the methods
        # below matter. Self, however, refers to an instance of Infer.

        @_overload
        def trulens_wrapper(self, model: TModel):
            return trulens_nn_models.get_model_wrapper(model)

        @_overload
        def project_name(self, **kwargs) -> str:
            """Generate a random project name."""

            return gen_name("project")

        @_overload
        def data_split_name(self, **kwargs) -> str:
            """Generate a random data split name."""

            return gen_name("data_split")

        @_overload
        def data_collection_name(self, **kwargs) -> str:
            """Generate a random data collection name."""

            return gen_name("data_collection")

        @_overload
        def embedding_layer(
            self, model: THugsTextClassifier, trulens_wrapper: Inferred(Any)
        ) -> str:
            """Guess embedding layer from layer name in a huggingface classifier."""

            layer_names = trulens_wrapper._layers.keys()

            r_embedding_layer_name = re.compile(
                r"|".join(
                    [
                        r".+_word_embeddings",
                        r".*transformer_word_emb",  # e.g. TransfoXLForSequenceClassification
                        r".+(?<!decoder)_embed_tokens",  # TODO(piotrm): check if appropriate
                        r".+_wte",  # "word token embedding" maybe?
                        r".*transformer_w",  # "word embedding" maybe?
                        r".*transformer_embeddings",
                        r".*transformer_embeddings_dropout",  # TODO(piotrm): check if appropriate
                        r".+_tokens_embed",  # e.g. OpenAIGPTForSequenceClassification
                        r".+_preprocessor_embeddings",  # e.g. PerceiverForSequenceClassification
                        r".*word_emb_emb_layers_0",  # e.g. transfo-xl-wt103
                        r".*canine_char_embeddings_LayerNorm",  # .e.g. google/canine-s
                    ]
                )
            )

            # TODO(piotrm):
            # - facebook/opt-6.7b has decoder_embed_tokens without encoder_embed_tokens
            # - some models have both of these, leading to error:
            #   ['transformer_embeddings_word_embeddings', 'transformer_embeddings_dropout']
            # -

            candidates = list(
                filter(r_embedding_layer_name.fullmatch, layer_names)
            )

            if len(candidates) == 0:
                raise Undispatch(
                    "No layers with name hinting at token/word embedding found. "
                    "Please specify one using the `embedding_layer` argument. "
                    "Layers are:\n" + retab("\n".join(layer_names), tab="\t")
                )

            if len(candidates) > 1:
                raise Undispatch(
                    f"More than one layer with expected name found: {candidates}. "
                    "Please specify the correct one using the `embedding_layer` argument."
                )

            return candidates[0]

        @_overload
        def output_layer(
            self, model: THugsTextClassifier, trulens_wrapper: Inferred(Any)
        ) -> str:

            layer_names = list(reversed(trulens_wrapper._layers.keys()))

            # TODO: Move this to somewhere else.
            common_names = [
                "classifier",
                "classifier_out_proj",
                "classifier_linear_out",
                "classification_head_out_proj",
                "score",
                "perceiver_decoder_decoder_final_layer",
                "logits_proj",
                "sequence_summary_summary"  # e.g. FlaubertForSequenceClassification
            ]

            found_names = [name for name in common_names if name in layer_names]

            if len(found_names) == 0:
                raise Undispatch(
                    "Could not find classifier output layer by name. "
                    "Please specify the `output_layer` parameter. "
                    "The layers are:\n" +
                    retab("\n".join(layer_names), tab="\t")
                )
            elif len(found_names) > 1:
                raise Undispatch(
                    f"More than one layer found that could be the classifier output: {found_names}."
                    "Please specify the correct one in the `output_layer` parameter. "
                    "The layers are:\n" +
                    retab("\n".join(layer_names), tab="\t")
                )
            else:
                return found_names[0]

        @_overload
        def vocab(
            self, model: THugsTextClassifier,
            tokenizer: Inferred(THugsTokenizer)
        ) -> Dict[str, int]:
            try:
                return dict(tokenizer.get_vocab())

            except NotImplementedError:
                # e.g. CanineTokenizer.from_pretrained('google/canine-s')

                if hasattr(tokenizer, "vocab_size"):
                    token_ids = list(range(tokenizer.vocab_size))
                    return {
                        tokenizer.decode(token_id): token_id
                        for token_id in token_ids
                    }

                else:
                    raise Undispatch(
                        f"Could not get vocabulary from tokenizer {tokenizer}."
                    )

        @_overload
        def n_embeddings(
            self, model: THugsTextClassifier, embedding_layer: Inferred(str),
            trulens_wrapper: Inferred(Any)
        ) -> int:
            embedding = trulens_wrapper._layers[embedding_layer]

            if hasattr(embedding, "embedding_dim"):
                # most huggingface models
                return embedding.embedding_dim

            if hasattr(embedding, "dim"):
                # ibert.QuantEmbedding saves embedding_dim in the dim field
                return embedding.dim

            if hasattr(embedding, "normalized_shape"):
                # if layer is LayerNorm, this may work
                return embedding.normalized_shape[0]

            raise Undispatch(
                f"Could not figure out n_embeddings from layer {embedding_layer}={embedding}."
            )

            # TODO: check that embedding is of the right type

        @_overload
        def n_output_neurons(
            self, model: THugsTextClassifier, output_layer: Inferred(str),
            trulens_wrapper: Inferred(Any)
        ) -> int:
            output = trulens_wrapper._layers[output_layer]

            # TODO: handle Identity, Dropout, Tanh???

            # TODO: check that layer is of the right type
            if hasattr(output, "out_features"):
                return output.out_features

            if hasattr(model, "num_labels"):
                return model.num_labels

            raise Undispatch(
                f"Could not figure out n_output_neurons from layer {output_layer} = {output}."
            )

        @_overload
        def huggingface_model_name(self, model: THugsTextClassifier) -> str:
            model_name = model.name_or_path

            if model_name is None or model_name == "":
                raise Undispatch("Got a blank name from model.")

            return model_name

        @_overload
        def model_name(
            self, model: THugsTextClassifier,
            huggingface_model_name: Inferred(str)
        ) -> str:
            """Use huggingface model name."""

            return huggingface_model_name

        @model_name.register
        def _(self, **kwargs) -> str:
            """Generate a random model name."""

            return gen_name("model")

        @_overload
        def rebatch_size(self, model: Inferred(TTorchModel)) -> int:
            """Determine rebatch size from memory usage and availability."""

            if Torch.get_device().type == "cuda":

                # Free unused gpu ram first so the available/used measurement below is accurate.
                torch.cuda.empty_cache()

                # Get how much cuda memory torch is using which is hopefully the
                # same as how much the given model is using. TODO(piotrm):
                # figure out what to do here if above assumption is not true.
                mem_free, mem_total = torch.cuda.mem_get_info()
                mem_used = mem_total - mem_free

                # Assume we can use all of the GPU ram.
                mem_available = mem_total

            else:

                import os

                import psutil
                mem_used = psutil.Process(os.getpid()).memory_info().rss
                vmem = psutil.virtual_memory()
                mem_total = vmem.total
                mem_free = vmem.available

                # Unlike in the gpu case, we cannot assume we can use all of GPU
                # ram for our purposes, so we presume we can use the rest of
                # free CPU ram only.
                mem_available = mem_free

            size = mem_available // int(mem_used * 3)
            # 3 is a heuristic for ram needed for back-propagation per
            # forward-propagation. TODO(piotrm): unclear whether an actual
            # forward pass has been done at this point so we cannot be sure of
            # actual forward pass RAM usage.

            if size == 0:
                size = 1
                print(
                    f"WARNING: model {model.__class__.__name__} may be too big to fit in memory."
                )

            return size

        @_overload
        def tokenizer(
            self, model: THugsTextClassifier,
            huggingface_model_name: Inferred(str)
        ) -> str:

            print(f"Getting tokenizer from model: {huggingface_model_name}")

            # TODO: Wav2Vec2CTCTokenizer fails to load
            # TODO: ESMTokenizer might have been renamed

            return transformers.AutoTokenizer.from_pretrained(
                huggingface_model_name
            )

        @_overload
        def n_tokens(
            self, model: THugsTextClassifier,
            tokenizer: Inferred(THugsTokenizer)
        ) -> int:
            n_tokens = tokenizer.model_max_length

            print(
                f"WARNING: using default n_tokens={n_tokens} for tokenizer {tokenizer}."
            )

            if n_tokens > 128:
                print(
                    f"WARNING: n_tokens={n_tokens} is very large, reducing to 128."
                )
                n_tokens = 128

            return n_tokens

        # The following are only for debugging and demonstration purposes.

        @_overload
        def debug_arg(self, debug_model: str) -> int:
            """Fail to infer anything the first time."""

            raise Undispatch("First failure reason.")

        @debug_arg.register
        def _(self, debug_model: str) -> int:
            """Fail to infer anything the second time."""

            raise Undispatch("Second failure reason.")

        @debug_arg.register
        def _(self, debug_model: str, debug_infer_me: Inferred(int)) -> int:
            """Infer debug_arg only if debug_model is secret."""

            if debug_model == "secret":
                return 42 + debug_infer_me

            raise Undispatch("Third failure reason.")

        @_overload
        def debug_infer_me(self, debug_model: str) -> int:
            """Infer debug_infer_me from debug_model."""

            return 100
