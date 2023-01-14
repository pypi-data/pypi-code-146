from .base import Base


class Flipper(Base):
    
    @classmethod
    def generate_code(cls, **kwargs):
        super().generate_code()
        cls._create_dir(cls, "flipper")
        template = cls._template(cls, "templates/flipper/", "flipper.txt")
        content = cls._render_content(cls, template, **kwargs)
        cls._write_file(cls, "lib.rs", content)
        template = cls._template(cls, "templates/flipper/", "cargo.txt")
        content = cls._render_content(cls, template, **kwargs)
        cls._write_file(cls, "Cargo.toml", content)
