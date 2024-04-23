from demigod import CommonDemigod
from metainfo import MetaInfo
from utils import *


class TenYearsLuck(MetaInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)

        self.ten_years_luck_gan_zhi = self.build_ten_years_luck_gan_zhi()
        ri_gan_idx = GAN.index(self.ri_gan) + 1
        tian_gan_sheng_wang_si_jue_idx = TIAN_GAN_SHENG_SI_JUE_WANG.index(self.ri_gan) + 1

        self.ri_zhi_n_nian_zhi = [self.nian_zhi, self.ri_zhi]
        self.ri_gan_n_nian_gan = [self.nian_gan, self.ri_gan]

        (
            self.ten_years_luck_sheng_si_list,
            self.ten_years_luck_lord_gods,
            self.ten_years_luck_demigods,
        ) = self.build_ten_years_luck_sheng_si(ri_gan_idx, tian_gan_sheng_wang_si_jue_idx)

        self.ten_years_luck_details = self.build_ten_years_luck_details()

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"

        ten_years_luck_list = sorted(self.ten_years_luck_details.values(), key=lambda x: x['idx'])
        ten_years_luck_display = "\n        ".join([f"{item['year_num']}年  {item['sheng_si']}  {item['lord_gods']}  {item['demigods']}" for item in ten_years_luck_list])
        msg += f'''
        大运    大运循环  大运十神  大运神煞
        {ten_years_luck_display}
        '''
        return msg

    def build_ten_years_luck_gan_zhi(self):
        start = JIA_ZI_NAME.index(self.yue_zhu) if self.yue_zhu in JIA_ZI_NAME else -1
        if start == -1:
            return []

        # （年干为阳干且性别为女） 和 （年干为阴干且性别为男） 为逆推
        # 其他两种为顺推
        is_shun = (self.nian_gan in ("甲", "丙", "戊", "庚", "壬")) and self.is_male
        start = start + 1 if is_shun else start - 1
        return [JIA_ZI_NAME[(start + (i if is_shun else -i)) % len(JIA_ZI_NAME)] for i in range(8)]

    def build_ten_years_luck_sheng_si(self, ri_gan_idx, tian_gan_sheng_wang_si_jue_idx):
        ten_years_luck_list, ten_years_luck_lord_gods_list, ten_years_luck_demigods = [], [], []
        for item in self.ten_years_luck_gan_zhi:
            sheng_si_idx = SHENG_SI_JUE_WANG_MAPPING[tian_gan_sheng_wang_si_jue_idx].index(item[1:])
            ten_years_luck_list.append(SHENG_SI_JUE_WANG_MAPPING[0][sheng_si_idx])

            lord_gods_idx = LORD_GODS_MATRIX[0].index(item[:1])
            ten_years_luck_lord_gods_list.append(LORD_GODS_MATRIX[ri_gan_idx][lord_gods_idx])

            common_demigod = CommonDemigod(
                gan_zhi=item,
                ba_zi=self.ba_zi,
                is_male=self.is_male
            )
            ten_years_luck_demigods.append(common_demigod.build_demigods())

        return ten_years_luck_list, ten_years_luck_lord_gods_list, ten_years_luck_demigods

    def build_ten_years_luck_details(self):
        ten_years_luck_details = {}
        for idx, item in enumerate(self.ten_years_luck_gan_zhi):
            ten_years_luck_details[item] = {
                'idx': idx,
                'year_num': self.lunar_year + idx * 10,
                'sheng_si': self.ten_years_luck_sheng_si_list[idx],
                'lord_gods': self.ten_years_luck_lord_gods[idx],
                'demigods': self.ten_years_luck_demigods[idx],
            }
        return ten_years_luck_details
