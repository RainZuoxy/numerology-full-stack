from typing import Tuple
import click
from numerology.commands.base import numerology_group, BaseCommand
from numerology.const.gua import TrigramType, Trigram64Type


class QueryTrigramCommand(BaseCommand):
    PARAM_TRIGRAM_SERIES = click.Option(
        ("--trigram-series",),
        required=True,
        prompt="请输入八卦序列，阴为0阳为1，顺序为'初二三四五上'",
        help='The person who want to greet.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params = [self.PARAM_TRIGRAM_SERIES]

    def get_trigram_series(self, **kwargs) -> str:
        return kwargs.get(self.PARAM_TRIGRAM_SERIES.name)

    @staticmethod
    def parse_trigram_series(trigram_series: str) -> Tuple[TrigramType, TrigramType]:
        _trigram_series = [i for i in map(bool, map(int, list(trigram_series)))]
        down_trigram = TrigramType.get_base_trigram(value=tuple(_trigram_series[:3]))
        up_trigram = TrigramType.get_base_trigram(value=tuple(_trigram_series[3:]))
        return up_trigram, down_trigram

    @staticmethod
    def query_trigram(up_trigram, down_trigram):
        trigram64 = Trigram64Type.get_trigram64(up_trigram=up_trigram, down_trigram=down_trigram)
        return trigram64

    def to_table(self):
        ...


@numerology_group.command(cls=QueryTrigramCommand)
def query_trigram(**kwargs):
    try:
        command = QueryTrigramCommand(name=QueryTrigramCommand.__name__)
        trigram_series = command.get_trigram_series(**kwargs)
        up_trigram, down_trigram = command.parse_trigram_series(trigram_series=trigram_series)
        res = command.query_trigram(up_trigram=up_trigram, down_trigram=down_trigram)
        _format = command.get_format_param(**kwargs)
        if _format == 'table':
            command.to_table(res)
        return res

    except Exception as e:
        print(e)


def main():
    numerology_group()
