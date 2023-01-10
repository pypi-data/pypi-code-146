from baseblock import Enforcer

from owl_builder.autotaxo.bp import AutoTaxoOrchestrator


def issues_09():
    # https://github.com/craigtrim/buildolw/issues/9

    input_text = 'tomorrow I have a meeting at 1 pm'
    assert input_text

    bp = AutoTaxoOrchestrator()
    assert bp

    result = bp.keyterms(input_text)
    print(result)

    Enforcer.is_list_of_str(result)


def main():
    issues_09()


if __name__ == "__main__":
    main()
