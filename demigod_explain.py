from constants import *


class DemigodExplain:
    def __init__(self, demigods, lord_gods):
        self.demigods = demigods
        self.lord_gods = lord_gods
        self.name = ""
        self.type = ""
        self.explanation = ""

    def explain(self):
        result = f'''
        {self.name}
        '''

        if self.type:
            result += f'''
        {self.type}
            '''

        result += f'''
        {self.explanation}
        '''

        return result

    def calc_all_demigod_explain(self, demigods, lord_gods):
        self.demigod_explain_mapping = {
            '天德贵人': TianDeGuiRen(demigods, lord_gods),
            '月德贵人': YueDeGuiRen(demigods, lord_gods),
            '天乙贵人': TianYiGuiRen(demigods, lord_gods),
            '文昌贵人': WenChangGuiRen(demigods, lord_gods),
            '德秀贵人': DeXiuGuiRen(demigods, lord_gods),
            '驿马': YiMa(demigods, lord_gods),
            '太极贵人': TaiJiGuiRen(demigods, lord_gods),
            '华盖': HuaGai(demigods, lord_gods),
            '咸池（桃花）': TaoHua(demigods, lord_gods),
            '劫煞': JieSha(demigods, lord_gods),
            '灾煞': ZaiSha(demigods, lord_gods),
            '血刃': XueRen(demigods, lord_gods),
            '福星': FuXing(demigods, lord_gods),
            '天德合': TianDeHe(demigods, lord_gods),
            '国印贵人': GuoYin(demigods, lord_gods),
            '天赦贵': TianSheGui(demigods, lord_gods),
            '将星': JiangXing(demigods, lord_gods),
            '金匮': JinKui(demigods, lord_gods),
            '羊刃': YangRen(demigods, lord_gods),
            '红艳': HongYan(demigods, lord_gods),
            '学士': XueShi(demigods, lord_gods),
            '流霞': LiuXia(demigods, lord_gods),
            '亡神': WangShen(demigods, lord_gods),
            '寡宿': GuaSu(demigods, lord_gods),
            '隔角': GeJiao(demigods, lord_gods),
            '丧门': SangMen(demigods, lord_gods),
            '吊客': DiaoKe(demigods, lord_gods),
            '披麻': PiMa(demigods, lord_gods),
            '岁破': SuiPo(demigods, lord_gods),
            '破碎': PoSui(demigods, lord_gods),
            '大耗': DaHao(demigods, lord_gods),
            '五鬼': WuGui(demigods, lord_gods),
            '天狗': TianGou(demigods, lord_gods),
            '红鸾': HongLuan(demigods, lord_gods),
            '龙德': LongDe(demigods, lord_gods),
            '天财': TianCai(demigods, lord_gods),
            '魁罡': KuiGang(demigods, lord_gods),
            '学堂': XueTang(demigods, lord_gods),
            '金舆': JinYu(demigods, lord_gods),
            '禄神': LuShen(demigods, lord_gods),
            '飞刃': FeiRen(demigods, lord_gods),
            '天医': TianYi(demigods, lord_gods),
            '元辰': YuanChen(demigods, lord_gods),
            '天喜': TianXi(demigods, lord_gods),
            '红峦': HongLuan2(demigods, lord_gods),
            '孤辰': GuChen(demigods, lord_gods),
            '天赦': TianShe(demigods, lord_gods),
            '六厄': LiuE(demigods, lord_gods),
            '词馆': CiGuan(demigods, lord_gods),
            '祸害': HuoHai(demigods, lord_gods),
            '童子': TongZi(demigods, lord_gods),
            '孤鸾': GuLuan(demigods, lord_gods),
            '十恶大败': ShiEDaBai(demigods, lord_gods),
            '阴阳差错': YinChaYangCuo(demigods, lord_gods),
            '金神': JinShen(demigods, lord_gods),
        }

        return (
            self.get_demigod_explain(self.demigods.nian_zhu_demigod),
            self.get_demigod_explain(self.demigods.yue_zhu_demigod),
            self.get_demigod_explain(self.demigods.ri_zhu_demigod),
            self.get_demigod_explain(self.demigods.shi_zhu_demigod),
        )

    def get_demigod_explain(self, demigod_list):
        return [self.demigod_explain_mapping[item] for item in demigod_list]

    def demigod_exist_position_for_age_stages(self, idx_name):
        exists_position_stage_mapping = []
        if idx_name in self.demigods.nian_zhu_demigod:
            exists_position_stage_mapping.append('少年时期')
        if idx_name in self.demigods.yue_zhu_demigod:
            exists_position_stage_mapping.append('青年时期')
        if idx_name in self.demigods.ri_zhu_demigod:
            exists_position_stage_mapping.append('中年时期')
        if idx_name in self.demigods.shi_zhu_demigod:
            exists_position_stage_mapping.append('老年时期')
        return exists_position_stage_mapping


class TianDeGuiRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "天德贵人"
        self.type = "护身神煞"
        self.explanation = "天有神助，遇难呈祥，化险为夷"


class YueDeGuiRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "月德贵人"
        self.type = "护身神煞"
        self.explanation = "天有神助，遇难呈祥，化险为夷"


class TianYiGuiRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "天乙贵人"
        self.type = "最吉神煞"
        self.explanation = "解难神煞、贵人相助、雪中送炭、做事容易成功"


class WenChangGuiRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "文昌贵人"
        self.type = "学业神煞"
        self.explanation = "气质雅秀，举止斯文，好学新知，有上进心。一生近官利贵，不与粗俗之辈乱交。"

    def explain(self):
        result = super().explain()

        demigod_position = super().demigod_exist_position_for_age_stages(self.name)
        if demigod_position:
            result += f'在：{",".join(demigod_position)}比较喜欢看书学习。\n'

        return result


class DeXiuGuiRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "德秀贵人"
        self.type = "贵人神煞"
        self.explanation = "逢凶化吉，献瑞呈祥。主人仪容清秀温柔爽朗，涵养出众，很有才华。"

    def explain(self):
        result = super().explain()

        if self.demigods.is_male:
            result += "男命：无冲破克压者，其人聪明晓事，温厚和气，文业通达，遇事常人贵人相助，总能逢凶化吉。带财官，主贵。此外，男命德秀贵人多带正气，所以命主很可能多在公、检、法或事业单位工作。"
        else:
            result += "为人仁慈、敏慧、慈善、温顺、修养高，一生有贵人相助，无险无虑，较为神佛帮助。"

        return result


