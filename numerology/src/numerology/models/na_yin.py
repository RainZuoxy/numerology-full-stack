from numerology.const import NaYinType
from numerology.models.base import NumerologyBaseMeta, BaseNaYin


class NaYin(metaclass=NumerologyBaseMeta):
    #金
    SHA_ZHONG_JIN = BaseNaYin(
        na_yin=NaYinType.SHA_ZHONG_JIN,
        desc="沙里淘的金，量少，金中较为贫穷者，但比一般的人还要富。"
    )
    HAI_ZHONG_JIN = BaseNaYin(
        na_yin=NaYinType.HAI_ZHONG_JIN,
        desc="藏而不露，善于藏富，多为隐形富豪。"
    )
    JIAN_FENG_JIN = BaseNaYin(
        na_yin=NaYinType.JIAN_FENG_JIN,
        desc="金中最厉害者，多为社会名人或者有突出贡献。"
    )
    CHAI_CHUAN_JIN = BaseNaYin(
        na_yin=NaYinType.CHAI_CHUAN_JIN,
        desc="头上戴金，金命中最富有者。"
    )
    BAI_LA_JIN = BaseNaYin(
        na_yin=NaYinType.BAI_LA_JIN,
        desc="祭祀台上矗立的涂了金粉的白蜡，金粉少，但位置尊贵。"
    )
    JIN_BO_JIN = BaseNaYin(
        na_yin=NaYinType.JIN_BO_JIN,
        desc="极薄的金纸，量很少，用在最尊贵的地方，贵而不富。"
    )
    #火
    LU_ZHONG_HUO=BaseNaYin(
        na_yin=NaYinType.LU_ZHONG_HUO,
        desc="最小的火，有柴则着，无柴则灭。"
    )
    SHAN_XIA_HUO=BaseNaYin(
        na_yin=NaYinType.SHAN_XIA_HUO,
        desc="性格特点来得快去得也快，平地木支持燃烧。"
        # support PING_DI_MU
    )
    SHAN_TOU_HUO=BaseNaYin(
        na_yin=NaYinType.SHAN_TOU_HUO,
        desc="大林木燃烧起来的火，旺盛而持久。"
    )
    FO_DENG_HUO=BaseNaYin(
        na_yin=NaYinType.FO_DENG_HUO,
        desc="寺庙的灯火，忌熄灭，必被保护者。一生多遇贵人帮助。"
    )
    TIAN_SHANG_HUO=BaseNaYin(
        na_yin=NaYinType.TIAN_SHANG_HUO,
        desc="天上云而非火，但影响人类生活。多有因牵连而变化之事。"
    )
    PI_LI_HUO=BaseNaYin(
        na_yin=NaYinType.PI_LI_HUO,
        desc="最厉害的火，雷劈地上引起的大火。历史上多是灾难年。"
    )
    # 木
    DA_LIN_MU = BaseNaYin(
        na_yin=NaYinType.DA_LIN_MU,
        desc="森林、山头火的支持者。或做大贡献、或出大事故。"
    )
    YANG_LIU_MU = BaseNaYin(
        na_yin=NaYinType.YANG_LIU_MU,
        desc=""
    )
    PING_DI_MU = BaseNaYin(
        na_yin=NaYinType.PING_DI_MU,
        desc="灌木、杂草，是山下火燃烧材料。占地广而能量弱。"
    )
    SONG_BAI_MU = BaseNaYin(
        na_yin=NaYinType.SONG_BAI_MU,
        desc=""
    )
    SANG_SONG_MU = BaseNaYin(
        na_yin=NaYinType.SANG_SONG_MU,
        desc="桑养蚕织丝绸，一生一死热爱故乡"
    )
    SHI_LIU_MU = BaseNaYin(
        na_yin=NaYinType.SHI_LIU_MU,
        desc="庭院树，象征多子多孙。被保护的命。"
    )
