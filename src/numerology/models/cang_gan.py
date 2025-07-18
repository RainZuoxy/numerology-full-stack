from numerology.const import DiZhiType, TianGanType
from numerology.models.base import NumerologyBaseMeta, BaseCangGan


class CangGan(metaclass=NumerologyBaseMeta):

    # 木芽破土，地温回升，冻土残存
    YIN = BaseCangGan(
        di_zhi=DiZhiType.YIN,
        zhu_qi=TianGanType.JIA, zhong_qi=TianGanType.BING, yu_qi=TianGanType.WU
    )
    # 草木繁茂，纯木之气统治
    MAO = BaseCangGan(
        di_zhi=DiZhiType.MAO,
        zhu_qi=TianGanType.YI
    )
    # 土湿木余，春雨蓄水库
    CHEN = BaseCangGan(
        di_zhi=DiZhiType.CHEN,
        zhu_qi=TianGanType.WU, zhong_qi=TianGanType.YI, yu_qi=TianGanType.GUI
    )
    # 火势初旺，金属受热，土气蒸腾
    SI = BaseCangGan(
        di_zhi=DiZhiType.SI,
        zhu_qi=TianGanType.BING, zhong_qi=TianGanType.GENG, yu_qi=TianGanType.WU
    )
    # 烈火炎上，土焦作灰
    WU = BaseCangGan(
        di_zhi=DiZhiType.WU,
        zhu_qi=TianGanType.DING, zhong_qi=TianGanType.JI
    )
    # 土燥火余，草木枯槁待雨
    WEI = BaseCangGan(
        di_zhi=DiZhiType.WEI,
        zhu_qi=TianGanType.JI, zhong_qi=TianGanType.DING, yu_qi=TianGanType.YI
    )
    # 金气肃杀，水汽凝结，土承变革
    SHEN = BaseCangGan(
        di_zhi=DiZhiType.SHEN,
        zhu_qi=TianGanType.GENG, zhong_qi=TianGanType.REN, yu_qi=TianGanType.WU
    )
    # 金精纯粹，秋露寒锋
    YOU = BaseCangGan(
        di_zhi=DiZhiType.YOU,
        zhu_qi=TianGanType.XIN
    )
    # 土藏金火，霜降杀百草
    XU = BaseCangGan(
        di_zhi=DiZhiType.XU,
        zhu_qi=TianGanType.WU, zhong_qi=TianGanType.XIN, yu_qi=TianGanType.DING
    )
    # 寒水汹涌，木气封存待春
    HAI = BaseCangGan(
        di_zhi=DiZhiType.HAI,
        zhu_qi=TianGanType.REN, zhong_qi=TianGanType.JIA
    )
    # 至阴寒水，冰封静止
    ZI = BaseCangGan(
        di_zhi=DiZhiType.ZI,
        zhu_qi=TianGanType.GUI
    )
    # 冻土含水，金气沉眠待醒
    CHOU = BaseCangGan(
        di_zhi=DiZhiType.CHOU,
        zhu_qi=TianGanType.JI, zhong_qi=TianGanType.GUI, yu_qi=TianGanType.XIN
    )
