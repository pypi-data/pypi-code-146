"""This module contains the decision tree base estimator and node class."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

# TODO: uncomment when done
# from itertools import pairwise, starmap
from itertools import starmap
from operator import eq, ge, lt
from typing import Optional, Union

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype

logger = logging
logger.basicConfig(
    level=logger.DEBUG, format="%(message)s", filename="debug.log", filemode="w"
)

VALID_CRITERION = {"max_depth", "min_samples_split", "min_gain"}


@dataclass(kw_only=True)
class Node:
    """A decision tree node.

    The decision tree node defines the basis data structure at each
    routine call of a decision tree estimator.

    Parameters
    ----------
    value : str or float, default=None
        The descriptive or target feature value of a node.

    threshold : float, optional
        The feature value to partition the dataset into two levels with
        some range (the default is None, which implies the split feature
        is categorical).

    branch : str, default=None
        The feature value on a split from the parent node on a feature
        value.

    parent : Node, optional
        The precedent node along the path from the root to a node.

    depth : int, default=0
        The number of levels from the root to a node.

    children : dict, default={}
        The nodes on each split of the parent node for each unique
        feature values.

    Examples
    --------
    Create a decision tree leaf node whose prediction "+" is based on
    feature "A" with value "a":

    >>> from mpitree.base_estimator import Node
    >>> child = Node(
    ...     value="+", branch="a", parent=Node(value="A"), depth=1
    ... )
    >>> parent = Node(value="A", branch=None, depth=0, children={"a": child})
    >>> print(str(parent) + "\\n" + str(child))
    ├── A [None]
    │  └── + [a]
    """

    value: Union[str, float] = None
    threshold: Optional[float] = None
    branch: str = None
    parent: Optional[Node] = None
    depth: int = field(default_factory=int)
    children: dict = field(default_factory=dict)

    def __str__(self):
        """Outputs a string-formatted node.

        The output string of a node is primarly dependent on the `depth`
        for horizontal spacing, `branch` and type being either an in-
        terior or leaf. Leaf nodes are prefixed with a terminal branch.

        Returns
        -------
        str
            The string-formatted node.

        Raises
        ------
        ValueError
            If the depth of a node is a negative integer.
        """
        if self.depth < 0:
            raise ValueError("Node's `depth` attribute must be positive.")

        spacing = self.depth * "│  " + ("└── " if self.is_leaf else "├── ")
        return spacing + f"{self.value} [{self.branch}]"

    def __eq__(self, other: Node):
        """Check if two node objects are equivalent.

        Performs a pair-wise comparison among attributes of both `Node`
        objects and returns true if attributes are equal and returns false
        otherwise. The function will raise a TypeError if an object is not
        a `Node` instance.

        Parameters
        ----------
        other : Node
            The comparision object.

        Returns
        -------
        bool
            Returns true if both `Node` objects contain identical values
            for all attributes.

        Raises
        ------
        TypeError
            If the comparision object `other` is not a `Node` instance.

        See Also
        --------
        DecisionTreeEstimator.__eq__ :
            Check if two decision tree objects are identical.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("Expected a `Node` object")
        return self.__dict__ == other.__dict__

    def __add__(self, other: Node):
        """Add another node to a existing node children.

        The operation will append another `Node` with its key, specified
        by its `branch` value, to an existing `Node` children dictionary.

        Parameters
        ----------
        other : Node
            The comparision object.

        Returns
        -------
        self
            The current instance of the `Node` class.

        Raises
        ------
        TypeError
            If `other` is not a `Node` instance.
        Attribute Error
            If `other` branch attribute is not instantiated.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("Expected a `Node` object")
        if other.branch is None:
            raise AttributeError("Object's `branch` attribute is not instantiated")

        other.parent = self
        self.children[other.branch] = other
        return self

    @property
    def is_leaf(self):
        """Return whether a node is terminal.

        A `Node` object is a leaf if it contains no children; and will
        return true; otherwise, the `Node` is considered an interior
        and will return false.

        Returns
        -------
        bool
            Returns true if the node is terminal.

        Raises
        ------
        TypeError
            If `children` attribute is not a `dict` type
        """
        if not isinstance(self.children, dict):
            raise TypeError("Expected `children` to be a `dict` object")
        return not self.children

    @property
    def left(self):
        """Return the left child of a numeric-feature node.

        The `left` property accesses the first item (i.e., child)
        corresponding to the partition whose values for some feature
        is less than the specified `threshold`.

        Returns
        -------
        Node or None
            Returns a `Node` if its key exists in its parent first
            child; otherwise, returns None

        Raises
        ------
        TypeError
            If `children` attribute is not a `dict` type
        """
        if not isinstance(self.children, dict):
            raise TypeError("Expected `children` to be a `dict` object")
        return self.children.get(f"< {self.threshold}")

    @property
    def right(self):
        """Return the right child of a numeric-feature node.

        The `right` property accesses the second item (i.e., child)
        corresponding to the partition whose values for some feature
        is greater than or equal to the specified `threshold`.

        Returns
        -------
        Node or None
            Returns a `Node` if its key exists in its parent second
            child; otherwise, returns None

        Raises
        ------
        TypeError
            If `children` attribute is not a `dict` type
        """
        if not isinstance(self.children, dict):
            raise TypeError("Expected `children` to be a `dict` object")
        return self.children.get(f">= {self.threshold}")


class DecisionTreeEstimator:
    """A decision tree estimator.

    General purpose decision tree base class used for subclassing other
    decision tree implementations specific to some learning task (e.g.,
    classification and regression).

    Parameters
    ----------
    root : Node, default=None
        The starting node with depth zero of a decision tree.

    n_levels : dict, default=None
        The list of unique feature values for each descriptive feature.

    n_thresholds : dict, default=None
        The possible splits of the continuous feature being tested.

    metric : {'find_entropy', 'find_variance'}
        The measure of impurity used for calculating the information gain.

    criterion : {'max_depth', 'min_samples_split', 'min_gain'}, optional
        Contains pre-pruning hyperparameters of a decision tree (the default
        is None and will be assigned as an empty dictionary).

    Attributes
    ----------
    _check_is_fitted

    Methods
    -------
    _check_valid_params(X, y)
        Check parameters have valid values.
    _find_optimal_threshold(self, X, y, d)
        Compute the optimal threshold between different target levels.

    See Also
    --------
    decision_tree.DecisionTreeClassifier : A decision tree classifier.
    decision_tree.DecisionTreeRegresor : A decision tree regressor.

    References
    ----------
    .. [1] J. D. Kelleher, M. B. Namee, and A. D'Arcy, Fundamentals
        of machine learning for Predictive Data Analytics: Algorithms,
        worked examples, and case studies. Cambridge, MA: The MIT
        Press, 2020.
    """

    def __init__(
        self,
        *,
        root=None,
        n_levels=None,
        n_thresholds=None,
        metric=None,
        criterion=None,
    ):
        self._root = root
        self._n_levels = n_levels
        self._n_thresholds = n_thresholds
        self._metric = metric
        self._criterion = criterion

    def __iter__(self, node=None):
        """Perform a depth-first search on the decision tree.

        The traversal starts at the root node and recursively traverses
        across all its children in a fixed-order. The `values` method
        assures children nodes are searched in a stack-like manner.

        Parameters
        ----------
        node : Node, optional
            The subsequent node of the depth-first traversal.

        Yields
        ------
        Node

        See Also
        --------
        DecisionTreeEstimator.__str__ :
            Return a string-formatted decision tree.

        Examples
        --------
        Traverse the decision tree and store the node's value in a list:

        >>> import pandas as pd
        >>> from mpitree.decision_tree import DecisionTreeClassifier
        >>> df = pd.DataFrame(
        ...     {"A": ["a", "b"], "B": ["a", "a"], "y": ["+", "-"]}
        ... )
        >>> X, y = df.iloc[:, :-1], df.iloc[:, -1]
        >>> tree = DecisionTreeClassifier().fit(X, y)
        >>> [node.value for node in iter(tree)]
        ['A', '+', '-']
        """
        if not node:
            node = self._root

        yield node
        for child in node.children.values():
            yield from self.__iter__(child)

    def __str__(self):
        """Return a string-formatted decision tree.

        The output string of a decision tree is delimited by a single new-
        line escape character before string-formatting every `Node` object.

        Returns
        -------
        str
            The string-formatted decision tree.

        Raises
        ------
        AttributeError
            If the decision tree has not been fitted.

        See Also
        --------
        DecisionTreeEstimator.__iter__ :
            Perform a depth-first search on the decision tree.
        """
        if not self._check_is_fitted:
            raise AttributeError("Decision tree is not fitted")
        return "\n".join(map(str, self))

    def __eq__(self, other: DecisionTreeEstimator):
        """Check if two decision trees are equivalent.

        Performs a pair-wise comparison among attributes of both
        `DecisionTreeEstimator` objects and returns true if all
        attributes are equal; otherwise, returns false. The function will
        raise a TypeError if an instance is not a `DecisionTreeEstimator`
        object. If either comparison object are not fitted, the function
        will raise an AttributeError.

        Parameters
        ----------
        other : DecisionTreeEstimator
            The comparision object.

        Returns
        -------
        bool
            Returns true if both `DecisionTreeEstimator` objects contain
            identical values for all attributes.

        Raises
        ------
        TypeError
            If the object is not a `DecisionTreeEstimator` object.
        AttributeError
            If either comparison objects are not fitted.

        See Also
        --------
        Node.__eq__ : Check if two node objects are identical.
        """
        if not isinstance(other, self.__class__):
            raise TypeError("Expected a 'DecisionTreeEstimator' object")
        if not self._check_is_fitted or not other._check_is_fitted:
            raise AttributeError("At least one 'DecisionTreeEstimator' is not fitted")

        return all(starmap(eq, zip(self, other)))

    @property
    def _check_is_fitted(self):
        """Check whether a decision tree is fitted.

        The decision tree is fitted if it calls the `fit` method where.
        resulting call will instantiate the root as a `Node` object.

        Returns
        -------
        bool
            Returns true if the root node is a `Node` object.

        See Also
        --------
        decision_tree.DecisionTreeClassifier.fit :
            Performs the ID3 (Iterative Dichotomiser 3) algorithm.
        """
        return isinstance(self._root, Node)

    def _check_valid_params(self, X, y) -> None:
        """Check parameters have valid values.

        The input data must not be empty. Both thresholds and criterion
        attributes must be `dict` types and the criterion attribute must
        have valid keys.

        Parameters
        ----------
        X, y : pd.DataFrame.dtypes
            The feature matrix and target vector of the dataset.

        Returns
        -------
        None
            Returns None when parameters have valid values.

        Raises
        ------
        Exception
            If either datasets `X` or `y` are empty
        TypeError
            If either `criterion` or `n_thresholds` are not `dict` types
        KeyError
            If any unexpected hyperparameters keys.

        See Also
        --------
        decision_tree.DecisionTreeClassifier.fit :
            Performs the ID3 (Iterative Dichotomiser 3) algorithm.

        Examples
        --------
        Decision tree with one invalid key for the criterion attribute:

        >>> import pandas as pd
        >>> from mpitree.decision_tree import DecisionTreeClassifier
        >>> df = pd.DataFrame({"A": ["a"], "y": ["+"]})
        >>> X, y = df.iloc[:, :-1], df.iloc[:, -1]
        >>> DecisionTreeClassifier(
        ...     criterion={"error": 1, "max_depth": 2}
        ... )._check_valid_params(X, y)
        Traceback (most recent call last):
            ...
        KeyError: "Unexpected Keys: {'error'}"
        """
        if X.empty or y.empty:
            raise Exception("Expected at least one sample in both `X` and `y`")

        if self._n_thresholds is None:
            self._n_thresholds = {}

        if self._criterion is None:
            self._criterion = {}
        elif not isinstance(self._criterion, dict) or not isinstance(
            self._n_thresholds, dict
        ):
            raise TypeError(
                "Expected `criterion` and `n_thresholds` parameters to be `dict` type"
            )
        elif keyerr := set(self._criterion) - VALID_CRITERION:
            raise KeyError(f"Unexpected Keys: {keyerr}")

        # TODO: assign elsewhere
        self._n_levels = {
            d: ((lt, ge) if is_numeric_dtype(X[d]) else np.unique(X[d]))
            for d in X.columns
        }

    def _find_optimal_threshold(self, X, y, d):
        """Compute the optimal threshold between different target levels.

        The optimal threshold is found by first sorting `X` with respect
        to feature `d`. A pair-wise comparison is applied to each con-
        secutive pairs and the possible thresholds is the mean of the
        feature values of different target levels. For each possible
        threshold, the split providing the highest information gain is
        selected as the optimal threshold.

        Parameters
        ----------
        X, y : pd.DataFrame.dtypes
            The feature matrix and target vector of the dataset.
        d : str
            The feature specified in `X`.

        Returns
        -------
        tuple
            The max information gain, the optimal threshold, and the re-
            maining uncertainty.
        """
        df = pd.concat([X, y], axis=1)
        df.sort_values(by=[d], inplace=True)

        logger.info("Sorted according to feature '%s'", d)
        logger.info(str(df))

        thresholds = []
        for i in range(len(df) - 1):
            pairs = df.iloc[i : i + 2, -1]
            if any(pairs.iloc[0] != val for val in pairs.values):
                thresholds.append(df.loc[pairs.index, d].mean())

        # FIXME: Incorrect threshold calculation
        # thresholds = []
        # for i, j in zip(pairwise(y.index), pairwise(y.values)):
        #     if j[0] != j[1]:
        #         thresholds.append(X.loc[pd.Index(i), d].mean())

        levels = []
        for threshold in thresholds:
            level = df[df[d] < threshold], df[df[d] >= threshold]
            weight = np.array([len(i) / len(df) for i in level])

            metric_total = self._metric(df.iloc[:, :-1], df.iloc[:, -1])
            metric_partial = [
                self._metric(level[0].iloc[:, :-1], level[0].iloc[:, -1]),
                self._metric(level[1].iloc[:, :-1], level[1].iloc[:, -1]),
            ]

            rem = weight.dot(metric_partial)
            levels.append(metric_total - rem)

        return max(levels), thresholds[np.argmax(levels)], rem

    def _partition_data(self, X, y, d, op, threshold=None):
        """Returns a subset of the data for some feature and level."""
        if threshold:
            return (
                *list(map(lambda f: f[op(X[d], threshold)], [X, y])),
                f"{'<' if op is lt else '>='} {threshold}",
            )
        idx = X[d] == op
        return X.loc[idx].drop(d, axis=1), y.loc[idx], op

    def predict(self, x):
        """Predict a test sample on a decision tree.

        The function traverses the decision tree by looking up the
        feature value at the current node from the test sample `x`.
        If the current feature contains numerical values, the left
        transition is always considered if the `x` is less than the
        threshold; otherwise, considers the right transition. If the
        feature contains categorical values, the feature value at `x`
        is used as a key to the current node children.

        Parameters
        ----------
        x : pd.DataFrame.dtypes
            The single test sample.

        Returns
        -------
        node.value : str or float
            The class (classification) real (regression) label for
            a prediction on `x`.

        Raises
        ------
        KeyError
            If a feature does not satisfy any value specified in `x`.

        See Also
        --------
        decision_tree.DecisionTreeClasifier.score :
            Evaluate the decision tree model on the test set.
        """
        node = self._root
        while not node.is_leaf:
            query_branch = x[node.value].values[0]

            if is_numeric_dtype(query_branch):
                next_node = node.left if query_branch < node.threshold else node.right
            else:
                try:
                    next_node = node.children[query_branch]
                except KeyError:
                    logger.error(
                        "Branch %s -> %s does not exist",
                        node.value,
                        query_branch,
                        exec_info=True,
                    )
            node = next_node
        return node.value
