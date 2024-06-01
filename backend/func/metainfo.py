import argparse
from collections import Counter

from backend.utils.utils import *


class MetaInfo:
    def __init__(self, **kwargs):

        self.input_datetime = parse_input_datetime_info(kwargs)
        # 默认为男性
        self.is_male = kwargs.get('is_male', True)
        self.input_datetime_str = self.input_datetime.strftime(default_date_format)
        offset_timestamp = (self.input_datetime - BASE_DATE)
        self.offset = offset_timestamp.days

        # yearCyl农历年与1864的相差数
        self.year_cyl = 1864
        # monCyl从1900年1月31日以来,闰月数
        self.mon_cyl = 14
        # 与1900年1月31日相差的天数,再加40
        self.day_cyl = self.offset + 40

        # 用offset减去每农历年的天数
        # 计算当天是农历第几天
        # iYear最终结果是农历的年份
        # offset是当年的第几天
        self.lunar_year = 1900
        days_of_year = 0
        while self.lunar_year < 2050 and self.offset > 0:
            days_of_year = year_days(self.lunar_year)
            self.offset -= days_of_year
            self.mon_cyl += 12
            self.lunar_year += 1

        if self.offset < 0:
            self.offset += days_of_year
            self.lunar_year -= 1
            self.mon_cyl -= 12

        self.year_cyl = self.lunar_year - 1864
        # 闰哪个月,1-12
        self.leap_month = leap_month_num(self.lunar_year)
        self.leap = False

        # 农历月份
        self.lunar_month = 1
        days_of_month = 0
        # 用当年的天数offset,逐个减去每月（农历）的天数，求出当天是本月的第几天
        while self.lunar_month < 13 and self.offset > 0:
            # 闰月
            if self.leap_month > 0 and self.lunar_month == (self.leap_month + 1) and not self.leap:
                self.lunar_month -= 1
                self.leap = True
                days_of_month = leap_days(self.lunar_year)
            else:
                days_of_month = month_days(self.lunar_year, self.lunar_month)

            self.offset -= days_of_month
            # 解除闰月
            if self.leap and self.lunar_month == (self.leap_month + 1):
                self.leap = False
            if not self.leap:
                self.mon_cyl += 1
            self.lunar_month += 1

        # offset为0时，并且刚才计算的月份是闰月，要校正
        if self.offset == 0 and self.leap_month > 0 and self.lunar_month == self.leap_month + 1:
            if self.leap:
                self.leap = False
            else:
                self.leap = True
                self.lunar_month -= 1
                self.mon_cyl -= 1

        # offset小于0时，也要校正
        if self.offset < 0:
            self.offset += days_of_month
            self.lunar_month -= 1
            self.mon_cyl -= 1

        # 农历日期
        self.lunar_day = self.offset + 1
        # 生肖
        self.zodiac = get_zodiac_of_year(self.lunar_year)
        # 生肖地支
        self.zodiac_zhi = get_zhi_of_year(self.lunar_year)
        # 生肖五行
        self.zodiac_element = ZHI_DETAILS[self.zodiac_zhi]['element']

        # 八字
        self.ba_zi = get_ba_zi_for_datetime(self.lunar_year, self.lunar_month, self.input_datetime)

        # 四柱
        (self.nian_zhu, self.yue_zhu, self.ri_zhu, self.shi_zhu) = self.ba_zi.split(",")

        # 各个干支
        ((self.nian_gan, self.nian_zhi),
         (self.yue_gan, self.yue_zhi),
         (self.ri_gan, self.ri_zhi),
         (self.shi_gan, self.shi_zhi)) = self.split_gan_zhi()
        self.all_gan = [self.nian_gan, self.yue_gan, self.ri_gan, self.shi_gan]
        self.all_zhi = [self.nian_zhi, self.yue_zhi, self.ri_zhi, self.shi_zhi]

        # 干支对应五行
        self.elements_matrix = self.mapping_gan_zhi_elements()
        [
            [self.nian_gan_element, self.yue_gan_element, self.ri_gan_element, self.shi_gan_element],
            [self.nian_zhi_element, self.yue_zhi_element, self.ri_zhi_element, self.shi_zhi_element]
        ] = self.elements_matrix

        # 命主克制的五行
        self.opposing_element = ELEMENTS_OPPOSING[self.ri_gan_element]

        self.all_elements = [
            self.nian_gan_element, self.nian_zhi_element,
            self.yue_gan_element, self.yue_zhi_element,
            self.ri_gan_element, self.ri_zhi_element,
            self.shi_gan_element, self.shi_zhi_element
        ]

        self.elements_count = Counter(self.all_elements)

        (
            self.nian_sound,
            self.yue_sound,
            self.ri_sound,
            self.shi_sound
         ) = (
            GAN_ZHI_SOUND_MAPPING[self.nian_zhu],
            GAN_ZHI_SOUND_MAPPING[self.yue_zhu],
            GAN_ZHI_SOUND_MAPPING[self.ri_zhu],
            GAN_ZHI_SOUND_MAPPING[self.shi_zhu]
        )

        # 农历生日
        self.lunar_of_input_datetime = datetime(self.lunar_year, self.lunar_month, self.lunar_day)
        self.lunar_of_input_datetime_str = f"{get_year_chinese_name(self.lunar_year)}年，{'闰' if self.leap else ''}{CHINESE_MONTH_NAME[self.lunar_month - 1]}月{get_day_chinese_name(self.lunar_day)}日"
        shi_chen_idx = get_shi_chen_idx(self.input_datetime.hour)
        self.shi_chen = ZHI[shi_chen_idx]

    def __str__(self):
        msg = f'''
        ## 基础信息
        生日：{self.input_datetime_str}
        农历：{self.lunar_of_input_datetime_str}({self.lunar_of_input_datetime.strftime('%Y-%m-%d')} {self.shi_chen}时)
        八字：{self.ba_zi}
        生肖：{self.zodiac}（{self.zodiac_zhi}:{self.zodiac_element}）
        年干     月干      日干（{"男" if self.is_male else "女"}主）    时干
        {self.nian_gan}（{self.nian_gan_element}）  {self.yue_gan}（{self.yue_gan_element}）   {self.ri_gan}（{self.ri_gan_element}）      {self.shi_gan}（{self.shi_gan_element}）
        年支     月令      日支          时支
        {self.nian_zhi}（{self.nian_zhi_element}）  {self.yue_zhi}（{self.yue_zhi_element}）   {self.ri_zhi}（{self.ri_zhi_element}）      {self.shi_zhi}（{self.shi_zhi_element}）
        纳音：
        {self.nian_sound}   {self.yue_sound}    {self.ri_sound}     {self.shi_sound}
        '''

        return msg

    def split_gan_zhi(self):
        return [[gan, zhi] for gan, zhi in (self.nian_zhu, self.yue_zhu, self.ri_zhu, self.shi_zhu)]

    def mapping_gan_zhi_elements(self):
        return [
            [GAN_DETAILS[item]['element'] for item in self.all_gan],
            [ZHI_DETAILS[item]['element'] for item in self.all_zhi]
        ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is a calc project of BaZi.')
    parser.add_argument('-b', '--birthday',
                        help='The birthday of yourself, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"',
                        required=True)
    parser.add_argument('-g', '--gander', help='The gander of yourself, default as male', action='store_true',
                        default=True)
    parser.add_argument('-e', '--explain', help='To check whether append explain details on different attributes',
                        action='store_true', default=False)

    args = parser.parse_args()

    print(f'Argument received: {args}')
    main_birthday = datetime.strptime(args.birthday, default_date_format)
    is_male = args.gander
    explain_append = args.explain
    prediction = MetaInfo(
        base_datetime=main_birthday,
        explain_append=explain_append,
        is_male=is_male,
    )
    print(prediction)
