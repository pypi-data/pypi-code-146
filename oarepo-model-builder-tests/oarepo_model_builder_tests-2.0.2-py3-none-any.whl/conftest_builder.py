from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class ConftestBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "conftest"
    template = "conftest"
    MODULE = "tests.conftest"

    def finish(self, **extra_kwargs):
        python_path = self.module_to_path(self.MODULE)
        self.process_template(
            python_path,
            self.template,
            **extra_kwargs,
        )