from enum import Enum

import click
from pydantic import BaseModel
from numerology import __version__ as lib_version
from numerology_cli import __version__ as cli_version


def show_version():
    v = {
        "numerology": lib_version,
        "numerology-cli": cli_version
    }

    return '\n'.join([f"{_p}: v{_v}" for _p, _v in v.items()])


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


@click.group(cls=click.Group, name='numerology', help='Numerology commands')
@click.version_option(show_version(), *('--version', '-v',), message='Version:\n%(version)s')
def numerology_group(**kwargs):  # noqa
    pass
