from baseblock import Enforcer

from owl_builder.autotaxo.bp import AutoTaxoOrchestrator

input_text = """
    A local area network (LAN) is a computer network that interconnects computers within a limited area such as a residence, school, laboratory, university campus or office building.
    By contrast, a wide area network (WAN) not only covers a larger geographic distance, but also generally involves leased telecommunication circuits.
    Ethernet and Wi-Fi are the two most common technologies in use for local area networks.
    Historical network technologies include ARCNET, Token Ring, and AppleTalk.
""".strip()


def test_bp():
    bp = AutoTaxoOrchestrator()
    assert bp

    results = bp.ttlresults(input_text)
    Enforcer.is_list_of_str(results)
