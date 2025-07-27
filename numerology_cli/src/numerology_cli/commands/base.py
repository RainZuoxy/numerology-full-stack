from enum import Enum

import click
from pydantic import BaseModel


@click.group(cls=click.Group, name='numerology', help='Numerology commands')
def numerology_group(**kwargs):  # noqa
    pass


class ShowType(Enum):
    TABLE = 'table'
    JSON = 'json'


class EnumChoice(click.Choice):
    def __init__(self, enum, case_sensitive=False, use_value=False):
        self.enum = enum
        self.use_value = use_value
        choices = [str(e.value) if use_value else e.name for e in self.enum]
        super().__init__(choices, case_sensitive)

    def convert(self, value, param, ctx):
        if isinstance(value, self.enum):
            return value
        result = super().convert(value, param, ctx)
        if not self.case_sensitive and result not in self.choices:
            result = next(c for c in self.choices if result.lower() == c.lower())
        if self.use_value:
            return next(e for e in self.enum if str(e.value) == result)
        return self.enum[result]


class BaseCommand(click.Command):
    PARAM_FORMAT = click.Option(
        ('--format',),
        default=ShowType.TABLE,
        type=EnumChoice(enum=ShowType, use_value=True),
        help='选择输出结果类型'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params = [self.PARAM_FORMAT]

    @classmethod
    def get_format_param(cls, **kwargs) -> bool:
        return kwargs.get(cls.PARAM_FORMAT.name, False)

    @staticmethod
    def to_json(*, value: BaseModel, **kwargs):
        return value.model_dump_json(**kwargs)
