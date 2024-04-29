import itertools

from constants import *


class LordGodExplain:
    def __init__(self, lord_gods):
        self.lord_gods = lord_gods
        self.name = ""
        self.short_name = ""
        self.type = ""
        self.character = ""
        self.imagery = ""
        self.career = ""
        self.representatives = ""
        self.representatives_for_male = ""
        self.representatives_for_female = ""

        self.total_weight = 0
        self.lord_gods_count = 0
        self.weight_matrix = [[0 for _ in range(4)] for _ in range(2)]

    def __post_construction__(self):
        self.total_weight, self.lord_gods_count, self.weight_matrix = self.calc_lord_god_weight()

    def explain(self):

        result = f'''
        {self.name}（{self.short_name}）
        类型：{self.type}
        计数：{self.lord_gods_count}
        权重：{self.total_weight}
        性格特征：
        {self.character}
        意象：
        {self.imagery}
        适合从事的职业：
        {self.career}
        代表人物：
        {self.representatives}，以及{self.representatives_for_male if self.lord_gods.is_male else self.representatives_for_female}
        '''

        return result

    def calc_lord_god_weight(self):
        total_weight = 0
        lord_gods_count = 0
        weight_matrix = [[0 for _ in range(4)] for _ in range(2)]
        for row_idx in range(len(POSITION_NAMES)):
            for col_idx in range(len(POSITION_NAMES[row_idx])):
                position_name = POSITION_NAMES[row_idx][col_idx]
                weight = 0
                # 天干权重直接加
                if '干' in position_name:
                    if self.name == self.lord_gods.lord_gods_matrix[row_idx][col_idx]:
                        delta_element = self.lord_gods.elements_matrix[row_idx][col_idx]
                        delta = self.lord_gods.elements_relationships_mapping[delta_element][1]
                        weight = POSITION_WEIGHT[row_idx][col_idx] + delta
                else:
                    zhi_lord_gods = self.lord_gods.lord_gods_matrix[row_idx][col_idx]
                    for idx, cang_gan in enumerate(zhi_lord_gods):
                        if self.name == cang_gan[2]:
                            weight = POSITION_WEIGHT[row_idx][col_idx]
                            weight += self.lord_gods.elements_relationships_mapping[cang_gan[1]][1]
                            weight *= CANG_GAN_WEIGHT[idx]
                            break
                if weight != 0:
                    lord_gods_count += 1
                    weight_matrix[row_idx][col_idx] = weight
                    total_weight += weight
        return round(total_weight, 4), lord_gods_count, weight_matrix

    def init_explanation(self):

        self.combine_explain_mapping = {
            '正印': self.calc_zheng_yin,
            '食神': self.calc_shi_shen,
            '正财': self.calc_zheng_cai,
            '七杀': self.calc_qi_sha,
            '偏印': self.calc_pian_yin,
            '伤官': self.calc_shang_guan,
        }

        self.single_explain_mapping = {
            '正印': ZhengYin(self.lord_gods),
            '食神': ShiShen(self.lord_gods),
            '正官': ZhengGuan(self.lord_gods),
            '正财': ZhengCai(self.lord_gods),

            '七杀': QiSha(self.lord_gods),
            '偏印': PianYin(self.lord_gods),
            '伤官': ShangGuan(self.lord_gods),
            '劫财': JieCai(self.lord_gods),

            '比肩': BiJian(self.lord_gods),
            '偏财': PianCai(self.lord_gods),
        }

    def calc_all_lord_gods_explain(self):
        all_explain = f"""
        ### 十神解析
        十神也讲究平衡，无论吉神与恶神，多了都不好；一位为真，两位为争，三位为杂，四五六个乱如麻，七个八个反成奇。
        """

        all_lord_gods_names = list(set(self.lord_gods.all_lord_gods))
        single_explain = [self.single_explain_mapping[item] for item in all_lord_gods_names]
        single_explain.sort(key=lambda x: (x.lord_gods_count, x.total_weight), reverse=True)
        for item in single_explain:
            all_explain += f"""
        {item.explain()}
        """

        all_explain += f"""
        十神之间也有相生相克的关系：
        """
        all_lord_gods_seq_w_weight = [item.name for item in single_explain]
        combine_explain = [self.combine_explain_mapping[item](self.single_explain_mapping) for item in all_lord_gods_seq_w_weight if item in self.combine_explain_mapping]
        for item in combine_explain:
            if not item:
                continue
            all_explain += f"""
        {item}
            """

        return all_explain

    def calc_zheng_yin(self, single_explain_mapping):
        result = ""
        main_lord_god_count = single_explain_mapping['正印'].lord_gods_count
        if main_lord_god_count < 0:
            return result

        result += """
        正印：
        财可以克印。
        """
        zheng_cai_count = single_explain_mapping['正财'].lord_gods_count
        if self.lord_gods.is_male:
            tmp = "男命正印代表母亲，正财代表男人老婆。男人一旦发财则母亲身体会不好。"
            if main_lord_god_count > zheng_cai_count:
                tmp += "命主正印更强，所以命主更向着婆婆。"
            elif main_lord_god_count < zheng_cai_count:
                tmp += "命主正财更强，所以命主更向着老婆。"
            else:
                tmp += "所以命主家的婆婆和媳妇家庭地位相对平等"
            result += f"""
        {tmp}
            """
        else:
            tmp = ""
            if main_lord_god_count > 0:
                tmp += "女命正印代表母亲。"
                if main_lord_god_count > 3:
                    tmp += "正印多的女人会受到母亲过多的照顾，而变成溺爱，因此，其人往往缺乏独立自主精神。"
            tmp += "命主如果发财则会妨碍到祖父或者女婿。"
            result += f"""
        {tmp}
            """

        if main_lord_god_count == single_explain_mapping['七杀'].lord_gods_count:
            result += f"""
        正印和七杀数量一致，说明所有七杀都被印克制，意味着官印相生，这时命主的学习能力比较强，学什么都很快，也很容易达成成就。
            """
        return result

    def calc_shi_shen(self, single_explain_mapping):
        result = ""
        main_lord_god_count = single_explain_mapping['食神'].lord_gods_count
        if main_lord_god_count < 0:
            return result

        pian_yin_count = single_explain_mapping['偏印'].lord_gods_count
        if pian_yin_count > 0:
            pian_yin_list = self.lord_god_exist_position_for_relationships('偏印')
            shi_shen_list = self.lord_god_exist_position_for_relationships('食神')

            if shi_shen_list and pian_yin_list:
                result += "食神和偏印不对付。\n"
                distinct = set()
                tmp = []
                for shi_shen, pian_yin in list(itertools.product(shi_shen_list, pian_yin_list)):
                    if shi_shen == pian_yin:
                        continue

                    pair = "+".join(sorted([shi_shen, pian_yin]))
                    if pair in distinct:
                        continue
                    tmp.append(f"{shi_shen}和{pian_yin}关系不好。\n")
                    distinct.add(pair)
                result += f"""
        {"".join(tmp)}  
                """

        qi_sha_count = single_explain_mapping['七杀'].lord_gods_count
        if 0 < qi_sha_count < main_lord_god_count:
            result += """
        食神可以克制官杀，压制七杀保护自己，减少病痛灾祸。
            """

        return "食神：\n" + result if result else ""

    def calc_zheng_cai(self, single_explain_mapping):
        result = ""
        main_lord_god_count = single_explain_mapping['正财'].lord_gods_count
        if main_lord_god_count < 0:
            return result

        pian_cai_count = single_explain_mapping['偏财'].lord_gods_count
        if main_lord_god_count + pian_cai_count > 5:
            result += "正财和偏财多的人财运好，但是要小心不要一直沉迷搞钱，对别的都不感兴趣。"

        return "正财：\n" + result if result else ""

    def calc_qi_sha(self, single_explain_mapping):
        result = ""
        main_lord_god_count = single_explain_mapping['七杀'].lord_gods_count
        if main_lord_god_count < 0:
            return result

        zhang_yin_count = single_explain_mapping['正印'].lord_gods_count
        shi_shen_count = single_explain_mapping['食神'].lord_gods_count
        pian_yin_count = single_explain_mapping['偏印'].lord_gods_count
        if not self.lord_gods.self_strong:
            if zhang_yin_count > main_lord_god_count:
                result += "身弱有正印化解七杀。七杀生正印，正印生日元。七杀反为我用，叫杀印相生。"

            if shi_shen_count > main_lord_god_count and pian_yin_count < shi_shen_count:
                result += "身弱有食神制杀，没有偏印损害食神，叫食神制杀。"

        return "七杀：\n" + result if result else ""

    def calc_pian_yin(self, single_explain_mapping):
        result = ""
        main_lord_god_count = single_explain_mapping['偏印'].lord_gods_count
        if main_lord_god_count < 0:
            return result

        result += """
        偏印：
        """
        pian_yin_list = self.lord_god_exist_position_for_relationships('偏印')
        result += f"""
        偏印有心思细腻的意象，比如自己的：{pian_yin_list} 的心思就有可能很细腻。
        """
        shi_shen_count = single_explain_mapping['食神'].lord_gods_count
        if shi_shen_count == 0:
            result += f"""
        命里有偏印没有食神，自己会和偏印所在宫的人不和：{pian_yin_list}
            """

        return result

    def calc_shang_guan(self, single_explain_mapping):
        result = ""
        main_lord_god_count = single_explain_mapping['伤官'].lord_gods_count
        if main_lord_god_count < 0:
            return result

        zheng_yin_count = single_explain_mapping['正印'].lord_gods_count
        if zheng_yin_count > main_lord_god_count:
            result += "伤官配印，非富即贵。如果一个人命中伤官特别强，又有强印来制，含义为:一个胆大，有魄力，才华横溢的人，同时又具备忍耐，慈爱，勤恳的德行，那么升官肯定特别快，到哪里都会脱颖而出，干出一番事业，更何况印也主权，所以伤官配印的人成为人上人的概率很高。"

        return "伤官：\n" + result if result else ""

    def lord_god_exist_position_for_body_parts(self, idx_name):
        position_mapping = []
        if idx_name == self.lord_gods.nian_gan_lord_gods:
            position_mapping.append('头')
        if idx_name in [item[2] for item in self.lord_gods.nian_zhi_lord_gods]:
            position_mapping.append('脖子')
        if idx_name == self.lord_gods.yue_gan_lord_gods:
            position_mapping.append('胸')
        if idx_name in [item[2] for item in self.lord_gods.yue_zhi_lord_gods]:
            position_mapping.append('腹部')
        if idx_name == self.lord_gods.ri_gan_lord_gods:
            position_mapping.append('小腹')
        if idx_name in [item[2] for item in self.lord_gods.ri_zhi_lord_gods]:
            position_mapping.append('屁股')
        if idx_name == self.lord_gods.shi_gan_lord_gods:
            position_mapping.append('大腿')
        if idx_name in [item[2] for item in self.lord_gods.shi_zhi_lord_gods]:
            position_mapping.append('小腿/脚部')
        return position_mapping

    def lord_god_exist_position_for_relationships(self, idx_name):
        position_mapping = []
        if idx_name == self.lord_gods.nian_gan_lord_gods:
            position_mapping.append('父亲')
        if idx_name in [item[2] for item in self.lord_gods.nian_zhi_lord_gods]:
            position_mapping.append('母亲')
        if idx_name == self.lord_gods.yue_gan_lord_gods:
            position_mapping.append('哥哥/姐姐')
        if idx_name in [item[2] for item in self.lord_gods.yue_zhi_lord_gods]:
            position_mapping.append('弟弟/妹妹')
        if idx_name in [item[2] for item in self.lord_gods.ri_zhi_lord_gods]:
            position_mapping.append('对象')
        if idx_name == self.lord_gods.shi_gan_lord_gods:
            position_mapping.append('长子')
        if idx_name in [item[2] for item in self.lord_gods.shi_zhi_lord_gods]:
            position_mapping.append('次子')
        return position_mapping


