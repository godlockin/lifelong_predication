import argparse

from constants import *
from lord_gods import LordGods


class FinanceStorage(LordGods):
    # 财位为离入户门最远的角落（房屋对角线）
    # 如果门在墙中间，则为对墙的两个墙角
    # 如果为多层，则看卧室所在层，多层都住人看男主人的卧室

    # 1、宜亮不宜暗2、应平整、安静3、宜坐宜卧4、宜放置吉祥物5、忌水
    # 如果是厕所，请一个三足金蟾放里面
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.finance_month = self.calc_finance_month()
        self.finance_strength_statement = self.calc_finance_strength()
        self.finance_supporting_status = self.calc_finance_supporting_status()
        self.finance_connection = self.calc_finance_connection()
        self.self_strong_finance_mapping = {
            (True, '旺'): '有欲望，能拿得起，可以发大财',
            (True, '弱'): '无欲望，遇到特殊的流年可以发小财',
            (True, '无'): '运见财发财，但不长久',
            (False, '旺'): '有欲望，但承载不了，发大财的时候会为其所累',
            (False, '弱'): '无欲望，一生顺遂，看淡了反而某些年份能发小财',
            (False, '无'): '不好发财，俗称“和尚命”'
        }
        self.finance_storage_mapping = {
            ('旺', True): '财旺有库，收入高也能存住钱。',
            ('旺', False): '财旺无库，收入高但是花费也高，不容易存钱。',
            ('弱', True): '财弱有库，收入不高但是能慢慢攒钱。',
            ('弱', False): '财弱无库，收入不高也花费大，不容易存钱。',
            ('无', True): '财无有库，财运不佳，但是适合做会计等岗位管理支出。',
            ('无', False): '财无无库，收入不高也容易漏财，不容易存钱。',
        }
        self.none_finance_append = self.append_content_none_finance(**kwargs)

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"

        msg += f'''
        ## 财运：
        财月：日元（{self.ri_gan}/{self.finance_month['element']}）所克制的五行（{self.finance_month['finance_element']}）所指的月份
        所以，日主的财月为 {self.finance_month['finance_month']}（{self.finance_month['finance_element']}）
        即农历：{self.finance_month['lunar_month']}
        又因为日主身{'强' if self.self_strong else '弱'}，所以财为「{'喜用' if self.self_strong else '忌凶'}」
        所以这几个月命主{'财运不错' if self.self_strong else '要小心破财'}
        '''

        self_strength_key = (self.self_strong, self.finance_strength_statement['finance_strength'])
        finance_storage_key = (
        self.finance_strength_statement['finance_strength'], self.finance_strength_statement['storage_exists'])
        msg += f'''
        命主日元：{self.ri_gan}，财为：{self.finance_strength_statement['wealth_element']}
        日元：{'强' if self.self_strong else '弱'}，财：{self.finance_strength_statement['finance_strength']}
        {self.self_strong_finance_mapping[self_strength_key]}
        财库为：{self.finance_strength_statement['wealth_storage']}，{'存在' if self.finance_strength_statement['storage_exists'] else '不存在'}于命局中，{'有' if self.finance_strength_statement['storage_exists'] else '无'}财库。
        {self.finance_storage_mapping[finance_storage_key]}
        {self.finance_connection}
        {self.finance_supporting_status}
        '''

        potential_years = self.finance_strength_statement['potential_years']
        if self_strength_key in potential_years:
            msg += f'''
        潜在发财年份：{potential_years[self_strength_key]}
            '''

        if self.none_finance_append:
            msg += f'''
        {self.none_finance_append}
            '''
        return msg

    def calc_finance_month(self):
        conditions = {
            '甲乙': {
                "element": "木",
                "finance_element": "土",
                "finance_month": ["戊辰", "己巳"],
                "lunar_month": "二月廿六～四月廿八"
            },
            '丙丁': {
                "element": "火",
                "finance_element": "金",
                "finance_month": ["庚午", "辛未"],
                "lunar_month": "四月廿九～七月初三"
            },
            '戊己': {
                "element": "土",
                "finance_element": "水",
                "finance_month": ["壬申", "癸酉"],
                "lunar_month": "七月初四～九月初五"
            },
            '庚辛': {
                "element": "金",
                "finance_element": "木",
                "finance_month": ["甲戌", "乙亥"],
                "lunar_month": "九月初六～十一月初五"
            },
            '壬癸': {
                "element": "水",
                "finance_element": "火",
                "finance_month": ["丙寅～丁卯", "丙子～丁丑"],
                "lunar_month": "正月初一～二月廿五，十一月初六～腊月廿九"
            }
        }

        for k, v in conditions.items():
            if self.ri_gan in k:
                return v

        return {}

    def calc_finance_strength(self):
        conditions = {
            "甲": {
                "formal_wealth": "己",
                "abnormal_wealth": "戊",
                "wealth_element": "土",
                "wealth_storage": "戌",
                "potential_years": {
                    (True, '旺'): [2025, 2026, 2027],
                    (True, '弱'): [2027, 2028, 2029],
                    (False, '旺'): [2025, 2031, 2032],
                    (False, '弱'): [2023, 2024, 2033],
                }
            },
            "乙": {
                "formal_wealth": "戊",
                "abnormal_wealth": "己",
                "wealth_element": "土",
                "wealth_storage": "戌",
                "potential_years": {
                    (True, '旺'): [2025, 2026, 2027],
                    (True, '弱'): [2027, 2028, 2029],
                    (False, '旺'): [2025, 2031, 2032],
                    (False, '弱'): [2023, 2024, 2033],
                }
            },
            "丙": {
                "formal_wealth": "辛",
                "abnormal_wealth": "庚",
                "wealth_element": "金",
                "wealth_storage": "丑",
                "potential_years": {
                    (True, '旺'): [2024, 2027, 2033],
                    (True, '弱'): [2028, 2029, 2030],
                    (False, '旺'): [2023, 2024, 2025],
                    (False, '弱'): [2027, 2031],
                }
            },
            "丁": {
                "formal_wealth": "庚",
                "abnormal_wealth": "辛",
                "wealth_element": "金",
                "wealth_storage": "丑",
                "potential_years": {
                    (True, '旺'): [2024, 2027, 2033],
                    (True, '弱'): [2028, 2029, 2030],
                    (False, '旺'): [2023, 2024, 2025],
                    (False, '弱'): [2027, 2031],
                }
            },
            "戊": {
                "formal_wealth": "癸",
                "abnormal_wealth": "壬",
                "wealth_element": "水",
                "wealth_storage": "辰",
                "potential_years": {
                    (True, '旺'): [2029, 2030, 2031],
                    (True, '弱'): [2022, 2023, 2032],
                    (False, '旺'): [2025, 2026, 2027],
                    (False, '弱'): [2024, 2027, 2028],
                }
            },
            "己": {
                "formal_wealth": "壬",
                "abnormal_wealth": "癸",
                "wealth_element": "水",
                "wealth_storage": "辰",
                "potential_years": {
                    (True, '旺'): [2029, 2030, 2031],
                    (True, '弱'): [2022, 2023, 2032],
                    (False, '旺'): [2025, 2026, 2027],
                    (False, '弱'): [2024, 2027, 2028],
                }
            },
            "庚": {
                "formal_wealth": "乙",
                "abnormal_wealth": "甲",
                "wealth_element": "木",
                "wealth_storage": "未",
                "potential_years": {
                    (True, '旺'): [2031, 2032, 2033],
                    (True, '弱'): [2022, 2023, 2025],
                    (False, '旺'): [2024, 2027, 2028],
                    (False, '弱'): [2028, 2029, 2030],
                }
            },
            "辛": {
                "formal_wealth": "甲",
                "abnormal_wealth": "乙",
                "wealth_element": "木",
                "wealth_storage": "未",
                "potential_years": {
                    (True, '旺'): [2031, 2032, 2033],
                    (True, '弱'): [2022, 2023, 2025],
                    (False, '旺'): [2024, 2027, 2028],
                    (False, '弱'): [2028, 2029, 2030],
                }
            },
            "壬": {
                "formal_wealth": "丁",
                "abnormal_wealth": "丙",
                "wealth_element": "火",
                "wealth_storage": "戌",
                "potential_years": {
                    (True, '旺'): [2024, 2025],
                    (True, '弱'): [2025, 2026, 2027],
                    (False, '旺'): [2028, 2029, 2030],
                    (False, '弱'): [2022, 2023, 2032],
                }
            },
            "癸": {
                "formal_wealth": "丙",
                "abnormal_wealth": "丁",
                "wealth_element": "火",
                "wealth_storage": "戌",
                "potential_years": {
                    (True, '旺'): [2024, 2025],
                    (True, '弱'): [2025, 2026, 2027],
                    (False, '旺'): [2028, 2029, 2030],
                    (False, '弱'): [2022, 2023, 2032],
                }
            }
        }

        finance_details = conditions[self.ri_gan]

        all_di_zhi_cang_gan = list(set(
            item for sublist in [self.di_zhi_cang_gan(di_zhi) for di_zhi in self.all_zhi] for item in sublist if item))
        formal_wealth = finance_details['formal_wealth']
        abnormal_wealth = finance_details['abnormal_wealth']
        formal_wealth_strength = self.calc_wealth_weight(formal_wealth, all_di_zhi_cang_gan)
        abnormal_wealth_strength = self.calc_wealth_weight(abnormal_wealth, all_di_zhi_cang_gan)
        max_strength = max(formal_wealth_strength, abnormal_wealth_strength)
        if 0 == max_strength:
            finance_strength = '无'
        elif 0 < max_strength < 1:
            finance_strength = '弱'
        else:
            finance_strength = '旺'

        finance_details.update({
            'finance_strength': finance_strength,
            'storage_exists': finance_details['wealth_storage'] in self.all_zhi,
        })
        return finance_details

    def calc_wealth_weight(self, item, all_di_zhi_cang_gan):
        strength = 0
        if item in all_di_zhi_cang_gan:
            strength += 0.4
            if item in self.all_gan:
                strength += 0.6
        return strength

    def calc_finance_supporting_status(self):
        wealth_storage = self.finance_strength_statement['wealth_storage']
        wealth_element = self.finance_strength_statement['wealth_element']

        wealth_storage_element = ZHI_DETAILS[wealth_storage]['element']
        result = f"财库为「{wealth_storage}({wealth_storage_element})」，"
        if wealth_element == wealth_storage_element:
            result += f"财星「{wealth_element}」同类相帮扶，进一步提升财运。"
        elif SWAPPED_ELEMENTS_SUPPORTING[wealth_element] == wealth_storage_element:
            result += f"生财星「{wealth_element}」（{wealth_storage_element}生{wealth_element}），非常有利于命主之财运。"
        elif SWAPPED_ELEMENTS_OPPOSING[wealth_element] == wealth_storage_element:
            result += f"克制财星「{wealth_element}」（{wealth_storage_element}克{wealth_element}），很不利于命主之财运。"
        elif ELEMENTS_OPPOSING[wealth_element] == wealth_storage_element:
            result += f"损耗财星「{wealth_element}」（{wealth_element}克{wealth_storage_element}），不利于命主之财运。"
        elif ELEMENTS_SUPPORTING[wealth_element] == wealth_storage_element:
            result += f"化泄财星「{wealth_element}（{wealth_element}生{wealth_storage_element}）」，不利于命主之财运。"

        return result

    def append_content_none_finance(self, **kwargs):
        result = []
        result.append("### 八字中全无财星")
        result.append("* 心目中没有经济和经营观念" +
                      ("\n** 一个人八字中全无财星，说明这个人对于钱财没有概念，做事不会考虑物质利益，不会精打细算，也不会将自己的心思放在经济谋划和长袖善舞的经营方面。" if self.explain_append else ""))
        result.append("* 开支计划性不强" +
                      ("\n** 也正因为从来不把钱财挂在心上，故此，即使赚再多的钱，也在身上存不住。常常是上午赚钱，下午就没有钱财在身上。支出用度，盲目性很大，计划性太差，易因投资、经营而破财、破产。" if self.explain_append else ""))
        result.append("* 父缘不足" +
                      ("\n** 八字中偏财为父，原局无财，自然与父缘分很浅。不是父亲早丧，就是父亲病残，无能很弱；或者就是父亲不在身边，聚少离多，没有沟通与交集，有也相当于无。" if self.explain_append else ""))
        result.append("* 妻缘浅薄" +
                      ("\n** 八字中正财为男子之妻，原局无财，说明妻缘较浅，或者晚婚；或者夫妻感情不好，难以白头偕老；或者妻子不在身边，聚少离多。" if self.explain_append else ""))
        result.append("* 需要用贵显富" +
                      ("\n** 八字不见财星之人，大多一生中与财结缘的机会不多。他们与常人不同，不会一门心思、全部精力都投入到赚钱方面。因此，他们获得财富的方式，大多要通过职业和职位的发展来求取利益，有了功名则有钱。" if self.explain_append else ""))

        # 克我者为官杀
        # 我克者为财才
        # 生我者为印枭
        # 我生者为食伤
        # 同我者为比劫
        self_detail = GAN_DETAILS[self.ri_gan]
        self_element = self.primary_element
        self_yinyang = self_detail['yinyang']
        # 1、八字中喜财用财，有食伤财源之人
        if self.self_strong:
            if (
                (self.lord_god_explain.single_explain_mapping['食神'].lord_gods_count + self.lord_god_explain.single_explain_mapping['伤官'].lord_gods_count) >= 5
            ):
                result.append("* 命主八字身强，喜财用财，八字中虽然全无财星，但有有力的食伤星可用。因为，食伤星犹如财的源头，既然有源头，则不要愁没钱的来源。也主其人，一生不会缺少钱花，要靠技术、名声、专长获得财富；但要善于积累。")
            elif (
                self.lord_god_explain.single_explain_mapping['正官'].lord_gods_count < self.lord_god_explain.single_explain_mapping['正印'].lord_gods_count
            ):
                result.append("* 命主八字身强，大多用官制身。如果官星偏弱，则要财星滋官显贵。见印泄官，则贵气不显，亦要财星制印。如果原局或者岁运不见财星，其人则一生清苦，毫无财运，宜守穷途。")
            elif (
                    (self.lord_god_explain.single_explain_mapping['食神'].lord_gods_count + self.lord_god_explain.single_explain_mapping['伤官'].lord_gods_count)
                    <= (self.lord_god_explain.single_explain_mapping['正官'].lord_gods_count + self.lord_god_explain.single_explain_mapping['七杀'].lord_gods_count)
            ):
                result.append("* 命主八字身强则要制要泄，如果制泄两出，相互缠斗，则要救应通关之财。如果局运之走，毫无财星。则官杀不能制身，食伤不能泄身，命主不得无益，自然是事业不顺，难有财运了。")
        else:
            if self.lord_god_explain.single_explain_mapping['七杀'].lord_gods_count >= 4:
                result.append("* 命主八字中杀旺身弱，财星则为仇神，如果，原局全无财星，反而是财运很好的表现。行运遇见印比帮身之时，因贵而富，富贵齐来。主因为职务、名声、地位而享有财富。")

        return f"""
    {'\n'.join(result)}
        """ if result else ''

    def calc_finance_connection(self):
        finance_element = ELEMENTS_OPPOSING[self.ri_gan_element]
        self_yinyang = GAN_DETAILS[self.ri_gan]['yinyang']
        finance_yinyang = ZHI_DETAILS[self.yue_zhi]['yinyang']
        if self_yinyang == finance_yinyang:
            finance_type = "偏财"
        else:
            finance_type = "正财"

        if self.yue_zhi_element == finance_element:
            return f"""
        命主财气为「{finance_element}」刚好处于月令，称之为“财气通门户”，财运很旺。而且为「{finance_type}」。
        又由于命主身{'强' if self.self_strong else '弱'}，所以财为「{'喜用' if self.self_strong else '忌凶'}」
        所以命主大概率{'大富大贵' if self.self_strong else '但不住财'}。
        """
        else:
            return ""


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
    prediction = FinanceStorage(
        base_datetime=main_birthday,
        meta_info_display=True,
        explain_append=explain_append,
        is_male=is_male,
    )
    print(prediction)