from collections import Counter

from ba_zi_elements import BaZiElements
from demigod_explain import DemigodExplain
from lord_gods import LordGods
from utils import *


class Demigod(BaZiElements):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.ri_zhi_n_nian_zhi = [self.nian_zhi, self.ri_zhi]
        self.ri_gan_n_nian_gan = [self.nian_gan, self.ri_gan]

        self.di_zhi_idx = self.get_di_zhi_idx(self.nian_zhi)
        self.di_zhi_order_backward = self.gou_jiao_sha_sequence((self.di_zhi_idx - 3))
        self.di_zhi_order_forward = self.gou_jiao_sha_sequence((self.di_zhi_idx + 3) % 12)

        self.nian_zhu_demigod = self.build_demigod(self.nian_gan, self.nian_zhi)
        self.yue_zhu_demigod = self.build_demigod(self.yue_gan, self.yue_zhi) + self.build_yue_zhu_demigod()
        self.ri_zhu_demigod = self.build_demigod(self.ri_gan, self.ri_zhi) + self.build_ri_zhu_demigod()
        self.shi_zhu_demigod = self.build_demigod(self.shi_gan, self.shi_zhi) + self.build_shi_zhu_demigod()
        self.all_demigod = self.nian_zhu_demigod + self.yue_zhu_demigod + self.ri_zhu_demigod + self.shi_zhu_demigod
        self.all_demigod_matrix = [
            self.nian_zhu_demigod, self.yue_zhu_demigod, self.ri_zhu_demigod, self.shi_zhu_demigod
        ]
        self.demigod_count = Counter(self.all_demigod)

        if self.explain_append:
            self.lord_gods = LordGods(**kwargs)
            self.demigod_explain = DemigodExplain(self, self.lord_gods)
            (
                self.nian_zhu_demigod_explain,
                self.yue_zhu_demigod_explain,
                self.ri_zhu_demigod_explain,
                self.shi_zhu_demigod_explain
            ) = self.demigod_explain.calc_all_demigod_explain(self, self.lord_gods)

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        ## 神煞：
        年柱：{",".join(self.nian_zhu_demigod)}
        月柱：{",".join(self.yue_zhu_demigod)}
        日柱：{",".join(self.ri_zhu_demigod)}
        时柱：{",".join(self.shi_zhu_demigod)}
        '''

        if self.explain_append and self.all_demigod:
            msg += f'''
        ### 神煞解析：
        年柱：
        {self.get_demigod_explain(self.nian_zhu_demigod_explain)}
        月柱：
        {self.get_demigod_explain(self.yue_zhu_demigod_explain)}
        日柱：
        {self.get_demigod_explain(self.ri_zhu_demigod_explain)}
        时柱：
        {self.get_demigod_explain(self.shi_zhu_demigod_explain)}
            '''

        return msg

    def get_demigod_explain(self, demigod_explain):
        if demigod_explain:
            str_explain = '\n'.join([item.explain() for item in demigod_explain if item.explain()])
            return f"{str_explain}\n" if str_explain else ""
        return ""

    def build_shi_zhu_demigod(self):
        result = []
        common_demigod = CommonDemigod(
            gan_zhi=self.shi_zhu,
            ba_zi=self.ba_zi,
            is_male=self.is_male
        )

        if common_demigod.hong_luan(self.nian_zhi, self.shi_zhi):
            result.append("红鸾")

        if self.jin_shen(self.shi_gan, self.shi_zhi):
            result.append("金神")

        if common_demigod.yuan_chen(self.is_male, self.nian_zhi, self.shi_zhi):
            result.append("元辰")

        if self.gu_chen(self.shi_zhi):
            result.append("孤辰")

        if self.gua_su(self.shi_zhi):
            result.append("寡宿")

        if self.tong_zi(self.shi_zhi):
            result.append("童子")

        return result

    def build_ri_zhu_demigod(self):
        result = []
        common_demigod = CommonDemigod(
            gan_zhi=self.ri_zhu,
            ba_zi=self.ba_zi,
            is_male=self.is_male
        )

        if self.kui_gang():
            result.append("魁罡贵人")

        if self.tong_zi(self.ri_zhi):
            result.append("童子")

        if self.jin_shen(self.ri_gan, self.ri_zhi):
            result.append("金神")

        if common_demigod.hong_luan(self.nian_zhi, self.ri_zhi):
            result.append("红鸾")

        if common_demigod.yuan_chen(self.is_male, self.nian_zhi, self.ri_zhi):
            result.append("元辰")

        if self.gu_chen(self.ri_zhi):
            result.append("孤辰")

        if self.gua_su(self.ri_zhi):
            result.append("寡宿")

        if self.shi_e_da_bai():
            result.append("十恶大败")

        if self.gu_luan_sha():
            result.append("孤鸾煞")

        if self.yin_yang_cha_cuo():
            result.append("阴阳差错")

        if self.si_fei():
            result.append("四废")

        if self.mu_yu():
            result.append("沐浴煞")

        return result

    def build_yue_zhu_demigod(self):
        result = []
        common_demigod = CommonDemigod(
            gan_zhi=self.shi_zhu,
            ba_zi=self.ba_zi,
            is_male=self.is_male
        )

        if common_demigod.hong_luan(self.nian_zhi, self.yue_zhi):
            result.append("红鸾")

        if common_demigod.yuan_chen(self.is_male, self.nian_zhi, self.yue_zhi):
            result.append("元辰")

        if self.gu_chen(self.yue_zhi):
            result.append("孤辰")

        if self.gua_su(self.yue_zhi):
            result.append("寡宿")

        return result

    def build_demigod(self, gan, zhi):
        result = []
        common_demigod = CommonDemigod(
            gan_zhi=gan + zhi,
            ba_zi=self.ba_zi,
            is_male=self.is_male
        )

        if common_demigod.tian_yi_gui_ren(self.ri_gan_n_nian_gan, zhi):
            result.append("天乙贵人")

        if common_demigod.tai_ji_gui_ren(self.ri_gan_n_nian_gan, zhi):
            result.append("太极贵人")

        if common_demigod.tian_de_gui_ren(self.yue_zhi, gan):
            result.append("天德贵人")

        if common_demigod.yue_de_gui_ren(self.yue_zhi, gan):
            result.append("月德贵人")

        if self.fu_xing(zhi):
            result.append("福星")

        if common_demigod.wen_chang(self.ri_gan_n_nian_gan, zhi):
            result.append("文昌贵人")

        if common_demigod.guo_yin(self.ri_gan_n_nian_gan, zhi):
            result.append("国印贵人")

        if self.xue_tang(gan, zhi):
            result.append("学堂")

        if self.ci_guan(gan, zhi):
            result.append("词馆")

        if self.de_xiu_gui_ren(gan, zhi):
            result.append("德秀贵人")

        if common_demigod.yi_ma(self.ri_zhi_n_nian_zhi, zhi):
            result.append("驿马")

        if common_demigod.hua_gai(self.ri_zhi_n_nian_zhi, zhi):
            result.append("华盖")

        if common_demigod.jiang_xing(self.ri_zhi_n_nian_zhi, zhi):
            result.append("将星")

        if common_demigod.jin_yu(self.ri_gan, zhi):
            result.append("金舆")

        if self.wang_shen(zhi):
            result.append("亡神")

        if self.tian_yi(zhi):
            result.append("天医")

        if common_demigod.lu_shen(self.ri_gan, zhi):
            result.append("禄神")

        if common_demigod.tian_xi(self.nian_zhi, zhi):
            result.append("天喜")

        if common_demigod.tian_luo(self.nian_gan, self.ri_zhi_n_nian_zhi, zhi):
            result.append("天罗")

        if common_demigod.di_wang(self.nian_gan, self.ri_zhi_n_nian_zhi, zhi):
            result.append("地网")

        if common_demigod.yang_ren(self.ri_gan, zhi):
            result.append("羊刃")

        if self.jie_sha(zhi):
            result.append("劫煞")

        if self.zai_sha(zhi):
            result.append("灾煞")

        if any(common_demigod.kong_wang(item, zhi) for item in [self.nian_zhu, self.ri_zhu]):
            result.append("空亡")

        # 勾绞煞
        # 阳男阴女, 命前三辰为勾, 命后三辰为绞.阴男阳女, 命前三辰为绞, 命后三辰为勾.
        # 查法: 以年支为主, 查四柱其余地支. 如庚午年生男, 命前三辰为酉为勾,命后三辰为卯为绞.
        if (self.is_male and di_zhi_yin_yang(self.nian_zhi) == "阳") or (
                not self.is_male and di_zhi_yin_yang(self.nian_zhi) == "阴"):
            if self.di_zhi_idx == self.di_zhi_order_backward:
                result.append("勾煞")
            elif self.di_zhi_idx == self.di_zhi_order_forward:
                result.append("绞煞")
        else:
            if self.di_zhi_idx == self.di_zhi_order_backward:
                result.append("绞煞")
            elif self.di_zhi_idx == self.di_zhi_order_forward:
                result.append("勾煞")

        if common_demigod.tao_hua(zhi, self.ri_zhi_n_nian_zhi):
            result.append("咸池（桃花）")

        if common_demigod.sang_men(zhi, self.ri_zhi_n_nian_zhi):
            result.append("丧门")

        if common_demigod.diao_ke(zhi, self.ri_zhi_n_nian_zhi):
            result.append("吊客")

        if common_demigod.pi_ma(zhi, self.ri_zhi_n_nian_zhi):
            result.append("披麻")

        return result

    def si_fei(self):
        """
        四废 春庚申, 辛酉, 夏壬子, 癸亥, 秋甲寅, 乙卯, 冬丙午, 丁巳. 查法: 凡四柱日干支生于该季为是.
        :return:
        """
        conditions = {
            "庚申": "寅卯辰",
            "辛酉": "寅卯辰",
            "壬子": "巳午未",
            "癸亥": "巳午未",
            "甲寅": "辰巳午",
            "乙卯": "辰巳午",
            "丙午": "未申酉",
            "丁巳": "未申酉"
        }
        return self.yue_zhi in conditions.get(self.ri_zhu, '')

    def yin_yang_cha_cuo(self):
        """
        阴阳差错 丙子, 丁丑, 戊寅, 辛卯, 壬辰, 癸巳, 丙午, 丁未,戊申, 辛酉, 壬戌, 癸亥. 查法: 日柱见者为是.
        :return:
        """
        conditions = [
            "丙子", "丁丑", "戊寅", "辛卯", "壬辰", "癸巳", "丙午", "丁未", "戊申", "辛酉", "壬戌", "癸亥"
        ]
        return self.ri_zhu in conditions

    def gu_luan_sha(self):
        """
        孤鸾煞 乙巳, 丁巳, 辛亥, 戊申, 壬寅, 戊午, 壬子, 丙午. 查法: 四柱日时同时出现以上任何两组者为是. 命犯孤鸾煞,
        :return:
        """
        conditions = ["乙巳", "丁巳", "辛亥", "戊申", "壬寅", "戊午", "壬子", "丙午"]
        return all(item in conditions for item in [self.ri_zhu, self.shi_zhu])

    def shi_e_da_bai(self):
        """
        十恶大败 甲 辰乙巳与壬申, 丙申丁亥及庚辰, 戊戌癸亥加辛巳, 己丑都来十位神. 查法: 四柱日干支逢之即是 六甲旬中有十个日值禄入空亡.
        :return:
        """
        conditions = [
            "甲辰",
            "乙巳",
            "壬申",
            "丙申",
            "丁亥",
            "庚辰",
            "戊戌",
            "癸亥",
            "辛巳",
            "己丑"
        ]

        return self.ri_zhu in conditions

    def gua_su(self, zhi):
        """
        亥子丑人, 见寅为孤, 见戌为寡.寅卯辰人, 见巳为孤, 见丑为寡.巳午未人, 见申为孤, 见辰为寡.申酉戌人, 见亥为孤,见未为寡.
        查法: 以年支为准, 四柱其它地支见者为是. 如巳年生人, 见申为孤辰, 见辰为寡宿.
        :param zhi:
        :return:
        """
        conditions = {
            "寅": ["亥", "子", "丑"],
            "戌": ["亥", "子", "丑"],
            "巳": ["寅", "卯", "辰"],
            "丑": ["寅", "卯", "辰"],
            "申": ["巳", "午", "未"],
            "辰": ["巳", "午", "未"],
            "亥": ["申", "酉", "戌"],
            "未": ["申", "酉", "戌"]
        }
        return self.nian_zhi in conditions.get(zhi, '')

    def gu_chen(self, zhi):
        """
        孤辰 亥子丑人, 见寅为孤, 见戌为寡.寅卯辰人, 见巳为孤, 见丑为寡.巳午未人, 见申为孤, 见辰为寡.申 酉戌人, 见亥为孤, 见未为寡.
        查法: 以年支为准, 四柱其它地支见者为是. 如巳年生人, 见申为孤辰, 见辰为寡宿.
        :param zhi:
        :return:
        """
        conditions = {
            "寅": ["亥", "子", "丑"],
            "巳": ["寅", "卯", "辰"],
            "申": ["巳", "午", "未"],
            "亥": ["申", "酉", "戌"]
        }
        return self.nian_zhi in conditions.get(zhi, '')

    def tian_she(self):
        """
        天赦 春戊寅, 夏甲午, 秋戊申, 冬甲子. 查法: 寅卯辰月生戊寅日, 巳午未月生甲午日, 申酉戌月生戊申日, 亥子丑月生甲子日.
        :return:
        """
        conditions = {
            ("戊", "寅"): "寅卯辰",
            ("甲", "午"): "巳午未",
            ("戊", "申"): "申酉戌",
            ("甲", "子"): "亥子丑"
        }

        return self.yue_zhi in conditions.get((self.ri_gan, self.ri_zhi), "")

    def jin_shen(self, gan, zhi):
        """
        金神 金神者, 乙丑, 己巳, 癸酉三组干支. 日柱或时柱见者为是.
        :param gan:
        :param zhi:
        :return:
        """
        conditions = [
            ("乙", "丑"),
            ("己", "巳"),
            ("癸", "酉"),
        ]
        return (gan, zhi) in conditions

    def gou_jiao_sha_sequence(self, di_zhi_idx):
        """
        排勾绞煞用顺序
        :param di_zhi_idx:
        :return:
        """
        di_zhi_length = len(DI_ZHI)
        if di_zhi_idx < 1:
            di_zhi_idx = di_zhi_length + di_zhi_idx - 1
        if di_zhi_idx > di_zhi_length:
            di_zhi_idx = di_zhi_idx % di_zhi_length
        return di_zhi_idx

    def get_di_zhi_idx(self, zhi):
        """
        返回地支的索引
        :param zhi:
        :return:
        """
        for i in range(1, 13):
            if zhi == DI_ZHI[i]:
                return i
        return 0

    def zai_sha(self, zhi):
        """
        灾煞 申子辰见午, 亥卯未见酉, 寅午戌见子, 巳酉丑见卯. 查法: 以年支为主, 四柱地支中见之者为是.
        :param zhi:
        :return:
        """
        conditions = {
            "午": ["申", "子", "辰"],
            "酉": ["亥", "卯", "未"],
            "子": ["寅", "午", "戌"],
            "卯": ["巳", "酉", "丑"]
        }

        return any(item in conditions.get(zhi, '') for item in self.ri_zhi_n_nian_zhi)

    def jie_sha(self, zhi):
        """
        劫煞 申子辰见巳, 亥卯未见申, 寅午戌见亥, 巳酉丑见寅. 查法: 以年柱或日柱为主, 四柱地支见之者为是.
        :param zhi:
        :return:
        """
        conditions = {
            "巳": ["申", "子", "辰"],
            "申": ["亥", "卯", "未"],
            "亥": ["寅", "午", "戌"],
            "寅": ["巳", "酉", "丑"]
        }

        return any(item in conditions.get(zhi, '') for item in self.ri_zhi_n_nian_zhi)

    def tian_yi(self, zhi):
        """
        # 天医 正月生见丑, 二月生见寅, 三月生见卯, 四月生见辰,五月生见巳, 六月生见午, 七月生见未, 八月生见申,九月生见酉, 十月生见戌,
        # 十一月生见亥, 十二月生见子. 查法: 以月支查其它地支, 见者为是.
        :param zhi:
        :return:
        """
        conditions = {
            "寅": "丑",
            "卯": "寅",
            "辰": "卯",
            "巳": "辰",
            "午": "巳",
            "未": "午",
            "申": "未",
            "酉": "申",
            "戌": "酉",
            "亥": "戌",
            "子": "亥",
            "丑": "子"
        }

        return zhi == conditions.get(self.yue_zhi)

    def wang_shen(self, zhi):
        """
        寅午戌干见巳，亥卯未干见寅，巳酉丑干见申，申子辰干见亥。
        申子辰合水局，亥卯未合木局，寅午戌合火局，巳酉丑合金局
        :param zhi:
        :return:
        """
        conditions = {
            "巳": "寅午戌",
            "寅": "亥卯未",
            "申": "巳酉丑",
            "亥": "申子辰"
        }

        is_wang_shen = any(item in conditions.get(zhi, '') for item in self.ri_zhi_n_nian_zhi)

        return any(item in conditions.get(zhi, '') for item in self.ri_zhi_n_nian_zhi)

    def de_xiu_gui_ren(self, gan, zhi):
        """
        德秀: 寅午戌月，丙丁为德，戊癸为秀。申子辰月，壬癸戊己为德，丙辛甲己为秀。巳酉丑月，庚辛为德，乙庚为秀。亥卯未月，甲乙为德，丁壬为秀。
        :param gan:
        :param zhi:
        :return:
        """
        conditions = {
            "寅午戌": ("丙丁", "戊癸"),
            "申子辰": ("壬癸戊己", "丙辛甲己"),
            "巳酉丑": ("庚辛", "乙庚"),
            "亥卯未": ("甲乙", "丁壬")
        }

        for key, value in conditions.items():
            if self.yue_zhi in key and (gan in value[0] or zhi in value[0]) and zhi in value[1]:
                return True

        return False

    def tong_zi(self, zhi):
        yue_conditions = [
            ("寅卯辰申酉戌", "寅子"),
            ("巳午未亥子丑", "卯未"),
        ]

        nian_conditions = [
            ("甲乙庚辛", "午卯"),
            ("戊己", "辰巳"),
            ("丙丁壬癸", "酉戌")
        ]

        for condition in yue_conditions:
            if zhi in condition[1] and self.yue_zhi in condition[0]:
                return True

        for condition in nian_conditions:
            if zhi in condition[1] and self.nian_gan in condition[0]:
                return True

        return False

    def ci_guan(self, gan, zhi):
        """
         词馆:甲干见庚寅, 乙干见辛卯, 丙干见乙巳, 丁干见戊午, 戊干见丁巳, 己干见庚午, 庚干见壬申,辛干见癸酉, 壬干见癸亥, 癸干见壬戌.
         学堂词馆查法, 均以年干或日干为主, 柱中地支临之为是. 学堂词馆其纳音五行, 必与年干日干五行 相一致.
        :param gan:
        :param zhi:
        :return:
        """
        conditions = {
            "甲": "庚寅",
            "乙": "辛卯",
            "丙": "乙巳",
            "丁": "戊午",
            "戊": "丁巳",
            "己": "庚午",
            "庚": "壬申",
            "辛": "癸酉",
            "壬": "癸亥",
            "癸": "壬戌"
        }

        return any(any(item in conditions.get(index_gan, '') for item in [gan, zhi])
                   for index_gan in self.ri_gan_n_nian_gan)

    def xue_tang(self, gan, zhi):
        """
        学堂
        金命见巳, 辛巳为正; 木命见亥, 己亥为正; 水命见申, 甲申为正; 土命见申, 戊申为正; 火 命见寅, 丙寅为正.
        年干/日干为亥，干为甲乙，支为己，为学堂。年干/日干为寅，干为丙丁，支为丙，为学堂。年干/日干为申，干为戊己，支为戊，为学堂。年干/日干为巳，干为庚辛，支为辛，为学堂。年干/日干为申，干为壬癸，支为甲，为学堂。
        :param gan:
        :param zhi:
        :return:
        """
        ganzhi = gan + zhi
        conditions = [
            ("甲乙", "己", "亥"),
            ("丙丁", "丙", "寅"),
            ("戊己", "戊", "申"),
            ("庚辛", "辛", "巳"),
            ("壬癸", "甲", "申"),
        ]

        for item in conditions:
            if zhi in item[0] and item[1] in ganzhi and any(item == item[2] for item in self.ri_gan_n_nian_gan):
                return True
        return False

    def kui_gang(self):
        """
        魁罡贵人 壬辰庚戌与庚辰, 戊戌魁罡四座神,不见财官刑煞并,身行旺地贵无伦. 查法: 日柱见者为是
        :return:
        """
        conditions = [
            ("壬", "辰"),
            ("庚", "戌"),
            ("庚", "辰"),
            ("戊", "戌")
        ]

        return (self.ri_gan, self.ri_zhi) in conditions

    def fu_xing(self, zhi):
        """
        福星 以年干或日干为主。凡甲丙两干见寅或子，乙癸两干见卯或丑，戊干见申，己干见未，丁干见亥，庚干见午，辛干见巳，壬干见辰是也
        :param zhi:
        :return:
        """
        conditions = {
            "甲丙": "寅子",
            "乙癸": "卯丑",
            "戊": "申",
            "己": "未",
            "丁": "亥",
            "庚": "午",
            "辛": "巳",
            "壬": "辰"
        }

        for key, value in conditions.items():
            if any(item in key for item in self.ri_gan_n_nian_gan) and zhi in value:
                return True

        return False

    def mu_yu(self):

        """
        只要是甲日逢地支子、乙日逢地支巳、丙日逢地支卯、丁日逢地支申、戊日逢地支卯、己日逢地支申、庚日逢地支午、辛日逢地支亥、壬日逢地支酉、癸日逢地支寅，那么皆为命带八字沐浴。
        :return:
        """
        conditions = [
            "甲子",
            "乙巳",
            "丙卯",
            "丁申",
            "戊卯",
            "己申",
            "庚午",
            "辛亥",
            "壬酉",
            "癸寅",
        ]
        return self.ri_zhu in conditions


class CommonDemigod:
    """
    通用神
    """

    def __init__(self, **kwargs):
        self.gan_zhi = kwargs.get("gan_zhi", '')
        self.ba_zi = kwargs.get("ba_zi", '')
        self.is_male = kwargs.get("is_male", True)
        (self.gan, self.zhi) = self.gan_zhi

        (self.nian_zhu,
         self.yue_zhu,
         self.ri_zhu,
         self.shi_zhu) = self.ba_zi.split(',')

        (
            self.nian_gan,
            self.nian_zhi
        ) = list(self.nian_zhu)
        (
            self.yue_gan,
            self.yue_zhi
        ) = list(self.yue_zhu)
        (
            self.ri_gan,
            self.ri_zhi
        ) = list(self.ri_zhu)
        (
            self.shi_gan,
            self.shi_zhi
        ) = list(self.shi_zhu)

        self.ri_zhi_n_nian_zhi = [self.nian_zhi, self.ri_zhi]
        self.ri_gan_n_nian_gan = [self.nian_gan, self.ri_gan]

    def build_demigods(self):
        result = []

        if self.tian_yi_gui_ren(self.ri_gan_n_nian_gan, self.zhi):
            result.append("天乙贵人")

        if self.tai_ji_gui_ren(self.ri_gan_n_nian_gan, self.zhi):
            result.append("太极贵人")

        if self.tian_de_gui_ren(self.yue_zhi, self.gan):
            result.append("天德贵人")

        if self.yue_de_gui_ren(self.yue_zhi, self.gan):
            result.append("月德贵人")

        if self.wen_chang(self.ri_gan_n_nian_gan, self.zhi):
            result.append("文昌贵人")

        if self.guo_yin(self.ri_gan_n_nian_gan, self.zhi):
            result.append("国印贵人")

        if self.yi_ma(self.ri_zhi_n_nian_zhi, self.zhi):
            result.append("驿马")

        if self.hua_gai(self.ri_zhi_n_nian_zhi, self.zhi):
            result.append("华盖")

        if self.jiang_xing(self.ri_zhi_n_nian_zhi, self.zhi):
            result.append("将星")

        if self.jin_yu(self.ri_gan, self.zhi):
            result.append("金舆")

        if self.lu_shen(self.ri_gan, self.zhi):
            result.append("禄神")

        if self.hong_luan(self.nian_zhi, self.zhi):
            result.append("红鸾")

        if self.tian_xi(self.nian_zhi, self.zhi):
            result.append("天喜")

        if self.tian_luo(self.gan, self.ri_zhi_n_nian_zhi, self.zhi):
            result.append("天罗")

        if self.di_wang(self.gan, self.ri_zhi_n_nian_zhi, self.zhi):
            result.append("地网")

        if self.yang_ren(self.gan, self.zhi):
            result.append("羊刃")

        if self.kong_wang(self.gan_zhi, self.zhi):
            result.append("空亡")

        if self.tao_hua(self.zhi, self.ri_zhi_n_nian_zhi):
            result.append("咸池（桃花）")

        if self.yuan_chen(self.is_male, self.nian_zhi, self.zhi):
            result.append("元辰")

        if self.sang_men(self.zhi, self.ri_zhi_n_nian_zhi):
            result.append("丧门")

        if self.diao_ke(self.zhi, self.ri_zhi_n_nian_zhi):
            result.append("吊客")

        if self.pi_ma(self.zhi, self.ri_zhi_n_nian_zhi):
            result.append("披麻")

        if self.hong_yan(self.zhi):
            result.append("红艳")

        return result

    def pi_ma(self, zhi, idx_zhi_list):
        """
        披麻查法：年日支后三位为披麻。
        :param zhi:
        :param idx_zhi_list:
        :return:
        """
        return any(ZHI.index(zhi) == ZHI.index(item) + 3 for item in idx_zhi_list)

    def diao_ke(self, zhi, idx_zhi_list):
        """
        吊客查法：年日支后两位为吊客。
        :param zhi:
        :param idx_zhi_list:
        :return:
        """
        return any(ZHI.index(zhi) == ZHI.index(item) + 2 for item in idx_zhi_list)

    def sang_men(self, zhi, idx_zhi_list):
        """
        丧门查法：年日支前两位为丧门。
        :param zhi:
        :return:
        """
        return any(ZHI.index(zhi) == ZHI.index(item) - 2 for item in idx_zhi_list)

    def yuan_chen(self, is_male, nian_zhi, zhi):
        """
        阳男阴女，其元辰是：
        子年见未，丑年见申，寅年见酉，卯年见戌，辰年见亥，巳年见子，
        午年见丑，未年见寅，申年见卯，酉年见辰，戌年见巳，亥年见午。
        阴男阳女，其元辰是：
        子年见巳，丑年见午，寅年见未，卯年见申，辰年见酉，巳年见戌，
        午年见亥，未年见子，申年见丑，酉年见寅，戌年见卯，亥年见辰。
        :param nian_zhi:
        :param is_male: 性别
        :param zhi:
        :return:
        """
        yang_nan_yin_nv_conditions = {
            "子": "未",
            "丑": "申",
            "寅": "酉",
            "卯": "戌",
            "辰": "亥",
            "巳": "子",
            "午": "丑",
            "未": "寅",
            "申": "卯",
            "酉": "辰",
            "戌": "巳",
            "亥": "午"
        }

        yin_nan_yang_nv_conditions = {
            "子": "巳",
            "丑": "午",
            "寅": "未",
            "卯": "申",
            "辰": "酉",
            "巳": "戌",
            "午": "亥",
            "未": "子",
            "申": "丑",
            "酉": "寅",
            "戌": "卯",
            "亥": "辰",
        }

        if (is_male and di_zhi_yin_yang(nian_zhi) == "阳") or (
                not is_male and di_zhi_yin_yang(nian_zhi) == "阴"):
            return zhi == yang_nan_yin_nv_conditions.get(nian_zhi, '')
        else:
            return zhi == yin_nan_yang_nv_conditions.get(nian_zhi, '')

    def tao_hua(self, zhi, idx_zhi_list):
        """
        咸池 挑花 申 子辰在酉, 寅午戌在卯, 巳酉丑在午, 亥卯未在子. 查法: 以年支或日支查四柱其它地支, 见者为 是.
        :param zhi:
        :return:
        """
        conditions = {
            "酉": ("申", "子", "辰"),
            "卯": ("寅", "午", "戌"),
            "午": ("巳", "酉", "丑"),
            "子": ("亥", "卯", "未")
        }

        return any(item in conditions.get(zhi, '') for item in idx_zhi_list)

    def kong_wang(self, jia_zi_name, zhi):
        """
        空亡 甲子 甲戌 甲申 甲午 甲辰 甲寅 乙丑 乙亥 乙酉 乙未 乙巳 乙卯 丙寅 丙子 丙戌 丙申 丙午 丙辰 丁卯 丁丑 丁亥 丁酉 丁未
        丁巳 戊辰 戊寅 戊子 戊戌 戊申 戊午 己巳 己卯 己丑 己亥 己酉 己未 庚午 庚辰 庚寅 庚子 庚戌 庚申 辛未 辛巳 辛卯 辛丑 辛亥
        辛酉 壬申 壬午 壬辰 壬寅 壬子 壬戌 癸酉 癸未 癸巳 癸卯 癸丑 癸亥 戌亥 申酉 午未 辰巳 寅卯 子丑 查 法: 以日柱为主, 柱中年、
        月、 时支见者为空亡.
        :param jia_zi_name:
        :param zhi:
        :return:
        """
        if JIA_ZI_NAME.index(jia_zi_name) <= JIA_ZI_NAME.index('癸酉'):
            if zhi in ["戌亥"]:
                return True
        elif JIA_ZI_NAME.index(jia_zi_name) <= JIA_ZI_NAME.index('癸未'):
            if zhi in ["申酉"]:
                return True
        elif JIA_ZI_NAME.index(jia_zi_name) <= JIA_ZI_NAME.index('癸巳'):
            if zhi in ["午未"]:
                return True
        elif JIA_ZI_NAME.index(jia_zi_name) <= JIA_ZI_NAME.index('癸卯'):
            if zhi in ["辰巳"]:
                return True
        elif JIA_ZI_NAME.index(jia_zi_name) <= JIA_ZI_NAME.index('癸丑'):
            if zhi in ["寅卯"]:
                return True
        elif JIA_ZI_NAME.index(jia_zi_name) <= JIA_ZI_NAME.index('癸亥'):
            if zhi in ["子丑"]:
                return True

        return False

    def yang_ren(self, ri_gan, zhi):
        """
        羊刃 甲羊刃在卯, 乙羊刃在寅, 丙戊羊刃在午, 丁己羊刃在巳,庚羊刃在酉, 辛羊刃在申, 壬羊刃在子, 癸 羊刃在亥.查法: 以日干为主,
        四支见之者为是.
        :param ri_gan:
        :param zhi:
        :return:
        """
        conditions = {
            "甲": "卯",
            "乙": "寅",
            "丁": "巳",
            "己": "巳",
            "丙": "午",
            "戊": "午",
            "庚": "酉",
            "辛": "申",
            "壬": "子",
            "癸": "亥"
        }

        return zhi == conditions.get(ri_gan)

    def di_wang(self, nian_gan, idx_zhi_list, zhi):
        """
        地网 辰为天罗, 戌为地网. 火命人逢戌亥为天罗, 水土命逢辰巳为地网. 辰见巳, 巳见辰为地网; 戌见亥, 亥见戌为天罗. 男忌天罗,
        女忌地网.查法: 以年支或日支为主, 其它地支见 之者为是.
        :param idx_zhi_list:
        :param nian_gan:
        :param zhi:
        :return:
        """
        if nian_gan not in "壬癸":
            return False

        return (zhi == "辰" and any(item == "巳" for item in idx_zhi_list)) or (
                zhi == "巳" and any(item == "辰" for item in idx_zhi_list))

    def tian_luo(self, nian_gan, idx_zhi_list, zhi):
        """
        天罗 辰为天罗, 戌为地网. 火命人逢戌亥为天罗, 水土命逢辰巳为地网. 辰见巳, 巳见辰为地网; 戌见亥, 亥见戌为天罗. 男忌天罗,
        女忌地网.查法: 以年支或日支为主, 其它地支见 之者为是.
        :param idx_zhi_list:
        :param nian_gan:
        :param zhi:
        :return:
        """
        if nian_gan not in "丙丁":
            return False

        return (zhi == "亥" and any(item == "戌" for item in idx_zhi_list)) or (
                zhi == "戌" and any(item == "亥" for item in idx_zhi_list))

    def tian_xi(self, nian_zhi, zhi):
        """
        天喜 天喜查法：以年支查: 子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥 其他地支见: 酉 申 未 午 巳 辰 卯 寅 丑 子 亥 戌
        :param nian_zhi:
        :param zhi:
        :return:
        """
        conditions = {
            "子": "酉",
            "丑": "申",
            "寅": "未",
            "卯": "午",
            "辰": "巳",
            "巳": "辰",
            "午": "卯",
            "未": "寅",
            "申": "丑",
            "酉": "子",
            "戌": "亥",
            "亥": "戌"
        }

        return zhi == conditions.get(nian_zhi)

    def hong_luan(self, nian_zhi, zhi):
        """
        红鸾 红鸾查法：以年支查: 子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥 其他地支见: 卯 寅 丑 子 亥 戌 酉 申 未 午 巳 辰
        :return:
        """
        conditions = {
            "子": "卯",
            "丑": "寅",
            "寅": "丑",
            "卯": "子",
            "辰": "亥",
            "巳": "戌",
            "午": "酉",
            "未": "申",
            "申": "未",
            "酉": "午",
            "戌": "巳",
            "亥": "辰",
        }
        return zhi == conditions.get(nian_zhi, '')

    def lu_shen(self, ri_gan, zhi):
        """
        禄神 甲禄在寅, 乙禄在卯, 丙戊禄在巳, 丁己禄在午,庚禄在申, 辛禄在酉, 壬禄在亥, 癸禄在子. 查法: 以日干查四支, 见之者为是.
        :param ri_gan:
        :param zhi:
        :return:
        """
        conditions = {
            "甲": "寅",
            "乙": "卯",
            "丁": "午",
            "己": "午",
            "丙": "巳",
            "戊": "巳",
            "庚": "申",
            "辛": "酉",
            "壬": "亥",
            "癸": "子"
        }

        return zhi == conditions.get(ri_gan)

    def jin_yu(self, ri_gan, zhi):
        """
        金舆 甲龙乙蛇丙戊羊, 丁己猴歌庚犬方,辛猪壬牛癸逢虎, 凡人遇此福气昌.
        :param ri_gan:
        :param zhi:
        :return:
        """
        conditions = {
            "甲": "辰",
            "乙": "巳",
            "丁": "申",
            "己": "申",
            "丙": "未",
            "戊": "未",
            "庚": "戌",
            "辛": "亥",
            "壬": "丑",
            "癸": "寅"
        }

        return zhi == conditions.get(ri_gan)

    def jiang_xing(self, idx_zhi_list, zhi):
        """
        将星 寅午戌见午, 巳酉丑见酉, 申子辰见子, 辛卯未见卯. 查法: 以年支或日支查其余各支, 见者为将星.
        :param idx_zhi_list:
        :param zhi:
        :return:
        """
        conditions = {
            "子": "申子辰",
            "午": "寅午戌",
            "酉": "巳酉丑",
            "卯": "亥卯未",
        }

        return any(item in conditions.get(zhi, '') for item in idx_zhi_list)

    def hua_gai(self, idx_zhi_list, zhi):
        """
        华盖 寅午戌见戌, 亥卯未见未,申子辰见辰, 巳酉丑见丑. 以年支或日支不主, 凡四柱中所见者为有华盖星.
        :param idx_zhi_list:
        :param zhi:
        :return:
        """

        conditions = {
            "辰": ["申", "子", "辰"],
            "戌": ["寅", "午", "戌"],
            "丑": ["巳", "酉", "丑"],
            "未": ["亥", "卯", "未"],
        }

        return any(item in conditions.get(zhi, '') for item in idx_zhi_list)

    def yi_ma(self, idx_zhi_list, zhi):
        """
        驿马 申子辰马在寅, 寅午戌马在申,巳酉丑马在亥, 亥卯未马在巳.
        :param idx_zhi_list:
        :param zhi:
        :return:
        """
        conditions = {
            "寅": "申子辰",
            "申": "寅午戌",
            "亥": "巳酉丑",
            "巳": "亥卯未",
        }

        return any(item in conditions.get(zhi, '') for item in idx_zhi_list)

    def guo_yin(self, idx_gan_list, zhi):
        """
        国印贵人 甲见戌, 乙见亥, 丙见丑, 丁见寅,戊见丑, 己见寅, 庚见辰, 辛见巳.壬见未, 癸见申
        :param idx_gan_list:
        :param zhi:
        :return:
        """
        conditions = {
            "甲": "戌",
            "乙": "亥",
            "丙": "丑",
            "丁": "寅",
            "戊": "丑",
            "己": "寅",
            "庚": "辰",
            "辛": "巳",
            "壬": "未",
            "癸": "申"
        }

        return any(conditions.get(item, '') == zhi for item in idx_gan_list)

    def wen_chang(self, idx_gan_list, zhi):
        """
        文昌贵人: 甲乙巳午报君知, 丙戊申宫丁己鸡.庚猪辛鼠壬逢虎,癸人见卯入云梯. 查法: 以年干或日干为主, 凡四柱中地支所见者为是
        :param idx_gan_list:
        :param zhi:
        :return:
        """
        conditions = {
            "巳": "甲",
            "午": "乙",
            "申": "丙戊",
            "酉": "丁己",
            "亥": "庚",
            "子": "辛",
            "寅": "壬",
            "卯": "癸",
        }

        return any(item in conditions.get(zhi, '') for item in idx_gan_list)

    def yue_de_gui_ren(self, yue_zhi, gan):
        """
        月德贵人 寅午戌月生者见丙, 申子辰月生者见壬,亥卯未月生者见甲,巳酉丑月生者见庚. 凡柱中年月日时干上见者为有月德贵人.
        :param gan: 年月日时干
        :return:
        """
        conditions = {
            "丙": ["寅", "午", "戌"],
            "壬": ["申", "子", "辰"],
            "甲": ["亥", "卯", "未"],
            "庚": ["巳", "酉", "丑"]
        }

        return yue_zhi in conditions.get(gan, '')

    def tian_de_gui_ren(self, yue_zhi, gan):
        """
        天德贵人 正月生者见丁, 二月生者见申,三月生者见壬, 四月生者见辛,五月生者见亥, 六月生者见甲,七月生者 见癸, 八月生者见寅,九月生者见丙,
        十月生者见乙,十一月生者见巳, 十二月生者见庚. 凡四柱年月日时上见者为有天德贵人.
        :param yue_zhi:
        :param gan:
        :return:
        """
        conditions = {
            "寅": "丁",
            "卯": "申",
            "辰": "壬",
            "巳": "辛",
            "午": "亥",
            "未": "甲",
            "申": "癸",
            "酉": "寅",
            "戌": "丙",
            "亥": "乙",
            "子": "巳",
            "丑": "庚"
        }

        return gan == conditions.get(yue_zhi, '')

    def tai_ji_gui_ren(self, idx_gan_list, zhi):
        """
        太极贵人 甲乙生人子午中, 丙丁鸡兔定亨通,戊己两干临四季(地支为土),庚辛寅亥禄丰隆,壬癸巳申偏喜美, 值此应当福气 钟,更须贵格来相扶,候封万户到三公.
        :param idx_gan_list:
        :param zhi:
        :return:
        """
        conditions = {
            "甲": "子午",
            "乙": "子午",
            "丙": "酉卯",
            "丁": "酉卯",
            "戊": "丑辰未戌",
            "己": "丑辰未戌",
            "庚": "寅亥",
            "辛": "寅亥",
            "壬": "巳申",
            "癸": "巳申",
        }
        return any(zhi in conditions.get(item, '') for item in idx_gan_list)

    def tian_yi_gui_ren(self, idx_gan_list, zhi):
        """
        天乙贵人 以日干起贵人，地支见者为是
        甲戊并牛羊, 乙己鼠猴乡, 丙丁猪鸡位, 壬癸兔蛇藏, 庚辛逢虎马, 此是贵人方. 查 法: 以日干起贵人, 地支见者为是
        :param idx_gan_list:
        :param zhi:
        :return:
        """
        conditions = {
            "甲": "丑未", "戊": "丑未",
            "乙": "子申", "己": "子申",
            "丙": "亥酉", "丁": "亥酉",
            "壬": "卯巳", "癸": "卯巳",
            "庚": "辛寅", "午": "辛寅",
        }

        return any(zhi in conditions.get(item, '') for item in idx_gan_list)

    def hong_yan(self, zhi):
        """
        此以日为主，年为副，见四柱之支，即甲乙午、丙寅、丁未、戊己辰、庚戌、辛酉、壬子、癸甲，皆为红艳煞。
        :param gan:
        :param all_zhi:
        :return:
        """
        conditions = {
            '午': "甲乙",
            '寅': "丙",
            '未': "丁",
            '辰': "戊己",
            '戌': "庚",
            '酉': "辛",
            '子': "壬",
        }

        return any(item in conditions.get(zhi, '') for item in self.ri_gan_n_nian_gan)