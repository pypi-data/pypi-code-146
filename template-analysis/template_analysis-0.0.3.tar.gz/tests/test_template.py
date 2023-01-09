from template_analysis.template import PlainText, Template, Variable


def test_variable_to_format_string() -> None:
    variable = Variable(0)
    assert variable.to_format_string() == "{}"


def test_plain_text_to_format_string() -> None:
    text = PlainText("dog")
    assert text.to_format_string() == "dog"


def test_template_to_format_string() -> None:
    template = Template([PlainText("cogito "), Variable(0), PlainText(" sum")])
    assert template.to_format_string() == "cogito {} sum"