class YiMa(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "驿马"
        self.type = "奔波，出门，车辆信息之神"
        self.explanation = "驿马星，主人多出门奔波，有贵人相助，事业有成，财运亨通。"

    def explain(self):
        result = super().explain()

        yi_ma_count = self.demigods.demigod_count[self.name]
        result += f'''
        可能会有{yi_ma_count}辆车，或者{yi_ma_count}次出远门的经历。
        '''
        if self.name in self.demigods.ri_zhu_demigod:
            result += f"""
        日柱上有驿马，可能会有一辆登记在{'太太' if self.demigods.is_male else '先生'}名下的车。\n
        """

        if '文昌贵人' in self.demigods.all_demigod and self.demigods.all_demigod.index(
                '文昌贵人') > self.demigods.all_demigod.index(self.name):
            result += f"""
        文昌贵人在驿马之后，说明这辆车的档次挺高的。\n
        """

        if '劫煞' in self.demigods.all_demigod and self.demigods.all_demigod.index(
                '劫煞') > self.demigods.all_demigod.index(self.name):
            result += f"""
        劫煞在驿马之后，说明这辆车可能会被偷。\n
        """
        return result


class TaiJiGuiRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "太极贵人"
        self.type = "贵人神煞"
        self.explanation = "主人聪明好学，文采飞扬，好奇心重，喜欢神秘事物。"

    def explain(self):
        result = super().explain()

        demigod_position = super().demigod_exist_position_for_age_stages(self.name)
        if demigod_position:
            result += f'在：{",".join(demigod_position)}会遇到懂周易的人。\n'

        return result


class HuaGai(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "华盖"
        self.type = "半吉半凶"
        self.explanation = "孤独内向的 i 人，爱干净整洁，有可能有洁癖，有艺术细胞，与佛道有缘，有皈依的念头。运气不佳，比较被动。山、医、命、相、卜有一技之长。"


class TaoHua(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "桃花"
        self.type = "花心之神"
        self.explanation = "贞操观念差，容易和多个异性发生关系。自己不用很出众，但是会有很多人愿意扑。"

    def explain(self):
        result = super().explain()
        conditions = {
            '偏财': self.calc_pian,
            '劫财': self.calc_jie,
            '比肩': self.calc_jie,
            '七杀': self.calc_sha,
            '正官': self.calc_zheng,
            '伤官': self.calc_shang,
        }

        self_calc = [
            self.calc_outside,
            self.calc_xing,
            self.calc_he,
            self.calc_mu_yu,
            self.calc_shui,
        ]

        distinct = []
        for item in self.demigods.all_demigod:
            if item in distinct or item not in conditions:
                continue
            result += conditions[item](item)

        for func in self_calc:
            result += func()

        return result

    def calc_pian(self, idx_god):
        result = ""
        if self.check_gods_meet(idx_god):
            result += "桃花坐正偏财，除本人有桃花外，有可能是老婆长得漂亮，也有可能是老婆会与人私通。偏财为父，成者父亲不正派。\n"
        return result

    def check_gods_meet(self, lord_god):
        return ((self.name in self.demigods.nian_zhu_demigod and lord_god in [
            self.lord_gods.nian_gan_lord_gods] + self.lord_gods.nian_zhi_lord_gods)
                or
                (self.name in self.demigods.yue_zhu_demigod and lord_god in [
                    self.lord_gods.yue_gan_lord_gods] + self.lord_gods.yue_zhi_lord_gods)
                or
                (self.name in self.demigods.ri_zhu_demigod and lord_god in [
                    self.lord_gods.ri_gan_lord_gods] + self.lord_gods.ri_zhi_lord_gods)
                or
                (self.name in self.demigods.shi_zhu_demigod and lord_god in [
                    self.lord_gods.shi_gan_lord_gods] + self.lord_gods.shi_zhi_lord_gods))

    def calc_jie(self, idx_god):
        result = ""
        if self.check_gods_meet(idx_god):
            result += "桃花坐比肩劫财，为“桃花劫”显示会因色破财，受人欺骗敲诈。"
            if self.demigods.is_male:
                result += "男命桃花劫，因而或因经常出入声色场所(如歌舞厅、夜总会等)而消耗不少金钱，或者自己成为“横刀夺爱的”的主角。"
            else:
                result += "女命桃花劫，有可能是受骗失身，或者为达某种目的而对某些男人以身相许(经云女命:劫比桃花大不良)。"
            result += "\n"
        return result

    def calc_sha(self, idx_god):
        result = ""
        if self.check_gods_meet(idx_god):
            result += "桃花坐七杀，为“桃花杀”，经云:酒色猖狂，只为桃花带杀。不论男女，皆色欲极重，并且会因桃色事件而招来杀身之祸，或被人狠狠地敲诈一笔，或因性乱染上杨梅大疮。\n"
        return result

    def calc_zheng(self, idx_god):
        result = ""
        if not self.demigods.is_male:
            return result

        if self.check_gods_meet(idx_god):
            result += "女命八字正官坐桃花，可能是老公长得帅，有好的事业工作。不过也有可能是老公在外金屋藏娇。\n"

        return result

    def calc_outside(self):
        result = ""
        if self.name in self.demigods.shi_zhu_demigod:
            result += "桃花落在时辰上，为“墙外桃花”，其所犯桃花的机会又大大增多。\n"
        return result

    def calc_xing(self):
        result = ""
        if all(item in self.demigods.all_zhi for item in ['子', '卯']):
            result += "桃花刑：八字带桃花，又有子卯相刑，异性缘特好，只讲一时快活，不要任何情调，并会因色欲而来不少麻烦。\n"
        return result

    def calc_he(self):
        di_zhi_he = [item[0] for item in DI_ZHI_HE]
        san_he = [item[0] for item in DI_ZHI_SAN_HE]
        for he_zhi in di_zhi_he:
            if len([item for item in self.demigods.all_zhi if item in he_zhi]) > 1:
                return "八字带桃花，又有三合、六合，异性缘特好，淫不可言。经云:桃花带合，必是浪游之子。\n"

        for he_zhi in san_he:
            if len([item for item in self.demigods.all_zhi if item in he_zhi]) > 1:
                return "八字带桃花，又有三合、六合，异性缘特好，淫不可言。经云:桃花带合，必是浪游之子。\n"

        return ""

    def calc_mu_yu(self):
        result = ""
        if "沐浴煞" in self.demigods.all_demigod:
            result += "沐浴桃花：八字带桃花，又有沐浴煞，男女俊美，异性缘特好，淫不可言。诗云:桃花沐浴不堪闻，叔伯姑姨合共婚，日月时胎如犯此，定知无义乱人伦。\n"
        return result

    def calc_shui(self):
        result = ""
        if [self.demigods.element_matrix[0] + self.demigods.element_matrix[0]].count('水') >= 5:
            result += "八字带桃花，又有水局，异性缘特好，淫不可言。经云:桃花带水，必是浪游之子。"
            if not self.demigods.is_male:
                result += "女命可为媢。"
            result += "\n"
        return result

    def calc_shang(self, idx_god):
        result = ""
        if self.lord_gods.all_lord_gods.count(idx_god) >= 5 or self.lord_gods.demigod_explain.single_explain_mapping[
            idx_god].total_weight >= 5:
            result += "八字带桃花，柱中伤官多，淫不可言，不知伦常为何物。\n"
        return result


class JieSha(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "劫煞"
        self.type = "凶神"
        self.explanation = "主是非、破财、主病伤刑法之灾，有时东西会找不到。"

    def explain(self):
        result = super().explain()

        result += self.check_self_strong()

        result += self.self_count()

        return result

    def check_self_strong(self):
        result = ""
        if not self.demigods.self_strong:
            result += "弱日元强旺又带劫煞，主人勇敢不怕死，可以从事武职，如军警、古代为将军。\n"
        return result

    def self_count(self):
        result = ""
        if self.demigods.all_demigod.count(self.name) >= 2:
            result += "八字带劫煞，又有劫煞，主人性格暴躁，易与人发生矛盾，或者有犯罪倾向。\n"
        return result


class ZaiSha(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "灾煞"
        self.type = "最凶的神煞"
        self.explanation = "命中逢灾煞，经常厄运缠身。主疾病、官司、牢狱、破财。"

    def explain(self):
        result = super().explain()

        result += self.check_protection()

        return result

    def check_protection(self):
        result = ""
        zai_sha_position = self.demigod_exist_position_for_age_stages(self.name)
        protection_position = list(
            set(self.demigod_exist_position_for_age_stages('天乙贵人') + self.demigod_exist_position_for_age_stages(
                '天德贵人') + self.demigod_exist_position_for_age_stages('月德贵人')))
        if not any(item in protection_position for item in zai_sha_position):
            result += "如果四柱没有天乙、天德、月德保护则会发生血光之灾横死。\n"
        return result


class XueRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "血刃"
        self.type = "身体伤害"
        self.explanation = "主血光之灾。容易遇到意外，开刀、住院。对尖锐物品比常人敏感，轻者皮肉伤折，重者生死意外。"

    def explain(self):
        result = super().explain()

        result += self.check_self_strong()

        result += self.check_car_accident()

        result += self.check_count()

        result += self.check_female()

        return result

    def check_self_strong(self):
        result = ""
        if self.demigods.self_strong:
            result += "强日元带血刃，大概率意外事故见血。\n"
        else:
            result += "弱日元带血刃，因病灾见血。\n"
        return result

    def check_car_accident(self):
        result = ""
        if all(item in self.demigods.all_demigod for item in ['驿马', '羊刃']):
            result += "驿马血刃，主人可能会有车祸。\n"
        return result

    def check_count(self):
        result = ""
        if self.demigods.all_demigod.count(self.name) >= 2:
            result += "血刃过多：血光之灾概率上升。"
            if (
                    not '正印' in self.lord_gods.all_lord_gods
                    or
                    not any('贵人' in item for item in self.demigods.all_demigod)
            ):
                result += "没有贵人/正印保护容易横死。"
            result += "\n"
        return result

    def check_female(self):
        return "女性：容易产厄、血崩，生产大出血。\n" if not self.demigods.is_male else ""


class FuXing(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "福星贵人"
        self.type = "吉星"
        self.explanation = "能够给生活带来逢凶化吉的机会，可以享福，比常人有更多的机会，需要好好把握才行。"


class TianDeHe(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "天德合"
        self.type = "逢凶化吉之神"
        self.explanation = "最大的特点是化解灾厄。命带天德贵人者会遇到很大的福德，其人心地善良，身体健康，人缘好，在生平之中较不会遇到横祸、盗难、灾劫等，纵使逢之也能适时得以化解。"


class GuoYin(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "国印贵人"
        self.type = ""
        self.explanation = "主人诚实可靠, 严守清规, 照章行事, 办事公道。 为人和悦,礼义仁慈, 气质轩昂。 如国印逢生旺, 有其它吉星相助, 不逢冲破克害, 不仅可以有掌印之能, 可亦为官掌实权。"


class TianSheGui(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "天赦贵"
        self.type = ""
        self.explanation = "主一生吉利，逢凶化吉。"


class JiangXing(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "将星"
        self.type = ""
        self.explanation = "易掌握权势，较有老板或主管之命。"


class JinKui(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "金匮"
        self.type = ""
        self.explanation = "表示可得配偶之财，宜用心择偶，男女可获得良缘。"


class YangRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "羊刃"
        self.type = ""
        self.explanation = "性情刚强，敢作敢为，为人精明，配合得宜能得大富贵。"


class HongYan(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "红艳"
        self.type = ""
        self.explanation = "命带红艳，男女长相讨人喜欢，带有性感的魅力。"


class XueShi(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "学士"
        self.type = ""
        self.explanation = "研究心、好奇心、探索欲、背诵能力很强。才华洋溢有读书命，学历多半较高。"


class LiuXia(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "流霞"
        self.type = ""
        self.explanation = "男忌酒色，女小心产厄。"


class WangShen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "亡神"
        self.type = ""
        self.explanation = "城府较深，比较有心机，喜怒哀乐，不形於色。"


class GuaSu(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "寡宿"
        self.type = ""
        self.explanation = "女命犯之夫早别离，独守空闺。"

    def explain(self):
        return super().explain() if not self.demigods.is_male else ""


class GeJiao(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "隔角"
        self.type = ""
        self.explanation = "易有牢狱之灾，六亲缘份较淡薄。"


class SangMen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "丧门"
        self.type = ""
        self.explanation = "避免观丧，探病。"


class DiaoKe(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "吊客"
        self.type = ""
        self.explanation = "表示可能不太利于亲人。 一般代表亲人出现意外，有伤病、最严重的就是去世。 而如果大运流年遇见了，也要多加小心。"


class PiMa(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "披麻"
        self.type = ""
        self.explanation = "披麻戴孝的意思。如果犯了披麻星，也就意味着会幼年失去双亲，或者亲人会离开。所以结婚莫逢披麻星，盖房莫盖披麻屋。"


class SuiPo(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "岁破"
        self.type = ""
        self.explanation = "八字逢之，较易有意外破财之事发生。"


class PoSui(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "破碎"
        self.type = ""
        self.explanation = "八字逢之，较易有意外破财之事发生。"


class DaHao(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "大耗"
        self.type = ""
        self.explanation = "八字逢之，较易有意外破财之事发生。"


class WuGui(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "五鬼"
        self.type = ""
        self.explanation = "易招惹是非小人。"


class TianGou(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "天狗"
        self.type = ""
        self.explanation = "流年逢之有血光之灾。"


class HongLuan(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "红鸾"
        self.type = ""
        self.explanation = "吉上加吉。"


class LongDe(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "龙德"
        self.type = ""
        self.explanation = "主逢凶化吉。"


class TianCai(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "天财"
        self.type = ""
        self.explanation = "意外之财"

    def explain(self):
        result = super().explain()

        result += self.check_self_strong()

        return result

    def check_self_strong(self):
        result = ""
        if self.demigods.self_strong:
            result += "八字身旺无忌\n"
        else:
            result += "身弱者得意外之财，紧接意外之灾。\n"
        return result


class KuiGang(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "魁罡"
        self.type = ""
        self.explanation = "性格严谨，聪慧，临事迅速果决，八字身旺主发达。"

    def explain(self):
        result = super().explain()

        result += self.check_tian_yi()

        return result

    def check_tian_yi(self):
        return "加上天乙贵人更佳。\n" if '天乙贵人' in self.demigods.all_demigod else ""


class XueTang(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "学堂"
        self.type = ""
        self.explanation = "模仿力、创作力、想象力、理解力都很强，适合讲课做老师。命中带有词馆的人，多为多学多才，聪明巧智，文章冠世，一生富贵之人。"


class JinYu(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "金舆"
        self.type = ""
        self.explanation = "财帛之星和配偶相关联，会受到配偶之财帛、技术之相助。"


class LuShen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "禄神"
        self.type = ""
        self.explanation = "人际社交广阔，财禄丰足，避免借贷担保，可避免诉讼。"


class FeiRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "飞刃"
        self.type = ""
        self.explanation = "攻击、意外、争端、是非之星"

    def explain(self):
        result = super().explain()

        result += self.check_position()

        return result

    def check_position(self):
        result = ""
        if any(self.name in item for item in [self.demigods.yue_zhu_demigod, self.demigods.shi_zhu_demigod]):
            result += "出现在月时两柱最严重。\n"
        return result


class TianYi(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "天医"
        self.type = ""
        self.explanation = "学习力、理解力、观察力、模仿力、好奇心、研究心、直觉观等能力皆强。适合学医，包括中/西医、心理医生，卜卦算命等。"


class YuanChen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "元辰"
        self.type = ""
        self.explanation = "耗损、口舌之星，主纷争。"


class TianXi(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "天喜"
        self.type = ""
        self.explanation = "喜悦如意愉快之星，具有幽默感、亲和力、人情味。"


class HongLuan2(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "红峦"
        self.type = ""
        self.explanation = "异性缘、浪漫思想、静态艺术色系组合能力皆强。"


class GuChen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "孤辰"
        self.type = ""
        self.explanation = "性格孤僻沉默不语、清心寡欲、依恋安逸、没有上进心。"


class TianShe(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "天赦"
        self.type = "福神"
        self.explanation = "一生不犯官司、诉讼、牢狱，一生凡事都能逢凶化吉有惊无险。"


class LiuE(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "六厄"
        self.type = "衰神"
        self.explanation = "命带六厄者最不利事业，其人常精神萎靡，总嫌人事不济，前途深藏危机，劳动成果被剽窃，得不到他人的认可或重视，不被提携或重用。"


class CiGuan(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "词馆"
        self.type = "福神"
        self.explanation = "如今官翰林，谓之词馆，取其学业精专，文章出类。命中带有词馆的人，多为多学多才，聪明巧智，文章冠世，一生富贵之人。"


class HuoHai(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "祸害"
        self.type = "凶神"
        self.explanation = "主官灾是非，财难积聚，争执被骗，不好的加倍坏下去，撞车，吃得多变糖尿病"


class TongZi(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "童子"
        self.type = "弱凶神（不利婚姻）"
        self.explanation = "童子命的人婚姻不利，晚婚，或无婚恋，痴迷爱情的倒不多，因为根本就不会谈恋爱，一谈就吹，或者有人追、自己会谈也不行，一谈就出意外，即使硬撮合的也会因故而分手，多次离婚，更有一结婚或一破身就生病。"


class GuLuan(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "孤鸾煞"
        self.type = "弱凶神（不利婚姻）"
        self.explanation = "命犯孤鸾煞，主婚姻不顺。孤鸾犯日本无儿，一见官星得子奇，运遇旺乡名姐妹，临风惆怅绿楼时。"


class ShiEDaBai(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "十恶大败"
        self.type = "大凶神"
        self.explanation = "十恶，就是大凶；大败，就是临阵怯敌，大败而归。没有”俸禄“，做不了公职人员，容易被裁员/提前退休。花钱如流水，难以聚财。"


class YinChaYangCuo(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "阴阳差错"
        self.type = "凶神"
        self.explanation = """
        一是婚姻不顺,易生误会和意外之事。女子逢之，夫家冷退婚姻难求；男子逢之家庭不幸。
        二是多数人身上附有异性灵体,这异性灵体会干挠破坏姻缘，情侣因误会而分手，夫妻一斗气就离婚,都是身上异性灵体的干挠破坏所制，而非本人意愿如此。
        三是命带阴差阳错易有同性恋的倾向。他们多数是犯了错受天道的惩罚,有些人会成为同性恋倾向。
        四是外交冷落,多有点孤傲,待人处事有所欠缺,会遇到莫名其妙的意外事件。做事往往坐失良机或机缘突变或功败垂成。
        五是不能跟首个有性关系的恋人结婚；或存在有同母异父或同父异母的兄弟姐妹之兆。
        """


class JinShen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "金神"
        self.type = "破败之神"
        self.explanation = """
        如果要破除命理金神煞，就要用火制，如果八字里有七煞或羊刃，就是金神为真贵人、反吉！
        金神命格：要月令通金气（申酉戌丑巳月），命中成火局武贵。
        生于亥卯未月而运行丙丁巳午火乡，则成富格。
        身弱要羊刃帮扶，身强要七杀、伤官，巳午月，岁运见丙丁火必发福，亥子破火必死。
        暗金地煞：也称为暗金的杀，有三分别为：
            “呻吟煞，子午卯酉月见巳，主杖责刑狱”
            “白衣煞，辰戌丑未月见丑，主妨害丧服哭泣之事”
            “破碎煞，寅申巳亥月见酉，主支离流血之灾”。
        """
