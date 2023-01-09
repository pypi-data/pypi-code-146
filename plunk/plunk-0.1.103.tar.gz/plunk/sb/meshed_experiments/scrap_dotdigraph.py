from functools import partial

from meshed import DAG, FuncNode
from sklearn.decomposition import PCA
import numpy as np


X_train = np.random.random((100, 30))
y_train = None
X_run = np.random.random((20, 30))


def make_learner_(learner_class, **learner_kwargs):
    model = learner_class
    # instantiate the learner
    learner_instance = model(**learner_kwargs)
    return learner_instance


def make_learner_node(
    learner_class, name='make_learner', output_name='learner', **learner_kwargs
):
    learner_ = partial(make_learner_, learner_class=learner_class)
    return FuncNode(func=learner_, name=name, out=output_name)


def make_train_learner_(learner, X_train, y_train, fitting_method_name='fit'):
    fitting_method = getattr(learner, fitting_method_name)
    fitted_learner = fitting_method(X_train, y_train)
    return fitted_learner


def make_train_learner_node(
    learner_bind='learner',
    X_train_bind='X_train',
    y_train_bind='y_train',
    fitting_method_name='fit',
    name='train_learner',
):
    make_train_learner__ = partial(
        make_train_learner_, fitting_method_name=fitting_method_name
    )
    return FuncNode(
        func=make_train_learner__,
        name=name,
        bind={
            'learner': learner_bind,
            'X_train': X_train_bind,
            'y_train': y_train_bind,
        },
        out='fitted_learner',
    )


def make_fitter_and_runner_nodes_(
    model, fit_bind='fit', transform_bind='transform', **model_kwargs,
):
    learner_node = make_learner_node(model, **model_kwargs)
    training_node = make_train_learner_node(learner_bind='learner')

    return (
        learner_node,
        training_node,
    )  # WTF, Commenting the training node make the DAG d_2 fail to construct!


if __name__ == '__main__':
    d_2 = DAG(make_fitter_and_runner_nodes_(model=PCA, transform_bind='score_samples'))

    print(d_2(X_train, y_train).score_samples(X_train))
    body = d_2.dot_digraph_body()
    d_2.dot_digraph()
