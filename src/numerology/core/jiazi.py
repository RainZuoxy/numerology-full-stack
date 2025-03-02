from enum import Enum

from numerology.core.base import Singleton, CellProperty
from numerology.const.wu_xing import BaseWuXing
from numerology.const.jiazi import JIAZI


class JiaZiItems(Enum):
    JIAZI = [CellProperty(name='甲', yinyang=True, wuxing=BaseWuXing.WOOD),
             CellProperty(name='子', yinyang=True, wuxing=BaseWuXing.WATER)]
    YICHOU = [CellProperty(name='乙', yinyang=False, wuxing=BaseWuXing.WOOD),
              CellProperty(name='丑', yinyang=False, wuxing=BaseWuXing.EARTH)]
    BINGYIN = [CellProperty(name='丙', yinyang=True, wuxing=BaseWuXing.FIRE),
               CellProperty(name='寅', yinyang=True, wuxing=BaseWuXing.WOOD)]
    DINGMAO = [CellProperty(name='丁', yinyang=False, wuxing=BaseWuXing.FIRE),
               CellProperty(name='卯', yinyang=False, wuxing=BaseWuXing.WOOD)]
    WUCHEN = [CellProperty(name='戊', yinyang=True, wuxing=BaseWuXing.EARTH),
              CellProperty(name='辰', yinyang=True, wuxing=BaseWuXing.EARTH)]
    JISI = [CellProperty(name='己', yinyang=False, wuxing=BaseWuXing.EARTH),
            CellProperty(name='巳', yinyang=False, wuxing=BaseWuXing.FIRE)]
    GENGWU = [CellProperty(name='庚', yinyang=True, wuxing=BaseWuXing.METAL),
              CellProperty(name='午', yinyang=True, wuxing=BaseWuXing.FIRE)]
    XINWEI = [CellProperty(name='辛', yinyang=False, wuxing=BaseWuXing.METAL),
              CellProperty(name='未', yinyang=False, wuxing=BaseWuXing.EARTH)]
    RENSHEN = [CellProperty(name='壬', yinyang=True, wuxing=BaseWuXing.WATER),
               CellProperty(name='申', yinyang=True, wuxing=BaseWuXing.METAL)]
    GUIYOU = [CellProperty(name='癸', yinyang=False, wuxing=BaseWuXing.WATER),
              CellProperty(name='酉', yinyang=False, wuxing=BaseWuXing.METAL)]
    JIAXU = [CellProperty(name='甲', yinyang=True, wuxing=BaseWuXing.WOOD),
             CellProperty(name='戌', yinyang=True, wuxing=BaseWuXing.EARTH)]
    YIHAI = [CellProperty(name='乙', yinyang=False, wuxing=BaseWuXing.WOOD),
             CellProperty(name='亥', yinyang=False, wuxing=BaseWuXing.WATER)]
    BINGZI = [CellProperty(name='丙', yinyang=True, wuxing=BaseWuXing.FIRE),
              CellProperty(name='子', yinyang=True, wuxing=BaseWuXing.WATER)]
    DINGCHOU = [CellProperty(name='丁', yinyang=False, wuxing=BaseWuXing.FIRE),
                CellProperty(name='丑', yinyang=False, wuxing=BaseWuXing.EARTH)]
    WUYIN = [CellProperty(name='戊', yinyang=True, wuxing=BaseWuXing.EARTH),
             CellProperty(name='寅', yinyang=True, wuxing=BaseWuXing.WOOD)]
    JIMAO = [CellProperty(name='己', yinyang=False, wuxing=BaseWuXing.EARTH),
             CellProperty(name='卯', yinyang=False, wuxing=BaseWuXing.WOOD)]
    GENGCHEN = [CellProperty(name='庚', yinyang=True, wuxing=BaseWuXing.METAL),
                CellProperty(name='辰', yinyang=True, wuxing=BaseWuXing.EARTH)]
    XINSI = [CellProperty(name='辛', yinyang=False, wuxing=BaseWuXing.METAL),
             CellProperty(name='巳', yinyang=False, wuxing=BaseWuXing.FIRE)]
    RENWU = [CellProperty(name='壬', yinyang=True, wuxing=BaseWuXing.WATER),
             CellProperty(name='午', yinyang=True, wuxing=BaseWuXing.FIRE)]
    GUIWEI = [CellProperty(name='癸', yinyang=False, wuxing=BaseWuXing.WATER),
              CellProperty(name='未', yinyang=False, wuxing=BaseWuXing.EARTH)]
    JIASHEN = [CellProperty(name='甲', yinyang=True, wuxing=BaseWuXing.WOOD),
               CellProperty(name='申', yinyang=True, wuxing=BaseWuXing.METAL)]
    YIYOU = [CellProperty(name='乙', yinyang=False, wuxing=BaseWuXing.WOOD),
             CellProperty(name='酉', yinyang=False, wuxing=BaseWuXing.METAL)]
    BINGXU = [CellProperty(name='丙', yinyang=True, wuxing=BaseWuXing.FIRE),
              CellProperty(name='戌', yinyang=True, wuxing=BaseWuXing.EARTH)]
    DINGHAI = [CellProperty(name='丁', yinyang=False, wuxing=BaseWuXing.FIRE),
               CellProperty(name='亥', yinyang=False, wuxing=BaseWuXing.WATER)]
    WUZI = [CellProperty(name='戊', yinyang=True, wuxing=BaseWuXing.EARTH),
            CellProperty(name='子', yinyang=True, wuxing=BaseWuXing.WATER)]
    JICHOU = [CellProperty(name='己', yinyang=False, wuxing=BaseWuXing.EARTH),
              CellProperty(name='丑', yinyang=False, wuxing=BaseWuXing.EARTH)]
    GENGYIN = [CellProperty(name='庚', yinyang=True, wuxing=BaseWuXing.METAL),
               CellProperty(name='寅', yinyang=True, wuxing=BaseWuXing.WOOD)]
    XINMAO = [CellProperty(name='辛', yinyang=False, wuxing=BaseWuXing.METAL),
              CellProperty(name='卯', yinyang=False, wuxing=BaseWuXing.WOOD)]
    RENCHEN = [CellProperty(name='壬', yinyang=True, wuxing=BaseWuXing.WATER),
               CellProperty(name='辰', yinyang=True, wuxing=BaseWuXing.EARTH)]
    GUISI = [CellProperty(name='癸', yinyang=False, wuxing=BaseWuXing.WATER),
             CellProperty(name='巳', yinyang=False, wuxing=BaseWuXing.FIRE)]
    JIAWU = [CellProperty(name='甲', yinyang=True, wuxing=BaseWuXing.WOOD),
             CellProperty(name='午', yinyang=True, wuxing=BaseWuXing.FIRE)]
    YIWEI = [CellProperty(name='乙', yinyang=False, wuxing=BaseWuXing.WOOD),
             CellProperty(name='未', yinyang=False, wuxing=BaseWuXing.EARTH)]
    BINGSHEN = [CellProperty(name='丙', yinyang=True, wuxing=BaseWuXing.FIRE),
                CellProperty(name='申', yinyang=True, wuxing=BaseWuXing.METAL)]
    DINGYOU = [CellProperty(name='丁', yinyang=False, wuxing=BaseWuXing.FIRE),
               CellProperty(name='酉', yinyang=False, wuxing=BaseWuXing.METAL)]
    WUXU = [CellProperty(name='戊', yinyang=True, wuxing=BaseWuXing.EARTH),
            CellProperty(name='戌', yinyang=True, wuxing=BaseWuXing.EARTH)]
    JIHAI = [CellProperty(name='己', yinyang=False, wuxing=BaseWuXing.EARTH),
             CellProperty(name='亥', yinyang=False, wuxing=BaseWuXing.WATER)]
    GENGZI = [CellProperty(name='庚', yinyang=True, wuxing=BaseWuXing.METAL),
              CellProperty(name='子', yinyang=True, wuxing=BaseWuXing.WATER)]
    XINCHOU = [CellProperty(name='辛', yinyang=False, wuxing=BaseWuXing.METAL),
               CellProperty(name='丑', yinyang=False, wuxing=BaseWuXing.EARTH)]
    RENYIN = [CellProperty(name='壬', yinyang=True, wuxing=BaseWuXing.WATER),
              CellProperty(name='寅', yinyang=True, wuxing=BaseWuXing.WOOD)]
    GUIMAO = [CellProperty(name='癸', yinyang=False, wuxing=BaseWuXing.WATER),
              CellProperty(name='卯', yinyang=False, wuxing=BaseWuXing.WOOD)]
    JIACHEN = [CellProperty(name='甲', yinyang=True, wuxing=BaseWuXing.WOOD),
               CellProperty(name='辰', yinyang=True, wuxing=BaseWuXing.EARTH)]
    YISI = [CellProperty(name='乙', yinyang=False, wuxing=BaseWuXing.WOOD),
            CellProperty(name='巳', yinyang=False, wuxing=BaseWuXing.FIRE)]
    BINGWU = [CellProperty(name='丙', yinyang=True, wuxing=BaseWuXing.FIRE),
              CellProperty(name='午', yinyang=True, wuxing=BaseWuXing.FIRE)]
    DINGWEI = [CellProperty(name='丁', yinyang=False, wuxing=BaseWuXing.FIRE),
               CellProperty(name='未', yinyang=False, wuxing=BaseWuXing.EARTH)]
    WUSHEN = [CellProperty(name='戊', yinyang=True, wuxing=BaseWuXing.EARTH),
              CellProperty(name='申', yinyang=True, wuxing=BaseWuXing.METAL)]
    JIYOU = [CellProperty(name='己', yinyang=False, wuxing=BaseWuXing.EARTH),
             CellProperty(name='酉', yinyang=False, wuxing=BaseWuXing.METAL)]
    GENGXU = [CellProperty(name='庚', yinyang=True, wuxing=BaseWuXing.METAL),
              CellProperty(name='戌', yinyang=True, wuxing=BaseWuXing.EARTH)]
    XINHAI = [CellProperty(name='辛', yinyang=False, wuxing=BaseWuXing.METAL),
              CellProperty(name='亥', yinyang=False, wuxing=BaseWuXing.WATER)]
    RENZI = [CellProperty(name='壬', yinyang=True, wuxing=BaseWuXing.WATER),
             CellProperty(name='子', yinyang=True, wuxing=BaseWuXing.WATER)]
    GUICHOU = [CellProperty(name='癸', yinyang=False, wuxing=BaseWuXing.WATER),
               CellProperty(name='丑', yinyang=False, wuxing=BaseWuXing.EARTH)]
    JIAYIN = [CellProperty(name='甲', yinyang=True, wuxing=BaseWuXing.WOOD),
              CellProperty(name='寅', yinyang=True, wuxing=BaseWuXing.WOOD)]
    YIMAO = [CellProperty(name='乙', yinyang=False, wuxing=BaseWuXing.WOOD),
             CellProperty(name='卯', yinyang=False, wuxing=BaseWuXing.WOOD)]
    BINGCHEN = [CellProperty(name='丙', yinyang=True, wuxing=BaseWuXing.FIRE),
                CellProperty(name='辰', yinyang=True, wuxing=BaseWuXing.EARTH)]
    DINGSI = [CellProperty(name='丁', yinyang=False, wuxing=BaseWuXing.FIRE),
              CellProperty(name='巳', yinyang=False, wuxing=BaseWuXing.FIRE)]
    WUWU = [CellProperty(name='戊', yinyang=True, wuxing=BaseWuXing.EARTH),
            CellProperty(name='午', yinyang=True, wuxing=BaseWuXing.FIRE)]
    JIWEI = [CellProperty(name='己', yinyang=False, wuxing=BaseWuXing.EARTH),
             CellProperty(name='未', yinyang=False, wuxing=BaseWuXing.EARTH)]
    GENGSHEN = [CellProperty(name='庚', yinyang=True, wuxing=BaseWuXing.METAL),
                CellProperty(name='申', yinyang=True, wuxing=BaseWuXing.METAL)]
    XINYOU = [CellProperty(name='辛', yinyang=False, wuxing=BaseWuXing.METAL),
              CellProperty(name='酉', yinyang=False, wuxing=BaseWuXing.METAL)]
    RENXU = [CellProperty(name='壬', yinyang=True, wuxing=BaseWuXing.WATER),
             CellProperty(name='戌', yinyang=True, wuxing=BaseWuXing.EARTH)]
    GUIHAI = [CellProperty(name='癸', yinyang=False, wuxing=BaseWuXing.WATER),
              CellProperty(name='亥', yinyang=False, wuxing=BaseWuXing.WATER)]


class JiaZi(Singleton):
    def __init__(self):
        dizhi = DiZhi().get_names()
        tiangan = TianGan().get_names()
        for i in range(1, 61):
            i1, i2 = (i % 10) - 1, (i % 12) - 1
            print(f'{i}', f'{tiangan[i1]}{dizhi[i2]}')


if __name__ == '__main__':
    import pypinyin
    from pypinyin import Style
    from numerology.core.dizhi import DiZhi
    from numerology.core.tiangan import TianGan


    def _get_wuxing(strr, c):
        a = c.current_node(data=strr)
        return str(a.data.wuxing)


    count = 0
    for i in JIAZI:
        result = pypinyin.lazy_pinyin(i, style=Style.NORMAL)
        yinyang = 'True' if count % 2 == 0 else 'False'
        print(''.join(result).upper(), end='', flush=True)
        print(f"=[CellProperty(name='{i[0]}',yinyang={yinyang}, wuxing={_get_wuxing(i[0], TianGan())}),"
              f"CellProperty(name='{i[-1]}',yinyang={yinyang}, wuxing={_get_wuxing(i[-1], DiZhi())})]")
        count += 1
