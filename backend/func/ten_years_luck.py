import argparse

from backend.func.demigod import CommonDemigod
from backend.func.lord_god_explain import LordGodExplain
from backend.func.lord_gods import LordGods
from backend.func.ten_years_luck_explain import TenYearsLuckExplain
from backend.utils.utils import *


class TenYearsLuck(LordGods):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.ten_years_luck_gan_zhi = self.build_ten_years_luck_gan_zhi()
        ri_gan_idx = GAN.index(self.ri_gan) + 1
        ri_zhi_cang_gan = self.nian_zhi_cang_gan_lord_gods[0][0]
        ri_zhi_cang_gan_idx = GAN.index(ri_zhi_cang_gan) + 1
        tian_gan_sheng_wang_si_jue_idx = TIAN_GAN_SHENG_SI_JUE_WANG.index(self.ri_gan) + 1

        self.ri_zhi_n_nian_zhi = [self.nian_zhi, self.ri_zhi]
        self.ri_gan_n_nian_gan = [self.nian_gan, self.ri_gan]

        (
            self.ten_years_luck_sheng_si_list,
            self.ten_years_luck_lord_gods,
            self.ten_years_luck_demigods,
        ) = self.build_ten_years_luck_attributes(ri_gan_idx, ri_zhi_cang_gan_idx, tian_gan_sheng_wang_si_jue_idx)

        self.ten_years_luck_details = self.build_ten_years_luck_details()
        self.ten_years_luck_list = sorted(self.ten_years_luck_details.items(), key=lambda x: x[1]['idx'])
        self.lord_god_explain = LordGodExplain(self)
        self.lord_god_explain.init_explanation()

        self.ten_years_luck_explains = TenYearsLuckExplain(self)

    def __str__(self):
        result = f"{super().__str__() if self.meta_info_display else ''}"
        result += f'''
        ## 大运：
        年份        大运循环        大运十神        大运神煞        {'大运状态' if self.explain_append else ''}
        '''
        lord_gods_set = set()
        ten_years_luck_out_list = []
        for (k, v) in self.ten_years_luck_list:
            tmp_lord_gods = v['lord_gods']
            lord_gods_set = lord_gods_set.union(set(tmp_lord_gods))
            msg = (f"{v['year_num']}年（{k}/{v['gan_element']}{v['zhi_element']}）  "
                   f"{v['sheng_si']}  "
                   f"{v['lord_gods']}  "
                   f"{v['demigods']} ")
            if self.explain_append:
                if v.get('is_finance', False):
                    msg += "（财）"
                msg += f"*{v['gan_support'][0]}|{v['zhi_support'][0]} ({self.self_score}|{v['gan_final_score']}|{v['zhi_final_score']})"
            msg += "\n"
            ten_years_luck_out_list.append(msg)

        result += f"{'        '.join(ten_years_luck_out_list)}"

        if self.explain_append:
            lord_gods_explain_list = []
            for lord_god in lord_gods_set:
                lord_gods_explain = self.lord_god_explain.single_explain_mapping[lord_god]
                lord_gods_explain_list.append(f"{lord_god}：{lord_gods_explain.imagery}")
            msg = '\n        '.join(lord_gods_explain_list)
            result += f'''
        ### 十神意象：
        {msg}
            '''

            result += f'''
        {self.ten_years_luck_explains}
            '''
        return result

    def build_ten_years_luck_gan_zhi(self):
        start = JIA_ZI_NAME.index(self.yue_zhu) if self.yue_zhu in JIA_ZI_NAME else -1
        if start == -1:
            return []

        # （年干为阳干且性别为女） 和 （年干为阴干且性别为男） 为逆推其他两种为顺推
        is_shun = not (
                (self.nian_gan in ("甲", "丙", "戊", "庚", "壬") and not self.is_male)
                or
                (self.nian_gan not in ("甲", "丙", "戊", "庚", "壬") and self.is_male)
        )
        start = start + 1 if is_shun else start - 1
        return [JIA_ZI_NAME[(start + (i if is_shun else -i)) % len(JIA_ZI_NAME)] for i in range(8)]

    def build_ten_years_luck_attributes(self, ri_gan_idx, ri_zhi_cang_gan_idx, tian_gan_sheng_wang_si_jue_idx):
        ten_years_luck_list, ten_years_luck_lord_gods_list, ten_years_luck_demigods = [], [], []
        for item in self.ten_years_luck_gan_zhi:
            sheng_si_idx = SHENG_SI_JUE_WANG_MAPPING[tian_gan_sheng_wang_si_jue_idx].index(item[1:])
            ten_years_luck_list.append(SHENG_SI_JUE_WANG_MAPPING[0][sheng_si_idx])

            lord_gods_idx = LORD_GODS_MATRIX[0].index(item[:1])
            lord_gods_pair = [
                LORD_GODS_MATRIX[ri_gan_idx][lord_gods_idx],
                LORD_GODS_MATRIX[ri_zhi_cang_gan_idx][lord_gods_idx]
            ]
            ten_years_luck_lord_gods_list.append(lord_gods_pair)

            common_demigod = CommonDemigod(
                gan_zhi=item,
                ba_zi=self.ba_zi,
                is_male=self.is_male
            )
            ten_years_luck_demigods.append(common_demigod.build_demigods())

        return ten_years_luck_list, ten_years_luck_lord_gods_list, ten_years_luck_demigods

    def build_ten_years_luck_details(self):
        ten_years_luck_details = {}
        opposing_element = ELEMENTS_OPPOSING[self.ri_gan_element]
        for idx, item in enumerate(self.ten_years_luck_gan_zhi):
            gan_element = GAN_DETAILS[item[0]]['element']
            zhi_element = ZHI_DETAILS[item[1]]['element']

            gan_delta = -1 if self.self_strong and gan_element in self.supporting_elements_sequence else 1
            zhi_delta = -1 if self.self_strong and zhi_element in self.supporting_elements_sequence else 1

            ten_years_luck_details[item] = {
                'idx': idx,
                'year_num': self.lunar_year + idx * 10,
                'sheng_si': self.ten_years_luck_sheng_si_list[idx],
                'lord_gods': self.ten_years_luck_lord_gods[idx],
                'demigods': self.ten_years_luck_demigods[idx],
                'gan_element': gan_element,
                'gan_final_score': self.self_score + gan_delta * 12,
                'zhi_element': zhi_element,
                'zhi_final_score': self.self_score + zhi_delta * 12,
                'gan_support': self.elements_relationships_mapping[gan_element],
                'zhi_support': self.elements_relationships_mapping[zhi_element],
                'is_finance': opposing_element == gan_element,
            }
        return ten_years_luck_details


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
    prediction = TenYearsLuck(
        base_datetime=main_birthday,
        explain_append=explain_append,
        is_male=is_male,
    )
    print(prediction)
