from pathlib import Path

from build_contract_rust import builder


def test_build_project():
    outcome = builder.build_project(
        project_path=Path("./testdata/input"),
        parent_output_directory=Path("./testdata/output"),
        specific_contract=None,
        cargo_target_dir=Path("/tmp/cargo-target-dir"),
        no_wasm_opt=False
    )

    actual_source = outcome.get_entry("adder").artifacts.src_package.read().decode()
    actual_wat = outcome.get_entry("adder").artifacts.text.read().decode()

    assert outcome.get_entry("adder").version == "1.2.3"
    assert outcome.get_entry("adder").codehash == "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
    assert actual_source == read_text_file(Path("./testdata/expected/adder-1.2.3.source.json")).strip()
    assert actual_wat == read_text_file(Path("./testdata/expected/adder.wat"))

    actual_source = outcome.get_entry("empty").artifacts.src_package.read().decode()
    actual_wat = outcome.get_entry("empty").artifacts.text.read().decode()
    assert outcome.get_entry("empty").version == "4.5.6"
    assert outcome.get_entry("empty").codehash == "20df405fa1733a22748c888f6c1571f2c12cc40a8b1de800e0fd105674b426a5"
    assert actual_source == read_text_file(Path("./testdata/expected/empty-4.5.6.source.json")).strip()
    assert actual_wat == read_text_file(Path("./testdata/expected/empty.wat"))


def read_text_file(path: Path) -> str:
    with open(path, "r") as f:
        return f.read()
