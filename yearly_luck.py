from demigod import CommonDemigod
from lord_gods import LordGods
from utils import *


class YearlyLuck(LordGods):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.max_years = kwargs.get("max_years", 100)
        self.yearly_luck = list(self.build_yearly_luck())

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"

        yearly_luck_items = []
        if self.explain_append:
            opposing_element = WU_XING_XIANG_KE[self.ri_gan_element]
            msg += f'''
        命主为 {'男' if self.is_male else '女'}，所以财为「{'欲望/资源' if self.is_male else '感情/钱'}」
        日主天干五行（{self.ri_gan_element}）所克制的元素（{opposing_element}）为为财
            '''
            for item in self.yearly_luck:
                year, gan_zhi, (gan, gan_god), (zhi, zhi_god), demigods = item
                if opposing_element == GAN_DETAILS[gan]['element']:
                    gan += "**"
                    gan_zhi += "**"
                if opposing_element == ZHI_DETAILS[zhi]['element']:
                    zhi += "*"
                    gan_zhi += "*"

                yearly_luck_items.append((year, gan_zhi, (gan, gan_god), (zhi, zhi_god), demigods))

        yearly_luck_items = self.yearly_luck if not self.explain_append else yearly_luck_items
        yearly_luck_str = "\n        ".join([str(item) for item in yearly_luck_items])
        msg += f'''
        流年：
        {yearly_luck_str}
        '''

        return msg

    def build_yearly_luck(self):
        start_year = self.lunar_year
        for delta in range(self.max_years):
            yield self.get_yearly_luck(start_year + delta)

    def get_yearly_luck(self, year_num):
        gan_zhi_for_year = get_gan_zhi_for_year(year_num)
        gan, zhi = list(gan_zhi_for_year)
        lord_god_gan = LORD_GODS_MATRIX[self.ri_gan_idx][LORD_GODS_MATRIX[0].index(gan)]
        zhi_cang_gan = self.di_zhi_cang_gan(zhi)[0]
        lord_god_zhi = LORD_GODS_MATRIX[self.ri_gan_idx][LORD_GODS_MATRIX[0].index(zhi_cang_gan)]

        common_demigod = CommonDemigod(
            gan_zhi=gan_zhi_for_year,
            ba_zi=self.ba_zi,
            is_male=self.is_male
        )
        return year_num, gan_zhi_for_year, (gan, lord_god_gan), (zhi, lord_god_zhi), common_demigod.build_demigods()
