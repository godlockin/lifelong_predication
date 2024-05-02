from utils import *


class TenYearsLuckExplain:
    def __init__(self, ten_years_luck):
        self.ten_years_luck = ten_years_luck

        self.ten_years_luck_explain_list = self.calc_ten_years_luck_explain_list()
        self.ten_years_luck_explains = self.build_explains()

    def __str__(self):
        result = f"""
        ### 大运解析：
        """
        for line in self.ten_years_luck_explains:
            result += f"""
        {line}
            """
        return result

    def calc_ten_years_luck_explain_list(self):
        for (ty_gan_zhi, ty_details) in self.ten_years_luck.ten_years_luck_list:
            # 年
            year_info = self.build_gan_zhi_relation(self.ten_years_luck.nian_zhu, ty_gan_zhi)
            # 月
            month_info = self.build_gan_zhi_relation(self.ten_years_luck.yue_zhu, ty_gan_zhi)
            # 日
            day_info = self.build_gan_zhi_relation(self.ten_years_luck.ri_zhu, ty_gan_zhi)
            # 时
            time_info = self.build_gan_zhi_relation(self.ten_years_luck.shi_zhu, ty_gan_zhi)
            yield {
                'ty_gan_zhi': ty_gan_zhi,
                'year_info': year_info,
                'month_info': month_info,
                'day_info': day_info,
                'time_info': time_info,
                'ty_details': ty_details,
            }

    def build_gan_zhi_relation(self, self_gan_zhi, ty_gan_zhi):
        self_gan, self_zhi = self_gan_zhi
        ty_gan, ty_zhi = ty_gan_zhi
        ty_gan_element = GAN_DETAILS[ty_gan]['element']
        ty_gan_element_weight = self.ten_years_luck.elements_relationships_mapping[ty_gan_element]
        ty_zhi_element = ZHI_DETAILS[ty_zhi]['element']
        ty_zhi_element_weight = self.ten_years_luck.elements_relationships_mapping[ty_zhi_element]

        gan_zhi_info = {
            'status': {
                'gan': [],
                'zhi': [],
            },
            'lord_gods': {
                'gan': [],
                'zhi': [],
            }
        }

        # 天干
        gan_element = GAN_DETAILS[self_gan]['element']
        gan_element_weight = self.ten_years_luck.elements_relationships_mapping[gan_element]

        ty_gan_lord_gods = LORD_GODS_MATRIX[GAN.index(self_gan) + 1][GAN.index(ty_gan) + 1]
        gan_zhi_info['lord_gods']['gan'].append(ty_gan_lord_gods)

        # 天干冲
        if TIAN_GAN_CHONG_MAPPING[self_gan] == ty_gan:
            is_ty_stronger = abs(ty_gan_element_weight[1]) - abs(gan_element_weight[1]) > 0
            gan_zhi_info['status']['gan'].append((self_gan, ty_gan, '冲', is_ty_stronger))

        # 天干合
        for key, value in TIAN_GAN_HE:
            if self_gan != ty_gan and all(item in key for item in [self_gan, ty_gan]):
                gan_zhi_info['status']['gan'].append((self_gan, ty_gan, '合', value))

        # 地支
        zhi_element = ZHI_DETAILS[self_zhi]['element']
        zhi_element_weight = self.ten_years_luck.elements_relationships_mapping[zhi_element]

        # 地支刑冲破害
        zhi_attribute = ZHI_ATTRIBUTES[self_zhi]
        for key, value in zhi_attribute.items():
            if isinstance(value, str) and ty_zhi == value:
                is_ty_stronger = abs(ty_zhi_element_weight[1]) - abs(zhi_element_weight[1]) > 0
                gan_zhi_info['status']['zhi'].append((self_zhi, ty_zhi, key, is_ty_stronger))
            elif isinstance(value, list) and ty_zhi in value:
                is_ty_stronger = abs(ty_zhi_element_weight[1]) - abs(zhi_element_weight[1]) > 0
                gan_zhi_info['status']['zhi'].append((self_zhi, ty_zhi, key, is_ty_stronger))

        self_cang_tian_gan = self.ten_years_luck.di_zhi_cang_gan(self_zhi)
        for cang_gan in self_cang_tian_gan:
            if not cang_gan:
                continue
            ty_zhi_lord_gods = LORD_GODS_MATRIX[GAN.index(ty_gan) + 1][GAN.index(cang_gan) + 1]
            gan_zhi_info['lord_gods']['zhi'].append(ty_zhi_lord_gods)

        return gan_zhi_info

    def build_explains(self):

        for explains in self.ten_years_luck_explain_list:
            ty_gan_zhi = explains['ty_gan_zhi']
            ty_details = explains['ty_details']
            year_info = explains['year_info']
            month_info = explains['month_info']
            day_info = explains['day_info']
            time_info = explains['time_info']

            result = f"""
        {ty_details['year_num']}（{ty_gan_zhi}） {'（财）' if ty_details['is_finance'] else ''}
        大运阶段：{ty_details['sheng_si']}
        趋势：前五年「{ty_details['gan_support'][0]}」～后五年「{ty_details['zhi_support'][0]}」
            """

            # 年
            status = year_info['status']
            gan_status = status['gan']
            zhi_status = status['zhi']
            if gan_status:
                status_results = self.calc_status_explain('年干', True, gan_status)
                result += f"""
            {'\n'.join(status_results)}
                """
            if zhi_status:
                status_results = self.calc_status_explain('年支', False, zhi_status)
                result += f"""
            {'\n'.join(status_results)}
                """

            result += f"""
            十年大运：{ty_gan_zhi}
            详情：{ty_details}
            年：{year_info}
            月：{month_info}
            日：{day_info}
            时：{time_info}
            """
            yield result

    def calc_status_explain(self, key, is_gan, status_list):
        result = [key]
        for status in status_list:
            self_item, ty_item, status, append_item = status
            # 合
            if '合' == status and append_item in self.ten_years_luck.elements_relationships_mapping:
                element_oriented = self.ten_years_luck.elements_relationships_mapping[append_item]
                result.append(f"""
        {self_item}+{ty_item}({status})=>「{append_item}」
        {append_item}为日主{'喜用' if append_item in self.ten_years_luck.supporting_elements_sequence else '忌凶'}，所以会{'增强' if element_oriented[1] > 0 else '减弱'}日主能量。
                    """)
            # 冲
            elif '冲' == status:
                gan_zhi_idx = 0 if is_gan else 1
                result.append(f"""
        {self_item}+{ty_item}({status})，而且大运力量{'大于' if append_item else '小于'}年干力量，所以会{'大幅' if append_item else '小幅'}减弱{key}能量。
        所以这段时间命主可能会和「{POSITION_RELATIONSHIP_NAMES[gan_zhi_idx][POSITION_NAMES[gan_zhi_idx].index(key)]}」关系不太好。
        同时也要注意自己「{POSITION_ORGAN_NAMES[gan_zhi_idx][POSITION_NAMES[gan_zhi_idx].index(key)]}」的健康。
                    """)
            # 刑
            elif '刑' == status or '被刑' == status:
                gan_zhi_idx = 0 if is_gan else 1
                result.append(f"""
        {self_item}+{ty_item}({status})，而且大运力量{'大于' if append_item else '小于'}年干力量，所以会{'大幅' if append_item else '小幅'}减弱{key}能量。
        所以这段时间命主可能会和「{POSITION_RELATIONSHIP_NAMES[gan_zhi_idx][POSITION_NAMES[gan_zhi_idx].index(key)]}」有口舌、财务的冲突。严重的可能家宅不安，亲人反目，婚姻宫不稳。
                """)
            # 破

        return result
