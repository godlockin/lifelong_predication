from demigod import CommonDemigod
from lord_gods import LordGods
from utils import *


class YearlyLuck(LordGods):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.max_years = kwargs.get("max_years", 100)

        self.yearly_luck = list(self.build_yearly_luck())

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        yearly_luck = "\n        ".join([str(item) for item in self.yearly_luck])
        msg += f'''
        流年：
        {yearly_luck}
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
