from demigod import CommonDemigod
from lord_god_explain import LordGodExplain
from ten_years_luck import TenYearsLuck
from utils import *
from yearly_luck_explain import YearlyLuckExplain


class YearlyLuck(TenYearsLuck):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.max_years = kwargs.get("max_years", 100)
        self.year_range = kwargs.get("year_range", [0, 100])
        max_year = max(self.year_range[1], self.max_years)
        self.year_range[1] = max_year
        self.max_years = max_year
        self.yearly_luck = list(self.build_yearly_luck())[self.year_range[0]:self.year_range[1]]

        self.lord_god_explain = LordGodExplain(self)
        self.lord_god_explain.init_explanation()
        self.opposing_element = ELEMENTS_OPPOSING[self.ri_gan_element]

        self.yearly_luck_items = self.build_yearly_luck_items()
        self.yearly_luck_list = sorted(self.yearly_luck_items.items(), key=lambda x: x[0])
        self.yearly_luck_luck_explains = YearlyLuckExplain(self)


    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += """
        ## 流年：
        """

        if self.explain_append:
            msg += f'''
        命主为 {'男' if self.is_male else '女'}，所以财为「{'欲望/资源' if self.is_male else '感情/钱'}」
        日主天干五行（{self.ri_gan_element}）所克制的元素（{self.opposing_element}）为为财。
            '''

        msg += f'''
        年份        流年十神        流年神煞        {'流年状态' if self.explain_append else ''}
        '''
        lord_gods_set = set()
        yearly_luck_out_list = []
        for item in self.yearly_luck_list:
            year, record = item
            gan_lord_god = record['gan_god']
            zhi_lord_god = record['zhi_god']
            lord_gods_set.add(gan_lord_god)
            lord_gods_set.add(zhi_lord_god)
            tmp = (f"{year}年（{record['gan_zhi']}）  "
                   f"{gan_lord_god},{zhi_lord_god}  "
                   f"{record['demigods']}")
            if record.get('is_finance', False):
                tmp += "（财）"
            if record.get('gan_support', ()):
                tmp += f"  *{record['gan_support'][0]}|{record['zhi_support'][0]}"
            tmp += "\n"
            yearly_luck_out_list.append(tmp)
        tmp_str = '        '.join(yearly_luck_out_list)
        msg += f"""
        {tmp_str}
        """

        if self.explain_append:
            lord_gods_explain_list = []
            for lord_god in lord_gods_set:
                lord_gods_explain = self.lord_god_explain.single_explain_mapping[lord_god]
                lord_gods_explain_list.append(f"{lord_god}：{lord_gods_explain.imagery}")
            tmp = '\n        '.join(lord_gods_explain_list)
            msg += f'''
        ### 十神意象：
        {tmp}
            '''

            msg += self.yearly_luck_luck_explains.__str__()

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

    def build_yearly_luck_items(self):
        yearly_luck_items = {}
        for item in self.yearly_luck:
            year, gan_zhi, (gan, gan_god), (zhi, zhi_god), demigods = item
            gan_element = GAN_DETAILS[gan]['element']
            zhi_element = ZHI_DETAILS[zhi]['element']

            item = {
                'year_num': year,
                'gan_zhi': gan_zhi,
                'gan': gan,
                'gan_god': gan_god,
                'zhi': zhi,
                'zhi_god': zhi_god,
                'demigods': demigods,
                'gan_element': gan_element,
                'zhi_element': zhi_element,
                'is_finance': self.opposing_element == gan_element,
                'gan_support': self.elements_relationships_mapping[gan_element],
                'zhi_support': self.elements_relationships_mapping[zhi_element]
            }

            yearly_luck_items[year] = item

        return yearly_luck_items
