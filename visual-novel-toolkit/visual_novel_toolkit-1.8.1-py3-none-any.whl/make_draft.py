from pathlib import Path

from click import edit


def make_draft() -> None:
    docs = Path("docs")
    docs.mkdir(exist_ok=True)

    drafts = docs / "drafts"
    drafts.mkdir(exist_ok=True)

    existed_drafts = sorted(drafts.glob("*.md"))
    last_draft = int(existed_drafts[-1].stem) if existed_drafts else 0

    new_draft = drafts / f"{last_draft+1:04}.md"
    new_draft.touch()

    edit(filename=str(new_draft))
