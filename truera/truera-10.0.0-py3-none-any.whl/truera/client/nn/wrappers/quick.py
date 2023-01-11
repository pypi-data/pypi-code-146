"""
# Quickstart: Unmanaged Anonymous Explanations.

The highest-level interface to nlp explanations. In this interface, the truera
workspace object is not exposed and all required ingestion elements are treated
anonymously, in that no name is needed to be given to a model, data split, or
data collection. The user needs to provide some model and some data. After this,
they can ask for any of the existing explanation types.

## Basic Usage

The `Explainer` object handles the highlevel interface. A model can be provided
either with the `Explainer` constructor or the `set_model` method, both of which
are overloaded for various model types and configuration options. Data is then
provided either with the `explain` or `set_data` methods, the first of which
also produces a default explanation. Finally, explanation parameters can be
provided to the `explain` or `set_explanation` methods.

```python
    Explainer(model).explain("hello there") 

    Explainer(model, tokenizer).explain(["first sentence", "second sentence"])
    
    Explainer(model, tokenizer, resolution=32).explain(...)

    exp = Explainer(model) # Do model wrapping and checking here.

    exp.explain(['first sentence', 'second sentence'])
    # Do the data wrapping, checking, and then produce some explanations.

    exp.explain(Path("somefile.csv"))

    exp.explain(Path("somefile.csv"), textfield="tweet", labelfield="sentiment")

    # Further usage

    explanations exp.global_token_influence(...)
    # ... is global_token_influence configuration

    exp.global_token_influence(data=somedataset, ...) 
    # TODO: should we try to get something like the working as well?
```

This should produce some basic explanations for "hello there" model input, the
two example sentences, or the contents of some CSV files. This, however, assumes
`model` is one of the recognized models types for which wrappers can be
inferred. We expect huggingface sentence classifiers to be one of the few
examples for which explanations can be retrieved as above.

# Input Types Robustness

Before explanations are provided, the user needs to provide at least a model and
at least one instance (instance requirement may be relaxed). These can be in
many forms.

## Data Types

    - datasets <class 'datasets.arrow_dataset.Dataset'> 
    - TODO: torch <class 'torch.utils.data.dataset.Dataset'> 
    - TODO: torch <class 'torch.utils.data.dataloader.DataLoader'> 
    - pandas <class 'pandas.core.frame.DataFrame'> 
    - pandas <class 'pandas.core.series.Series'>
    - TODO nltk datasets 
    - numpy <class 'numpy.ndarray'> 
    - python typing.Mapping or <class 'dict'> 
    - python typing.Sequence or <class 'list'> or <class 'tuple'>
    - python typing.Iterable 
    - TODO filenames 
    - TODO tensorflow 
    - TODO remote sources?

## Model Types

    - transformers torch classifiers `TTorchHugsTextClassifier` (see infer.py)
    - TODO: transformers tf classifiers `TTFHugsTextClassifier` (see infer.py)
    - TODO: transformers classifiers `THugsTextClassifier` (see infer.py)
    - TODO: transformers <class 'transformers.modeling_utils.PreTrainedModel'>
    - TODO: torch <class 'torch.nn.modules.module.Module'>
    - TODO: tensorflow <class 'tensorflow.python.framework.ops.Graph'> 
    - TODO: tensorflow <class 'keras.engine.training.Model'> 
    - TODO: blackbox / callable predict function

## Tokenizer Types

Tokenizers can sometimes be inferred from model but if not, they can be provided
in one of several forms:

    - transformers tokenizers `THugsTokenizer` (see infer.py)
    - TODO: tensorflow pre-processors 
    - TODO: nltk tokeninzers

# Keyword/Position Robustness

The `Explainer` constructor should be robust in terms of how it extracts the
required information from arguments if they are provided by keyword or by
position. No keywords should be mandatory but if given, they should contain
specific contents (not be robust in terms of their contents). For example:

```python
   Explainer(model=some_pretrained_model).explain(data='some sentence')
```

The `model` keyword should always specific a model and `data` should always
specify data. On the other hand, positional arguments are handled be their type,
not their position. If one of the data types (as above) is encountered, it is
assumed to be data, not anything else. Thus these are equivalent:

```python
    Explainer(tokenizer, model) 
    
    Explaimer(model, tokenizer)
```

This might cause problems if multiple arguments with the same type are provided
at once. Will have to reconsider this in the future.

# Dispatch

The robustness described above is a generalization of the concept of "dispatch"
or method overloading in typed languages. There a method may have multiple
definitions with different argument types. The runtime determines the
appropriate method to use from among options based on the types provided as
arguments. We generalize the concept to python and our use case in several ways:

- Position independence. Non-keyword arguments can be placed in any position.
- Types from optional packages. Some types may refer to packages not installed
  hence we need to be able to resolve them only if installed but otherwise
  ignore.

# Optional Parameters and Inference

The overloaded `Explainer` methods come with many optional arguments. For
example, this model specification based on a pytorch huggingface classification
model:

```python
    def set_model(self,
          model: TTorchHugsClassifier, 
          tokenizer: Inferred(THugsTokenizer),
          embedding_layer: Inferred(str),
          output_layer: Inferred(str),
          n_output_neurons: Inferred(int),
          n_embeddings: Inferred(int),
          n_tokens: Inferred(int)
    ) -> str:
```

The arguments annotated with the `Inferred` type indicate that they can be
inferred but that if the inference fails, an error is raised. These are filled
in automatically before the method is called using the various infernce
utilities in `infer.py` in the class `Infer.Inferences`. For example this method
for figuring out the `embedding_layer`:

```python
    def embedding_layer(
        self, model: THugsTextClassifier, trulens_wrapper: Inferred(Any) = None
    ) -> str:
```

Notice that this method itself includes optional arguments annotated with
`Inferred` so they get filled in by other utility methods.

Arguments annotated with `Optional` (our own Optional variant, not the one that
comes with python), are also inferred but failure of inference is a warning and
results in disabled features.

# External Robustness vs Internal Interfaces

Even though dispatch is robust to many types of arguments, and we can wrap
different types of models and datasets, it is important that after dispatch is
done, we have a consistent set of objects to work with. At the surface level
this is in terms of producing a collection of wrappers with strict interfaces.
Regardless of what a user provides as data, we will store it and process it
using a very specific type. Therefore, any functionality we provide will be in
terms of the specific type, not in terms of the provided type.

# Limitations

As the main operation of this file is producing wrappers from a wide variety of
data, we have some limitations in terms of what can be made visible to a user
after wrappers are made. If a user provides data as a torch DataLoader, for
example, they will not be able to interact with us in through DataLoader after
we have produced our wrappers, they can only interact with us in terms
implemented by the produced wrappers.

## pylint

The method overloading confuses pylint. One can use these exceptions:

- pylint: disable=E1101

  Use this if pylint complains about unexpected keyword arguments to overloaded
  methods.

- pylint: disable=E1123

  Same.

# Ramp to Managed Experience

The user has several avenues to expand towards the more custom managed
experience via the TrueraWorkspace. 

## Names and Workspace

One can retrieve and/or provide a workspace object to/from the `Explainer`:

```python
    e = Explainer(workspace=some_existing_workspace)

    e.workspace # is the underlying workspace
```

Secondly, a user can give optional names to models and data_splits so that they
can then be accessed from the managed workspace:

```python
    e = Explainer(model, model_name="foo")
    e.explain(["hello there", "bob !"], data_split_name="mysplit")

    e.workspace.get_models() # contains model "foo"
    e.workspace.get_data_splits() # contains data_split "mysplit"
```

One can also let `Explainer` generate random names for them which can then be
used with a workspace.

```python
    e = Explainer()

    model_name = e.set_model(model)

    data_split_name = e.set_data("some data")
```

## Use autowrap

The second ramp is via access to `autowrap`:

```python
    e = Explainer().autowrap(...) # ... is all autowrap arguments
```

The produced wrappers are then stored in the `Explainer`.

TODO: Presently this is not useful as autowrap wraps models and data at once so
there is no reason at all to use autowrap and the other Explainer methods at the
same time.

## Use existing wrappers

Finally, one can specify existing wrappers to the `Explainer`:

```python
    e = Explainer()
    
    e.set_model(model_run=..., model_load=...)

    e.set_data(split_load=...)

    e.explain()
```

TODO: This may not yet work. Need regeneration of wrappers in parts, instead of
all at once.
"""

