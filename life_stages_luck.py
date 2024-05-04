
from ba_zi_elements import BaZiElements
from utils import *


class LifeStagesLuck(BaZiElements):
    """
    喜用则这段时间比较顺利
    忌凶则不太顺利

    |少年|青年|中年|晚年|
    |:-:|:-:|:-:|:-:|
    |年干|月干|日元|时干|
    |*1-9岁*|19-27岁||*46-54岁*|
    |年支|月令|日支|时支|
    |*10-18岁*|*28-36岁*|*37-45岁*|*55岁以后*|
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)

        self.kid_age = self.elements_relationships_mapping[self.nian_gan_element]
        self.teenage = self.elements_relationships_mapping[self.nian_zhi_element]
        self.young_adult = self.elements_relationships_mapping[self.yue_gan_element]
        self.adult = self.elements_relationships_mapping[self.yue_zhi_element]
        self.elder_adult = self.elements_relationships_mapping[self.ri_zhi_element]
        self.old_age = self.elements_relationships_mapping[self.shi_gan_element]
        self.elder_age = self.elements_relationships_mapping[self.shi_zhi_element]

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        ## 人生阶段运势：
        年柱少年                 月柱青年                 日柱中年               时柱晚年
        年干（1-9岁）            月干（19-27岁）           日元（自己）           时干（46-54岁）
        {self.kid_age}          {self.young_adult}                                {self.old_age}
        年支（10-18岁）          月令（28-36岁）           日支（37-45岁）        时支（晚年）
        {self.teenage}          {self.adult}          {self.elder_adult}       {self.elder_age}
        '''
        return msg

