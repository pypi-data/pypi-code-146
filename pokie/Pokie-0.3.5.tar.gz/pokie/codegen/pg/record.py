from rick.util.string import snake_to_pascal, snake_to_camel
from rick_db import fieldmapper

from pokie.codegen.spec import TableSpec
from pokie.codegen.textfile import TextBuffer


class RecordGenerator:
    def gen_source(
        self, spec: TableSpec, camelcase=False, gen: TextBuffer = None, imports=True
    ):
        """
        Generate a RickDB Record class source definition

        :param spec:
        :param camelcase: if True, attributes will be camelCased
        :param gen: optional TextBuffer
        :param imports: include import line
        :return: source code string
        """
        if gen is None:
            gen = TextBuffer()

        if imports is True:
            gen.writeln("from rick_db import fieldmapper", newlines=3)

        gen.writeln(
            "@fieldmapper(tablename='{}', pk='{}', schema='{}')".format(
                spec.table, spec.pk, spec.schema
            )
        )
        gen.writeln("class {}Record:".format(snake_to_pascal(spec.table)))
        for field in spec.fields:
            if field.pk is False:
                attr = field.name if camelcase is False else snake_to_camel(field.name)
            else:
                attr = "id"

            gen.writeln(
                "{name} = '{field}'".format(name=attr, field=field.name), level=1
            )
        gen.writeln(gen.newline())
        return gen.read()

    def gen_class(self, spec: TableSpec, camelcase=False):
        """
        Generate a RickDB Record class from a spec
        :param spec:
        :param camelcase: if True, attributes will be camelCased
        :return: Record class
        """

        class clsRecord:
            pass

        for field in spec.fields:
            if field.pk is False:
                attr = field.name if camelcase is False else snake_to_camel(field.name)
            else:
                attr = "id"

            setattr(clsRecord, attr, field.name)

        fieldmapper(clsRecord, spec.pk, tablename=spec.table, schema=spec.schema)
        return clsRecord