# TODO: Lots of things here should be moved to utilities and/or shared with
# utilities in trulens.

from __future__ import annotations

import dataclasses
from pathlib import Path
import typing
from typing import Any, Callable, Dict, Iterable

import numpy as np

from truera.client.local.intelligence.local_explainer import LocalExplainer
from truera.client.local.intelligence.local_nlp_explainer import \
    LocalNLPExplainer
from truera.client.local.local_truera_workspace import LocalTrueraWorkspace
from truera.client.nn.client_configs import LayerAnchor
from truera.client.nn.client_configs import NLPAttributionConfiguration
from truera.client.nn.wrappers import nlp as nlp
from truera.client.nn.wrappers.autowrap import autowrap as autowrapper_autowrap
from truera.client.nn.wrappers.infer import gen_name
from truera.client.nn.wrappers.infer import infer_defaults
from truera.client.nn.wrappers.infer import Inferred
from truera.client.nn.wrappers.infer import THugsAudioClassifier
from truera.client.nn.wrappers.infer import THugsTokenizer
from truera.client.nn.wrappers.infer import TTorchHugsTextClassifier
from truera.client.nn.wrappers.torch import Torch
from truera.client.truera_workspace import TrueraWorkspace
from truera.client.util.func_utils import bind_relevant_and_call
from truera.client.util.func_utils import overload
from truera.client.util.func_utils import render_sig
from truera.client.util.python_utils import caller_frame
from truera.client.util.python_utils import import_optional
from truera.client.util.type_utils import Optional

