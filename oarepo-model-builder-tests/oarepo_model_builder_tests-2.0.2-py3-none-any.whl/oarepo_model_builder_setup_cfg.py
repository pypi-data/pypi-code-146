from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.cfg import CFGOutput


class OarepoModelBuilderSetupCfgBuilder(OutputBuilder):
    TYPE = "oarepo_model_builder_setup_cfg"

    TEST_DEPENDENCIES = [("invenio-app",">=1.3.3"),
                         ("invenio-db[postgresql,mysql,versioning]",">=1.0.14,<2.0.0"),
                         ("pytest-invenio",">=1.4.11"),
                         ("invenio_search[opensearch2]",">=2.0.0"),
                         ("Werkzeug","<2.2.0"),
                         ("Flask-Login",">=0.6.1"),
                         ("pyyaml",">=6.0"),
                         ("requests",">=2.28.1"),
                        ]


    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        #ext_class = self.settings.python.ext_class.rsplit(".", maxsplit=1)
        for package, version in self.TEST_DEPENDENCIES:
            output.add_dependency(
                package, version, group="options.extras_require", section="tests"
            )



