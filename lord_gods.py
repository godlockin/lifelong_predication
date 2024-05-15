from collections import defaultdict, Counter

from ba_zi_elements import BaZiElements
from constants import *
from lord_god_explain import LordGodExplain


class LordGods(BaZiElements):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.ri_gan_idx = GAN.index(self.ri_gan) + 1
        (
            self.nian_gan_core_lord_gods,
            self.yue_gan_core_lord_gods,
            self.ri_gan_core_lord_gods,
            self.shi_gan_core_lord_gods
        ) = self.handle_gan_lord_gods(self.ri_gan_idx, self.all_gan)

        (
            self.nian_zhi_core_lord_gods,
            self.yue_zhi_core_lord_gods,
            self.ri_zhi_core_lord_gods,
            self.shi_zhi_core_lord_gods
        ) = self.handle_zhi_lord_gods(self.all_zhi)
        self.all_zhi_core_lord_gods = [
            self.nian_zhi_core_lord_gods,
            self.yue_zhi_core_lord_gods,
            self.ri_zhi_core_lord_gods,
            self.shi_zhi_core_lord_gods
        ]

        (
            (self.nian_zhi_cang_gan_list, self.nian_zhi_cang_gan_lord_gods),
            (self.yue_zhi_cang_gan_list, self.yue_zhi_cang_gan_lord_gods),
            (self.ri_zhi_cang_gan_list, self.ri_zhi_cang_gan_lord_gods),
            (self.shi_zhi_cang_gan_list, self.shi_zhi_cang_gan_lord_gods)
        ) = self.handle_zhi_cang_gan_lord_gods(self.ri_gan_idx)

        """
        [
            ["比肩", ...],
            [[('丙', '火', '正印'), ('戊', '土', '劫财'), ('庚', '金', '伤官')], ...]
        ]
        """
        self.lord_gods_w_cang_gan_matrix = [
            [
                self.nian_gan_core_lord_gods, self.yue_gan_core_lord_gods, self.ri_gan_core_lord_gods, self.shi_gan_core_lord_gods
            ],
            [
                self.nian_zhi_cang_gan_lord_gods, self.yue_zhi_cang_gan_lord_gods, self.ri_zhi_cang_gan_lord_gods, self.shi_zhi_cang_gan_lord_gods
            ]
        ]

        self.lord_gods_w_cang_gan_core_matrix = self.calc_lord_gods_w_cang_gan_core_matrix()

        self.all_gan_lord_gods, self.all_zhi_lord_gods = self.lord_gods_w_cang_gan_core_matrix[0], self.lord_gods_w_cang_gan_core_matrix[1]

        self.all_lord_gods = self.all_gan_lord_gods + self.all_zhi_lord_gods
        self.all_lord_gods_list = [item for sublist in self.all_lord_gods for item in sublist if item]
        self.all_lord_gods_counter = Counter(self.all_lord_gods_list)
        self.distinct_all_lord_gods = list(set(self.all_lord_gods_list))
        self.lord_gods_supporting = self.calc_lord_gods_supporting()
        self.lord_gods_supporting_lines = self.build_lord_gods_supporting_lines()

        self.lord_god_explain = LordGodExplain(self)
        self.lord_god_explain.init_explanation()

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        ## 十神：
        年干：{self.nian_gan_core_lord_gods}（{self.nian_gan},{GAN_DETAILS[self.nian_gan]['element']}）
        年支：*{self.nian_zhi_core_lord_gods}（{self.nian_zhi},{ZHI_DETAILS[self.nian_zhi]['element']}）{self.nian_zhi_cang_gan_lord_gods}
        
        月干：{self.yue_gan_core_lord_gods}（{self.yue_gan},{GAN_DETAILS[self.yue_gan]['element']}）
        月令：*{self.yue_zhi_core_lord_gods}（{self.yue_zhi},{ZHI_DETAILS[self.yue_zhi]['element']}）{self.yue_zhi_cang_gan_lord_gods}
        
        日干：日主（{self.ri_gan},{GAN_DETAILS[self.ri_gan]['element']}）
        日支：*{self.ri_zhi_core_lord_gods}（{self.ri_zhi},{ZHI_DETAILS[self.ri_zhi]['element']}）{self.ri_zhi_cang_gan_lord_gods}
        
        时干：{self.shi_gan_core_lord_gods}（{self.shi_gan},{GAN_DETAILS[self.shi_gan]['element']}）
        时支：*{self.shi_zhi_core_lord_gods}（{self.shi_zhi},{ZHI_DETAILS[self.shi_zhi]['element']}）{self.shi_zhi_cang_gan_lord_gods}
        
        ### 十神喜忌：
        {self.lord_gods_supporting_lines}
        
        ### 性格
        人前表现出来的气质：{APPEARANCE_MAPPING[self.nian_gan_core_lord_gods]}
        人后真实的性格：{APPEARANCE_MAPPING[self.shi_gan_core_lord_gods]}
        '''

        if self.explain_append:
            double_append = self.calc_double_appear()
            if double_append:
                msg += double_append
            msg += self.lord_god_explain.calc_all_lord_gods_explain()
        return msg

    def handle_zhi_cang_gan_lord_gods(self, ri_gan_idx):
        # 循环所有地支
        # 第一步找到每个地支的藏干
        di_zhi_cang_gan_list = [self.di_zhi_cang_gan(item) for item in self.all_zhi]
        # 第二步根据每个藏干找到对应的十神
        di_zhi_lord_gods_list = [
            # 对于每个地支的藏干元素，查表去找它的十神
            (cang_gan_list, [(item, GAN_MATRIX[GAN.index(item)][3], LORD_GODS_MATRIX[ri_gan_idx][LORD_GODS_MATRIX[0].index(item)])
                             for item in cang_gan_list if item])
            for cang_gan_list in di_zhi_cang_gan_list
        ]

        return di_zhi_lord_gods_list

    def handle_gan_lord_gods(self, ri_gan_idx, bz_list):
        return [LORD_GODS_MATRIX[ri_gan_idx][LORD_GODS_MATRIX[0].index(item)] for item in bz_list]

    def handle_zhi_lord_gods(self, bz_list):
        gan_details = GAN_DETAILS[self.ri_gan]
        gan_element = gan_details['element']
        gan_yinyang = gan_details['yinyang']
        lord_gods = []
        for item in bz_list:
            zhi_details = ZHI_DETAILS[item]
            zhi_element = zhi_details['element']
            zhi_yinyang = zhi_details['yinyang']
            if gan_element == zhi_element:
                if gan_yinyang == zhi_yinyang:
                    lord_gods.append("比肩")
                else:
                    lord_gods.append("劫财")
            elif ELEMENTS_SUPPORTING[gan_element] == zhi_element:
                if gan_yinyang == zhi_yinyang:
                    lord_gods.append("食神")
                else:
                    lord_gods.append("伤官")
            elif SWAPPED_ELEMENTS_SUPPORTING[gan_element] == zhi_element:
                if gan_yinyang == zhi_yinyang:
                    lord_gods.append("偏印")
                else:
                    lord_gods.append("正印")
            elif ELEMENTS_OPPOSING[gan_element] == zhi_element:
                if gan_yinyang == zhi_yinyang:
                    lord_gods.append("偏财")
                else:
                    lord_gods.append("正财")
            elif SWAPPED_ELEMENTS_OPPOSING[gan_element] == zhi_element:
                if gan_yinyang == zhi_yinyang:
                    lord_gods.append("七杀")
                else:
                    lord_gods.append("正官")
        return lord_gods

    def di_zhi_cang_gan(self, zhi):
        """
        地支藏干
        子藏癸 卯藏乙 午藏丁己  酉藏辛
        寅藏 甲丙戊  巳藏 丙庚戊  申藏 庚壬戊  亥藏 甲壬
        丑藏 辛癸己 辰藏 癸乙戊  未藏 乙丁己  戌藏 丁辛戊
        :param zhi:
        :return:
        """
        return CANG_GAN.get(zhi, ["", "", ""])

    def calc_double_appear(self):
        result = []
        if self.nian_gan == self.yue_gan:
            result.append(f"""
        年干与月干相同，名为“叠遇”。
            """)
            if self.nian_gan_core_lord_gods == self.yue_gan_core_lord_gods:
                result.append(f"""
        主人32岁之前，性格脾气学识感情婚姻养成之时。命里反反复复见，来来回回走三遍。好的坏的，主反复难安。
                """)
            if '比肩' == self.nian_gan_core_lord_gods:
                result.append(f"""
        比肩叠遇，出身穷困，人穷志短，不重钱财，手艺吃饭。
        比肩叠遇主出身平常，上有兄姐，身无暗疾，仪容端庄，不重钱财，言多不密，三十二岁前是非小人多。
            """)
            if '劫财' == self.nian_gan_core_lord_gods:
                result.append(f"""
        劫财叠遇，母安父先亡，六亲无靠，人生必遭一直两次大败。晚婚，不然二婚不到头。
        劫财叠遇主刚愎自负，喜怒形于色，聪明反被聪明误，三十二岁前必有大败；与父无缘，不宜早婚，恐有婚变。
                """)
            if '食神' == self.nian_gan_core_lord_gods:
                result.append(f"""
        食神叠遇，出身富贵，性慈善良，女嫁良夫早得子，长寿自得。
        食神叠遇主出身安逸之家，性慈善良，女命早年得子，不见无刑冲、枭神夺食者，一生长寿悠游自得。
                """)
            if '伤官' == self.nian_gan_core_lord_gods:
                tmp = "伤官叠遇，年少不良，孤傲刚毅，六亲无靠，手艺立业，逍遥自得。"
                if not self.is_male:
                    tmp += "女命晚婚或夫亡再嫁或少年独守空房。"
                tmp += "伤官叠遇主性孤傲刚毅，六亲无靠；女命三十二岁前婚姻难言缱绻，多嫁老夫，先同居后成婚。"
                result.append(f"""
        {tmp}
                """)
            if '正财' == self.nian_gan_core_lord_gods or '偏财' == self.nian_gan_core_lord_gods:
                tmp = "财星叠遇，出生富贵，口含金匙，"
                if self.is_male:
                    tmp += "男主双妻娇美。"
                else:
                    tmp += "女主欺婆骂夫。"
                tmp += "正财偏财叠遇主天生理财头脑，男命恐有双妻，女命易因财失家。"
                result.append(f"""
        {tmp}
                """)
            if '正官' == self.nian_gan_core_lord_gods:
                tmp = "正官叠遇，"
                if self.is_male:
                    tmp += "男主性情温和，学识过人，早年成家。"
                else:
                    tmp += "女主一女二夫，婚姻不顺。"
                result.append(f"""
        {tmp}
                """)
            if '七杀' == self.nian_gan_core_lord_gods:
                tmp = "七杀叠遇，出身贫寒，多灾多病。"
                if self.is_male:
                    tmp += "男防牢狱。"
                else:
                    tmp += "女防失身。"
                result.append(f"""
        {tmp}
                """)
            if '偏印' == self.nian_gan_core_lord_gods:
                tmp = "主修身好佛，心性偏激。"
                if self.is_male:
                    tmp += "男命心灵手巧，孤芳自赏。"
                else:
                    tmp += "女命洁身自好，远嫁他乡。"
                tmp += "偏印叠遇主品性孤慧，剑走偏锋，六亲无靠，晚年吉祥。"
                result.append(f"""
        {tmp}
                """)
            if '正印' == self.nian_gan_core_lord_gods:
                result.append(f"""
        正印叠遇主有修养，女命再见阳刃格，主性格独立，婚姻不顺。
                """)

        if self.nian_gan == self.shi_gan:
            result.append(f"""
        年干与时干相同，名为“两头挂”。
                    """)
            if '七杀' == self.nian_gan_core_lord_gods or '正官' == self.nian_gan_core_lord_gods:
                result.append(f"""
        七杀两头挂，到老无后人。正官、七杀两头挂，因为官多为杀。无论男女命，主一生灾祸不断，不易有儿子。命局搭配不合者，甚至难有子女。
                """)
            if '伤官' == self.nian_gan_core_lord_gods:
                tmp = "伤官两头挂，亲情剩不下。"
                if not self.is_male:
                    tmp += "女命伤官两头挂，好骂丈夫是刁人。"
                tmp += "无论男女命，主六亲无靠，骨肉难近，注重精神享受，常有怀才不遇之感慨。若伤官伤尽，则主富贵双全。若逢正官格，一生贫贱无疑。女命宜养妇德。"
                result.append(f"""
        {tmp}
                """)
            if '食神' == self.nian_gan_core_lord_gods:
                result.append(f"""
        食神两头挂，吃喝全天下。无论男女命，皆主一生有口福。
                """)
            if '正印' == self.nian_gan_core_lord_gods or '偏印' == self.nian_gan_core_lord_gods:
                result.append(f"""
        印绶两头挂，必定慈善人。无论男女命，皆主善良，宜从事宗教、艺术、专长类工作。女命则不利于子息。
                """)
            if '正财' == self.nian_gan_core_lord_gods or '偏财' == self.nian_gan_core_lord_gods:
                result.append(f"""
        财星两头挂，出手大方人。无论男女命，皆主为人阔绰，出手大方。
                """)
            if '劫财' == self.nian_gan_core_lord_gods or '比肩' == self.nian_gan_core_lord_gods:
                result.append(f"""
        劫财两头挂，茕茕孑立人。比肩、劫财两头挂，无论男女命，皆主一生难得真正得力之亲友。若逢财格，一生贫寒彻骨。
                """)

        if self.yue_gan == self.shi_gan:
            result.append(f"""
        月干与时干相同，名为“月时两见”。
                    """)
            if self.yue_gan_core_lord_gods == self.shi_gan_core_lord_gods:
                if '正官' == self.yue_gan_core_lord_gods:
                    tmp = "正官月时两见，无论男女命，皆主下有弟妹或亲人需要照顾。"
                    if self.is_male:
                        tmp += "男命为人正直。"
                    else:
                        tmp += "女命为情所困。"
                    result.append(f"""
        {tmp}
                    """)
                if '七杀' == self.yue_gan_core_lord_gods:
                    result.append(f"""
        七杀月时两见。无论男女命，皆主性格浮躁，行事虎头蛇尾。上有兄姐，出身平凡。
                    """)
                if '食神' == self.yue_gan_core_lord_gods or '伤官' == self.yue_gan_core_lord_gods:
                    tmp = "食伤月时两见，无论男女命，皆主性格孤傲，不屈于物质现实生活，六亲不靠。"
                    if not self.is_male:
                        tmp += "女命三十二岁之前，婚姻无靠。"
                    result.append(f"""
        {tmp}
                    """)
                if '正印' == self.yue_gan_core_lord_gods or '偏印' == self.yue_gan_core_lord_gods:
                    tmp = "印绶月时两见，无论男女命，皆主为人清高，好礼佛，性格执拗，婚姻坎坷。"
                    if not self.is_male:
                        tmp += "女命主子息迟或无缘。"
                    result.append(f"""
        {tmp}
                    """)
                if '正财' == self.yue_gan_core_lord_gods or '偏财' == self.yue_gan_core_lord_gods:
                    tmp = "财星月时两见，无论男女命，皆主为人现实，重视物质生活。"
                    if not self.is_male:
                        tmp += "女命不利公婆，旺夫兴家。"
                    result.append(f"""
        {tmp}
                    """)
                if '比肩' == self.yue_gan_core_lord_gods or '劫财' == self.yue_gan_core_lord_gods:
                    result.append(f"""
        比劫月时两见，无论男女命，主任情而钱财难得，主婚姻及财运一生不顺，尤忌财格。
                    """)

        return f"""
        ### 叠遇
        {" ".join(result)}
        """ if result else ""

    def calc_lord_gods_w_cang_gan_core_matrix(self):
        core_matrix = defaultdict(list)
        for row_idx, row in enumerate(self.lord_gods_w_cang_gan_matrix):
            for col_idx, col in enumerate(row):
                if 0 == row_idx:
                    core_matrix[row_idx].append([col])
                else:
                    core_matrix[row_idx].append([item[2] for item in col])
        return core_matrix

    def calc_lord_gods_supporting(self):
        result = defaultdict(list)
        self_details = GAN_DETAILS[self.ri_gan]
        self_yin_yang = self_details['yinyang']
        def append_records(self_yin_yang, element, key):
            if element == self.ri_gan_element:
                result[key].append({
                    "name": "比肩",
                    "element": element,
                    "yinyang": self_yin_yang
                })
                result[key].append({
                    "name": "劫财",
                    "element": element,
                    "yinyang": YIN_YANG_SWAP[self_yin_yang]
                })
            elif element == ELEMENTS_SUPPORTING[self.ri_gan_element]:
                result[key].append({
                    "name": "食神",
                    "element": element,
                    "yinyang": self_yin_yang
                })
                result[key].append({
                    "name": "伤官",
                    "element": element,
                    "yinyang": YIN_YANG_SWAP[self_yin_yang]
                })
            elif element == SWAPPED_ELEMENTS_SUPPORTING[self.ri_gan_element]:
                result[key].append({
                    "name": "偏印",
                    "element": element,
                    "yinyang": self_yin_yang
                })
                result[key].append({
                    "name": "正印",
                    "element": element,
                    "yinyang": YIN_YANG_SWAP[self_yin_yang]
                })
            elif element == ELEMENTS_OPPOSING[self.ri_gan_element]:
                result[key].append({
                    "name": "偏财",
                    "element": element,
                    "yinyang": self_yin_yang
                })
                result[key].append({
                    "name": "正财",
                    "element": element,
                    "yinyang": YIN_YANG_SWAP[self_yin_yang]
                })
            elif element == SWAPPED_ELEMENTS_OPPOSING[self.ri_gan_element]:
                result[key].append({
                    "name": "七杀",
                    "element": element,
                    "yinyang": self_yin_yang
                })
                result[key].append({
                    "name": "正官",
                    "element": element,
                    "yinyang": YIN_YANG_SWAP[self_yin_yang]
                })

        for element in self.supporting_elements_sequence:
            append_records(self_yin_yang, element, "support_lord_gods")
        for element in self.opposing_elements_sequence:
            append_records(self_yin_yang, element, "opposing_lord_gods")

        return result

    def build_lord_gods_supporting_lines(self):
        result = []
        for key, value_list in self.lord_gods_supporting.items():
            for value in value_list:
                result.append(f"{value['name']}({'喜用' if key == 'support_lord_gods' else '忌凶'})"
                              f"「{value['yinyang']}{value['element']}」")
            result.append("-"*14)
        return "\n".join(result[:-1])
