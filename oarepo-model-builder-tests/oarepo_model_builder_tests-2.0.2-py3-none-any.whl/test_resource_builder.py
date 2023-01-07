from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class TestResourceBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "test_resource"
    template = "test_resource"
    MODULE = "tests.test_resource"

    def finish(self, **extra_kwargs):
        python_path = self.module_to_path(self.MODULE)
        self.process_template(
            python_path,
            self.template,
            **extra_kwargs,
        )