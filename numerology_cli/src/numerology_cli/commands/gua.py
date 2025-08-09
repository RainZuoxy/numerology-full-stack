import json
from typing import Tuple
import click
from numerology_cli.commands.base import numerology_group, BaseCommand
from numerology.const.gua import TrigramType, Trigram64Type


class QueryTrigramCommand(BaseCommand):
    PARAM_TRIGRAM_SERIES = click.Option(
        ("--trigram-series",),
        required=True,
        prompt=(
            "Please enter your trigram series, 0 for yin and 1 for yang, in order 'first -> top'"
            "example: 010111 -> index:6, name:Song"
        ),
        help='The person who want to greet.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.help = "According to Yao's trigram series, query the trigram"
        self.params = self.params + [self.PARAM_TRIGRAM_SERIES]

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

    def to_table(self, results):
        item = results.value
        name, index, ico = item.name, item.index, item.icon
        up_symbol = Trigram64Type.get_mapping()[item.up_trigram]
        down_symbol = Trigram64Type.get_mapping()[item.down_trigram]
        click.echo("The following is the result of the query:".encode(encoding='utf-8'))
        click.echo(f"Name：{name}".encode(encoding='utf-8'))
        click.echo(f"Index：{index}".encode(encoding='utf-8'))
        click.echo(f"Icon：{ico}".encode(encoding='utf-8'))
        click.echo(
            f"Up Trigram：{item.up_trigram.value.icon}-{item.up_trigram.value.name}-{up_symbol}".encode(encoding='utf-8')
        )
        click.echo(
            f"Down Trigram：{item.down_trigram.value.icon}-{item.down_trigram.value.name}-{down_symbol}".encode(
                encoding='utf-8')
        )

    def to_json(self, results):
        tmp = {
            "name": results.value.name,
            "value": results.value.model_dump(mode='json'),
        }
        return json.dumps(tmp, ensure_ascii=False)


@numerology_group.command(cls=QueryTrigramCommand)
def query_trigram(**kwargs):
    try:
        command = QueryTrigramCommand(name=QueryTrigramCommand.__name__)
        trigram_series = command.get_trigram_series(**kwargs)
        up_trigram, down_trigram = command.parse_trigram_series(trigram_series=trigram_series)
        res = command.query_trigram(up_trigram=up_trigram, down_trigram=down_trigram)
        _format = command.get_format_param(**kwargs)
        match _format.value:
            case 'table':
                command.to_table(results=res)
            case 'json':
                _json = command.to_json(results=res)
                click.echo(_json.encode(encoding='utf-8'))
            case _:
                click.echo(res)

        return res

    except Exception as e:
        print(e)


def main():
    numerology_group()
