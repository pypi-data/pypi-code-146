from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class TestServiceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "test_service"
    template = "test_service"
    MODULE = "tests.test_service"

    def finish(self, **extra_kwargs):
        python_path = self.module_to_path(self.MODULE)
        self.process_template(
            python_path,
            self.template,
            **extra_kwargs,
        )