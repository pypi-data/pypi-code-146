import factory
from wagtail.blocks.stream_block import StreamValue
from wagtail_factories.blocks import StreamFieldFactory, StructBlockFactory

from coop.factories import FuzzyWords

from .blocks import ChoiceFieldBlock, FieldBlock, FileFieldBlock, FormBlocks


class BasicFieldBlockFactory(StructBlockFactory):
    label = FuzzyWords(3)
    help_text = FuzzyWords(5, True)
    required = factory.Faker('pybool')
    placeholder = FuzzyWords(3, True)

    class Meta:
        model = FieldBlock


class TextFieldBlockFactory(BasicFieldBlockFactory):
    field_type = 'text'


class TextAreaBlockFactory(BasicFieldBlockFactory):
    field_type = 'textarea'


class EmailFieldBlockFactory(BasicFieldBlockFactory):
    field_type = 'email'


class NumberFieldBlockFactory(BasicFieldBlockFactory):
    field_type = 'number'


class DateFieldBlockFactory(BasicFieldBlockFactory):
    field_type = 'date'


class TimeFieldBlockFactory(BasicFieldBlockFactory):
    field_type = 'time'


class CheckboxFieldFactory(BasicFieldBlockFactory):
    field_type = 'checkbox'


class BaseChoiceFactory(StructBlockFactory):
    label = FuzzyWords(3)
    help_text = FuzzyWords(5, True)
    required = factory.Faker('pybool')
    choices = factory.Faker('texts', nb_texts=6, max_nb_chars=10)

    class Meta:
        model = ChoiceFieldBlock


class SelectChoiceFactory(BaseChoiceFactory):
    field_type = 'select'


class CheckBoxChoiceFactory(BaseChoiceFactory):
    field_type = 'checkbox'


class RadioChoiceFactory(BaseChoiceFactory):
    field_type = 'radio'


class FileFieldFactory(StructBlockFactory):
    label = FuzzyWords(3)
    help_text = FuzzyWords(5, True)
    required = False

    class Meta:
        model = FileFieldBlock


class FormBlocksFactory(StreamFieldFactory):
    def __init__(self, **kwargs):
        factories = {}
        super().__init__(factories, **kwargs)

    def generate(self, instance, step):
        blocks = [
            ('basic_field', TextFieldBlockFactory()),
            ('basic_field', TextAreaBlockFactory()),
            ('basic_field', EmailFieldBlockFactory()),
            ('basic_field', NumberFieldBlockFactory()),
            ('basic_field', DateFieldBlockFactory()),
            ('basic_field', TimeFieldBlockFactory()),
            ('basic_field', CheckboxFieldFactory()),
            ('choice_field', SelectChoiceFactory()),
            ('choice_field', CheckBoxChoiceFactory()),
            ('choice_field', RadioChoiceFactory()),
            ('file_field', FileFieldFactory()),
            ('heading', 'Heading'),
        ]

        return StreamValue(FormBlocks(), blocks)
