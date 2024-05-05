import argparse

from marriage_gods import MarriageGods
from metainfo import MetaInfo
from utils import *


class Intermarriage:
    def __init__(self, **kwargs):
        self.man_birthday = kwargs.get('man_birthday', constants.BASE_DATE)
        self.man_demigod = MarriageGods(
            birthday=self.man_birthday,
            is_male=True
        )

        self.woman_birthday = kwargs.get('woman_birthday', constants.BASE_DATE)
        self.woman_demigod = MarriageGods(
            birthday=self.woman_birthday,
            is_male=False
        )
        self.explain_append = kwargs.get('explain_append', False)

        self.marry_date = kwargs.get('marry_date', constants.BASE_DATE)
        self.ru_zhui = kwargs.get('ru_zhui', False)

        self.lv_cai_he_hun = self.build_lv_cai_he_hun()
        self.pursue = self.calc_pursue_relationship()
        self.relationships = self.calc_relationship()
        self.marry_date_comment = self.check_marry_date()

        if self.explain_append:
            self.lv_cai_he_hun_explain = self.calc_lv_cai_he_hun_explain()

    def __str__(self):
        if any(item == constants.BASE_DATE for item in [self.man_birthday, self.woman_birthday]):
            return ""

        result = f'''
        ## 合婚：
        男方：{self.man_demigod}
        女方：{self.woman_demigod}
        追求关系：{self.pursue}
        '''

        result += f'''
        呂才合婚：{self.lv_cai_he_hun}
        '''

        if self.explain_append:
            result += f'{self.lv_cai_he_hun_explain}'

        relationship_str = "\n        ".join(self.relationships) if self.relationships else ""
        if relationship_str:
            result += f'''
        {relationship_str}
        '''

        if self.marry_date_comment:
            result += f'''
        {self.marry_date_comment}
            '''

        return result

    def build_lv_cai_he_hun(self):
        man_idx = int(get_gong_gua_for_gan_zhi(self.man_demigod.nian_zhu, True))
        woman_idx = int(get_gong_gua_for_gan_zhi(self.woman_demigod.nian_zhu, False))

        if not (man_idx and woman_idx):
            return '未知'

        # 数组从0开始，而我们计算从1开始，所以需要减1
        # 注意数组没有第5行和第5列，如果大于等于5，需要再减1
        man_idx = man_idx - 2 if man_idx >= 6 else man_idx - 1
        woman_idx = woman_idx - 2 if woman_idx >= 6 else woman_idx - 1

        # 根据表格取结果，返回配婚结果
        return GONG_GUA[man_idx][woman_idx]  # 顺序一样

    def calc_pursue_relationship(self):
        """
        感情里谁克谁代表谁对谁满意 谁去追求谁
        :return:
        """
        male_primary_element = self.man_demigod.primary_element
        female_primary_element = self.woman_demigod.primary_element

        if ELEMENTS_OPPOSING[female_primary_element] == male_primary_element:
            return '女方追男方'
        elif ELEMENTS_SUPPORTING[male_primary_element] == female_primary_element:
            return '女方追男方'
        return '男方追女方'

    def calc_relationship(self):
        """
        天干合代表彼此投缘 合化 投缘 合得来
        半合 拱合 拱会 有一段时间感情很好 其他时候缘分不深
        三合 中神在谁坐下 感情结果谁主导 或者谁说了算
        冲 代表性格有差异 不投缘 容易分手
        刑 吵架多 但是能快速和好
        害（穿） 互相伤害 互相折磨 自己受伤比较深 容易分开
        破 见面困难 或者对方该他做的事做不到
        :return:
        """

        male_ri_gan = self.man_demigod.ri_gan
        male_ri_zhi = self.man_demigod.ri_zhi
        female_ri_gan = self.woman_demigod.ri_gan
        female_ri_zhi = self.woman_demigod.ri_zhi

        result = []

        # 天干相同
        if male_ri_gan == female_ri_gan:
            result.append('吵吵闹闹欢喜冤家')

        # 天干和合
        for pair in TIAN_GAN_HE:
            gan, element = pair
            if male_ri_gan in gan and female_ri_gan in gan:
                msg = '双方很合得来' + self.check_support_gander(element)
                result.append(msg)
                break

        # 天干冲
        for pair in TIAN_GAN_CHONG:
            if male_ri_gan in pair and female_ri_gan in pair:
                result.append('性格有差异，不投缘，容易分手')
                break

        # 地支拱会
        for pair in DI_ZHI_GONG_HUI:
            zhi, element = pair
            if male_ri_zhi in zhi and female_ri_zhi in zhi:
                msg = '有一段时间感情很好，其他时候缘分不深' + self.check_support_gander(element)
                result.append(msg)
                break

        # 地支拱合
        for pair in DI_ZHI_GONG_HE:
            zhi, element = pair
            if male_ri_zhi in zhi and female_ri_zhi in zhi:
                msg = '有一段时间感情很好，其他时候缘分不深' + self.check_support_gander(element)
                result.append(msg)
                break

        # 三合
        for pair in DI_ZHI_SAN_HE:
            zhi, element = pair
            if male_ri_zhi in zhi and female_ri_zhi in zhi:
                middle_god = zhi[1]
                msg = "三合局，感情结果由中神主导"
                if male_ri_zhi == middle_god:
                    msg += '中神在男方坐下，关系由男方主导'
                elif female_ri_zhi == middle_god:
                    msg += '中神在女方坐下，关系由女方主导'
                else:
                    continue
                result.append(msg)

        # 地支冲
        for pair in DI_ZHI_CHONG:
            if male_ri_zhi in pair and female_ri_zhi in pair:
                result.append('性格有差异，不投缘，容易分手')
                break

        # 地支害
        for pair in DI_ZHI_HAI:
            if male_ri_zhi in pair and female_ri_zhi in pair:
                result.append('互相伤害，互相折磨，容易分开')
                break

        # 地支刑
        for pair in DI_ZHI_XING:
            if male_ri_zhi in pair and female_ri_zhi in pair:
                result.append('吵架多，但是能快速和好')
                break

        return result

    def check_support_gander(self, element):
        msg = ""
        man_element_positive = self.man_demigod.elements_relationships_mapping[element][1]
        woman_element_positive = self.woman_demigod.elements_relationships_mapping[element][1]
        if man_element_positive > woman_element_positive:
            msg += '，这段关系由男方主导。'
        elif man_element_positive < woman_element_positive:
            msg += '，这段关系由女方主导。'
        else:
            msg += '，这段关系里双方平等。'
        return msg

    def calc_lv_cai_he_hun_explain(self):
        '''
        延年婚主長壽有福，男女和諧，積德積慶，終生安康，上吉之配。

        生氣婚主多子多福，兒孫滿堂，子孝孫賢，有福有祿，上吉之配。

        天醫婚主無災無病，一生平安，兒女和睦，無奸無盜，上吉之配。

        六煞婚主化險為夷，夫妻和順，雖富不達，豐衣足食。尋常之配。

        禍害婚主遇難可解，逢凶化吉，坎坷勞碌，可保小康，尋常之配。

        伏位婚主一生平淡，有子有女，團圓和氣，無驚無險，尋常之配。

        五鬼婚主口舌是非，生活不寧，鄰裏不和，時有官司，次凶之配。

        絕命婚主平生坎坷，生世艱辛，東離西走，家遭凶禍，大凶之配。
        :return:
        '''
        result = "男女依據宅命兩相配合，上應天星，分為八類婚姻，即延年、生氣、天醫、伏位、六煞、五鬼、禍害、絕命。\n"
        conditions = {
            "延年": "長壽有福，男女和諧，積德積慶，終生安康，上吉之配。",
            "生氣": "多子多福，兒孫滿堂，子孝孫賢，有福有祿，上吉之配。",
            "天醫": "無災無病，一生平安，兒女和睦，無奸無盜，上吉之配。",
            "六煞": "化險為夷，夫妻和順，雖富不達，豐衣足食。尋常之配。",
            "禍害": "遇難可解，逢凶化吉，坎坷勞碌，可保小康，尋常之配。",
            "伏位": "一生平淡，有子有女，團圓和氣，無驚無險，尋常之配。",
            "五鬼": "口舌是非，生活不寧，鄰裏不和，時有官司，次凶之配。",
            "絕命": "平生坎坷，生世艱辛，東離西走，家遭凶禍，大凶之配。",

            "生气": "多子多福，兒孫滿堂，子孝孫賢，有福有祿，上吉之配。",
            "天医": "無災無病，一生平安，兒女和睦，無奸無盜，上吉之配。",
            "祸害": "遇難可解，逢凶化吉，坎坷勞碌，可保小康，尋常之配。",
            "绝命": "平生坎坷，生世艱辛，東離西走，家遭凶禍，大凶之配。",
        }
        result += f"""
        {self.lv_cai_he_hun}：{conditions[self.lv_cai_he_hun]}
        
        上婚，主子孫昌盛，家宅平安；中婚為中吉，雖然有不吉因素，但是無大妨；如遇下婚，就要進行趨避。
        """

        return result + "\n"

    def check_marry_date(self):
        """
        關於合婚，僅從出生的年份看是不合理的，要全面的考察出生時間，婚姻是人生的大事，下面是關於婚配時間的選取，僅僅供大家參考
        首先陰差陽錯日不能選
        :return:
        """
        messed_up_date = [
            "辛卯",
            "壬辰",
            "癸已",
            "丙午",
            "丁未",
            "戊申",
            "辛酉",
            "壬戌",
            "癸亥",
            "丙子",
            "丁醜",
            "丁丑",
            "戊寅",
        ]

        result = f""
        comment = "古代對結婚的月份很有講究，"
        if self.ru_zhui:
            idx_zhi = self.man_demigod.nian_zhi
            comment += "由于是入赘，将使用男方的生辰进行校验。"
        else:
            idx_zhi = self.woman_demigod.nian_zhi
            comment += "将使用女方的生辰进行校验。"
        result += f'''
        {comment}
        '''

        """
        古代對結婚的月份很有講究，下面是婚嫁的利月和妨月
        ||子午生|醜未生|寅申生|卯酉生|辰戌生|已亥生|
        |:-:|:-:|:-:|:-:|:-:|:-:|:-:|
        |大利月|6，12|5，11|2，  8|1，  7|4，10|3，  9|
        |妨媒人|1，  7|4，10|3，  9|6，12|5，11|2，  8|
        |妨翁姑|2，  8|3，  9|4，10|5，11|6，12|1，  7|
        |妨父母|3，  9|2，  8|5，11|4，10|1，  7|6，12|
        |妨夫方|4，10|1，  7|6，12|3，  9|2，  8|5，11|
        |妨女方|5，11|6，12|1，  7|2，  8|3，  9|4，10|
        """
        conditions = {
            "子午": {
                (6, 12): "大利月",
                (1, 7): "妨媒人",
                (2, 8): "妨翁姑",
                (3, 9): "妨父母",
                (4, 10): "妨夫方",
                (5, 11): "妨女方",
            },
            "丑未": {
                (5, 11): "大利月",
                (4, 10): "妨媒人",
                (3, 9): "妨翁姑",
                (2, 8): "妨父母",
                (1, 7): "妨夫方",
                (6, 12): "妨女方",
            },
            "寅申": {
                (2, 8): "大利月",
                (3, 9): "妨媒人",
                (4, 10): "妨翁姑",
                (5, 11): "妨父母",
                (6, 12): "妨夫方",
                (1, 7): "妨女方",
            },
            "卯酉": {
                (1, 7): "大利月",
                (6, 12): "妨媒人",
                (5, 11): "妨翁姑",
                (4, 10): "妨父母",
                (3, 9): "妨夫方",
                (2, 8): "妨女方",
            },
            "辰戌": {
                (4, 10): "大利月",
                (1, 7): "妨媒人",
                (6, 12): "妨翁姑",
                (3, 9): "妨父母",
                (2, 8): "妨夫方",
                (5, 11): "妨女方",
            },
            "巳亥": {
                (3, 9): "大利月",
                (2, 8): "妨媒人",
                (1, 7): "妨翁姑",
                (6, 12): "妨父母",
                (5, 11): "妨夫方",
                (4, 10): "妨女方",
            },
        }

        marry_date_meta = MetaInfo(base_datetime=self.marry_date)
        check_date = marry_date_meta.ri_zhu

        check = {}
        for key, value in conditions.items():
            if idx_zhi in key:
                check = {v: k for k, v in value.items()}
                break

        if constants.BASE_DATE != self.marry_date:
            idx_month = marry_date_meta.lunar_month
            msg = ''
            for key, value in check.items():
                if idx_month in value:
                    msg = key
                    break

            idx_month = marry_date_meta.lunar_month
            result += f"""
        预期婚期为：{marry_date_meta.input_datetime.strftime('%Y-%m-%d')}，农历：{marry_date_meta.lunar_of_input_datetime_str}
        年支为：{idx_zhi}，婚期预计为农历 {idx_month} 月「{msg}」
        """
            if check_date in messed_up_date:
                result += f"""
       古詩有：陰差陽錯歌
    　　陰並陽錯是如何？ 辛卯壬辰癸已多。
    　　丙午丁未戊申是，辛酉壬戌癸亥過。
    　　丙子丁醜戊寅日，十二宮中細細歌。
       所以 {check_date} 日不宜結婚，容易出現婚姻問題。
                """

        result += f"""
       结婚月份福祸参考：
        """
        check_list = sorted(check.items(), key=lambda x: x[1])
        check_list_str = [f"{item[1][0]}/{item[1][1]}月：{item[0]}\n" for item in check_list]
        result += "        ".join(check_list_str)
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is a calc project of BaZi.')
    parser.add_argument('-b', '--birthday',
                        help='The birthday of yourself, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"',
                        required=True)
    parser.add_argument('-g', '--gander', help='The gander of yourself, default as male', action='store_true',
                        default=True)
    parser.add_argument('-e', '--explain', help='To check whether append explain details on different attributes',
                        action='store_true', default=False)
    parser.add_argument('-c', '--couple_birthday',
                        help='The birthday of your couple, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"',
                        required=False, default="2014-01-03 05:20:00")
    parser.add_argument('-md', '--marry_date',
                        help='The date which you couples prepare to get marriage, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"',
                        required=False)
    parser.add_argument('-rz', '--ru_zhui',
                        help='Set male as primary info to do calculation, and there were a special case on male\'s marriage is [ru zhui], default as False',
                        action='store_true', default=False)

    args = parser.parse_args()

    print(f'Argument received: {args}')

    main_birthday = datetime.strptime(args.birthday, default_date_format)
    is_male = args.gander
    explain_append = args.explain
    couple_birthday = datetime.strptime(args.couple_birthday, default_date_format)
    marry_date = datetime.strptime(args.marry_date, default_date_format) if args.marry_date else constants.BASE_DATE
    ru_zhui = args.ru_zhui

    if is_male:
        man_birthday, woman_birthday = main_birthday, couple_birthday
    else:
        man_birthday, woman_birthday = couple_birthday, main_birthday
    prediction = Intermarriage(
        man_birthday=man_birthday,
        woman_birthday=woman_birthday,
        meta_info_display=True,
        explain_append=explain_append,
        marry_date=marry_date,
        ru_zhui=ru_zhui,
    )
    print(prediction)
