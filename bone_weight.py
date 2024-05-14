import argparse

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
            '时': LIFE_WEIGHT_HOUR_RATIO[str(self.input_datetime.hour)] if self.input_datetime.hour else LIFE_WEIGHT_HOUR_RATIO['24']
        }
        return result


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
    prediction = BoneWeight(
        base_datetime=main_birthday,
        meta_info_display=True,
        explain_append=explain_append,
        is_male=is_male,
    )
    print(prediction)