class ZhengYin(LordGodExplain):
    def __init__(self, lord_gods):
        super().__init__(lord_gods)
        self.name = "正印"
        self.short_name = "印"
        self.type = "吉神（天使）"
        self.character = "聪明智慧，记性好，喜欢学习，心地善良，责任心强，少病少灾"
        self.imagery = "房子，文书，教育，口碑，权利，超我，完美的道德标准"
        self.career = "教师，艺术家，出版商，秘书，护士，宗教家，星象家，棋手"
        self.representatives = "长辈，贵人，师长"
        self.representatives_for_male = "自己的母亲"
        self.representatives_for_female = "自己的祖父或女婿"
        super().__post_construction__()

    def explain(self):
        result = super().explain()

        result += """
        正印是完美的道德标准，是一种超我，是一种权利，是一种责任心。
        """

        position_explain, supporting_list, opposing_list = self.calc_position_explain()
        if position_explain:
            result += f"""
        {position_explain}
            """

        house_explain = self.calc_house_explain()
        if house_explain:
            result += f"""
        {house_explain}
            """

        not_exists_explain = self.calc_not_exists_explain()
        if not_exists_explain:
            result += f"""
        {not_exists_explain}
            """

        return result

    def calc_position_explain(self):
        position_explain = []
        supporting_list = []
        opposing_list = []
        if self.name == self.lord_gods.nian_gan_lord_gods:
            position_explain.append("父亲家族比较注重知识文化。\n受祖母、双亲宠爱、呵护（尤其是母亲）。\n双亲及长辈个性温和，富有人情味。\n幼时家境大多较好。")
            tmp_s, tmp_o = self.append_opinion(self.lord_gods.nian_gan_element, '年干')
            supporting_list.extend(tmp_s)
            opposing_list.extend(tmp_o)

        nian_zhi_lord_gods = [item[2] for item in self.lord_gods.nian_zhi_lord_gods]
        if self.name in nian_zhi_lord_gods:
            position_explain.append("母亲家族比较注重知识文化。\n兄弟姐妹样貌都长得不错，理智，口才好，写作能力亦佳。\n记忆力好。")
            tmp_s, tmp_o = self.append_opinion(self.lord_gods.nian_zhi_element, '年支')
            supporting_list.extend(tmp_s)
            opposing_list.extend(tmp_o)

        if self.name == self.lord_gods.yue_gan_lord_gods:
            position_explain.append("初入社会时就通过文笔获得好名声。\n受母亲的教养比父亲多。\n聪明、慈悲、性好胜、博学、容易成名。\n儿女孝顺，尤其是次子、次女、四子、四女；儿女善变、乏耐性、但不失稳重。")
            tmp_s, tmp_o = self.append_opinion(self.lord_gods.yue_gan_element, '月干')
            supporting_list.extend(tmp_s)
            opposing_list.extend(tmp_o)

        yue_zhi_lord_gods = [item[2] for item in self.lord_gods.yue_zhi_lord_gods]
        if self.name in yue_zhi_lord_gods:
            position_explain.append("有一定积累之后通过文笔获得好名声。\n同时，月令能量比较强大，代表命主比较顾家，但是有的时候有点懒，佛系拖延症。\n大都是智慧型人物。\n因为容易受父母宠溺而养成耽于安乐、华而不实、依赖心重的个性。\n富有人情味、爱面子、喜欢人家恭维，有优越感，守旧，用钱保守。\n男性多不是长子，女性多是长女（代行母职）")
            tmp_s, tmp_o = self.append_opinion(self.lord_gods.yue_zhi_element, '月支')
            supporting_list.extend(tmp_s)
            opposing_list.extend(tmp_o)

        ri_zhi_lord_gods = [item[2] for item in self.lord_gods.ri_zhi_lord_gods]
        if self.name in ri_zhi_lord_gods:
            tmp = "对象家族有掌权之人，"
            if self.lord_gods.self_strong:
                tmp += "而且能帮助到自己的事业。"
            else:
                tmp += "但是对象跟自己关系不好。"

            if self.lord_gods.is_male:
                tmp += "\n男命正印在日支，比较喜欢年纪比较大的异性，御姐。\n"

            tmp += "配偶贤良有助力，以日主弱者尤佳（甲子、乙亥、戊午、己巳日）。\n配偶气质高雅。\n容易逃避现实问题。\n有谦让的君子风度。"

            tmp_s, tmp_o = self.append_opinion(self.lord_gods.ri_zhi_element, '日支')
            supporting_list.extend(tmp_s)
            opposing_list.extend(tmp_o)
            position_explain.append(tmp)

        if self.name == self.lord_gods.shi_gan_lord_gods:
            position_explain.append("儿女聪明孝顺，晚年享受盛誉，衣食无忧。\n职业居处常变动。")

        shi_zhi_lord_gods = [item[2] for item in self.lord_gods.shi_zhi_lord_gods]
        if self.name in shi_zhi_lord_gods:
            position_explain.append("巧于谋事，食禄丰厚。\n一生与名声、荣誉结缘。\n掌大权、任要职，是受重视的人物；生月支是正官者，晚年尊荣。\n性生活比较呆板清淡。")

        return "\n".join(position_explain), supporting_list, opposing_list

    def append_opinion(self, element, position) -> (list, list):
        if element in self.lord_gods.supporting_elements_sequence:
            return [position], []
        elif element in self.lord_gods.opposing_elements_sequence:
            return [], [position]
        else:
            return [], []


    def calc_house_explain(self):
        house_explain = ""
        if self.lord_gods.self_strong:
            return house_explain

        house_explain_items = []
        if self.name == self.lord_gods.nian_gan_lord_gods:
            house_explain_items.append("父亲家族会帮忙买房子")

        nian_zhi_lord_gods = [item[2] for item in self.lord_gods.nian_zhi_lord_gods]
        if self.name in nian_zhi_lord_gods:
            tmp = "母亲家族会帮忙"
            if nian_zhi_lord_gods.index(self.name) == 0:
                tmp += "买房子"
            else:
                tmp += "出首付"
            house_explain_items.append(tmp)

        if self.name == self.lord_gods.yue_gan_lord_gods:
            house_explain_items.append("哥哥姐姐会帮忙买房子")

        yue_zhi_lord_gods = [item[2] for item in self.lord_gods.yue_zhi_lord_gods]
        if self.name in yue_zhi_lord_gods:
            tmp = "弟弟妹妹会帮忙"
            if yue_zhi_lord_gods.index(self.name) == 0:
                tmp += "买房子"
            else:
                tmp += "出首付"
            house_explain_items.append(tmp)

        ri_zhi_lord_gods = [item[2] for item in self.lord_gods.ri_zhi_lord_gods]
        if self.name in ri_zhi_lord_gods:
            tmp = "对象会帮忙"
            if ri_zhi_lord_gods.index(self.name) == 0:
                tmp += "买房子"
            else:
                tmp += "凑首付"
            house_explain_items.append(tmp)

        shi_lord_gods = [self.lord_gods.shi_zhi_lord_gods] + [item[2] for item in self.lord_gods.shi_zhi_lord_gods]
        if self.name in shi_lord_gods:
            house_explain_items.append("晚辈会帮忙买房子")

        return "\n".join(house_explain_items)

    def calc_not_exists_explain(self):
        return "命中没有正印的人，不爱学习、没有责任心、记性不好、学非所用，与母亲缘分浅，经常生病\n" if self.lord_gods_count == 0 else ""


