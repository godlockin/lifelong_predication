from collections import defaultdict

from backend.constants.constants import *
from backend.func.ten_years_luck_explain import TenYearsLuckExplain


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
        ty_records_map = {}
        for ty_item in self.ten_years_luck_explain_list:
            ty_gan_zhi = ty_item['ty_gan_zhi']
            ty_details = ty_item['ty_details']
            ty_year_num = str(ty_details['year_num'])

            ty_records_line = f"""
        {ty_year_num}（{ty_gan_zhi}/{ty_details['gan_element']}{ty_details['zhi_element']}） {'（财）' if ty_details['is_finance'] else ''}「{ty_details['sheng_si']}（{SHENG_SI_JUE_WANG_MAPPING[0].index(ty_details['sheng_si']) + 1}/{len(SHENG_SI_JUE_WANG_MAPPING[0])}）」
        十神：{ty_details['lord_gods']}  
        神煞：{ty_details['demigods']}
        前五年「{ty_details['gan_support'][0]}」～后五年「{ty_details['zhi_support'][0]}」
            """
            ty_records_map[ty_year_num] = {
                'ty_gan_zhi': ty_gan_zhi,
                'ty_details': ty_details,
                'ty_records': ty_records_line
            }

        yearly_records = []
        ty_records_use = {}
        for yearly_item in self.ten_years_luck.yearly_luck_list:
            year, record = yearly_item
            ty_records = ty_records_map.get(str(year), {})

            # 大运开始，添加大运信息
            if ty_records:
                ty_records_use = ty_records
                yearly_records.append(ty_records['ty_records'])

            [
                year_details,
                month_details,
                day_details,
                hour_details
            ] = [self.build_gan_zhi_relation(item, record['gan_zhi']) for item in self.ten_years_luck.ba_zi.split(",")]
            ty_details = ty_records_use.get('ty_details', {})
            explains = {
                'year_info': year_details,
                'month_info': month_details,
                'day_info': day_details,
                'time_info': hour_details,
                'ty_details': ty_details,
            }

            gan_final_score = record['gan_final_score'] + ty_details['gan_element_delta']
            zhi_final_score = record['zhi_final_score'] + ty_details['zhi_element_delta']
            if_nice_luck = []
            if 40 <= gan_final_score <= 60:
                if_nice_luck.append(f"前半年")
            if 40 <= zhi_final_score <= 60:
                if_nice_luck.append(f"后半年")
            if_nice = ("和".join(if_nice_luck) + ("都" if len(if_nice_luck) == 2 else "") + "还不错") if if_nice_luck else ""

            body_wonder = self.calc_wondering_list(ty_details['gan_element'], ty_details['zhi_element'], POSITION_ORGAN_NAMES)
            family_wonder = self.calc_wondering_list(ty_details['gan_element'], ty_details['zhi_element'], POSITION_RELATIONSHIP_NAMES)

            wondering_str = "命主自身要注意" + ",".join(body_wonder) + "\n" if body_wonder else ""
            wondering_str += "命主家人要注意" + ",".join(family_wonder) + "\n" if body_wonder else ""

            yearly_records.append(f"""
        {year}年({record['gan_zhi']}/{record['gan_element']}{record['zhi_element']})，{'（财）' if record.get('is_finance', False) else ''}
        前半年「{record['gan_support'][0]}」~后半年「{record['zhi_support'][0]}」
        {if_nice}({self.ten_years_luck.self_score}|{gan_final_score}|{zhi_final_score})
        {wondering_str if wondering_str else ""}
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
