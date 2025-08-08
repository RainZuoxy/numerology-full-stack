from abc import ABC, abstractmethod
from datetime import datetime
from functools import partial
from typing import Any, Union, List, Callable, Tuple, Dict

from numerology.const import Gender
from numerology.const.datetime_format import DateTimeFormat
from numerology.core.chart import BaZiChartGenerateMixin, ShiShenGenerateMixin
from numerology.core.ganzhi_calendar import GanZhiCalendar
from numerology.models import MainInfoChart
from numerology.models.chart import ShiShenChart, GanZhiChart


class ChartTasks:

    @classmethod
    def get_shi_shen(cls):
        ...

    @classmethod
    def get_ba_zi(cls):
        ...

    @classmethod
    def get_preferred_shi_shen(cls):
        ...

    @classmethod
    def get_dread_shi_shen(cls):
        ...

    # @classmethod
    # def get


class ChartGenerator(BaZiChartGenerateMixin, ShiShenGenerateMixin):

    def __init__(self, dob: datetime, gender: Gender):
        self.dob = dob
        self.gender = gender

    def build(self):
        self.gan_zhi_calendar = GanZhiCalendar(dob=self.dob)
        self.main_chart = MainInfoChart(dob=self.dob, gender=self.gender)
        return self

    def generate_shi_shen(self):
        day_master = self.get_day_master(day_pillar=self.gan_zhi_calendar.day)
        get_shi_shen = partial(self.get_shi_shen, day_master=day_master)
        get_shi_shen_by_cang_gan = partial(self.get_shi_shen_by_cang_gan, day_master=day_master)

        return ShiShenChart(
            tg_year=get_shi_shen(
                target=self.gan_zhi_calendar.year.tian_gan
            ),
            dz_year=get_shi_shen_by_cang_gan(
                di_zhi=self.gan_zhi_calendar.year.di_zhi.type
            ),
            tg_month=get_shi_shen(
                target=self.gan_zhi_calendar.month.tian_gan
            ),
            dz_month=get_shi_shen_by_cang_gan(
                di_zhi=self.gan_zhi_calendar.month.di_zhi.type
            ),
            dz_day=get_shi_shen_by_cang_gan(
                di_zhi=self.gan_zhi_calendar.day.di_zhi.type
            ),
            tg_hour=get_shi_shen(
                target=self.gan_zhi_calendar.hour.tian_gan
            ),
            dz_hour=get_shi_shen_by_cang_gan(
                di_zhi=self.gan_zhi_calendar.hour.di_zhi.type
            ),
        )

    def generate_ba_zi(self):
        return GanZhiChart(
            tg_year=self.gan_zhi_calendar.year.tian_gan,
            dz_year=self.gan_zhi_calendar.year.di_zhi,
            tg_month=self.gan_zhi_calendar.year.tian_gan,
            dz_month=self.gan_zhi_calendar.year.di_zhi,
            tg_day=self.gan_zhi_calendar.day.tian_gan,
            dz_day=self.gan_zhi_calendar.day.di_zhi,
            tg_hour=self.gan_zhi_calendar.hour.tian_gan,
            dz_hour=self.gan_zhi_calendar.hour.di_zhi,
        )

    def generate_main_destiny(self, flag:bool, num:int):
        main_destiny = self.get_main_destiny(
            month_pillar=self.gan_zhi_calendar.month,
            flag_for_gender_and_chinese_zodiac=flag,
            num=num
        )
        tmp = []
        for (tg,dz,) in main_destiny:
            tmp.append(f"{tg.type.value}{dz.type.value}")
        return tmp

class ChartConf:
    _chart_conf: dict[str, Any]
    _tasks: List[Tuple[Callable, Dict[str, Any]]]
    _results: Dict
    """
    _tasks: [ (function, params,), ... ]
    """

    def __init__(self, conf: dict = None, task: Any = None):

        self._chart_conf = conf if conf else {}
        self._tasks = task if task else []
        self._results = {}

    @property
    def results(self):
        return self._results

    def _set(self, key: str, value: Any) -> "ChartConf":
        self._chart_conf[key] = value
        return self

    def set_gender(self, gender: Union[str, Gender]) -> "ChartConf":
        if isinstance(gender, str) and gender.upper() not in Gender.__members__:
            raise ValueError(f"gender must be in {Gender.__members__}")

        if isinstance(gender, str) and gender.upper() in Gender.__members__:
            gender = Gender[gender.upper()]

        self._set("gender", gender)
        return self

    def set_dob(self, dob: Union[str, datetime], dt_format: str = DateTimeFormat.ISO_FORMAT.value) -> "ChartConf":
        if isinstance(dob, str):
            try:
                dob = datetime.strptime(dob, dt_format)
            except ValueError:
                raise ValueError(f"invalid datetime format {dt_format} to convert '{dob}'") from None

        self._set("dob", dob)

        return self

    def add_task(self, task: Any) -> "ChartConf":
        self._tasks.append(task)
        return self

    def build(self) -> ChartGenerator:
        return ChartGenerator(**self._chart_conf).build()

    def generate(self):

        for _task, _params in self._tasks:
            if _task.__name__ not in self._results:
                _result = _task(**_params) if _params else _task()
                self._results[_task.__name__] = _result

        return self

    def get_task_result(self, task_name: str) -> Any:
        return self._results.get(task_name)


class TaskConf(ABC):

    @abstractmethod
    def task_mapping(self):
        pass

    def get_generator_type(self):
        pass

    def validate_task(self, task_types):
        tmp = []
        for task_type in task_types:
            if self.task_mapping().get(task_type):
                tmp.append(task_type)

        return tmp

    def add_tasks(self, task_types):
        _task_types = self.validate_task(task_types=task_types)
        tmp = ...
        return tmp


if __name__ == '__main__':
    import pprint


    class BaZiTaskConf(TaskConf):
        def task_mapping(self):
            cg = ChartGenerator
            return {
                "generate_ba_zi": cg.generate_ba_zi,
                "generate_shi_shen": cg.generate_shi_shen,
            }


    cf = ChartConf().set_gender(gender=Gender.MALE).set_dob(dob="1983-02-09 18:30:00")
    cg = cf.build()
    (
        cf
        .add_task(
            (
                cg.standard_start_age,
                {
                    "start_age": cg.get_start_age(
                        dob=cg.dob,
                        flag_for_gender_and_chinese_zodiac=cg.get_flag_for_gender_and_chinese_zodiac(
                            gender=cg.gender, dizhi_year=cg.gan_zhi_calendar.year.di_zhi
                        )
                    )
                },

            )
        )
        .add_task((cg.get_chinese_zodiac, {"type_": cg.gan_zhi_calendar.year.di_zhi.type},))
    )
    cf.generate()
    (
        cf
        .add_task((cg.generate_ba_zi, None))
        .add_task((cg.generate_shi_shen, None,))
    )
    cf.generate()
    res = cf.results
    # for k, v in cf.results.items():
    #     print(k)
    #     print(v)
    pprint.pprint(
        {
            k: v if isinstance(v, (int, str, float,)) else v.model_dump() for k, v in cf.results.items()
        },
        indent=4,
        depth=4)
    #
    # cg = ChartGenerator(dob="1996-01-19 09:30:00", gender=Gender.MALE)
    # ss = cg.build().generate_shi_shen()
    # print(ss.model_dump_json())
