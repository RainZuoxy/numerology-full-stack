# from numerology.const.wuxing import WuXing, TianGan, DiZhi
# from numerology.core.base.wuxing import WuXing
# import datetime
# from lunardate import LunarDate

# from numerology.core.shishen import ShiShen
# from numerology.core.tiangan import TianGan, TianGanItems
# from numerology.core.dizhi import DiZhi


if __name__ == '__main__':
    # def test_relationship(c):
    #     element = c().current_node(name=BaseWuXing.EARTH.value)
    #     print(element.data)
    #     print(element.produce().data, '生', element.data)
    #     print(element.support().data, '助', element.data)
    #     print(element.weaken().data, '泄', element.data)
    #     print(element.consume().data, '耗', element.data)
    #     print(element.restrain().data, '克', element.data)
    #     # branches1 = Branches()
    #     # branches2 = Branches()
    #     # print(id(branches1), id(branches2))


    def test_nayin():
        nayin = [
            '海中金', '炉中火', '大林木',
            '路旁土', '剑锋金', '山头火',
            '洞下水', '城墙土', '白腊金',
            '杨柳木', '泉中水', '屋上土',
            '霹雳火', '松柏木', '常流水',
            '沙中金', '山下火', '平地木',
            '壁上土', '金箔金', '佛灯火',
            '天河水', '大驿土', '钗钏金',
            '桑松木', '大溪水', '沙中土',
            '天上火', '石榴木', '大海水',
        ]
        # count = -0.5
        d = DiZhi().get_names()
        t = TianGan().get_names()
        print('[')
        for i in range(1, 61):
            # count += 0.5
            i1, i2 = (i % 10) - 1, (i % 12) - 1
            # print(f'"{t[i1]}{d[i2]}":"{nayin[int(count)]}",')
            print(f'"{t[i1]}{d[i2]}",')

        print(']')
        # date=LunarDate.fromSolarDate(2023,9,22)

        # print(date)
        # cur = datetime.datetime.now()
        # t = cur.time()
        # print(t)


    # def test_relationship2(c):
    #     # f"{element.produce().data.name}({element.produce().data.wuxing.value}/{'阳' if element.produce().data.yinyang else '阴'})"
    #     element = c().current_node(name=BaseTianGan.JIA.value)
    #     print(element.data.name)
    #     print('/'.join([f"{i.data.name}" for i in element.produce()]), '-生-', element.data.name)
    #     print('/'.join([f"{i.data.name}" for i in element.support()]), '-助-', element.data.name)
    #     print('/'.join([f"{i.data.name}" for i in element.weaken()]), '-泄-', element.data.name)
    #     print('/'.join([f"{i.data.name}" for i in element.consume()]), '-耗-', element.data.name)
    #     print('/'.join([f"{i.data.name}" for i in element.restrain()]), '-克-', element.data.name)


    def test_relationship3(c, name):
        element = c().current_node(name=name)
        print(element.data.name)
        print('/'.join([f"{i.data.name}" for i in element.produce()]), '-生-', element.data.name)
        print('/'.join([f"{i.data.name}" for i in element.support()]), '-助-', element.data.name)
        print('/'.join([f"{i.data.name}" for i in element.weaken()]), '-泄-', element.data.name)
        print('/'.join([f"{i.data.name}" for i in element.consume()]), '-耗-', element.data.name)
        print('/'.join([f"{i.data.name}" for i in element.restrain()]), '-克-', element.data.name)


    def test_shishen():
        # 日主:癸水
        a = ShiShen(rizhu=TianGan().current_node(name=BaseTianGan.GUI.value).data)
        print(
            a.get_shishen(
                target=TianGan().current_node(name=BaseTianGan.BING.value).data
            )
        )


    # print(f"{'test_relationship:wuxing':=^100}")
    # test_relationship(WuXing)
    # print(f"{'test_nayin':=^100}")
    # test_nayin()
    # print(f"{'test_relationship:tiangan':=^100}")
    # test_relationship2(TianGan)
    # print(f"{'test_relationship:dizhi':=^100}")
    # test_relationship3(DiZhi, BaseDiZhi.CHOU.value)
    # print('-' * 100)
    # test_relationship3(DiZhi, BaseDiZhi.ZI.value)
    # print('-' * 100)
    # test_relationship3(DiZhi, BaseDiZhi.YIN.value)
    # print('-' * 100)
    # test_relationship3(DiZhi, BaseDiZhi.SI.value)
    # print('-' * 100)
    # test_relationship3(DiZhi, BaseDiZhi.WU.value)
    # print('-' * 100)
    # test_relationship3(DiZhi, BaseDiZhi.YOU.value)
    # print('-' * 100)

    a = TianGanItems
    print(a)
