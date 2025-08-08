import json
import click
from pydantic import BaseModel
from numerology_cli.commands.base import EnumChoice, numerology_group, BaseCommand
from numerology.const.gender import Gender
from numerology.core.generator import ChartConf


class GenerateBaZiChartCommand(BaseCommand):
    PARAM_NAME = click.Option(
        ('--name',),
        prompt='求算人名',
        help='The person who want to greet.'
    )

    PARAM_DOB_TIME = click.Option(
        ('--dob-time',),
        required=True,
        prompt='求算日期',
        help='生辰八字 (YYYY-MM-DD HH:MM:SS)'
    )

    PARAM_GENDER = click.Option(
        ('--gender',),
        required=True,
        prompt='性别',
        help='求算人性别(男/女)',
        type=EnumChoice(Gender, case_sensitive=False)
    )

    PARAM_DAYUN_NUMBER = click.Option(
        ('--dayun-number',),
        required=False,
        default=7,
        type=int,
        help='计算大运的次数'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ba_zi = None
        self.help = "根据阳历转换阴历，并生成八字、十神、大运等基本信息。"
        self.params = [
            self.PARAM_NAME, self.PARAM_DOB_TIME, self.PARAM_GENDER, self.PARAM_DAYUN_NUMBER, self.PARAM_FORMAT
        ]

    @classmethod
    def get_name_param(cls, **kwargs) -> str:
        return kwargs.get(cls.PARAM_NAME.name, 'UNKNOWN')

    @classmethod
    def get_gender_param(cls, **kwargs) -> Gender:
        return kwargs.get(cls.PARAM_GENDER.name)

    @classmethod
    def get_dayun_number_param(cls, **kwargs) -> int:
        return kwargs.get(cls.PARAM_DAYUN_NUMBER.name)

    @classmethod
    def get_dob_time_param(cls, **kwargs) -> str:
        return kwargs.get(cls.PARAM_DOB_TIME.name)

    def get_bazi_chart(self, **kwargs):
        _dob_time = self.get_dob_time_param(**kwargs)
        _gender = self.get_gender_param(**kwargs)

        cf = ChartConf().set_gender(gender=_gender).set_dob(dob=_dob_time)
        cg = cf.build()

        _flag = cg.get_flag_for_gender_and_chinese_zodiac(
            gender=cg.gender, dizhi_year=cg.gan_zhi_calendar.year.di_zhi
        )

        (
            cf
            .add_task(
                (
                    cg.standard_start_age,
                    {
                        "start_age": cg.get_start_age(
                            dob=cg.dob,
                            flag_for_gender_and_chinese_zodiac=_flag
                        )
                    },

                )
            )
            .add_task((cg.get_chinese_zodiac, {"type_": cg.gan_zhi_calendar.year.di_zhi.type},))
            .add_task((cg.get_day_master, {"day_pillar": cg.gan_zhi_calendar.day},))
            .add_task((cg.generate_main_destiny, {"num": self.get_dayun_number_param(**kwargs), "flag": _flag},))
            .add_task((cg.generate_ba_zi, None,))
            .add_task((cg.generate_shi_shen, None,))
        )
        cf.generate()
        res = cf.results

        return res

    def to_table(self, results: dict):
        for func_name, result in results.items():
            click.echo(f"{str(func_name).title():=^50}")
            click.echo(f"{str(result)}")

    def to_json(self, results: dict) -> str:
        tmp = {}
        for func_name, result in results.items():
            if isinstance(result, BaseModel):
                tmp[func_name] = result.model_dump(mode='json')
            else:
                tmp[func_name] = result
        return json.dumps(tmp, ensure_ascii=False)


@numerology_group.command(cls=GenerateBaZiChartCommand)
def generate_bazi_results(**kwargs):
    try:
        command = GenerateBaZiChartCommand(name=GenerateBaZiChartCommand.__name__)
        res = command.get_bazi_chart(**kwargs)
        _format = command.get_format_param(**kwargs)
        match _format.value:
            case 'table':
                command.to_table(results=res)
            case 'json':
                _json = command.to_json(results=res)
                click.echo(_json)
            case _:
                click.echo(res)
        return res
    except Exception as e:
        click.echo(e)


def main():
    numerology_group()