class ShiShen(LordGodExplain):
    def __init__(self, lord_gods):
        super().__init__(lord_gods)
        self.name = "食神"
        self.short_name = "食"
        self.type = "福神"
        self.character = "口才好，喜欢玩，好歌舞酒色，吃货，多福多寿，心宽体胖，为人宽宏大量，对艺术天赋异禀"
        self.imagery = "胖、大、有福气、衣食无忧"
        self.career = "演绎、娱乐、美术、美容、服装设计、餐饮酒店"
        self.representatives = "晚辈、下属"
        self.representatives_for_male = "孙子"
        self.representatives_for_female = "女儿"
        super().__post_construction__()

    def explain(self):
        result = super().explain()

        result += """
        食神的主要作用是生财，吃喝玩乐还能赚钱。但是食神不宜过多，会身体肥胖，贪图享乐，好逸恶劳，不务正业，不知节俭。
        """

        self_strong_explain = self.calc_self_strong_explain()
        if self_strong_explain:
            result += f"""
        {self_strong_explain}
            """

        position_explain = self.calc_position_explain()
        if position_explain:
            result += f"""
        {position_explain}
            """

        not_exists_explain = self.calc_not_exists_explain()
        if not_exists_explain:
            result += f"""
        {not_exists_explain}
            """

        return result

    def calc_self_strong_explain(self):
        if self.lord_gods.self_strong:
            return "自身日主比较强，食神为喜用，泄化日主，食神一切好的一面就来了\n"
        else:
            return "自身日主比较弱，食神为忌凶，代表自己腹有诗书但是没有伯乐，易郁郁寡欢怀才不遇，自己的思想与世俗格格不入\n"

    def calc_position_explain(self):
        position_explain = []

        nian_lord_gods = [self.lord_gods.nian_gan_lord_gods] + [item[2] for item in self.lord_gods.nian_zhi_lord_gods]
        if self.name in nian_lord_gods:
            position_explain.append("食神在年柱，代表从小家庭殷实，衣食无忧。")

        yue_lord_gods = [self.lord_gods.yue_gan_lord_gods] + [item[2] for item in self.lord_gods.yue_zhi_lord_gods]
        if self.name in yue_lord_gods:
            position_explain.append("食神在月柱，代表青年时期可以发财。")

        ri_lord_gods = [item[2] for item in self.lord_gods.ri_zhi_lord_gods]
        if self.name in ri_lord_gods:
            position_explain.append("食神在日柱，代表中年时期可以发财。")

        shi_lord_gods = [self.lord_gods.shi_gan_lord_gods] + [item[2] for item in self.lord_gods.shi_zhi_lord_gods]
        if self.name in shi_lord_gods:
            position_explain.append("食神在时柱，代表晚年生活无忧，同时子孙也可以发财。同时，时柱为子女宫，食神旺容易生儿子。")
            if not self.lord_gods.is_male and self.name in self.lord_gods.shi_gan_lord_gods:
                position_explain.append("女命食神在时干，可能会梨型身材，好生养。")

        return "\n".join(position_explain)

    def calc_not_exists_explain(self):
        return "命中没有食神的人，不会玩，口才不好，不善言辞\n" if self.lord_gods_count == 0 else ""


