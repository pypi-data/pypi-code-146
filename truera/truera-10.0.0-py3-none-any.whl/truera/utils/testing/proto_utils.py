import json
import unittest

from google.protobuf import text_format
from google.protobuf.json_format import MessageToJson
from google.protobuf.message import Message

from truera.utils.testing.json_utils import json_load_for_test


def _updateOrReadProto(
    actual_proto: Message,
    expected_proto_filename: str,
    proto_instance: Message,
    update_file=False,
    float_format=None
):
    if update_file:
        string = text_format.MessageToString(
            actual_proto, float_format=float_format
        )
        with open(expected_proto_filename, 'w') as f:
            f.write(string)
        return False
    with open(expected_proto_filename) as f:
        string = f.readlines()
        string = ''.join(string)
    text_format.Parse(string, proto_instance)
    return proto_instance


def _jsonNotAlmostEqualWrapped(
    test_case,
    a,
    b,
    atol,
    rtol,
    stack_trace,
    appendum,
    ignore_repeated_order=False
):
    stack_trace.append(appendum)
    if _jsonNotAlmostEqual(
        test_case,
        a,
        b,
        atol,
        rtol,
        stack_trace,
        ignore_repeated_order=ignore_repeated_order
    ):
        return True
    stack_trace.pop()
    return False


# TODO(piotrm): keep floats but remove their precision as per tolerance parameters
def _remove_floats(a):
    """ Replace all floats in the given dict/list structure with 0.0. This is used to sort
    structures without incorporating floats in the sort.
    """
    if isinstance(a, dict):
        return {k: _remove_floats(v) for k, v in a.items()}
    elif isinstance(a, list):
        return list(map(_remove_floats, a))
    elif isinstance(a, float):
        return 0.0
    else:
        return a


def _jsonNotAlmostEqual(
    test_case, a, b, atol, rtol, stack_trace, ignore_repeated_order=False
):
    if type(a) != type(b):
        stack_trace.append("'s type does not match.")
        return True
    if isinstance(a, dict):
        if _jsonNotAlmostEqualWrapped(
            test_case,
            a.keys(),
            b.keys(),
            atol,
            rtol,
            stack_trace,
            ".keys()",
            ignore_repeated_order=ignore_repeated_order
        ):
            return True
        for key in a.keys():
            if _jsonNotAlmostEqualWrapped(
                test_case,
                a[key],
                b[key],
                atol,
                rtol,
                stack_trace,
                "[{}]".format(key),
                ignore_repeated_order=ignore_repeated_order
            ):
                return True
    elif isinstance(a, list):
        if _jsonNotAlmostEqualWrapped(
            test_case,
            len(a),
            len(b),
            atol,
            rtol,
            stack_trace,
            "'s length",
            ignore_repeated_order=ignore_repeated_order
        ):
            return True

        # If we want to ignore order of items, lets sort them first so order will be
        # canonified. Sorted order is based on string representation without floats so
        # floating point precision should not affect the sort.
        if ignore_repeated_order:
            a = sorted(a, key=lambda obj: str(_remove_floats(obj)))
            b = sorted(b, key=lambda obj: str(_remove_floats(obj)))

        for i in range(len(a)):
            if _jsonNotAlmostEqualWrapped(
                test_case, a[i], b[i], atol, rtol, stack_trace,
                "[{}]".format(i)
            ):
                return True
    elif isinstance(a, float):
        if abs(a - b) > atol + rtol * abs(b):
            stack_trace.append(
                " does not match within the desired tolerance: {} vs {}.".
                format(a, b)
            )
            return True
    else:
        if a != b:
            stack_trace.append(" does not match.")
            return True
    return False