trulens = import_optional("trulens", "NLP model explanations")


# Create a overloading dispatch that also fills in Inferred arguments if
# they are not provided.
def _config_factory(bindings):
    self = bindings.arguments['self']
    return self.cache


_overload = overload(
    post_bind_handlers=[infer_defaults(config_factory=_config_factory)]
)


class Explainer():
    """
    High-level explanations interface for NLP models. There is no model, data
    collection, or split naming in this interface. 
    """

    # Which keys to keep in parameter cache `self.cache`:
    CACHE_KEYS = set(
        [
            'model',
            'get_model',  # autowrap
            'eval_model',  # autowrap
            'vocab',  # autowrap
            'unk_token_id',  # autowrap
            'pad_token_id',  # autowrap
            'special_tokens',  # autowrap
            'text_to_inputs',  # autowrap
            'text_to_token_ids',  # autowrap
            'text_to_spans',  # autowrap
            'n_embeddings',  # autowrap
            'n_tokens',  # autowrap
            'ds_from_source',  # autowrap
            'standardize_databatch',  # autowrap
            'embedding_layer',  # NLPAttributionConfiguration
            'embedding_anchor',  # NLPAttributionConfiguration
            'output_layer',  # NLPAttributionConfiguration
            'output_anchor',  # NLPAttributionConfiguration
            'n_output_neurons',  # NLPAttributionConfiguration
            'n_metrics_records',  # NLPAttributionConfiguration
            'ref_token',  # NLPAttributionConfiguration
            'resolution',  # NLPAttributionConfiguration
            'rebatch_size',  # NLPAttributionConfiguration
            'project_name',  # LocalTrueraWorkspace
            'model_name',  # LocalTrueraWorkspace
            'data_collection_name',  # LocalTrueraWorkspace
            'data_split_name',  # LocalTrueraWorkspace
            'score_type',  # LocalTrueraWorkspace
        ]
        # 'model_path' # autowrap, not using
        # 'data_path' # autowrap, not using
    )

    def update_cache(self, **kwargs):
        """
        Updated wrapping configuration parameters. Replaces None values with
        non-None and missing keys with None.
        """

        # First set all the missing keys in config to ones that come from kwargs.
        self.cache.update(
            **{k: v for k, v in kwargs.items() if k not in self.cache}
        )

        # Then update any keys that are not None in kwargs.
        self.cache.update(**{k: v for k, v in kwargs.items() if v is not None})

    def update_cache_from_locals(self, keys: Optional(Iterable[str]) = None):
        """
        Update the cache values of all of the `keys` or `CACHE_KEYS` that have
        non-None value in the caller's locals.
        """

        keys = keys or self.CACHE_KEYS

        locals = caller_frame().f_locals

        self.update_cache(
            **{k: locals[k] for k in keys if locals.get(k) is not None}
        )

    def __init__(
        self, *args, workspace: Optional(TrueraWorkspace) = None, **kwargs
    ):
        """
        Initalize and create model parameters from the given args if any. If
        `workspace` is given, uses it under the hood or otherwise creates one.
        """

        self.tru = workspace or LocalTrueraWorkspace()

        # Once project parameters are figured out, add the various named objects
        # with anonymous or specified names.
        self.project_name = None
        self.model_name = None
        self.data_collection_name = None
        self.data_split_name = None

        # Once wrappers are constructed, hold them here.
        self.wrappers = nlp.WrapperCollection()

        self.cache = dict()

        # If arguments were given to constructor, assume they were setting up a model.
        if len(args) + len(kwargs) > 0:
            self.set_model(*args, **kwargs)

        # Will be filled in later once enough wrappers are constructed.
        self.explainer: LocalExplainer = None

    @property
    def workspace(self):
        return self.tru

    def autowrap(self, **kwargs) -> None:
        # docstring comes from autowrap.autowrapper below.
        # TODO: fix signature in printout to be also from autowrap.autowrapper .

        new_wrappers = bind_relevant_and_call(autowrapper_autowrap, **kwargs)

        self.wrappers.join_in_place(new_wrappers)

        self.update_cache(**kwargs)

        return self

    # Use autowrap's docstring.
    autowrap.__doc__ = autowrapper_autowrap.__doc__

    def __getattr__(self, name: str) -> Any:
        """
        Dispatch looking for not found attributes to LocalExplainer if they are 
        defined there. If neither Explainer nor LocalExplainer has the required 
        attribute, an index of available methods is printed.
        """

        if hasattr(LocalNLPExplainer, name) and self.explainer is None:
            raise RuntimeError(
                "Before calling `LocalNLPExplainer` methods, a model and data need to be specified."
            )

        if self.explainer is not None and hasattr(self.explainer, name):
            return getattr(self.explainer, name)

        # TODO: Potentially restrict to these:?
        """
        def get_feature_influences(self): pass
        def list_performance_metrics(self): pass
        def compute_performance(self): pass
        def global_token_summary(self): pass
        def data_exploration_tab(self): pass
        def record_explanations_attribution_tab(self): pass
        def model_robustness_analysis_tab(self): pass
        def token_influence_comparison_tab(self): pass
        def evaluate_text_tab(self): pass
        def upload_project(self): pass
        """

        msg = f"Explainer has no such attribute {name}.\n\n"

        msg += "#######################################\n"
        msg += "Available methods:\n\n"
        for k in dir(self):
            v = getattr(self, k)
            if not isinstance(v, Callable):
                continue
            if k[0] == "_":
                continue
            msg += "  " + render_sig(v) + "\n"

        msg += "#######################################\n"
        msg += "Available explanation methods:\n\n"
        for k in dir(LocalNLPExplainer):
            v = getattr(LocalNLPExplainer, k)
            if not isinstance(v, Callable):
                continue
            if k[0] == "_":
                continue
            msg += "  " + render_sig(v) + "\n"

        raise AttributeError(msg)

    def _build_wrappers(self):
        """
        Build or rebuild wrappers using autowrap.
        """

        print(f"(re)building wrappers for {self.cache['data_split_name']}")

        # Fill in arguments to autowrap from ones contained in config.
        # Call autowrap and add the results to our wrappers.
        self.wrappers.join_in_place(
            bind_relevant_and_call(autowrapper_autowrap, self.cache)
        )

        wrappers = self.wrappers

        model_run_wrapper = wrappers.model_run_wrapper
        model_load_wrapper = wrappers.model_load_wrapper

        # Check that some data has been specified.
        assert "_data_len" in self.cache, "Need to specify some data to explain first."

        # Adjust n_metrics_records to make sure its not larger than the number of instances to explain.
        # TODO: This should not be done here.
        if "n_metrics_records" in self.cache:
            self.cache['n_metrics_records'] = min(
                self.cache['_data_len'], self.cache['n_metrics_records']
            )
        else:
            self.cache['n_metrics_records'] = self.cache['_data_len']

        # Create an attribution configuration, from the common set of
        # configuration parameters that are accepted by the NLP variant.
        attr_config = bind_relevant_and_call(
            NLPAttributionConfiguration, self.cache
        )

        # Create a project if not already present in the stateful interface.
        if self.project_name is None:
            self.project_name = gen_name("project")
            self.tru.add_project(
                self.project_name,
                score_type=self.cache['score_type'],
                input_type="text"
            )
            print(f"created anonymous project {self.project_name}")

        # Create a data collection in the stateful interface.
        if self.data_collection_name is None:
            self.data_collection_name = gen_name("data_collection_name")
            self.tru.add_data_collection(self.data_collection_name)
            print(
                f"created anonymous data collection {self.data_collection_name}"
            )

        # Create a split in the stateful interface. Delete the old one if one
        # already exist with the given name.
        if (self.data_split_name is None) or (
            'data_split_name' in self.cache and
            self.data_split_name != self.cache['data_split_name']
        ):
            self.data_split_name = self.cache['data_split_name']

            if self.data_split_name in self.tru.get_data_splits():
                self.tru.delete_data_split(self.data_split_name)

            self.tru.add_nn_data_split(
                self.data_split_name, wrappers, split_type="test"
            )

            # Delete the cached split name so that it does not get filled in as
            # default value in subsequent calls. Refer to `self.data_split_name`
            # from now on.
            del self.cache['data_split_name']

        # Same with model.
        if (
            self.model_name is None or (
                'model_name' in self.cache and
                self.model_name != self.cache['model_name']
            )
        ):
            self.model_name = self.cache['model_name']

            # Create a model in the stateful interface.
            self.tru.add_nn_model(
                self.model_name, model_load_wrapper, model_run_wrapper,
                attr_config
            )
            self.tru.set_model(self.model_name)

            # Delete model name in cache so that any subsequent model will be
            # given a new name if needed.
            del self.cache['model_name']

        # Finally get an explainer.
        self.explainer: LocalExplainer = self.tru.get_explainer(
            self.data_split_name
        )

    def explain(self, *args, **kwargs) -> 'pandas.Dataframe':
        """
        Produce an explanation. Data must be specified by args, kwargs or by a prior set_data.
        """

        rebuild: bool = False

        if len(args) + len(kwargs) > 0:
            self.set_data(*args, **kwargs)
            rebuild = True

        if rebuild or self.explainer is None:
            # build the wrappers
            self.set_explanation(**kwargs)
            self._build_wrappers()

        return bind_relevant_and_call(
            self.explainer.get_feature_influences, kwargs
        )

    # Model Wrappers

    @_overload
    def set_model(
        self, model_run: nlp.Wrappers.ModelRunWrapper,
        model_load: nlp.Wrappers.ModelLoadWrapper, model_name: Inferred(str)
    ) -> str:
        """Use existing wrappers."""

        print("Using existing wrappers.")

        self.wrappers.join_in_place(
            nlp.Wrappers(model_run=model_run, model_load=model_load)
        )

        self.update_cache_from_locals()

        return model_name

    @set_model.register
    def _(self, model: THugsAudioClassifier, *args, **kwargs) -> str:
        raise NotImplementedError("Audio classifiers are not yet supported.")

    @set_model.register
    def _(self,
          model: TTorchHugsTextClassifier,
          tokenizer: Inferred(THugsTokenizer),
          embedding_layer: Inferred(str),
          output_layer: Inferred(str),
          n_output_neurons: Inferred(int),
          n_embeddings: Inferred(int),
          n_tokens: Inferred(int),
          model_name: Inferred(str),
          vocab: Inferred(Dict[str, int])
         ) -> str:
        """Wrap a huggingface torch sequence classifier model."""

        print("Wrapping huggingface classifier.")

        unk_token_id = tokenizer.unk_token_id
        pad_token_id = tokenizer.pad_token_id
        special_tokens = list(tokenizer.all_special_ids)

        tok_args = dict(
            padding='max_length', max_length=n_tokens, truncation=True
        )

        text_to_inputs = lambda texts: dict(
            args=[],
            kwargs=tokenizer.batch_encode_plus(
                list(texts),
                return_tensors="pt",  # model eval needs pytorch tensors
                **tok_args
            ).to(Torch.get_device())
        )

        text_to_token_ids = lambda texts: tokenizer.batch_encode_plus(
            list(texts),
            return_tensors='np',  # truera wants numpy tensors instead
            **tok_args
        )['input_ids']

        # eval_model not needed, is callable already
        # TODO: fix verify to make eval_model optional
        # TODO: return probits instead of logits
        eval_model = lambda model, args, kwargs: model(
            *args, **kwargs
        ).logits.detach().cpu().numpy()

        text_to_spans = lambda texts: tokenizer.batch_encode_plus(
            list(texts),
            return_tensors='np',
            return_offsets_mapping=True,
            **tok_args
        )['offset_mapping']

        get_model = lambda _: model
        score_type = "logits"  # TODO: determine this?

        self.update_cache_from_locals()

        return model_name

    @set_model.register
    def _(self, huggingface_model_name: str, **kwargs) -> None:
        """Wrap the huggingface model given by name."""

        print(f"Load huggingface model by name: {huggingface_model_name}.")

        transformers = import_optional(
            "transformers", "huggingface model wrapping"
        )
        model = transformers.AutoModelForSequenceClassification.from_pretrained(
            huggingface_model_name
        )

        return self.set_model(model=model, **kwargs)  # pylint: disable=E1123

    @set_model.register
    def _(self, model: 'tensorflow.Graph',
          model_name: Inferred(str)) -> str:
        """Wrap a tensorflow 1 Graph."""

        raise NotImplementedError()

    @set_model.register
    def _(self, model: 'tensorflow.keras.Model',
          model_name: Inferred(str)) -> str:
        """Wrap a tensorflow 2 Model."""

        raise NotImplementedError()

    @set_model.register
    def _(self, model: 'torch.nn.Module',
          model_name: Inferred(str)) -> str:
        """Wrap a torch module."""

        raise NotImplementedError()

    @set_model.register
    def _(self, model: typing.Callable,
          model_name: Inferred(str)) -> str:
        """Wrap a blackbox Callable predictor."""

        raise NotImplementedError()

    # This signature is only for demonstration purposes to show how errors get
    # reported to the user.
    @set_model.register
    def _(
        self,
        debug_model: str,
        debug_arg: Inferred(int)
    ) -> str:
        """
        This is a dummy definition meant for debugging and demonstration
        purposes only.
        """

        print("set_model debug method called with:")
        print("\tdebug_model=", debug_model)
        print("\tdebug_arg=", debug_arg)

        return "lol"

    # Explanation Configuration

    @_overload
    def set_explanation(
        self,
        rebatch_size: Inferred(int),
        ref_token: Optional(str),
        resolution: Optional(int) = 16,
        n_metrics_records: Optional(int) = 128,
        embedding_anchor: Optional(LayerAnchor) = LayerAnchor.OUT,
        output_anchor: Optional(LayerAnchor) = LayerAnchor.OUT,
        **kwargs
    ) -> None:
        if ref_token is None:
            if self.wrappers.tokenizer_wrapper is not None:
                ref_token = self.wrappers.tokenizer_wrapper.pad_token
            else:
                ref_token = "[PAD]"

        self.update_cache_from_locals()

    # Tokenizer Wrappers

    @_overload
    def set_tokenizer(self, tokenizer: nlp.Wrappers.TokenizerWrapper) -> None:
        """Use existing tokenizer wrapper."""

        self.wrappers.join_in_place(
            nlp.WrapperCollection(tokenizer_wrapper=tokenizer)
        )

    @set_tokenizer.register
    def _(
        self,
        tokenizer: THugsTokenizer
    ) -> None:
        """Wrap a huggingface tokenizer."""

        # TODO: these two tokenizers have slightly different methods
        # batch_encode vs. batch_encode_plus

        raise NotImplementedError()

    # Data Wrappers

    @_overload  #accumulate=Wrappers)
    def set_data(
        self, data: nlp.Wrappers.SplitLoadWrapper,
        data_split_name: Inferred(str)
    ) -> str:
        """Load instances using an existing split load wrapper."""

        self.wrappers.join_in_place(
            nlp.WrapperCollection(split_load_wrapper=data)
        )

        self.update_cache_from_locals()

        return data_split_name

    @set_data.register
    def _(self, path: Path, data_split_name: Inferred(str)) -> str:
        """Load data from the named file."""

        if not path.exists():
            raise ValueError(f"File {path} does not exist.")

        if path.suffix == ".csv":
            # TODO: use chunky csv reader here

            pd = import_optional("pandas", "CSV loading")
            df = pd.read_csv(path)

            return self.set_data(data=df, data_split_name=data_split_name)
        else:
            raise ValueError(f"Do not know how to read {path}.")

    @set_data.register
    def _(self, data: str, data_split_name: Inferred(str)) -> str:
        """Load a single string."""

        return self.set_data(data=[data], data_split_name=data_split_name)

    @set_data.register
    def _(self, data: 'numpy.ndarray', data_split_name: Inferred(str)) -> str:
        """Load instances from a numpy array."""

        return self.set_data(list(data), data_split_name=data_split_name)

    @set_data.register
    def _(
        self,
        data: 'pandas.DataFrame',
        text_field: str,
        label_field: Optional(str),
        data_split_name: Inferred(str)
    ) -> str:
        """Load instances from a pandas DataFrame."""

        texts = list(data[text_field])

        labels = None

        if label_field is not None:
            labels = list(data[label_field])

        # use sequences wrapper
        # pylint: disable=E1123
        return self.set_data(
            data=texts, labels=labels, data_split_name=data_split_name
        )

    @set_data.register
    def _(self, data: 'pandas.Series', data_split_name: Inferred(str)) -> str:
        """Load instances from a pandas Series."""

        # use sequences wrapper
        return self.set_data(data=list(data), data_split_name=data_split_name)

    @set_data.register
    def _(self, data: 'datasets.Dataset', data_split_name: Inferred(str)) -> str:
        """Load instances from datasets package Dataset."""

        raise NotImplementedError()

    @set_data.register
    def _(self, data: 'torch.utils.data.Dataset', data_split_name: Inferred(str)) -> str:
        """Load instances from a torch Dataset."""

        raise NotImplementedError()

    @set_data.register
    def _(self, data: 'torch.utils.data.DataLoader', data_split_name: Inferred(str)) -> str:
        """Load instances from a torch DataLoader."""

        raise NotImplementedError()

    @set_data.register
    def _(
        self,
        data: typing.Sequence,
        labels: Optional(typing.Sequence),
        data_split_name: Inferred(str)
    ) -> str:
        """Load instaces from a sequence."""

        data_len = len(data)

        if labels is None:
            labels = [0] * data_len

        data = np.array(data)
        labels = np.array(labels)
        ids = np.array(list(range(data_len)))

        ds_from_source = lambda _: nlp.Types.StandardBatch(
            text=data, labels=labels, ids=ids
        )
        # currently trubatch refers to dict
        standardize_databatch = dataclasses.asdict

        if "_data_len" in self.cache:
            del self.cache['_data_len']

        print(f"Have {data_len} instance(s) in {data_split_name}.")

        self.update_cache_from_locals()

        self.update_cache(_data_len=data_len)

        return data_split_name

    @set_data.register
    def _(self, data: typing.Iterable, data_split_name: Inferred(str)) -> str:
        """Load instances from an iterable."""

        # Convert to sequence and use that wrapper.
        # TODO: create a generator wrapper

        return self.set_data(list(data), data_split_name=data_split_name)
