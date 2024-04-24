from collections import Counter

from metainfo import MetaInfo
from utils import *


class BaZiElements(MetaInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.primary_element = get_heavenly_stem_element(self.ri_gan)
        self.support_element = SWAPPED_WU_XING_XIANG_SHENG[self.primary_element]
        self.self_strong = self.calc_element_strength()

        self.elements_relationships = self.calc_element_relationship()
        self.elements_weight = self.calc_element_weight()
        elements_weight_rounded = {element: round(weight, 2) for element, weight in self.elements_weight.items()}

        self.elements_relationships_mapping = {
            element: (ELEMENTS_RELATIONS[i], elements_weight_rounded[element])
            for i, element in enumerate(self.elements_relationships)
        }

        self.elements_matrix = [
            [
                self.nian_gan_element, self.yue_gan_element, self.ri_gan_element, self.shi_gan_element
            ],
            [
                self.nian_zhi_element, self.yue_zhi_element, self.ri_zhi_element, self.shi_zhi_element
            ]
        ]

        if self.self_strong:
            self.supporting_elements_sequence = self.elements_relationships[:3]
            self.opposing_elements_sequence = self.elements_relationships[3:]
        else:
            self.supporting_elements_sequence = self.elements_relationships[:2]
            self.opposing_elements_sequence = self.elements_relationships[2:]

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        五行强弱：{"强" if self.self_strong else "弱"}
        喜用：{self.supporting_elements_sequence}
        忌凶：{self.opposing_elements_sequence}
        '''

        elements_relations = [f"{key}:{value}" for key, value in self.elements_relationships_mapping.items()]
        msg += f'''
        五行运气：
        {"  ".join(elements_relations)}
        '''

        if self.explain_append:
            gan_details = GAN_DETAILS[self.ri_gan]
            msg += f'''
        干支五行解析：
        日主：{self.ri_gan}（{gan_details['yinyang']}{gan_details['element']}）
        {self.append_gan_details(self.ri_gan)}
            '''

            element_details = self.append_element_details(self.ri_gan_element)
            msg += f'''
        五行：{self.ri_gan_element}
        {element_details['explain']}
        幸运色：{element_details['color']}
        幸运数字：{element_details['number']}
        幸运方位：{element_details['direction']}
        最佳相处方式：{element_details['company_with']}
            '''

        return msg

    def calc_element_strength(self):
        """
        五行相生记正分，相同记正分，相克记负分
        如果八字的加分大于50则为身强，扣分大于50则为身弱。
        :return:
        """

        positive_weight = 0
        negative_weight = 0
        for row in range(len(self.element_matrix)):
            for col in range(len(self.element_matrix[row])):
                if self.element_matrix[row][col] in [self.primary_element, self.support_element]:
                    positive_weight += GAN_ZHI_WU_XING_WEIGHT[row][col]
                else:
                    negative_weight += GAN_ZHI_WU_XING_WEIGHT[row][col]

        if positive_weight > 50:
            return True
        elif negative_weight < -50:
            return False
        return False

    def calc_element_relationship(self):
        """
        运气公式：
        |名称|变化|身强|身弱|
        |:-:|:-:|:-:|:-:|
        |旺|快涨|我生的|同我的|
        |相|慢涨|我克的|生我的|
        |休|横盘|克我的|我生的|
        |囚|慢跌|生我的|我克的|
        |死|快跌|同我的|克我的|
        :return:
        """
        elements_sequence = []
        if self.self_strong:
            elements_sequence.append(WU_XING_XIANG_SHENG[self.primary_element])
            elements_sequence.append(WU_XING_XIANG_KE[self.primary_element])
            elements_sequence.append(SWAPPED_WU_XING_XIANG_KE[self.primary_element])
            elements_sequence.append(SWAPPED_WU_XING_XIANG_SHENG[self.primary_element])
            elements_sequence.append(self.primary_element)
        else:
            elements_sequence.append(self.primary_element)
            elements_sequence.append(SWAPPED_WU_XING_XIANG_SHENG[self.primary_element])
            elements_sequence.append(WU_XING_XIANG_SHENG[self.primary_element])
            elements_sequence.append(SWAPPED_WU_XING_XIANG_KE[self.primary_element])
            elements_sequence.append(WU_XING_XIANG_KE[self.primary_element])

        return elements_sequence

    def calc_element_weight(self):
        ba_zi_elements_list = [
            self.nian_gan_element, self.nian_zhi_element,
            self.yue_gan_element, self.yue_zhi_element,
            self.ri_gan_element, self.ri_zhi_element,
            self.shi_gan_element, self.shi_zhi_element
        ]

        elements_count = Counter(ba_zi_elements_list)

        elements_weight = {}
        element_to_index = {element: idx for idx, element in enumerate(self.elements_relationships)}
        for element, idx in element_to_index.items():
            elements_weight[element] = round((elements_count[element] / 8), 2)
            elements_weight[element] += ELEMENTS_POSITION_DELTA[idx]
            elements_weight[element] += ZODIAC_ELEMENT_WEIGHT if element == self.zodiac_element else 0

        return elements_weight

    def append_element_details(self, zhu):
        conditions = {
            '木': {
                'explain': "木主慈，以仁为主。名日曲直，体形曲而直立。",
                'color': "绿色/青色",
                'number': "3/8",
                'direction': "东",
                'company_with': '装可怜、共情、卖惨、吃软不吃硬',
            },
            '火': {
                'explain': "火主礼，名日炎上，为向上发光、发热、温暖之意。",
                'color': "红色、赤色、橋红色、粉红色",
                'number': "2/7",
                'direction': "南",
                'company_with': '夸赞，彩虹屁，避免硬碰硬',
            },
            '土': {
                'explain': "土主信， 土日稼穑，为生券万物、券育、孕育之意",
                'color': "黄色",
                'number': "5/10",
                'direction': "中",
                'company_with': '遵守承诺，给与足够的信任',
            },
            '金': {
                'explain': "金主义，金日从革，为变革、肃清之意。",
                'color': "白色、金色",
                'number': "4/9",
                'direction': "西",
                'company_with': '主动承担责任，讲义气，动之以情，不要晓之以理',
            },
            '水': {
                'explain': "水主智，水称为润下，为滋润万物、寒冷向下之意",
                'color': "黑色",
                'number': "1/6",
                'direction': "北",
                'company_with': '多包容、以理服人、温和处事',
            },
        }
        return conditions[zhu]

    def append_gan_details(self, gan):
        conditions = {
            '甲': '有恻隐之心、上进心、有情有义、喜欢为人挺身而出、说话直、善良，但缺乏应变能力、做事多劳苦',
            '乙': '富有同情心、温柔、苗条、但内心占有欲强、独立性差、多虑',
            '丙': '朝气蓬勃、热情开朗、适合社交活动、懂礼貌、爱面子、没耐心、易被误解为好大喜功',
            '丁': '外静内进、思想缜密、讲文明、给人启示、但是多疑与心机',
            '戊': '诚实、厚重沉稳、为人憨直、有主见、有持久力、但是固执',
            '己': '重视内涵、多才多艺、行事依规蹈矩、但度量欠广，易生疑心',
            '庚': '精神粗旷豪爽、意气轻燥、性情刚烈而重义气，个性好胜、具有破坏性、人缘佳、易相处',
            '辛': '阴沉，温润秀气、重感情、虛荣心强而爱好面子、有强烈的自尊心、但缺乏坚强的意志',
            '壬': '清浊并容，宽宏大度、能潜伏和包容，富于勇气、但依赖性强、漫不经心',
            '癸': '平静柔和、内向、勤勉力行、但爱好猜臆、注重原则不务实际、时有破坏性、重情调、喜钻牛角尖',
        }
        return conditions[gan]