# Checks whether the actual proto matches the content in the
# passed file.
# If update_file, then updates the file content and returns False. (This option
# is meant for re-recording the expected output when the test fails.)
def assertProtoEquals(
    actual_proto: Message,
    expected_proto_filename: str,
    proto_instance: Message,
    update_file=False
):
    return_val = _updateOrReadProto(
        actual_proto,
        expected_proto_filename,
        proto_instance,
        update_file=update_file
    )
    if update_file:
        return False
    # TODO(apoorv) This is a bit hacky, maybe use the message differencer api
    # available to c++ code.
    return text_format.MessageToString(
        actual_proto
    ) == text_format.MessageToString(proto_instance)


def assertProtosAreSameWithTestCase(
    test_case: unittest.TestCase, proto1: Message, proto2: Message
):
    test_case.maxDiff = None
    test_case.assertEqual(
        text_format.MessageToString(proto1),
        text_format.MessageToString(proto2)
    )


def assertProtoEqualsWithTestCase(
    test_case: unittest.TestCase,
    actual_proto,
    expected_proto_filename,
    proto_instance,
    update_file=False,
    float_format=None
):
    """Check whether the given proto is similar to the one specified by the filename. Optionally
    updates the file to the given values. Similarity is equality modulo floating values beyond
    certain precision as specified by float_format.

    :param test_case: The test case associated with a similarity check. Will fail under that case
                      if similarity is insufficient.
    :param actual_proto: The proto to compare.
    :param expected_proto_filename: Source of the expected value of the proto.
    :param proto_instance: An instance of the protobuf class stored in expected_proto_filename.
    :param update_file: Whether to update the file with given proto (will also fail test case).
    :param float_format: Format of floats for comparison purposes.
    """
    return_val = _updateOrReadProto(
        actual_proto,
        expected_proto_filename,
        proto_instance,
        update_file=update_file
    )
    if update_file:
        test_case.fail("Test in record mode. (update_file=True)")
    # TODO(apoorv) This is a bit hacky, maybe use the message differencer api
    # available to c++ code.
    test_case.maxDiff = None
    test_case.assertEqual(
        text_format.MessageToString(proto_instance, float_format=float_format),
        text_format.MessageToString(actual_proto, float_format=float_format)
    )


def assertProtoAlmostEqualsWithTestCase(
    test_case: unittest.TestCase,
    actual_proto,
    expected_proto_filename,
    proto_instance,
    atol=1e-3,
    rtol=1e-3,
    update_file=False,
    ignore_repeated_order=False
):
    """Check whether the given proto is similar to the one specified by the filename. Optionally
    updates the file to the given values. Similarity is equality modulo floating values beyond
    certain precision by atol and rtol arguments, as well as module optionally the order of
    repeating fields. This last option, however, requires repeated fields to be unique save for
    floating values. The exact logic of atol/rtol is: given floats actual a, expected b, they are
    similar enough when abs(a - b) <= atol + rtol * abs(b)

    :param test_case: The test case associated with a similarity check. Will fail under that case
                      if similarity is insufficient.
    :param actual_proto: The proto to compare.
    :param expected_proto_filename: Source of the expected value of the proto.
    :param proto_instance: An instance of the protobuf class stored in expected_proto_filename.
    :param atol: absolute (additive) tolerance of floats.
    :param rtol: relative (multiplicative) tolerance of floats.
    :param update_file: Whether to update the file with given proto (will also fail test case).
    :param ignore_repeated_order: Do not require repeated fields to have the same order of items.
    """

    _updateOrReadProto(
        actual_proto,
        expected_proto_filename,
        proto_instance,
        update_file=update_file
    )
    if update_file:
        test_case.fail("Test in record mode. (update_file=True)")
    expected_response = json_load_for_test(MessageToJson(proto_instance))
    actual_response = json_load_for_test(MessageToJson(actual_proto))
    error_message = ["root"]
    test_case.assertFalse(
        _jsonNotAlmostEqual(
            test_case,
            expected_response,
            actual_response,
            atol,
            rtol,
            error_message,
            ignore_repeated_order=ignore_repeated_order
        ), "".join(error_message)
    )
