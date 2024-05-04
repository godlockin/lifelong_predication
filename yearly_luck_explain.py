from collections import defaultdict

from constants import *
from ten_years_luck_explain import TenYearsLuckExplain


class YearlyLuckExplain(TenYearsLuckExplain):
    def __init__(self, ten_years_luck):
        super().__init__(ten_years_luck)

        self.yearly_luck_explain_list = self.build_yearly_luck_explain_list()

    def __str__(self):
        result = f"""
        ### 流年解析：
        """

        result += "".join(self.yearly_luck_explain_list)

        return result

    def build_yearly_luck_explain_list(self):
        ty_records = {}
        for ty_item in self.ten_years_luck_explain_list:
            ty_gan_zhi = ty_item['ty_gan_zhi']
            ty_details = ty_item['ty_details']
            ty_year_num = str(ty_details['year_num'])

            ty_records_line = f"""
        {ty_year_num}（{ty_gan_zhi}） {'（财）' if ty_details['is_finance'] else ''}「{ty_details['sheng_si']}（{SHENG_SI_JUE_WANG_MAPPING[0].index(ty_details['sheng_si']) + 1}/{len(SHENG_SI_JUE_WANG_MAPPING[0])}）」
        前五年「{ty_details['gan_support'][0]}」～后五年「{ty_details['zhi_support'][0]}」
            """
            ty_records[ty_year_num] = {
                'ty_gan_zhi': ty_gan_zhi,
                'ty_details': ty_details,
                'ty_records': ty_records_line
            }

        yearly_records = []
        for yearly_item in self.ten_years_luck.yearly_luck_list:
            year, record = yearly_item
            ty_records = ty_records.get(str(year), {})

            # 大运开始，添加大运信息
            if ty_records:
                yearly_records.append(ty_records['ty_records'])

            [
                year_details,
                month_details,
                day_details,
                hour_details
            ] = [self.build_gan_zhi_relation(item, record['gan_zhi']) for item in self.ten_years_luck.ba_zi.split(",")]
            explains = {
                'year_info': year_details,
                'month_info': month_details,
                'day_info': day_details,
                'time_info': hour_details,
            }

            yearly_records.append(f"""
        {year}年，{'（财）' if record.get('is_finance', False) else ''}
        前半年「{record['gan_support'][0]}」~后半年「{record['zhi_support'][0]}」
            """)
            all_lord_gods = defaultdict(float)
            for condition in self.key_mapping:
                info_details, lord_gods_list = self.build_info_explain(condition, explains)
                yearly_records.append("".join(info_details))
                for pair in lord_gods_list:
                    all_lord_gods[pair[0]] += pair[1]
            all_lord_gods_list = sorted(all_lord_gods.items(), key=lambda x: x[1], reverse=True)
            yearly_records.append(f"""
        整体大运增长十神能量：{[(item[0], round(item[1] / 10, 5)) for item in all_lord_gods_list]}
            """)

        return yearly_records
