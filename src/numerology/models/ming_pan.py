from typing import Union, List, Dict, Any
from datetime import datetime

from pydantic import BaseModel

from numerology.const.wu_xing import Gender
from numerology.tools.datetimes import convert_to_datetime, convert_to_lunar_datetime
from numerology.models.ba_zi import BaZiGenerator


class BaZi(BaseModel):
    dob_time: Union[str, datetime]
    lunar_dob_time: datetime = None
    ba_zi_generator: BaZiGenerator = None

    def model_post_init(self, __context: Any):
        self.dob_time = self.clean_birth_datetime(self.dob_time)
        self.lunar_dob_time = self.convert_to_lunar_datetime(self.get_datetime())
        self.ba_zi_generator = BaZiGenerator(dob_time=self.dob_time, lunar_dob_time=self.get_lunar_datetime())
        self._init()

    def _init(self):
        self._analysis_ba_zi()

    @classmethod
    def clean_birth_datetime(cls, dob_time: Union[str, datetime]) -> datetime:
        try:
            return convert_to_datetime(datetime_string=dob_time.strip()) if isinstance(dob_time, str) else dob_time
        except Exception as e:
            raise ValueError('The birth datetime is incorrect')

    @classmethod
    def convert_to_lunar_datetime(cls, dob_time: datetime) -> datetime:
        try:
            return convert_to_lunar_datetime(dob_time)
        except Exception as e:
            raise ValueError(f'搞什么鬼, 给的是什么东西{e}')

    def get_datetime(self):
        return self.dob_time

    def get_lunar_datetime(self):
        return self.lunar_dob_time

    def _get_ba_zi_generator(self):
        return self.ba_zi_generator

    def _analysis_ba_zi(self):
        self._get_ba_zi_generator().analysis()

    def get_primary_element(self):
        return self._get_ba_zi_generator().day_pillar.tian_gan.wu_xing.get_name()

    def get_results(self) -> List[Dict[str, str]]:
        return [pillar.__dict__() for pillar in self.ba_zi_generator.get_pillars()]

    def get_wu_xing(self) -> List[Dict[str, str]]:
        return [pillar.get_wu_xing() for pillar in self.ba_zi_generator.get_pillars()]

    def get_shi_shen(self):
        return [pillar.get_shi_shen() for pillar in self.ba_zi_generator.get_pillars()]

    def get_dayun(self, gender: Gender, num: int = 7):
        origin_tg_index_by_month = self.ba_zi_generator.month_pillar.tian_gan.sequence
        origin_dz_index_by_month = self.ba_zi_generator.month_pillar.di_zhi.sequence
        step = 1 if gender.value == self.ba_zi_generator.year_pillar.di_zhi.positive else -1

        for i in range(num):
            origin_tg_index_by_month += step
            tg_dayun_index = origin_tg_index_by_month % 10

            origin_dz_index_by_month += step
            dz_dayun_index = origin_dz_index_by_month % 12
            from numerology.models.jia_zi import TianGan, DiZhi

            yield TianGan.get_tian_gan_by_index(tg_dayun_index), DiZhi.get_di_zhi_by_index(dz_dayun_index)

    def results(self) -> dict:
        _results = {}
        for pillar in self.ba_zi_generator.get_pillars():
            tian_gan = self._format_results(pillar.tian_gan)
            di_zhi = self._format_results(pillar.di_zhi)
            _results[pillar.name] = {"tian_gan": tian_gan, "di_zhi": di_zhi}

        return _results

    @staticmethod
    def print_formatted_display(results: dict):
        display_text = []
        for name, details in results.items():
            display_text.append(
                f"{name}:\t天干: {details['tian_gan']}\t地支: {details['di_zhi']}"
            )

        return "\n".join(display_text)

    def _format_results(self, item):
        caption = [item.wu_xing.name]

        if item.shi_shen:
            caption.append(item.shi_shen.value)

        caption.append(("阳" if item.positive else "阴"))

        return f"{item.name} ({'-'.join(caption)})"

    def print_wu_xing_formatted_display(self):
        display_text = []
        for pillar in self.ba_zi_generator.get_pillars():
            pillar_wu_xing = pillar.get_wu_xing()

            tian_gan = pillar_wu_xing.get("tian_gan")
            tian_gan = f"{tian_gan.get('name')} (" + ("阳" if tian_gan.get('positive') else "阴") + ")"
            di_zhi = pillar_wu_xing.get("di_zhi")
            di_zhi = f"{di_zhi.get('name')} (" + ("阳" if di_zhi.get('positive') else "阴") + ")"

            display_text.append(
                f"{pillar_wu_xing.get('name')}:\t天干: {tian_gan}\t地支: {di_zhi}"
            )

        return "\n".join(display_text)

    def print_shi_shen_formatted_display(self):
        display_text = []
        for pillar in self.ba_zi_generator.get_pillars():
            pillar_shi_shen = pillar.get_shi_shen()

            tian_gan = pillar_shi_shen.get("tian_gan")
            tian_gan = f"{tian_gan.get('name')} (" + ("阳" if tian_gan.get('positive') else "阴") + ")"
            di_zhi = pillar_shi_shen.get("di_zhi")
            di_zhi = f"{di_zhi.get('name')} (" + ("阳" if di_zhi.get('positive') else "阴") + ")"

            display_text.append(
                f"{pillar_shi_shen.get('name')}:\t天干: {tian_gan}\t地支: {di_zhi}"
            )

        return "\n".join(display_text)
