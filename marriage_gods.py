from ba_zi_elements import BaZiElements
from utils import *


class MarriageGods(BaZiElements):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.sound_year = get_sound_for_gan_zhi(self.nian_zhu)
        self.sound_month = get_sound_for_gan_zhi(self.yue_zhu)
        self.sound_day = get_sound_for_gan_zhi(self.ri_zhu)
        self.sound_time = get_sound_for_gan_zhi(self.shi_zhu)

        self.marriage_gods = self.build_marriage_gods_list()

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        年柱  月柱  日柱  时柱
        {self.nian_zhu}（{self.sound_year}）  {self.yue_zhu}（{self.sound_month}）  {self.ri_zhu}（{self.sound_day}）  {self.shi_zhu}（{self.sound_time}） 
        合婚神煞：{",".join(self.marriage_gods)}
        '''
        return msg

    def build_marriage_gods_list(self):
        """
        鼠年出生者，男命四月生人犯重婚煞兼大败煞、小狼藉煞、脚踏煞、破碎煞、劫煞；女命五月生人犯再嫁煞兼绝烟火煞、大狼藉煞、头带煞。
        牛年出生者，男命五月生人犯重婚煞兼桃花煞、脚踏煞、六害煞；女命六月生人犯再嫁煞兼头带煞。
        虎年出生者，男命六月生人犯重婚煞兼飞天狼藉煞、脚踏煞；女命七月生人犯再嫁煞兼铁扫帚煞、绝房煞、头带煞。
        兔年出生者，男命七月生人犯重婚煞兼脚踏煞、劫煞；女命八月生人犯再嫁煞见铁扫帚煞、头带煞。
        龙年出生者，男命八月生人犯重婚煞兼桃花煞、脚踏煞；女命九月生人犯再嫁煞兼小狼藉煞、头带煞。
        蛇年出生者，男命九月生人犯重婚煞兼脚踏煞；女命十月生人犯再嫁煞兼小狼藉煞、头带煞。
        马年出生者，男命十月生人犯重婚煞兼大败煞、脚踏煞、劫煞；女命冬月生人犯再嫁煞兼大狼藉煞、绝烟火煞、头带煞。
        羊年出生者，男命冬月生人犯重婚煞兼桃花煞、飞天狼藉煞、脚踏煞、六害煞；女命腊月生人犯再嫁煞。
        猴年出生者，男命腊月生人犯重婚煞兼脚踏煞；女命正月生人犯再嫁煞兼飞天狼藉煞、头带煞。
        鸡年出生者，男命正月生人犯重婚煞兼飞天狼藉煞、脚踏煞、劫煞；女命二月生人犯再嫁煞兼小狼藉煞、头带煞。
        狗年出生者，男命二月生人犯重婚煞兼大狼藉煞、小狼藉煞、绝房煞、脚踏煞、桃花煞、绝烟火煞；女命三月生人犯再嫁煞兼骨髓破煞、八败煞、头带煞、苦焦煞。
        猪年出生者，男命三月生人犯重婚煞兼八败煞、脚踏煞；女命四月生人犯再嫁煞、头带煞。
        :return:
        """
        year_idx = get_year_index(self.lunar_year)
        idx = year_idx + 1
        month_chinese_name = get_month_chinese_name(self.lunar_month)
        marriage_god_list = []
        for i in range(14):
            if month_chinese_name in (GOD_LIST_PRIMARY[idx][i], GOD_LIST_SECONDARY[idx][i]):
                marriage_god_list.append(GOD_LIST_PRIMARY[0][i] if month_chinese_name == GOD_LIST_PRIMARY[idx][i] else GOD_LIST_SECONDARY[0][i])
        return marriage_god_list

