import click

from numerology_cli.commands.base import EnumChoice, numerology_group, BaseCommand
from numerology.const.gender import Gender


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
            self.PARAM_NAME, self.PARAM_DOB_TIME, self.PARAM_GENDER,self.PARAM_DAYUN_NUMBER, self.PARAM_FORMAT
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
        _gender = self.get_gender_param(**kwargs).value
        _dayun_number = self.get_dayun_number_param(**kwargs)
        res = self.get_bazi(dob_time=_dob_time, gender=_gender,dayun_number=_dayun_number)
        res.update(
            {
                'name': self.get_name_param(**kwargs),
            }
        )
        return res

    def to_table(self, results: dict):
        dayun = []
        for combo in results['da_yun']:
            tian_gan, di_zhi = combo.get('tian_gan'), combo.get('di_zhi')
            dayun.append(
                f"{tian_gan.name}{di_zhi.name}"
                f"|{tian_gan.shi_shen.value}-{di_zhi.shi_shen.value}"
                f"|{tian_gan.element.base.name}"
                f"{di_zhi.element.base.name}"
            )
        print('\n八字排盘结果如下:')
        print('求人算名: ', results['name'])
        print('求人性别: ', results['gender'])
        print('公历日期: ', results['dob_time'])
        print('农历日期: ', results['lunar_dob_time'])
        print('日柱用神: ', results['primary_element'])
        print('大运:', ' -> '.join(dayun))
        print(self.ba_zi.print_formatted_display(results=results['details']))


@numerology_group.command(cls=GenerateBaZiChartCommand)
def generate_bazi_results(**kwargs):
    try:
        command = GenerateBaZiChartCommand(name=GenerateBaZiChartCommand.__name__)
        res = command.get_bazi_chart(**kwargs)
        _format = command.get_format_param(**kwargs)
        if _format == 'table':
            command.to_table(res)
        else:
            print(res)
        return res
    except Exception as e:
        print(e)


def main():
    numerology_group()
