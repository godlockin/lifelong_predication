from backend.constants.constants import *


class ZodiacExplain:
    def __init__(self, meta_info):
        self.meta_info = meta_info
        self.zhi = meta_info.zodiac_zhi
        self.details = ZHI_ATTRIBUTES[self.zhi]
        zodiacs = ['合', '六', '会', '冲', '刑', '被刑', '害', '破']
        for zodiac in zodiacs:
            setattr(self, zodiac, self.calc_zodiac(zodiac))

        self.against = self.calc_against()

    def __str__(self):
        msg = f"""
        ### 生肖关系：
        三合：{', '.join(self.合)}
        六合：{', '.join(self.六)}
        三会：{', '.join(self.会)}
        冲：{', '.join(self.冲)}
        刑：{', '.join(self.刑)}
        被刑：{', '.join(self.被刑)}
        害：{', '.join(self.害)} 
        破：{', '.join(self.破)}
        """

        if self.against:
            msg += f'''
        {self.against}
            '''

        return msg

    def calc_zodiac(self, idx):
        target_item = self.details[idx]
        if isinstance(target_item, tuple):
            return [ZHI_DETAILS[item]['zodiac'] for item in target_item]
        elif isinstance(target_item, str):
            return [ZHI_DETAILS[target_item]['zodiac']]
        else:
            return []

    def calc_against(self):
        positive = {
            '三合': self.合,
            '六合': self.六,
            '三会': self.会,
        }

        negative = {
            '冲': self.冲,
            '刑': self.刑,
            '被刑': self.被刑,
            '害': self.害,
            '破': self.破,
        }

        against_list = []
        for key, value in negative.items():
            for k, v in positive.items():
                if value in v or value == v:
                    against_list.append((value, key, k))

        result = ""
        if not against_list:
            return result

        result = "在命主与这些生肖的各种关系中，也可能会有抵消的可能，比如："
        result += ",".join([f"{item[0]} - {item[1]}/{item[2]}" for item in against_list])

        return result
