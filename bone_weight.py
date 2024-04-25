from constants import *
from metainfo import MetaInfo


class BoneWeight(MetaInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.bone_weight = self.calc_bone_weight()

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        骨重：{self.bone_weight}
        箴言：{LIFE_WEIGHT_MAPPING[str(self.bone_weight)]}
        '''
        return msg

    def calc_bone_weight(self):
        weight = 0
        weight += LIFE_WEIGHT_YEAR_RATIO[self.nian_zhu]
        weight += LIFE_WEIGHT_MONTH_RATIO[str(self.lunar_month)]
        weight += LIFE_WEIGHT_DAY_RATIO[str(self.lunar_day)]
        weight += LIFE_WEIGHT_HOUR_RATIO[str(self.birthday_normal.hour)]
        return int(weight) if weight.is_integer() else round(weight, 1)
