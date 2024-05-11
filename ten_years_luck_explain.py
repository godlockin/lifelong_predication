from collections import defaultdict

from lord_god_explain import LordGodExplain
from utils import *


class TenYearsLuckExplain:
    def __init__(self, ten_years_luck):
        self.ten_years_luck = ten_years_luck

        self.ten_years_luck_explain_list = self.calc_luck_explain_list(self.ten_years_luck.ten_years_luck_list)
        self.ten_years_luck_explains = self.build_explains()

        self.lord_god_explain = LordGodExplain(self.ten_years_luck)
        self.lord_god_explain.init_explanation()
        self.key_mapping = [
            ('年', 'year'),
            ('月', 'month'),
            ('日', 'day'),
            ('时', 'time'),
        ]

    def __str__(self):
        result = f"""
        ### 大运解析：
        """

        for line, ty_lord_gods_list in self.ten_years_luck_explains:
            all_lord_gods = defaultdict(float)
            for pair in ty_lord_gods_list:
                all_lord_gods[pair[0]] += pair[1]
            result += f"""
        {line}
            """
            sort_list = sorted(all_lord_gods.items(), key=lambda x: x[1], reverse=True)

            lord_gods_explain_list = []
            for (lord_god, weight) in sort_list:
                ori_weight = round(self.lord_god_explain.single_explain_mapping[lord_god].total_weight, 4)
                lord_gods_explain = self.lord_god_explain.single_explain_mapping[lord_god]
                final_weight = round((weight + ori_weight), 4)
                lord_gods_explain_list.append((lord_god, ori_weight, weight, final_weight, lord_gods_explain.imagery))
            lord_gods_explain_list = sorted(lord_gods_explain_list, key=lambda x: (x[2], x[3]), reverse=True)
            tmp = "".join([f'\n        {item[0]}（{item[1]}+{item[2]}~{item[3]}）：{item[4]}' for item in lord_gods_explain_list])
            result += f'''
        -- 十神意象：
            {tmp}
                '''

        return result

    def calc_luck_explain_list(self, base_list):
        for (ty_gan_zhi, ty_details) in base_list:
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
        if self_gan in TIAN_GAN_CHONG_MAPPING and TIAN_GAN_CHONG_MAPPING[self_gan] == ty_gan:
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

            result = [f"""
        ### {ty_details['year_num']}（{ty_gan_zhi}/{ty_details['gan_element']}{ty_details['zhi_element']}） {'（财）' if ty_details['is_finance'] else ''}
        大运阶段：{ty_details['sheng_si']}（{SHENG_SI_JUE_WANG_MAPPING[0].index(ty_details['sheng_si']) + 1}/{len(SHENG_SI_JUE_WANG_MAPPING[0])}）
        趋势：前五年「{ty_details['gan_support'][0]}」～后五年「{ty_details['zhi_support'][0]}」
            """]

            all_lord_gods = defaultdict(float)
            for key_pair in self.key_mapping:
                info_details, zhu_lord_gods_list = self.build_info_explain(key_pair, explains)
                result += info_details if info_details else []
                for pair in zhu_lord_gods_list:
                    all_lord_gods[pair[0]] += pair[1]
            all_lord_gods_list = sorted(all_lord_gods.items(), key=lambda x: x[1], reverse=True)
            result.append(f"""
        整体大运增长十神能量：{[(item[0], round(item[1] / 7, 5)) for item in all_lord_gods_list]}
            """)

            yield "".join(list(dict.fromkeys(result))), all_lord_gods_list

    def build_info_explain(self, key_pair, explains):
        result = []
        key_name, key_idx = key_pair
        zhu_msg = f"""
        {key_name}柱
        """
        result.append(zhu_msg)
        info_detail = explains[key_idx + "_info"]
        status = info_detail['status']
        gan_status = status['gan']
        zhi_status = status['zhi']
        if gan_status:
            status_results = self.calc_status_explain(key_name + '干', True, gan_status)
            result += status_results
        if zhi_status:
            status_results = self.calc_status_explain(key_name + '支', False, zhi_status)
            result += status_results

        lord_gods = info_detail['lord_gods']
        all_lord_gods = defaultdict(float)
        for item in lord_gods['gan']:
            gan_key = key_name + '干'
            weight = POSITION_WEIGHT[0][POSITION_NAMES[0].index(gan_key)]
            if weight:
                all_lord_gods[item] += weight

        for idx, item in enumerate(lord_gods['zhi']):
            zhi_key = key_name + '支'
            if key_name == '月':
                zhi_key = '月令'
            all_lord_gods[item] += POSITION_WEIGHT[1][POSITION_NAMES[1].index(zhi_key)] * CANG_GAN_WEIGHT[idx]

        all_lord_gods_list = sorted(all_lord_gods.items(), key=lambda x: x[1], reverse=True)
        result.append(f"""
        十神中增加{all_lord_gods_list}的能量。
            """)
        return result, all_lord_gods_list

    def calc_status_explain(self, key, is_gan, status_list):
        result = []
        if '月支' == key:
            key = '月令'
        key_msg = f"""
        {key}
        """
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
        {self_item}+{ty_item}({status})，而且大运力量{'大于' if append_item else '小于'}{key}力量，所以会{'大幅' if append_item else '小幅'}减弱{key}能量。
        冲是人与人之间的冲突，必须干掉一个才罢休严重了也会威胁生命。是外人对命主的攻讦，如果婚姻宫的冲动可能导致家暴甚至离婚。
        在生活、工作、心理、健康等起伏不定，有动。情绪状态很差，做事不顺心，人缘关系差，易遇到意料之外的钱财损失，破财不断。注意脾胃方面疾病，此年整体对事业财运和健康打击甚大。
        所以这段时间命主可能会和「{POSITION_RELATIONSHIP_NAMES[gan_zhi_idx][POSITION_NAMES[gan_zhi_idx].index(key)]}」关系不太好。
        同时也要注意自己「{POSITION_ORGAN_NAMES[gan_zhi_idx][POSITION_NAMES[gan_zhi_idx].index(key)]}」的健康。
                    """)
            # 刑
            elif '刑' == status or '被刑' == status:
                gan_zhi_idx = 0 if is_gan else 1
                result.append(f"""
        {self_item}+{ty_item}({status})，而且大运力量{'大于' if append_item else '小于'}{key}力量，所以会{'大幅' if append_item else '小幅'}减弱{key}能量。
        刑是上天的刑罚，要得病、坐牢、车祸受到惩罚才休止，严重了会威胁生命。是外在的非人力量对命主的攻讦。
        所以这段时间命主可能会和「{POSITION_RELATIONSHIP_NAMES[gan_zhi_idx][POSITION_NAMES[gan_zhi_idx].index(key)]}」有口舌、财务的冲突。严重的可能家宅不安，亲人反目，婚姻宫不稳。
        同时也要注意自己「{POSITION_ORGAN_NAMES[gan_zhi_idx][POSITION_NAMES[gan_zhi_idx].index(key)]}」的健康。
                """)
            # 破
            elif '破' == status:
                gan_zhi_idx = 0 if is_gan else 1
                result.append(f"""
        {self_item}+{ty_item}({status})，而且大运力量{'大于' if append_item else '小于'}{key}力量，所以会{'大幅' if append_item else '小幅'}减弱{key}能量。
        事业上有破之象，险阻较多，宜静不宜动。小心意料之外的横祸，或者是钱财损失，以及因人际关系引起的工作矛盾。
        感情运势低迷，找不到伴侣或者伴侣矛盾重重，家庭关系不和睦。身体方面注意脾胃疾病，八字带有丑的人会出现失眠，心烦意乱的问题。
        所以这段时间命主可能会和「{POSITION_RELATIONSHIP_NAMES[gan_zhi_idx][POSITION_NAMES[gan_zhi_idx].index(key)]}」有情感的冲突，或者对共同的事业带来负面影响。
        同时也要注意自己「{POSITION_ORGAN_NAMES[gan_zhi_idx][POSITION_NAMES[gan_zhi_idx].index(key)]}」的健康。
                """)
            # 害
            elif '害' == status:
                gan_zhi_idx = 0 if is_gan else 1
                result.append(f"""
        {self_item}+{ty_item}({status})，而且大运力量{'大于' if append_item else '小于'}{key}力量，所以会{'大幅' if append_item else '小幅'}减弱{key}能量。
        易有意外伤害、他人暗算、口舌是非等事发生事业及人际关系上，容易犯小人，工作进展阻滞。
        财星破损，有散财、破财之灾，很难把握住机会。感情方面易跟伴侣产生分歧、生争执和误会，引发家庭矛盾，婚姻容易出现危机。
        注意本年肠胃不佳，肝胆出现疾病，饮食方面需格外当心，防固疾复发，也易受外伤，注重自己的身体状况和养生。
        所以这段时间命主可能会和「{POSITION_RELATIONSHIP_NAMES[gan_zhi_idx][POSITION_NAMES[gan_zhi_idx].index(key)]}」有财务纷争，可能会有意外损失。
        同时也要注意自己「{POSITION_ORGAN_NAMES[gan_zhi_idx][POSITION_NAMES[gan_zhi_idx].index(key)]}」的健康。
                """)

        return [key_msg] + result if result else result