class ZhengGuan(LordGodExplain):
    def __init__(self, lord_gods):
        super().__init__(lord_gods)
        self.name = "正官"
        self.short_name = "官"
        self.type = "吉神（富神）"
        self.character = "守信用、正直、光明冷落、好面子，在乎名声地位、廉洁、公正、稳重"
        self.imagery = "大哥、领导、领袖、地位、受人敬仰"
        self.career = "政治、法律、侦探、法官、记者、公职"
        self.representatives = "领导、上司"
        self.representatives_for_male = "女儿"
        self.representatives_for_female = "老公"
        super().__post_construction__()

    def explain(self):
        result = super().explain()

        result += """
        自带正官的人容易当官。朋友也大多是正经人。不正派的人不去结交不去得罪，但也不得罪。朋友不多，很难有死党知己。
        正官太多容易死心眼、固执、强迫症。
        正官多的人一生追求名誉地位，什么都可以不要，就是要当领导
        """

        position_explain = self.calc_position_explain()
        if position_explain:
            result += f"""
        {position_explain}
            """

        if not self.lord_gods.is_male:
            female_explain = self.calc_female_explain()
            if female_explain:
                result += f"""
        {female_explain}
            """

        not_exists_explain = self.calc_not_exists_explain()
        if not_exists_explain:
            result += f"""
        {not_exists_explain}
            """

        return result

    def calc_position_explain(self):
        position_explain = []

        if self.name in [self.lord_gods.nian_gan_lord_gods] + [item[2] for item in self.lord_gods.nian_zhi_lord_gods]:
            position_explain.append("正官在年柱，小时候做过班干部。")

        if self.name in [self.lord_gods.yue_gan_lord_gods] + [item[2] for item in self.lord_gods.yue_zhi_lord_gods]:
            position_explain.append("正官在月柱，代表青年得志，年轻的时候就能带团队。")

        if self.name in [item[2] for item in self.lord_gods.ri_zhi_lord_gods]:
            position_explain.append("正官在日柱，代表有组织领导能力。")

        if self.name in [self.lord_gods.shi_gan_lord_gods] + [item[2] for item in self.lord_gods.shi_zhi_lord_gods]:
            position_explain.append("正官在时柱，代表晚年有权有势，子女光明正直。")
            if not self.lord_gods.is_male and self.name in [self.lord_gods.shi_gan_lord_gods]:
                position_explain.append("女命正官在时干，容易生男孩。")

        return "\n".join(position_explain)

    def calc_not_exists_explain(self):
        return "命中没有正官，代表对自己无法严格要求，不喜欢拘束，木无法律，我行我素很难做领导\n" if self.lord_gods_count == 0 else ""

    def calc_female_explain(self):
        female_explain = "正官对女性来说代表着老公，所以不宜过多。"
        if self.lord_gods_count == 0:
            female_explain += "命中没有正官的女性，容易晚婚甚至终身不嫁。"
        elif self.lord_gods_count == 1:
            female_explain += "命中有一个正官的女性最好命，会和老公琴瑟和鸣相伴一生。"
        elif self.lord_gods_count == 2:
            female_explain += "命中有两个正官的女性，会对老公不是很满意，会遇到令自己心动的男子。"
        else:
            female_explain += "命中多个正官的女性，一生中可能会经历多个先生。"

        return female_explain + "\n"


