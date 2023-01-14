from .base import Base


class PSP22(Base):

    @classmethod
    def generate_code(cls, **kwargs) -> None:
        super().generate_code()
        cls._create_dir(cls, "psp22")
        template = cls._template(cls, "templates/psp22", "psp22.txt")
        content = cls._render_content(cls, template, **kwargs)
        cls._write_file(cls, "lib.rs", content)
        template = cls._template(cls, "templates/psp22", "cargo.txt")
        content = cls._render_content(cls, template, **kwargs)
        cls._write_file(cls, "Cargo.toml", content)
