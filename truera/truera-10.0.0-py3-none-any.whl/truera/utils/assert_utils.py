def assert_set_equals(
    expected_set,
    actual_set,
    expected_set_name="expected_set",
    actual_set_name="actual_set",
    additional_message=""
):
    assert actual_set == expected_set, "Set {} doesnt match {}. Missing: {}, Extra: {}. {}".format(
        actual_set_name, expected_set_name, expected_set - actual_set,
        actual_set - expected_set, additional_message
    )