class ZhengCai(LordGodExplain):
    def __init__(self, lord_gods):
        super().__init__(lord_gods)
        self.name = "正财"
        self.short_name = "财"
        self.type = "吉神（天使）"
        self.character = "守本分，诚实可靠，脚踏实地，勤俭节约，重视家庭，诚信，爱妻子，值得信赖"
        self.imagery = "稳定收入，合法收入"
        self.career = "银行，财政，外交，中介，零售，杂货，百货，药商"
        self.representatives = "富翁，商人"
        self.representatives_for_male = "妻子"
        self.representatives_for_female = "父亲"
        super().__post_construction__()

    def explain(self):
        result = super().explain()

        result += """
        财喜藏不喜漏。天干之财为虚财，地支藏干里的财为真财
        """

        self_strong_explain = self.calc_self_strong_explain()
        if self_strong_explain:
            result += f"""
        {self_strong_explain}
            """

        if self.lord_gods.is_male:
            male_explain = self.calc_male_explain()
            if male_explain:
                result += f"""
        {male_explain}
            """

        position_explain = self.calc_position_explain()
        if position_explain:
            result += f"""
        {position_explain}
            """

        not_exists_explain = self.calc_not_exists_explain()
        if not_exists_explain:
            result += f"""
        {not_exists_explain}
            """

        return result

    def calc_position_explain(self):
        position_explain = []

        if self.name in [self.lord_gods.nian_gan_lord_gods] + [item[2] for item in self.lord_gods.nian_zhi_lord_gods]:
            position_explain.append("正财在年柱，工薪（有稳定收入）家庭，家庭条件还可以有房子住，但是和发财关系不大")

        if self.name in [self.lord_gods.yue_gan_lord_gods] + [item[2] for item in self.lord_gods.yue_zhi_lord_gods]:
            position_explain.append("正财在月柱，最完美，30岁以后有稳定收入才算是富命。")

        if self.name in [item[2] for item in self.lord_gods.ri_zhi_lord_gods]:
            position_explain.append("正财在日柱，代表夫妻恩爱。")

        shi_zhi_lord_gods = [item[2] for item in self.lord_gods.shi_zhi_lord_gods]
        shi_lord_gods = [self.lord_gods.shi_gan_lord_gods] + shi_zhi_lord_gods
        if self.name in shi_lord_gods:
            tmp = "正财在时柱，代表孩子发财，晚年有稳定收入。"
            if shi_lord_gods in shi_zhi_lord_gods:
                tmp += "在时支（55岁以后），代表晚年可能再婚。"
            position_explain.append(tmp)

        return "\n".join(position_explain)

    def calc_not_exists_explain(self):
        if self.lord_gods_count != 0:
            return ""
        result = "命中没有正财，一生财来财去一场空，烂桃花多。"
        if self.lord_gods.is_male:
            result += "男人与妻缘分薄，晚婚，夫妻感情不好。\n"
        else:
            result += "女人与父缘分薄，父亲不重视自己。父多早丧，或病残，父亲无能。\n"
        return result

    def calc_self_strong_explain(self):
        result = ""
        if not self.lord_gods.self_strong:
            result += "自身日主比较弱，正财为忌凶，代表自己不会理财，为人吝啬，不容易发财\n"
        return result

    def calc_male_explain(self):
        result = "正财是男人的妻子。"
        if self.lord_gods_count > 3:
            result += "男人正财多，多妻之像，或者不重视结发之妻。\n"
        return result


class QiSha(LordGodExplain):
    def __init__(self, lord_gods):
        super().__init__(lord_gods)
        self.name = "七杀"
        self.short_name = "杀"
        self.type = "凶神（病神）"
        self.character = "执行力强，有正义感，侠义精神，做事有魄力，勇于向困难挑战，勇于突破困境，坚强意志与干劲。同时也有可能霸道，急躁如火，脾气古怪，任性倔强，好胜好斗，报复心强，偏激叛逆，鲁莽冲动，听不进谏言，易树敌。"
        self.imagery = "小人，仇人，得病"
        self.career = "武职，如军警、法院等需要有杀气的行业，适合做二把手"
        self.representatives = "军人、警察、公检法单位"
        self.representatives_for_male = "儿子"
        self.representatives_for_female = "情人"
        super().__post_construction__()

    def explain(self):
        result = super().explain()

        result += """
        七杀为日元的天敌，四凶神中的索命鬼，因此八字首先看七杀。安顿了七杀方可论富贵，否则有命无命都两说。
        不过聪明不过伤官，伶俐不过七杀，七杀多的人，聪明伶俐。
        """

        if not self.lord_gods.is_male:
            female_explain = self.calc_female_explain()
            if female_explain:
                result += f"""
        {female_explain}
            """

        self_strong_explain = self.calc_self_strong_explain()
        if self_strong_explain:
            result += f"""
        {self_strong_explain}
            """

        position_explain = self.calc_position_explain()
        if position_explain:
            result += f"""
        {position_explain}
            """

        position_explain_extra = self.calc_position_explain_extra()
        if position_explain_extra:
            result += f"""
        {position_explain_extra}
            """

        not_exists_explain = self.calc_not_exists_explain()
        if not_exists_explain:
            result += f"""
        {not_exists_explain}
            """

        return result

    def calc_position_explain(self):
        """
        五行身体部位
        甲肝乙胆丙小肠，丁心戊胃己脾乡
        庚金大肠辛金肺，壬是膀胱癸肾藏

        宫位与身体部位
        |年|月|日|时|
        |:-|:-|:-|:-|
        |年干|月干|日元|时干|
        |头|胸|小腹|大腿|
        |年支|月令|日支|时支|
        |脖子|腹部|屁股|小腿/脚部|
        :return:
        """
        position_explain = "七杀在哪个五行、位置，代表哪里的器官容易生病"

        position = super().lord_god_exist_position_for_body_parts(self.name)
        gan_position = []
        zhi_position = []
        if self.name == self.lord_gods.nian_gan_lord_gods:
            gan_position.append("头")

        if self.name in [item[2] for item in self.lord_gods.nian_zhi_lord_gods]:
            zhi_position.append("脖子")

        if self.name == self.lord_gods.yue_gan_lord_gods:
            gan_position.append("胸")

        if self.name in [item[2] for item in self.lord_gods.yue_zhi_lord_gods]:
            zhi_position.append("腹部")

        if self.name == self.lord_gods.ri_gan_lord_gods:
            gan_position.append("小腹")

        if self.name in [item[2] for item in self.lord_gods.ri_zhi_lord_gods]:
            zhi_position.append("屁股")

        if self.name == self.lord_gods.shi_gan_lord_gods:
            gan_position.append("大腿")

        if self.name in [item[2] for item in self.lord_gods.shi_zhi_lord_gods]:
            zhi_position.append("小腿/脚部")

        if not position:
            return ""

        position_explain += f"，所以命主的 {position} 需要当心。\n"

        all_lord_gods = self.lord_gods.all_lord_gods
        if (
                ('正印' not in all_lord_gods)
                and
                ('食神' in all_lord_gods and '偏印' not in all_lord_gods)
        ):
            position_explain += f"此人七杀没被化解，所以"
            position_explain += f"{gan_position}容易出急症，" if gan_position else ""
            position_explain += f"{zhi_position}容易出慢性病。" if zhi_position else ""
            position_explain += "\n"

        if self.name in [self.lord_gods.nian_gan_lord_gods] + [item[2] for item in self.lord_gods.nian_zhi_lord_gods]:
            position_explain += "七杀在年柱，小时候家里管的比较严，可能过于严格棍棒教育\n"
        return position_explain

    def calc_position_explain_extra(self):
        pass

    def calc_self_strong_explain(self):
        result = "七杀如果有东西克制可能会变好，但是如果没有克制，在天干容易突发灾祸致残致死，在地支为慢性恶疾。\n"
        if self.lord_gods.self_strong:
            result += "此人属于身强命，身强不怕七杀，七杀来克反而好，叫身杀两停。\n"
        else:
            result += "身弱的人，七杀多，容易出意外，容易生病。\n"
            if '正印' in self.lord_gods.all_lord_gods:
                result += "有正印化解七杀。七杀生正印，正印生日元。七杀反为我用，叫杀印相生。\n"

            if '食神' in self.lord_gods.all_lord_gods and not '偏印' in self.lord_gods.all_lord_gods:
                result += "有食神制杀，没有偏印损害食神，叫食神制杀。\n"

        return result

    def calc_not_exists_explain(self):
        result = ""
        if self.lord_gods_count != 0:
            return result
        result += "命里没有七杀，代表心不会太狠，不会报复别人容易被欺负。"
        if self.lord_gods.is_male:
            result += "男人没有七杀，不易生儿子。\n"
        else:
            result += "女人没有七杀，不会有情人。\n"

        return result

    def calc_female_explain(self):
        result = "七杀旺的女人比较瘦，筷子腿。"
        result += "同时七杀对女人来说是其他人的老公。"
        if self.lord_gods_count > 3:
            result += "女人七杀多，多夫之像，遇到心动的男人的可能性比较大。\n"
        return result


