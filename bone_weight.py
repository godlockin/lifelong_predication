from constants import *
from metainfo import MetaInfo


class BoneWeight(MetaInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)
        self.bone_weight_map = self.calc_bone_weight()
        tmp_bone_weight = sum(self.bone_weight_map.values())
        self.bone_weight = int(tmp_bone_weight) if tmp_bone_weight.is_integer() else round(float(tmp_bone_weight), 1)

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        ## 称骨
        骨重：{self.bone_weight}
        箴言：{LIFE_WEIGHT_MAPPING[str(self.bone_weight)]}
        '''
        if self.explain_append:
            msg += f'''
        称骨解析：
        {self.bone_weight_map}
            '''
        return msg

    def calc_bone_weight(self):
        result = {
            '年': LIFE_WEIGHT_YEAR_RATIO[self.nian_zhu],
            '月': LIFE_WEIGHT_MONTH_RATIO[str(self.lunar_month)],
            '日': LIFE_WEIGHT_DAY_RATIO[str(self.lunar_day)],
            '时': LIFE_WEIGHT_HOUR_RATIO[str(self.input_datetime.hour)]
        }
        return result
