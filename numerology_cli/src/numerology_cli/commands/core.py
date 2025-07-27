import click
from click import Parameter


class NumerologyBaseCommand(click.Command):

    PARAM_LOG = Parameter()