class PianYin(LordGodExplain):
    def __init__(self, lord_gods):
        super().__init__(lord_gods)
        self.name = "偏印"
        self.short_name = "枭"
        self.type = "郁神（枭印）"
        self.character = "观察敏锐，分析力、感受力、理解力强，即使是困难的东西能很快学会，多才多艺，心思细腻，但是也会过于敏感，内心孤独，时常情绪低落，优柔寡断，犹豫不决，不善与人交往，宁可独处也不去人多的地方。"
        self.imagery = "学习玄学有特殊天赋，经常会情绪低落"
        self.career = "研究，民意代表，发明，设计，创造，科技，武术，演绎行销，直销，广告，模特，艳星等特殊行业"
        self.representatives = "军师，参谋"
        self.representatives_for_male = "祖父"
        self.representatives_for_female = "母亲"
        super().__post_construction__()

    def explain(self):
        result = super().explain()

        position_explain = self.calc_position_explain()
        if position_explain:
            result += f"""
        {position_explain}
            """

        not_exists_explain = self.calc_not_exists_explain()
        if not_exists_explain:
            result += f"""
        {not_exists_explain}
            """

        return result

    def calc_not_exists_explain(self):
        return "命局没有偏印，做事不注重细节，没法感知别人内心的感受。" if self.lord_gods_count == 0 else ""

    def calc_position_explain(self):

        position_explain = []
        if self.name == self.lord_gods.nian_gan_lord_gods:
            position_explain.append("双亲是有理想有能力的人，由于忙碌冷落了你。\n与出生地无缘，会抛弃祖产在他乡创立家业。\n如果年支又是偏印，长亲不利，祖上寒微。")

        nian_zhi_lord_gods = [item[2] for item in self.lord_gods.nian_zhi_lord_gods]
        if self.name in nian_zhi_lord_gods:
            position_explain.append("兄弟姐妹不喜欢受束缚，善辩，不喜欢吐露心事，容易与亲族疏远，被认为是“怪人”。\n与出生地缘分薄，大多在他乡打拼。")

        if self.name == self.lord_gods.yue_gan_lord_gods:
            position_explain.append("生活方式异于常人，常被认为是“怪人”。\n头脑灵活第六感强，求知欲强，不喜陈旧很创新。\n宜当医生、艺术家。")

        yue_zhi_lord_gods = [item[2] for item in self.lord_gods.yue_zhi_lord_gods]
        if self.name in yue_zhi_lord_gods:
            result = "偏印在月令代表必有一技之长"
            if len(self.lord_gods.all_lord_gods) - 1 > 0:
                result += "，在其他干支代表命主会主动学习技术技能。"
            position_explain.append(result)
            position_explain.append("性情，爱之欲其生，恨之欲其死。\n孤独，不喜欢袒露心声，遇事常以消极的态度抵制。\n与打针、吃药结了不了之缘（肠胃病居多）。有的人久病成医，与宗教也很有缘，常吃斋或清修。\n以五术为业，若临衰病死绝之位，其貌不扬，人气不好。")

        ri_zhi_lord_gods = [item[2] for item in self.lord_gods.ri_zhi_lord_gods]
        if self.name in ri_zhi_lord_gods:
            position_explain.append("看日元当令与否：日强者，配偶贤良，日弱者，配偶带给你烦恼。\n丙寅、壬申日的女性，幸福、得优秀的子女；男性妻子娴淑。\n丁卯、癸酉日生人，幼年时代易患大病，早离双亲，婚姻不美满。\n癸酉日生的女性，夫缘尤劣。\n庚辰、辛丑日生者，与父母缘薄；男性，妻缘不好，女性，可得贤良子女，一生幸福，但庚辰日生者，夫缘不佳。\n辛未、庚戌日生人，双亲缘薄，婚姻不美满；女性，表面柔顺内心冷酷，克翁姑。\n幼年时容易生病，而且都属于严重危险的急症。\n能以发明、创作成功。")

        if self.name in self.lord_gods.shi_gan_lord_gods:
            position_explain.append("枭印在时干，子女不旺，不容易有子嗣。\n兼职多，晚年亦不得清闲。\n子女性情不良（特异的特质），若为喜用神，子女酉特殊成就、孝顺；若为忌神，子女夭折，甚者绝嗣。")

        shi_zhi_lord_gods = [item[2] for item in self.lord_gods.shi_zhi_lord_gods]
        if self.name in shi_zhi_lord_gods:
            position_explain.append("不喜欢热闹、喧哗，喜欢独自研究学术、技艺，铁I人。\n对医药、占卜、风水、宗教等有深入的研究或特殊的成就。\n时干正印则代表同时拥有两种以上的工作。")

        return "\n".join(position_explain) if position_explain else ""


