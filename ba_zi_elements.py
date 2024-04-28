from collections import Counter

from elements_explain import ElementsExplain
from metainfo import MetaInfo
from utils import *


class BaZiElements(MetaInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.primary_element = get_heavenly_stem_element(self.ri_gan)
        self.support_element = SWAPPED_ELEMENTS_SUPPORTING[self.primary_element]
        self.self_strong = self.calc_element_strength()

        self.elements_relationships = self.calc_element_relationship()
        self.elements_weight = self.calc_element_weight()
        elements_weight_rounded = {element: round(weight, 2) for element, weight in self.elements_weight.items()}

        self.elements_relationships_mapping = {
            element: (ELEMENTS_RELATIONS[i], elements_weight_rounded[element])
            for i, element in enumerate(self.elements_relationships)
        }

        self.all_elements = [self.nian_gan_element, self.nian_zhi_element,
                             self.yue_gan_element, self.yue_zhi_element,
                             self.ri_zhi_element,
                             self.shi_gan_element, self.shi_zhi_element, ]

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

        if self.explain_append:
            self.elements_explain = ElementsExplain(self)

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        ## 五行分析
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
            msg += str(self.elements_explain)

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
                    positive_weight += GAN_ZHI_POSITION_WEIGHT[row][col]
                else:
                    negative_weight -= GAN_ZHI_POSITION_WEIGHT[row][col]

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
            elements_sequence.append(ELEMENTS_SUPPORTING[self.primary_element])
            elements_sequence.append(ELEMENTS_OPPOSING[self.primary_element])
            elements_sequence.append(SWAPPED_ELEMENTS_OPPOSING[self.primary_element])
            elements_sequence.append(SWAPPED_ELEMENTS_SUPPORTING[self.primary_element])
            elements_sequence.append(self.primary_element)
        else:
            elements_sequence.append(self.primary_element)
            elements_sequence.append(SWAPPED_ELEMENTS_SUPPORTING[self.primary_element])
            elements_sequence.append(ELEMENTS_SUPPORTING[self.primary_element])
            elements_sequence.append(SWAPPED_ELEMENTS_OPPOSING[self.primary_element])
            elements_sequence.append(ELEMENTS_OPPOSING[self.primary_element])

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
