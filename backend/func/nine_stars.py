from collections import defaultdict

from backend.func.ba_zi_elements import BaZiElements
from backend.constants.constants import *


class NineStars(BaZiElements):
    def __init__(self, **kwargs):
        input_date_time = kwargs.get('base_datetime', None)
        if not ('base_datetime' in kwargs or kwargs.get('base_datetime')):
            kwargs['base_datetime'] = BASE_DATE
        self.self_element = kwargs.get('self_element', '')

        super().__init__(**kwargs)
        if not self.self_element and BASE_DATE != input_date_time:
            self.self_element = self.primary_element

        self.base_idx_mapping = self.init_base_idx_mapping()
        self.position_matrix_str = self.position_matrix_to_str()
        self.country_luck_idx = self.calc_country_luck_idx()
        self.target_idx_mapping = self.calc_target_idx_mapping()
        self.target_star_matrix = self.calc_target_star_matrix()
        self.target_star_matrix_str = self.list_matrix_to_str(self.target_star_matrix)
        self.ba_gua_matrix = self.calc_ba_gua_matrix()
        self.ba_gua_matrix_str = self.list_matrix_to_str(self.ba_gua_matrix)

    def __str__(self):
        msg = f"""
        ## 九星飞泊
        目标年份为{self.input_datetime.year}（{self.nian_zhu}）
        九星宫位为：
        「{self.position_matrix_str}」
        
        {self.ba_gua_matrix_str}
        
        {self.target_star_matrix_str}
        """

        return msg

    def init_base_idx_mapping(self):
        # position: star_idx
        # 以2024，九紫离火运为基线
        return 2024, 9, {
            4: 2,
            9: 7,
            2: 9,
            3: 1,
            5: 3,
            7: 5,
            8: 6,
            1: 8,
            6: 4,
        }

    def calc_target_idx(self, idx, append_delta, gap_num):
        tmp_idx = (idx + append_delta - 1) % gap_num + 1
        return tmp_idx

    def calc_target_idx_mapping(self):
        target_year = self.lunar_of_input_datetime.year
        delta = target_year - self.base_idx_mapping[0]

        return {
            key: self.calc_target_idx(value, delta, 9)
            for key, value in self.base_idx_mapping[2].items()
        }

    def calc_element_relationship(self, base_element, target_element):
        if base_element == target_element:
            return "正旺"
        elif ELEMENTS_SUPPORTING[base_element] == target_element:
            return "生"
        elif SWAPPED_ELEMENTS_OPPOSING[base_element] == target_element:
            return "休"
        elif ELEMENTS_OPPOSING[base_element] == target_element:
            return "煞"
        elif SWAPPED_ELEMENTS_SUPPORTING[base_element] == target_element:
            return "囚"

    def calc_country_luck_idx(self):
        target_year = self.input_datetime.year
        delta = target_year - self.base_idx_mapping[0]
        return self.calc_target_idx(self.base_idx_mapping[1], delta, 20)

    def calc_ba_gua_matrix(self):

        ba_gua_symbol = {
            '1': "---",
            '0': "- -",
        }

        ba_gua_matrix = defaultdict(list)
        for row_idx, row in enumerate(BA_GUA_POSITION_MATRIX):
            for col_idx, col in enumerate(row):
                if col == 5:
                    continue
                details = BA_GUA_POSITION_MEANING_INDEXING[col]
                symbol = details['binary_symbol']
                msg = f"""
        {details['name']}宫（{col}）{details['location']}
        「{ba_gua_symbol.get(symbol[0], '')}
          {ba_gua_symbol.get(symbol[1], '')}
          {ba_gua_symbol.get(symbol[2], '')}」
        {details['family_member']}位（{details['element']}）
        {details['image']}
        应用作{details['usage']}这样可以{details['promote']}
        不应用作{details['oppose']}否则{details['inhibition']}
                """
                if self.self_element:
                    msg += f"""
        与命主关系为「{self.calc_element_relationship(self.self_element, details['element'])}」
                """
                ba_gua_matrix[row_idx].append(msg)

        return ba_gua_matrix

    def calc_target_star_matrix(self):
        position_matrix = defaultdict(list)
        for row_idx, row in enumerate(BA_GUA_POSITION_MATRIX):
            for col_idx, col in enumerate(row):
                details = NINE_STARS_DETAILS[self.target_idx_mapping[col]]
                msg = f"""
        {BA_GUA_POSITION_MEANING_INDEXING[col]['name']}宫：{details['name']}星（{details['color']}）
        五行属{details['element']}，是{details['meaning']}
                """
                if self.self_element:
                    msg += f"""
        与命主关系为「{self.calc_element_relationship(self.self_element, details['element'])}」
                """
                position_matrix[row_idx].append(msg)
        return position_matrix

    def position_matrix_to_str(self):
        return f"""
        {"-".join([f"{item}" for item in BA_GUA_POSITION_MATRIX[0]])}
        {"-".join([f"{item}" for item in BA_GUA_POSITION_MATRIX[1]])}
        {"-".join([f"{item}" for item in BA_GUA_POSITION_MATRIX[2]])}
        """

    def list_matrix_to_str(self, list_matrix):
        return "\n\n".join(["\n".join(lst for lst in line) for line in list_matrix.values()])
