from numerology_cli.commands.base import numerology_group as cli
from numerology_cli.commands.ba_zi import GenerateBaZiChartCommand  # noqa
from numerology_cli.commands.gua import QueryTrigramCommand  # noqa


def main():
    cli()


if __name__ == '__main__':
    cli()
