from constants.constants import *


class ZodiacExplain:
    def __init__(self, meta_info):
        self.meta_info = meta_info
        self.zhi = meta_info.zodiac_zhi
        self.details = ZHI_ATTRIBUTES[self.zhi]
        self.san_he = self.calc_zodiac('合')
        self.liu_he = self.calc_zodiac('六')
        self.san_hui = self.calc_zodiac('会')
        self.chong = self.calc_zodiac('冲')
        self.xing = self.calc_zodiac('刑')
        self.bei_xing = self.calc_zodiac('被刑')
        self.hai = self.calc_zodiac('害')
        self.po = self.calc_zodiac('破')

        self.against = self.calc_against()

    def __str__(self):
        msg = f"""
        ### 生肖关系：
        三合：{', '.join(self.san_he)}
        六合：{', '.join(self.liu_he)}
        三会：{', '.join(self.san_hui)}
        冲：{', '.join(self.chong)}
        刑：{', '.join(self.xing)}
        被刑：{', '.join(self.bei_xing)}
        害：{', '.join(self.hai)} 
        破：{', '.join(self.po)}
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
            '三合': self.san_he,
            '六合': self.liu_he,
            '三会': self.san_hui,
        }

        negative = {
            '冲': self.chong,
            '刑': self.xing,
            '被刑': self.bei_xing,
            '害': self.hai,
            '破': self.po,
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
