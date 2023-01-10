from owl_builder.autotaxo.bp import AutoTaxoOrchestrator


def test_01():
    input_text = """The best emoji for this sentence is the smiley face with sunglasses emoji.
                    This emoji conveys that Reno is a fun place to visit,
                    and that there are many activities to enjoy while you're there.!""".strip()

    bp = AutoTaxoOrchestrator()
    assert bp

    results = bp.keyterms(input_text)
    print(results)


def test_02():
    input_text = """tell me:""".strip()

    bp = AutoTaxoOrchestrator()
    assert bp

    results = bp.keyterms(input_text)
    print(results)


def test_03():
    input_text = """""".strip()

    bp = AutoTaxoOrchestrator()
    assert bp

    results = bp.keyterms(input_text)
    print(results)


def main():
    test_01()
    test_02()
    test_03()


if __name__ == "__main__":
    main()
