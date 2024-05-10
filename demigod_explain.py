from constants import *


class DemigodExplain:
    def __init__(self, demigods, lord_gods):
        self.demigods = demigods
        self.lord_gods = lord_gods
        self.name = ""
        self.type = ""
        self.explanation = ""

    def explain(self):
        type_str = f'（{self.type}）' if self.type else ''
        result = f'''
        {self.name}{type_str}
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
            '天厨': TianChu(demigods, lord_gods),
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
        self.explanation = "天有神助，遇难呈祥，化险为夷。如果天德月德并存，其人多一生如意，荣华富贵，在社会上能获得很高的名誉地位，少凶灾横祸。"


class TianChu(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "天厨"
        self.type = "食神禄"
        self.explanation = f"""
        天厨又名「食神禄」，先贤陆位亦说:「天厨，宜食禀」，食禀是藏食粮的仓库。
        天厨乃食神建禄之宫，食神是人命福星，食神既能得禄，其福必厚，故谓之天厨。
        天厨入命的人，如不逢刑冲克破空亡，一生不愁吃穿，食禄不虞匮乏，可以享降天之禄、得天赐之福，古人谓之“衣食无忧，福禄满堂”。
        八字带有天厨贵人的命，一生大都能够平安吉顺，遇事可以化险为夷、福禄优游。
        女命逢天厨贵人，有口福，爱美食，爱做饭，且烹饪技术一流，饭菜之香胜于他人，能迅速拉高一家人的幸福指数，因此有旺夫一说。
        """


class YueDeGuiRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "月德贵人"
        self.type = "护身神煞"
        self.explanation = f"""
        天有神助，遇难呈祥，化险为夷。
        月德贵人同天乙贵人一样，是一颗很好的吉星，命主在命局中逢上带有月德贵人，一生处世无忧，化险为夷，平生很少生病，不犯官刑。
        但需要注意的是，月德是勤勉敏慧之徳星，虽然命主身带此吉星，也需本身勤勉自助，才能在紧要关头获得帮助。
        天德和月德，都是贵人吉星的名称。与其它贵人星有一个最大的不同处，就是天月德比较趋向于一个人个性方面的表现，也就是说天月德谈的是性格。
        一般来说，八字有天月德入命的人，不但具有贵气的特质，行为处事坦白而无私，也有慈悲心或者同情心。
        人言积善之家必有余庆，所以天月德也具有遇事化险为夷的功能。
        """


class JiuChou(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "九丑"
        self.type = ""
        self.explanation = f"""
        此煞名“丑”，不是指容貌不好看，相反的，此日生者大多容貌美丽，或很有吸引人的魅力。
        其所以名“丑”，是指名声方面的风评，因感情的事容易出问题，严重的可能会惹上法律纠纷，名声受损。
        """


class TianYiGuiRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "天乙贵人"
        self.type = "最吉神煞"
        self.explanation = f"""
        人命有天乙贵人，遇事有人帮，临难有人解，是化险为夷最有力的贵人之星。
        解难神煞、贵人相助、雪中送炭、做事容易成功。后天际遇中的提携、解厄之神，若人遇之则荣名早达，成事多助，官禄易进。
        天乙贵人：人缘、社交缘、异性缘、长辈缘。
        一生少病，人缘佳，易有社会地位，很适合从事公关性质的工作。
        天乙贵人入命：心性聪明，出入近贵。
        大运流年见天乙贵人：有生官发财之机，最少亦有吉祥庆事加临。
        天乙贵人坐旺地：身体健康吉祥富贵，福禄加倍。
        天乙贵人逢合为忌：多见劳苦，劳苦功高。
        天乙贵人逢刑冲：多劳累，遇事则贵人去。
        女命天乙贵人入命、日主自坐二德者：可嫁贵夫。
        天乙贵人是八字里面最重要、最吉祥的一颗贵人星，八字带天乙贵人吉星的人，无形之中会散发一种贵气，给人亲切好相处的感觉。
        还可以转危为安，有很多人发生了意外的危难，受到的伤害却很小，经常都是因为八字里面带有天乙贵人这颗贵人吉星。
        """


class WenChangGuiRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "文昌贵人"
        self.type = "学业神煞"
        self.explanation = f"""
        气质雅秀，举止斯文，好学新知，有上进心。一生近官利贵，不与粗俗之辈乱交。
        文昌多取食神之临官为贵, 为食神建禄之称。文昌入命,主聪明过人,又主化险为夷。气质雅秀,举止温文,男命逢着内涵,女命逢着仪容得体；具有上进心，不与粗俗之辈乱交朋友。
        文昌逢合为喜：富加且贵。文昌逢合为忌：多见忙碌，劳苦功高。文昌坐旺地：身体健康，幸福如意，利考试，贵气十足。文昌逢刑冲：劳累辛苦。
        文昌入命：心性聪明，出入近贵，气质文雅，好学新知，一生可以近贵利官。
        """

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
            result += ("男命：无冲破克压者，其人聪明晓事，温厚和气，文业通达，遇事常人贵人相助，总能逢凶化吉。"
                       "带财官，主贵。此外，男命德秀贵人多带正气，所以命主很可能多在公、检、法或事业单位工作。")
        else:
            result += "为人仁慈、敏慧、慈善、温顺、修养高，一生有贵人相助，无险无虑，较为神佛帮助。"

        return result


class YiMa(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "驿马"
        self.type = "奔波，出门，车辆信息之神"
        self.explanation = f"""
        驿马星，主人多出门奔波，有贵人相助，事业有成，财运亨通。
        代表这个人一生走动多、远行、会出远门。一生驿马运重，即使是在一个地方，也经常会忙个不停，这些都是驿马的作用。
        驿马坐旺地：利禄亨通。驿马为喜用：心高气爽，动则有喜。四柱财官有力，真好马也。
        驿马为喜用，自坐财官地：岁运逢财官星，主升迁。
        驿马为忌且逢冲：是非波动。
        吉神坐马：有乔迁之喜或顺动之利。
        凶神坐马：奔走四方，忙于生计。
        驿马与财星同柱：为喜则财源广进；为忌则奔走四方。
        驿马与财官、贵人同柱：才是真马。
        驿马与正官同柱：为喜者风儒雅士，为忌者性格开放。
        驿马坐七杀，带羊刃或劫煞：小心突发事故。
        驿马逢冲，带羊刃、元辰、空亡：注意人身意外。
        驿马见合：有牵制之虑。
        驿马坐死墓绝、羊刃、劫煞：做事有始无终，飘泊无定。
        驿马自坐绝地：凶，尤岁运再逢冲。
        驿马自坐死、绝方：做事少成。桃花坐马：为情爱受难。
        驿马坐劫煞或羊刃：劳碌奔波，心性多冲动；尤岁运再逢。
        劫煞坐马：容易有意外危险。马星生财者：有名扬之机。
        男命，驿马自坐财星：娶他乡富女。
        女命，驿马与天乙贵人同柱：不利姻缘。
        女命，驿马坐独官：夫为有用人，儿孙亦同。
        女命，驿马自同：嫁远乡。
        驿马逢冲：心猿意马，奔波，忙碌，乃天涯之客。
        流年驿马逢冲：此年多奔波，有迁异职动之机，并多见出国或远行。
        驿马冲动，若带羊刃、血支等神煞，应该小心行事。
        """

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

        if ('文昌贵人' in self.demigods.all_demigod
                and self.demigods.all_demigod.index('文昌贵人') == self.demigods.all_demigod.index(self.name) + 1):
            result += f"""
        文昌贵人在驿马之后，说明这辆车的档次挺高的。\n
        """

        if ('劫煞' in self.demigods.all_demigod
                and self.demigods.all_demigod.index('劫煞') == self.demigods.all_demigod.index(self.name) + 1):
            result += f"""
        劫煞在驿马之后，说明这辆车可能会被偷。\n
        """
        return result


class TaiJiGuiRen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "太极贵人"
        self.type = "贵人神煞"
        self.explanation = f"""
        主人聪明好学，文采飞扬，好奇心重，喜欢神秘事物。
        命中带有太极贵人的八字，可以事职平顺亨通、福禄兼得，事情能够化险为夷，一生多得贵人相助，晚年可以幸福安逸，太极贵人可以说是一颗非常珍贵的吉星。
        """

    def explain(self):
        result = super().explain()

        demigod_position = super().demigod_exist_position_for_age_stages(self.name)
        if demigod_position:
            result += f'在{demigod_position}会遇到懂周易的人。\n'

        return result


class HuaGai(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "华盖"
        self.type = "半吉半凶"
        self.explanation = f"""
        孤独内向的 i 人，爱干净整洁，有可能有洁癖，有艺术细胞，与佛道有缘，有皈依的念头。
        运气不佳，比较被动。山、医、命、相、卜有一技之长。
        华盖是一颗吉祥之星，有揽护君主威严的职权，所以华盖是权力的象征，也是工作职事变化的代表性，亦是艺术之星。
        华盖是八字忌神，虽然聪明好学，但个性比较有孤僻现象，常见血气方刚，不靠六亲。
        如果是八字喜神，一生可以自立更生，见解超群，才华有过人之处；可谓气宇不凡，是一个有条件、有能力成就事业的人。
        双华盖入命：命中多贵人。
        华盖为八字吉神：一生利官近贵，技艺出众。
        岁运华盖逢刑冲：事职有动；若岁运不利，小心意外危难。
        华盖坐空亡、或逢刑冲：工作起伏变动较多。
        华盖带将星，福气深厚。
        华盖在空亡、死、绝之地，可修身养性，修习佛理，净化自身。
        女命，华盖坐日支：形同寡宿。
        华盖临生旺地为喜用，此人才华横溢；
        华盖临（日干）墓地，在日支和时柱为忌，不利子女的健康或运势；若有气，可能为僧道；
        华盖+七杀、桃花，可能成为艺人、巫师；
        华盖+桃花+贵人，会为艺人明星。
        """


class TaoHua(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "桃花"
        self.type = "花心之神"
        self.explanation = f"""
        贞操观念差，容易和多个异性发生关系。自己不用很出众，但是会有很多人愿意扑。
        命带桃花，其人聪明，有同情心，爱风骚，多才艺。桃花处于升旺之地时，其主任帅气/俊美。
        男命慷慨好交游，喜美色；女命风情万种，漂亮诱人。
        命带桃花,其人性巧,有同情心,爱风流,多才艺,能艺术,如果八字出现桃花而且处于生旺之地则主其人姿容俊美
        如果是男人,则慷慨好交游,喜美色
        如果是女人则风情万种, 漂亮诱人。桃花并主聪明,异性缘佳。
        桃花忌见水,见之则生理欲望比较强。如申子辰人逢癸酉或亥子丑水。
        时支桃花,时干不宜再见伤官,因为伤官本身已伤害官星(夫星),如再坐桃花, 将导致多夫,及婚姻不美满的情形。
        几种情况：
        桃花在年月：称为『内桃花』，夫妻恩爱。
        桃花在日时：称为『外桃花』，夫妻多纷争；尤岁运再逢。
        时上桃花：桃花强，感情丰富。
        桃花入命，干见杀星：为人多情、欲望强。
        桃花与禄神同柱：有异性缘。
        桃花与羊刃同柱：感情风波，是非多灾。
        桃花与空亡同柱：人缘有欠缺之忧，一生为情多苦。
        桃花与元辰同现或桃花逢刑冲：可能会因为钱财女人方面遇到问题。
        不易犯桃花者：桃花坐空亡；命不带桃花。
        男命，桃花合禄：一生多有女贵人，多见帮助。
        男命，桃花与禄神同柱：能得桃花之助力。
        女命，流年大运见桃花刑冲：不利姻缘。
        桃花喜与正官、正印同柱：表示自己有自制能力，不致于滥。
        喜与食神同柱：表示将欲求转为文学、艺术的才华。
        忌与七杀同柱：表示容易为欲望犯罪，女性则被迫，坠入风尘。
        与伤官同柱（欲望强）：表示喜新厌旧、容易自恃才貌、追求时髦，对于感情不太在乎。
        与劫财同柱：敢爱敢恨、横刀夺爱、争风吃醋。
        与偏印同柱：生理欲望较强，同性。
        与比肩同柱：孤芳自赏、独身主义。
        """

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
            self.lord_gods.nian_gan_core_lord_gods] + self.lord_gods.nian_zhi_cang_gan_lord_gods)
                or
                (self.name in self.demigods.yue_zhu_demigod and lord_god in [
                    self.lord_gods.yue_gan_core_lord_gods] + self.lord_gods.yue_zhi_cang_gan_lord_gods)
                or
                (self.name in self.demigods.ri_zhu_demigod and lord_god in [
                    self.lord_gods.ri_gan_core_lord_gods] + self.lord_gods.ri_zhi_cang_gan_lord_gods)
                or
                (self.name in self.demigods.shi_zhu_demigod and lord_god in [
                    self.lord_gods.shi_gan_core_lord_gods] + self.lord_gods.shi_zhi_cang_gan_lord_gods))

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
            result += ("桃花坐七杀，为“桃花杀”，经云:酒色猖狂，只为桃花带杀。"
                       "不论男女，皆色欲极重，并且会因桃色事件而招来杀身之祸，或被人狠狠地敲诈一笔，或因性乱染上杨梅大疮。\n")
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
        if [self.demigods.elements_matrix[0] + self.demigods.elements_matrix[0]].count('水') >= 5:
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
        self.explanation = f"""
        主是非、破财、主病伤刑法之灾，有时东西会找不到。
        劫煞主意外危难、健康、刑法上面的问题。为喜具有竞争心，肯求上进，做事有魄力，敢担当。
        劫煞与贵星同柱：谋事有成。
        劫煞与天乙贵人、或喜用神同柱：有才能和智谋。
        劫煞与羊刃同柱：小心意外危险。
        """

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
        self.explanation = f"""
        命中逢灾煞，经常厄运缠身。主疾病、官司、牢狱、破财。
        灾煞也叫“白虎煞”，其性勇猛，冲破将星，谓之灾煞。
        此煞主人身意外，根据所处五行支，在水火，防焚溺，金木，杖刃；土，坠落瘟疫。若与七杀同柱来克身，可能有危难。
        也主刑律官司。若灾煞是正官、正印的生旺之支，多是武权。
        """

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
        self.explanation = f"""
        最大的特点是化解灾厄。天月德助，处世无殃。能把遇到凶险转化为吉祥、顺利，随处保护。
        命带天德贵人者会遇到很大的福德，其人心地善良，身体健康，人缘好，在生平之中较不会遇到横祸、盗难、灾劫等，纵使逢之也能适时得以化解。
        天月德助，处世无殃。能把遇到凶险转化为吉祥、顺利，随处保护。天地德秀之气，其特点是化解危难。
        命带天德贵人者有福德，其人心地善良，身体健康，人缘好，在生平之中较不会遇到意外等，纵使逢之也能适时得以化解。
        天德和月德，都是贵人吉星的名称。与其它贵人星有一个最大的不同处，就是天月德比较趋向于一个人个性方面的表现，也就是说天月德谈的是性格。
        一般来说，八字有天月德入命的人，不但具有贵气的特质，行为处事坦白而无私，也有慈悲心或者同情心。
        人言积善之家必有余庆，所以天月德也具有遇事化险为夷的功能。
        """


class GuoYin(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "国印贵人"
        self.type = ""
        self.explanation = f"""
        主人诚实可靠, 严守清规, 照章行事, 办事公道。 为人和悦,礼义仁慈, 气质轩昂。
        如国印逢生旺, 有其它吉星相助, 不逢冲破克害, 不仅可以有掌印之能, 可亦为官掌实权。
        亦主一生工作，生活环境多动，若流年岁运逢之即主工作变动或家庭搬迁。
        """


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
        self.explanation = f"""
        易掌握权势，较有老板或主管之命。
        将星跟权力地位有关，命带将星的人，给人不可侵犯的感觉，很自然的散发出一种无形、难以言喻的权威感，让人望而生敬。
        很多做官的人或工商高层主管八字里面大都带有将星，所以也称为将权，八字带有将星，称做将权入命。
        将星入命：能文能武，一生有权柄威信，具有组织领导能力，会见掌权之机。
        将星为真格：须正官、七杀有力，或印星有力。将星入命，岁运为财官：大权在握，利禄亨通。
        将星与亡神同现：才智过人，深具谋略，会是栋梁之才。将星无破：财、官运亨通。将星三合为忌神：奔波多劳。将星逢冲克，权利事职有变动。
        """


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
        self.explanation = f"""
        性情刚强，敢作敢为，为人精明，配合得宜能得大富贵。
        羊刃是一种很强硬的气力，但它不一定是凶恶的，必须看八字中的整体组合。
        假如一个人的八字很弱，羊刃可以起到很大的匡助作用，比如你贫穷困难时，羊刃就是一个强有力的兄弟，能帮助和支持你；假如八字比较旺，再来羊刃的话就危险了，缺乏适当制约的话，他会与你争夺，劫财。
        羊刃是五行过旺之气，通常被认为是凶星。刃，即刀，故亦常与手术、杀伤有关。情绪容易激动，易树敌，生涯充满惊涛骇浪。
        从事机械、技术之研究，成功的人很多。虽然常碰到困难，但若成功时，所缔造的都是丰功伟业。
        羊刃+血刃+驿马同柱：人身意外、多惊多险、交通意外事故。
        时刃者, 岁运并临, 可能会有意外危难。
        年刃者，祖上家运可能不太顺利，影响到置产、钱财储蓄、家人之间的关系。
        """


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
        self.explanation = f"""
        男忌酒色，女小心产厄。
        流霞逢冲：易犯人身意外。男命：酒色。女命：分娩方面的意外。
        古人称血煞。轻者可能会有皮肉之伤，健康方面的问题，重者可能会有人身意外。
        命犯血煞，最怕八字凶神带重，大运流年又走在凶煞冲克之地，可能会因为一些事情而受伤或出现人身意外，如果八字有吉神转化，是可以化险为夷的。
        岁运走在流霞、血支、血刃的流年，不论轻重，或多或少可能会受伤。
        如果是在不利的流年岁月期间，外出、开车多加小心谨慎，防止意外发生的严重性增加。
        """


class WangShen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "亡神"
        self.type = ""
        self.explanation = f"""
        城府较深，比较有心机，喜怒哀乐，不形於色。
        亡神若为命局中所喜用的地支，并与吉神同柱，则会沉稳干练，谋略深算，严谨有威，好胜心强。
        如果恰为命局所忌的地支，又与其它凶煞同柱，则性情中存在着虚伪掩饰的成分，家业容易不顺，影响置业和储蓄；
        夫妻感情一般，多波折；子女的健康或运势也容易出现问题；自己也经常得罪人，严重的话会有法律纠纷出现。
        亡神入命为八字凶神的人，做起起事来总感觉无精打采，不利家运，一生难免争纷，严重者可能会惹上法律纠纷，容易涉足酒色场所。
        不管男命还是女命，夫妻间都容易争吵，子女也会有不省心的情况发生。
        古人论命特别强调了亡神入命的危害，其实不是没有道理。
        亡神入命：城府多深，做事疑虑。
        亡神与天乙贵人同现：老谋深算。
        亡神为喜：面有威仪、足智多谋、处事严谨、断事如神，是一个真人不露相的人。
        最怕亡神是命中凶忌之神：其人心性难定、事难如愿、脾气粗俗。
        """


class GuaSu(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "寡宿"
        self.type = ""
        self.explanation = f"""
        女命犯之夫早别离，独守空闺。命犯孤辰寡宿，主形孤肉露，面无与气，不利六亲，婚姻不顺。
        男命怕孤辰落在财星之地，或日主的死绝之方。女命怕寡宿落在夫星之地，或日主的死绝之方。
        这现像造成缘份难偕久之憾，难免刑克，内心容易伤感，尤其是孤寡入命又见空亡的八字，一生比较孤单。八字忌孤辰、寡宿同时入命。
        如果命带孤辰或寡宿，八字又有华盖出现，则是一个非常聪明的孤独之人，往往具有特殊才华，很多艺术家、哲学家、五术家，或是修道者、牧师，多是这种命格。
        """

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
        self.explanation = f"""
        避免观丧，探病。
        年支前两位为丧门，比如巳年生人，前两位未就是丧门，后两位卯就是吊客，后三位寅就是批麻。
        披麻、吊客、丧门皆为凶星。如大运、流年遇之，多主人身意外，伤病等事出现，也不容易聚财。
        """


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
        self.explanation = f"""
        披麻戴孝的意思。如果犯了披麻星，也就意味着会幼年失去双亲，或者亲人会离开。所以结婚莫逢披麻星，盖房莫盖披麻屋。
        年支前两位为丧门，比如巳年生人，前两位未就是丧门，后两位卯就是吊客，后三位寅就是批麻。
        披麻、吊客、丧门皆为凶星。如大运、流年遇之，多主人身意外，伤病等事出现，也不容易聚财。
        """


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
        self.explanation = f"""
        财帛之星和配偶相关联，会受到配偶之财帛、技术之相助。
        日坐金舆：能得异性之助；命带金舆：得祖荫。又称金舆禄神，此星入命能得扶助，一生能得富贵。
        女人逢之，幸福安吉、骨肉安泰。
        男人逢之，得贤妻，享妻钱财，荣富显贵。
        古代皇族，多带此星。金舆是贵人乘坐的车子。乃禄命之旌旗，三才之节钺。主人性柔、貌美，举止温顺。
        """


class LuShen(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "禄神"
        self.type = ""
        self.explanation = f"""
        人际社交广阔，财禄丰足，避免借贷担保，可避免诉讼。
        身旺见禄，喜见财官。身弱喜禄而逢死绝遭刑冲，又逢吉祥救应，家运可能不太顺利，容易影响到置产、家人之间的关系；同时在求财方面也较为困难。
        在年月为“建禄”，四柱天干要见财官，“建禄生是月，财官喜透天”也。透财，富。透官，贵。
        在时为“归禄”，不喜官星，“日禄归时没官星，号曰青云得路。
        ”主少年发达。“建禄”主长辈之荫，主少年时代幸福。若逢卫破，家运可能不太顺利。
        身（日主）若太旺，不屑于祖辈留有的家产，不愿坐享现成之福，会自己在外乡创事业。若逢偏印，即破禄而无禄。
        在日为“专禄”（甲寅、乙卯、庚申、辛酉四日），主会享受，爱过阔绰的生活。要有羊刃来保护（因禄柔、刃刚），若被合去则无禄。被冲不利丈夫或者妻子的健康和运势。
        八字如果有禄有财：丰盈一生。
        八字如果有禄无财：祖先庇荫。
        八字若无禄有财：白手起家。
        大运流年与禄神冲克：可能有意外危险，难聚财，健康上也要注意。
        """


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
        self.explanation = f"""
        学习力、理解力、观察力、模仿力、好奇心、研究心、直觉观等能力皆强。适合学医，包括中/西医、心理医生，卜卦算命等。
        天医是掌管疾病之事的星神。四柱逢天医,如不旺,又无贵人吉神相扶,不利于身体健康，容易身弱无力。
        若生旺又有贵人相生助,不仅身体健壮,而且特别适合从事医学、心理学、哲学等。学习力、理解力、观察力、模仿力、好奇心、研究心、直觉观等能力皆强。
        """


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
        self.explanation = f"""
        性格孤僻沉默不语、清心寡欲、依恋安逸、没有上进心。命犯孤辰寡宿，主形孤肉露，面无与气，不利六亲，婚姻不顺。
        男命怕孤辰落在财星之地，或日主的死绝之方。女命怕寡宿落在夫星之地，或日主的死绝之方。
        这现像造成缘份难偕久之憾，难免刑克，内心容易伤感，尤其是孤寡入命又见空亡的八字，一生比较孤单。八字忌孤辰、寡宿同时入命。
        如果命带孤辰或寡宿，八字又有华盖出现，则是一个非常聪明的孤独之人，往往具有特殊才华，很多艺术家、哲学家、五术家，或是修道者、牧师，多是这种命格。
        """


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
        self.explanation = f"""
        童子命的人婚姻不利，晚婚，或无婚恋，痴迷爱情的倒不多，
        因为根本就不会谈恋爱，一谈就吹，或者有人追、自己会谈也不行，一谈就出意外，
        即使硬撮合的也会因故而分手，多次离婚，更有概率一结婚或一破身就生病。
        犯童子煞的人一般时运不好事业受阻，容易遇到人格有问题的人，遭到嫉妒和排斥，自己有时已经很努力了，但是结果没有意义。
        前途一片光明有时自己找不到出路，就像被困在陷阱的动物渴望寻找到出路一样。尤其是婚姻感情方面不顺利，晚婚居多。
        """


class GuLuan(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "孤鸾煞"
        self.type = "弱凶神（不利婚姻）"
        self.explanation = f"""
        又名“呻吟煞”。夫妻多纷争。
        命犯孤鸾煞，主婚姻不顺。孤鸾犯日本无儿，一见官星得子奇，运遇旺乡名姐妹，临风惆怅绿楼时。
        男命：婚姻中不太懂的相处，和妻子不和睦，可能会出现外遇事件。
        女命：夫妻感情多一般，正缘来的晚，多为晚婚，注意健康问题。
        女命带孤鸾与子女缘分薄，若四柱中见官杀则不适用此条。孤鸾日生的女子不利姻缘，夫妻感情多波折，两人需要面对的问题较多。
        """


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
        一般带阴差阳错者可能有同母异父或同父异母的兄弟姐妹，在丧期中成婚、谈亲事时发生不愉快之事，妻子与父母相处的不太融洽，和妻舅感情疏远。做事阻碍较大，容易错失良机。
        """


class YinYangSha(DemigodExplain):
    def __init__(self, demigods, lord_gods):
        super().__init__(demigods, lord_gods)
        self.name = "阴阳煞"
        self.type = "凶神"
        self.explanation = """
        行事阴阳颠倒，多有事成反败之虞。好变不好，诸事多见在阴错阳差下，或完成、或结束。
        阴差阳错，是太过与不及、男女不和的意思。
        一般带阴差阳错者可能有同母异父或同父异母的兄弟姐妹，在丧期中成婚、谈亲事时发生不愉快之事，妻子与父母相处的不太融洽，和妻舅感情疏远。
        做事阻碍较大，容易错失良机。
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
