import argparse
from collections import Counter

from elements_explain import ElementsExplain
from metainfo import MetaInfo
from utils import *


class BaZiElements(MetaInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        # 命主五行
        self.primary_element = GAN_DETAILS[self.ri_gan]['element']
        self.support_element = SWAPPED_ELEMENTS_SUPPORTING[self.primary_element]

        # 命主自身强弱
        self.self_strong = self.calc_element_strength()
        # 命主旺衰
        self.self_positive = self.calc_positive()

        # 命主五行喜忌关系
        self.elements_strength_sequence = self.calc_elements_strength_sequence()

        # 命主五行强度
        self.elements_weight = self.calc_element_weight()

        self.elements_relationships_mapping = {
            element: (ELEMENTS_RELATIONS[i], self.elements_weight[element])
            for i, element in enumerate(self.elements_strength_sequence)
        }

        if self.self_strong:
            self.supporting_elements_sequence = self.elements_strength_sequence[:3]
            self.opposing_elements_sequence = self.elements_strength_sequence[3:]
        else:
            self.supporting_elements_sequence = self.elements_strength_sequence[:2]
            self.opposing_elements_sequence = self.elements_strength_sequence[2:]

        if self.explain_append:
            self.elements_explain = ElementsExplain(self)

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        ## 五行分析
        五行强弱：{"强" if self.self_strong else "弱"}+{'旺' if self.self_positive else '衰'}
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
        for row in range(len(self.elements_matrix)):
            for col in range(len(self.elements_matrix[row])):
                if self.elements_matrix[row][col] in [self.primary_element, self.support_element]:
                    positive_weight += GAN_ZHI_POSITION_WEIGHT[row][col]
                else:
                    negative_weight -= GAN_ZHI_POSITION_WEIGHT[row][col]

        if positive_weight > 50:
            return True
        return False

    def calc_elements_strength_sequence(self):
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

        elements_weight = {}
        element_to_index = {element: idx for idx, element in enumerate(self.elements_strength_sequence)}
        for element, idx in element_to_index.items():
            base_weight = (self.elements_count[element] / 8)
            base_weight += ELEMENTS_POSITION_DELTA[idx]
            base_weight += ZODIAC_ELEMENT_WEIGHT if element == self.zodiac_element else 0
            elements_weight[element] = round(base_weight, 2)

        return elements_weight

    def calc_positive(self):
        # 月令五行与日主相同为旺
        return GAN_DETAILS[self.ri_gan]['element'] == ZHI_DETAILS[self.yue_zhi]['element']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is a calc project of BaZi.')
    parser.add_argument('-b', '--birthday', help='The birthday of yourself, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"', required=True)
    parser.add_argument('-g', '--gander', help='The gander of yourself, default as male', action='store_true', default=True)
    parser.add_argument('-e', '--explain', help='To check whether append explain details on different attributes', action='store_true', default=False)

    args = parser.parse_args()

    print(f'Argument received: {args}')
    main_birthday = datetime.strptime(args.birthday, default_date_format)
    is_male = args.gander
    explain_append = args.explain
    prediction = BaZiElements(
        base_datetime=main_birthday,
        meta_info_display=True,
        explain_append=explain_append,
        is_male=is_male,
    )
    print(prediction)