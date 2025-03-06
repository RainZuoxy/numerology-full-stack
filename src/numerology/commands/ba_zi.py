import click

from numerology.commands.base import EnumChoice, numerology_group, BaseCommand
from numerology.const.wu_xing import Gender
from numerology.models.ming_pan import BaZi


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__ba_zi = None
        self.help = "根据阳历转换阴历，并生成八字、十神、大运等基本信息。"
        self.params = [self.PARAM_NAME, self.PARAM_DOB_TIME, self.PARAM_GENDER, self.PARAM_FORMAT]

    @classmethod
    def get_name_param(cls, **kwargs) -> str:
        return kwargs.get(cls.PARAM_NAME.name, 'UNKNOWN')

    @classmethod
    def get_gender_param(cls, **kwargs) -> Gender:
        return kwargs.get(cls.PARAM_GENDER.name)

    @classmethod
    def get_dob_time_param(cls, **kwargs) -> str:
        return kwargs.get(cls.PARAM_DOB_TIME.name)

    def get_bazi_chart(self, **kwargs):
        _dob_time = self.get_dob_time_param(**kwargs)
        _gender = self.get_gender_param(**kwargs)
        self.__ba_zi = BaZi(dob_time=_dob_time)
        return {
            'name': self.get_name_param(**kwargs),
            'gender': '男' if _gender.name == Gender.MALE.name else '女',
            'dob_time': self.__ba_zi.get_datetime(),
            'lunar_dob_time': self.__ba_zi.get_lunar_datetime(),
            'primary_element': self.__ba_zi.get_primary_element(),
            'da_yun': ', '.join([f"{tg.name}{dz.name}" for tg, dz in self.__ba_zi.get_dayun(_gender)]),
            'details': self.__ba_zi.results()
        }

    def to_table(self, results: dict):
        print('\n八字排盘结果如下:')
        print('求人算名: ', results['name'])
        print('求人性别: ', results['gender'])
        print('公历日期: ', results['dob_time'])
        print('农历日期: ', results['lunar_dob_time'])
        print('日柱用神: ', results['primary_element'])
        print('大运:', results['da_yun'])
        print(self.__ba_zi.print_formatted_display(results=results['details']))


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
