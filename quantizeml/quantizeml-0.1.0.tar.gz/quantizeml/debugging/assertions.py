import os
import tensorflow as tf


def assert_enabled():
    """Check if run-time assertions are enabled

    Assertions are enabled by default. They can be disabled by setting the
    "ASSERT_ENABLED" environment variable to "0".

    Returns:
        bool: True if assertions are enabled.
    """
    return os.environ.get("ASSERT_ENABLED", "1") == "1"


def assert_equal(x, y, message=None):
    """Assert the condition `x == y` holds element-wise.

    If assertions are enabled, this wraps the corresponding tensorflow assertion.
    Otherwise it does nothing.

    Args:
      x (:obj:`tensorflow.Tensor`): a tensor
      y (:obj:`tensorflow.Tensor`): a tensor of the same dtype as and broadcastable to `x`.
      message (str): A string to prefix to the default message. Defaults to None.

    Raises:
      InvalidArgumentError: if the check can be performed immediately and is False.
      The check can be performed immediately in eager mode or if `x` and `y` are statically known.
    """
    if assert_enabled():
        tf.debugging.assert_equal(x, y, message)


def assert_none_equal(x, y, message=None):
    """Assert the condition `x != y` holds element-wise.

    If assertions are enabled, this wraps the corresponding tensorflow assertion.
    Otherwise it does nothing.

    Args:
      x (:obj:`tensorflow.Tensor`): a tensor
      y (:obj:`tensorflow.Tensor`): a tensor of the same dtype as and broadcastable to `x`.
      message (str): A string to prefix to the default message. Defaults to None.

    Raises:
      InvalidArgumentError: if the check can be performed immediately and is False.
      The check can be performed immediately in eager mode or if `x` and `y` are statically known.
    """
    if assert_enabled():
        tf.debugging.assert_none_equal(x, y, message=message)


def assert_less(x, y, message=None):
    """Assert the condition `x < y` holds element-wise.

    If assertions are enabled, this wraps the corresponding tensorflow assertion.
    Otherwise it does nothing.

    Args:
      x (:obj:`tensorflow.Tensor`): a tensor
      y (:obj:`tensorflow.Tensor`): a tensor broadcastable to `x`.
      message (str): A string to prefix to the default message. Defaults to None.

    Raises:
      InvalidArgumentError: if the check can be performed immediately and is False.
      The check can be performed immediately in eager mode or if `x` and `y` are statically known.
    """
    if assert_enabled():
        tf.debugging.assert_less(tf.cast(x, tf.float32), tf.cast(y, tf.float32), message)


def assert_less_equal(x, y, message=None):
    """Assert the condition `x <= y` holds element-wise.

    If assertions are enabled, this wraps the corresponding tensorflow assertion.
    Otherwise it does nothing.

    Args:
      x (:obj:`tensorflow.Tensor`): a tensor
      y (:obj:`tensorflow.Tensor`): a tensor broadcastable to `x`.
      message (str): A string to prefix to the default message. Defaults to None.

    Raises:
      InvalidArgumentError: if the check can be performed immediately and is False.
      The check can be performed immediately in eager mode or if `x` and `y` are statically known.
    """
    if assert_enabled():
        tf.debugging.assert_less_equal(tf.cast(x, tf.float32), tf.cast(y, tf.float32), message)


def assert_rank_at_least(x, rank, message=None):
    """Assert that `x` has rank of at least `rank`.

    If assertions are enabled, this wraps the corresponding tensorflow assertion.
    Otherwise it does nothing.

    Args:
      x (:obj:`tensorflow.Tensor`): a tensor
      rank (:obj:`tensorflow.Tensor`): a scalar integer tensor
      message (str): A string to prefix to the default message. Defaults to None.

    Raises:
      InvalidArgumentError: if the check cannot be performed statically and is False.
      ValueError: if the check can be performed statically and is False.
    """
    if assert_enabled():
        tf.debugging.assert_rank_at_least(x, rank, message)
