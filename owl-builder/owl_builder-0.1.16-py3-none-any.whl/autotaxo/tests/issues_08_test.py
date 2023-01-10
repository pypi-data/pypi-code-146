from baseblock import Enforcer

from owl_builder.autotaxo.bp import AutoTaxoOrchestrator


def issues_08():
    # https://github.com/craigtrim/buildolw/issues/8

    bp = AutoTaxoOrchestrator()
    assert bp

    result = bp.keyterms("show my history")
    print(result)

    Enforcer.is_list_of_str(result)


def main():
    issues_08()


if __name__ == "__main__":
    main()