class ShangGuan(LordGodExplain):
    def __init__(self, lord_gods):
        super().__init__(lord_gods)
        self.name = "伤官"
        self.short_name = "伤"
        self.type = "狂神"
        self.character = "聪明灵巧，个性突出，容易抢风头，能言善辩，不服输，胆大有魄力，有才华，很有自信，但是也可能自负，语言尖锐刻薄，狂傲不羁，度量狭小，记仇，得理不饶人，任性蛮横，逞强好胜，一身傲骨，鄙视他人，死不认错。"
        self.imagery = "口舌，官司，纷争（男）" if self.lord_gods.is_male else "克夫（女）"
        self.career = "文学，书画，艺术，如文学家，影星，歌星，舞蹈家，音乐家，画家"
        self.representatives = "晚辈，学生，下属"
        self.representatives_for_male = "祖母，孙女"
        self.representatives_for_female = "儿子"
        super().__post_construction__()

    def explain(self):
        result = super().explain()

        result += """
        伤官可以旺财，因为伤官上进心强。
        本命有伤官，大运流年遇到伤官，会有官司口舌纷争。
        """

        self_strong_explain = self.calc_self_strong_explain()
        if self_strong_explain:
            result += f"""
        {self_strong_explain}
            """

        position_explain = self.calc_position_explain()
        if position_explain:
            result += f"""
        {position_explain}
            """

        if not self.lord_gods.is_male:
            female_explain = self.calc_female_explain()
            if female_explain:
                result += f"""
        {female_explain}
            """

        return result

    def calc_position_explain(self):

        position_explain = []
        nian_zhi_lord_gods = [item[2] for item in self.lord_gods.nian_zhi_lord_gods]
        if self.name in [self.lord_gods.nian_gan_lord_gods] + nian_zhi_lord_gods:
            position_explain.append("年柱伤官代表出身贫寒家庭，小时候经常跟人起冲突，跟父母吵架。")

        yue_zhi_lord_gods = [item[2] for item in self.lord_gods.yue_zhi_lord_gods]
        if self.name in [self.lord_gods.yue_gan_lord_gods] + yue_zhi_lord_gods:
            position_explain.append("月柱伤官代表青年时期经常跟人起冲突，可能染上官司。不适合从事平凡工作，点子多，才华横溢，头脑灵活，感受性强，爱好艺术，生活方式异于凡人，不容易被人了解。兄弟姐妹不全，大多不是头胎（数量少、流产、夭折）。")
            if self.name in yue_zhi_lord_gods:
                position_explain.append("伤官在月令，鬼头鬼脑，聪明绝顶，原创力、叛逆性强，不太服从管教，宜从事艺术、科技类的工作。特别严重的可能法律意识淡薄。")
        # 伤官食神是财禄，生财的，财路广
        ri_zhi_lord_gods = [item[2] for item in self.lord_gods.ri_zhi_lord_gods]
        if self.name in ri_zhi_lord_gods:
            position_explain.append("日柱伤官代表夫妻吵架和官司。")

        shi_zhi_lord_gods = [item[2] for item in self.lord_gods.shi_zhi_lord_gods]
        if self.name in [self.lord_gods.shi_gan_lord_gods] + shi_zhi_lord_gods:
            position_explain.append("时柱伤官代表晚年经常跟人起冲突，可能染上官司。")

        if not self.lord_gods.is_male and self.name in yue_zhi_lord_gods and self.name in ri_zhi_lord_gods:
            position_explain.append("女性伤官在月令（能量强）和日支（夫妻宫）大概率离婚。")
            if self.name in nian_zhi_lord_gods + yue_zhi_lord_gods + ri_zhi_lord_gods + shi_zhi_lord_gods:
                position_explain.append("女性伤官四柱都有为，可能会有婚外情。")

        return "\n".join(position_explain)

    def calc_not_exists_explain(self):
        return "命局没有偏印，做事不注重细节，没法感知别人内心的感受。" if self.lord_gods_count == 0 else ""

    def calc_female_explain(self):
        female_explain = "女带伤官必骂夫，夫妻经常吵吵闹闹。"
        if self.name in [item[2] for item in self.lord_gods.ri_zhi_lord_gods]:
            female_explain += "女坐伤官必克夫。这等女性，若非为人多才艺，就是长相清逸秀丽，或二者兼而有之。多半属于女强人型，很有气质、才华洋溢，成就往往超越男性，因此伤官旺的女性具有开拓性，宜于从事事业，而不宜于做家庭主妇。"

        return female_explain

    def calc_self_strong_explain(self):
        result = ""
        if self.lord_gods.self_strong:
            result += "身强又逢伤官，无论男女都长相清秀，受人喜欢。\n"
        return result


class JieCai(LordGodExplain):
    def __init__(self, lord_gods):
        super().__init__(lord_gods)
        self.name = "劫财"
        self.short_name = "劫"
        self.type = "骗神（地支里也叫羊刃）"
        self.character = "性格开朗，心思敏捷，个性明显，自尊心强，口才好，善于活跃气氛，鬼点子多，初次交往中能得到别人好感，但是也可能固执己见，自我矛盾，好酒好赌，贪小便宜，好吹牛抬杠，不讲信用，借钱不还，不诚实，满嘴瞎话。"
        self.imagery = "赌博、破财、克夫、克妻、滑头、骗子"
        self.career = "自由职业，服务，直销，投资，贸易，流动行业"
        self.representatives = "异性朋友，同辈，同姓族人"
        self.representatives_for_male = "姐妹"
        self.representatives_for_female = "兄弟"
        super().__post_construction__()

    def explain(self):
        result = super().explain()

        result += """
        劫财之人见面熟，交际手腕高，见人说人话，见鬼说鬼话。
        """

        result += """
        认识你以后就开始借钱，还不还钱要看其他十神的组合。借了一圈朋友的钱以后，开始进去新的朋友圈，混熟以后再借钱。喜欢做传销的项目，因为朋友多，骗完一圈，再换圈子骗。
        劫财之人为了达到个人的目的，下跪发毒誓，甜言蜜语，会利用一切可以打动别人的东西去打动别人。你可要防备了，他对你是有目的和歹心的，利用完你就会一脚蹬开。你可要防备了，他对你是有目的和歹心的，利用完你就会一脚蹬开。
        选择合伙人时，命里劫财过多的人赚不择手段，坑紧拐骗。你一定会吃亏。
        所以劫财过多，很难发财。
        特别是女生选男朋友的时候要注意，劫财多会用卑鄙霸道手段讲女方骗上床，然后开始借钱，最后骗财骗色。
        """ if self.lord_gods_count > 3 else ""

        position_explain = self.calc_position_explain()
        if position_explain:
            result += f"""
        {position_explain}
            """

        gander_explain = self.calc_gander_explain()
        if gander_explain:
            result += f"""
        {gander_explain}
            """

        return result

    def calc_position_explain(self):
        position_explain = []

        if self.name in [self.lord_gods.nian_gan_lord_gods] + [item[2] for item in self.lord_gods.nian_zhi_lord_gods]:
            position_explain.append("年柱劫财，祖业耗散，无财产留给后人，家庭不好，早年贫困。")

        if self.name in [self.lord_gods.yue_gan_lord_gods] + [item[2] for item in self.lord_gods.yue_zhi_lord_gods]:
            position_explain.append("月柱劫财为自己破财，还代表社会上的朋友借你的钱不还或者给你带来财帛损失。")

        if self.name in [item[2] for item in self.lord_gods.ri_zhi_lord_gods]:
            position_explain.append("日柱劫财代表分居或者离婚的几率很大。")

        if self.name in [self.lord_gods.shi_gan_lord_gods] + [item[2] for item in self.lord_gods.shi_zhi_lord_gods]:
            position_explain.append("时柱劫财代表晚年孤苦没有收入。")

        return "\n".join(position_explain)

    def calc_gander_explain(self):
        result = ""
        if self.lord_gods_count == 0:
            return result

        if self.lord_gods.is_male:
            result += "男命劫财旺，有姐妹的概率比较高。"
        else:
            result += "女命劫财旺，有兄弟的概率比较高。"

        result += "但是有计划生育了，所以这个不一定准确。"

        if self.lord_gods_count > 3:
            result += "劫财多的人，异性缘分多，但是不会长久。"

        return result


class BiJian(LordGodExplain):
    def __init__(self, lord_gods):
        super().__init__(lord_gods)
        self.name = "比肩"
        self.short_name = "比"
        self.type = "友神"
        self.character = "意志坚强，重情重义，独立自主，不轻易变动，敦厚老实，做事有耐心，力争上游，但也可能固执己见，独断专行，自我中心，朋友多，知己不多，严厉刻薄，不通人情，自我封闭，闭门造车，刚愎自用。"
        self.imagery = "忌凶克财，喜用合作得财，人缘好"
        self.career = "直销，开矿，运动员，流动行业，机械运动，中介，健身行业"
        self.representatives = "同性朋友，同辈，同学，合伙人，股东"
        self.representatives_for_male = "兄弟"
        self.representatives_for_female = "姐妹"
        super().__post_construction__()

    def explain(self):
        result = super().explain()

        result += """
        比肩人内心的想法是一生平安。
        """
        result += """
        比肩多的人特别关心宠爱部下和朋友，但是和领导不会打交道。
        """ if self.lord_gods_count > 2 else ""

        self_strong_explain = self.calc_self_strong_explain()
        if self_strong_explain:
            result += f"""
        {self_strong_explain}
            """

        position_explain = self.calc_position_explain()
        if position_explain:
            result += f"""
        {position_explain}
            """

        return result

    def calc_self_strong_explain(self):
        result = ""
        if self.lord_gods.self_strong:
            result += "身旺不喜比肩帮，运走比肩反遭殃。比肩为忌神，得不到朋友或兄弟的帮助，反而被争夺财物。"
        else:
            result += "身弱逢比运最通，合作营谋处处丰。比肩为用神，多得朋友或兄弟帮助。"
        result += "\n"
        return result

    def calc_position_explain(self):
        position_explain = []

        if self.name in [self.lord_gods.nian_gan_lord_gods] + [item[2] for item in self.lord_gods.nian_zhi_lord_gods]:
            position_explain.append(f"比肩在年柱，少年时期{'被同辈、同学坑' if self.lord_gods.self_strong else '多得同辈照顾'}")

        if self.name in [self.lord_gods.yue_gan_lord_gods] + [item[2] for item in self.lord_gods.yue_zhi_lord_gods]:
            position_explain.append(f"比肩在月柱，青年时期{'被同辈、朋友坑，有财务冲突' if self.lord_gods.self_strong else '有同事、朋友照应'}。")
        #自我观念强，不愿受限制，是难以驾驭的人。
        if self.name in [item[2] for item in self.lord_gods.ri_zhi_lord_gods]:
            position_explain.append(f"比肩在日柱，壮年时期{'与合伙人多有龃龉' if self.lord_gods.self_strong else '有伙伴合作愉快'}")

        if self.name in [self.lord_gods.shi_gan_lord_gods] + [item[2] for item in self.lord_gods.shi_zhi_lord_gods]:
            position_explain.append(f"比肩在时柱，晚年{'和朋友、兄弟有矛盾' if self.lord_gods.self_strong else '有朋友、兄弟照应'}")

        return "\n".join(position_explain)


class PianCai(LordGodExplain):
    def __init__(self, lord_gods):
        super().__init__(lord_gods)
        self.name = "偏财"
        self.short_name = "才"
        self.type = "侠神"
        self.character = "慷慨大方，重义轻财，聪明机巧，开朗乐观，乐善好施，人脉广阔，风流多情，豪爽出手大方，易得女人幻想。不过也可能不重视金钱，不善理财，一心多用，轻浮放荡，嗜酒好色，赌性大。"
        self.imagery = "侠客，做生意，意外之财"
        self.career = "商业，企业，投资和投机，金融，信息咨询"
        self.representatives = "富翁，商人"
        self.representatives_for_male = "父亲和情人"
        self.representatives_for_female = "婆婆"
        super().__post_construction__()

    def explain(self):
        result = super().explain()

        result += """
        偏财比正财会赚钱，正财多为工作收入，偏财是敏锐的商业眼光做生意得来的。
        但是它不好的一点就是时有时无，来的时候金山银海，但是会很长时间不来钱。
        偏财喜欢交朋友，三教九流都有，所以有广大的人脉关系，能得到相当多的情报资讯。
        偏财为人大方慷慨，会去帮助朋友，所以对方愿意提供消息，让自己获得回报。
        偏财爱往外面跑，到处结交朋友，与他人谈天说地，交际应酬特别多，加上出手大方，会愿意去分享，因此人缘特别好。对于陌生的人士，很快便可以熟识，并且能打成一片，建立友谊。
        """

        if self.lord_gods.is_male:
            male_explain = self.calc_male_explain()
            if male_explain:
                result += f"""
        {male_explain}
            """

        self_strong_explain = self.calc_self_strong_explain()
        if self_strong_explain:
            result += f"""
        {self_strong_explain}
            """

        position_explain = self.calc_position_explain()
        if position_explain:
            result += f"""
        {position_explain}
            """

        return result

    def calc_self_strong_explain(self):
        result = ""
        if not self.lord_gods.self_strong:
            result += "日元身弱偏财为忌神，总想着不劳而获，但是偏财不是经常有，就会贪图享受、懒惰\n"
        return result

    def calc_position_explain(self):
        position_explain = []

        if self.name in [self.lord_gods.nian_gan_lord_gods] + [item[2] for item in self.lord_gods.nian_zhi_lord_gods]:
            position_explain.append("偏财在年柱，代表发财必须离开家乡发展。")

        if self.name in [self.lord_gods.yue_gan_lord_gods]:
            position_explain.append("偏财在月干最好，代表父亲优秀能干，对自己的帮助大。")

        if self.name in [item[2] for item in self.lord_gods.yue_zhi_lord_gods]:
            position_explain.append("偏财在月支，代表自己能存下巨额的财富。")

        if self.name in [item[2] for item in self.lord_gods.ri_zhi_lord_gods]:
            position_explain.append("偏财在日支，代表配偶会给自己带来财富，同时代表感情方面会有烂桃花。")
            if self.lord_gods.is_male:
                position_explain.append("男命偏财在日支（夫妻宫），可能心有二意，脚踩两条船，有贼心没贼胆的喜欢搞暧昧，有贼心有贼胆的可能回去嫖娼。")

        if self.name in [self.lord_gods.shi_gan_lord_gods] + [item[2] for item in self.lord_gods.shi_zhi_lord_gods]:
            position_explain.append("偏财在时柱，代表晚年会比较有钱，子女的条件也会不错。")

        return "\n".join(position_explain)

    def calc_male_explain(self):
        result = "偏财是男人的小妾"
        if self.lord_gods_count > 3:
            result += "，所以偏财多的男人有外遇的可能性比较大。"
        return result
