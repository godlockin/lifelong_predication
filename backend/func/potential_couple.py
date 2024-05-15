import argparse

from backend.constants.constants import *
from backend.func.demigod import Demigod
from backend.func.lord_gods import LordGods


class PotentialCouple(LordGods):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.element_appearance_mapping = self.init_element_appearance_mapping()

        self.position_relationship_mapping = self.calc_position_relationship_mapping()

        self.primary_couple_gan_details, self.secondary_couple_gan_details = self.calc_couple_gan()
        self.gan_appearance = self.calc_gan_appearance()
        self.position_appearance = self.calc_position_appearance()
        self.gan_zhi_appearance = self.calc_gan_zhi_appearance()
        self.element_based_appearance = self.calc_element_based_appearance()
        self.guan_position = self.calc_guan_position(**kwargs)
        self.finance_position = self.calc_finance_position()
        self.finance_columns = self.calc_finance_columns()
        self.palace = self.calc_palace()

    def calc_position_relationship_mapping(self):
        return {
            "年柱": "婚恋对象年龄较大，大约在一旬左右甚至以上；或者 距离较远，有可能不是当地的或同城的；也有可能是上司或老板等。",
            "月柱": "婚恋对象年龄稍大，大约在半旬左右甚至以上；或者 距离稍近，有可能是当地或同城的熟人、同学、朋友等。",
            "日柱": "婚恋对象年龄相仿，大约在两三岁或是同龄人，也有可能稍小；或者 距离很近，有可能是经常接触的熟人朋友等。",
            "时柱": "婚恋对象年龄较小，有可能相差半旬左右或以上；或者距离稍远，也有可能是熟人朋友或下属等。",
        }

    def init_element_appearance_mapping(self):
        return {
            '火': '亮丽，面红润。',
            '木': '高，发秀。',
            '水': '较胖，团活，面黑，人机灵，相貌一般。',
            '土': '敦厚结实，个头矮，较丑。',
            '金': '白皙端庄。',
        }

    def __str__(self):
        couple_name = "太太" if self.is_male else "先生"
        msg = f'''
        ## 未来伴侣：
        命主日支：{self.ri_zhi} 被称为夫妻宫，代表了{couple_name}的情况。
        {self.gan_zhi_appearance}
        '''
        msg += self.element_based_appearance

        if self.guan_position:

            msg += f'''
        从干支上来看，{couple_name}的年龄和距离可能为：
            '''
            if not self.explain_append:
                for item in self.guan_position:
                    msg += f'''
        {self.position_relationship_mapping[POSITION_COLUMN_NAMES[item[1]]]}
                    '''
            else:
                for i, item in enumerate(self.guan_position):
                    msg += f'''
        {'正' if '正' in item[0] else '次'}缘{i + 1}：{self.position_relationship_mapping[POSITION_COLUMN_NAMES[item[1]]]}
                    '''

        if self.finance_position:
            msg += f'''
        从财运上来看，{couple_name}的财务状况可能为：
            '''
            if not self.explain_append:
                for idx, item in enumerate(self.finance_position):
                    msg += f'''
        {item[0]}
        {self.finance_columns[idx]}
                    '''
            else:
                for idx, item in enumerate(self.finance_position):
                    msg += f'''
        {idx + 1}缘：{item[0]}
        {self.finance_columns[idx]}
                    '''

        msg += f'''
        从宫位上来看：
        {self.palace}
        '''

        return msg

    def calc_position_appearance(self):
        """
        古人从配偶宫看另一半长相的论断是：
        日支为子午卯酉者，主配偶长相漂亮或帅气，身材纤巧，或文弱书卷，比较周正或端庄，而且有才华或能力，性情浪漫，富有情调，情趣昂然，但感情善变。
        日支为寅申巳亥者，主配偶长相随和，身材一般，学识文静，比较大众化，聪明伶俐，富有情调，时有浪漫，讨人喜欢，但比较顽皮。
        日支为辰戌丑未者，主配偶质朴敦厚，相貌一般，朴实无华，身材健壮，性情固执，缺乏浪漫，但很踏实重情。
        :return:
        """
        conditions = [
            ("子午卯酉", "配偶长相漂亮或帅气，身材纤巧，或文弱书卷，比较周正或端庄，而且有才华或能力，性情浪漫，富有情调，情趣昂然，但感情善变。"),
            ("寅申巳亥", "配偶长相随和，身材一般，学识文静，比较大众化，聪明伶俐，富有情调，时有浪漫，讨人喜欢，但比较顽皮。"),
            ("辰戌丑未", "配偶质朴敦厚，相貌一般，朴实无华，身材健壮，性情固执，缺乏浪漫，但很踏实重情。"),
        ]
        for condition in conditions:
            if self.ri_zhi in condition[0]:
                return condition[1]

    def calc_couple_gan(self):
        """
        比如男命以财星为妻，女命以官星为夫，这个“财”和这个“官”，就是配偶星。

        什么是官星呢？
        生辰八字是以日主代表自己的，克日主的那个五行，就是官星。
        以阴阳区分，阴阴、阳阳这样的同性相克关系的，称为偏官(或七杀);而阴阳这样的异性相克的，称为正官。
        正官一般代表正夫的多，成婚的机率也大;而偏官代表情人的多，成婚的机率也小，但成为再婚对象的机率则大。

        什么是财星呢？
        同理，被日主所克的那个五行，就是财星。
        也是以阴阳区分，阴阴、阳阳这样的同性相克关系的，称为偏财;而阴阳这样的异性相克关系的，称为正才(正财去了贝旁)。
        正才一般代表正妻的多，成婚的机率也大;而偏财代表情人的多，成婚的机率也小，但成为再婚对象的机率则大。
        :return:
        """
        self_ri_gan_details = GAN_DETAILS[self.ri_gan]
        self_ri_gan_element = self_ri_gan_details['element']
        self_ri_gan_yinyang = self_ri_gan_details['yinyang']
        if self.is_male:
            self.couple_gan_element = ELEMENTS_OPPOSING[self_ri_gan_element]
        else:
            self.couple_gan_element = SWAPPED_ELEMENTS_OPPOSING[self_ri_gan_element]

        couple_primary_yin_yang = YIN_YANG_SWAP[self_ri_gan_yinyang]
        couple_secondary_yin_yang = self_ri_gan_yinyang

        primary_couple_details, secondary_couple_details = {}, {}
        for item in ZHI_MATRIX:
            if item[3] == couple_primary_yin_yang and item[4] == self.couple_gan_element:
                primary_couple_details = ZHI_DETAILS[item[0]]
            if item[3] == couple_secondary_yin_yang and item[4] == self.couple_gan_element:
                secondary_couple_details = ZHI_DETAILS[item[0]]
        return primary_couple_details, secondary_couple_details

    def calc_gan_appearance(self):
        """
        ①夫妻星(财、官)为火，主亮丽，面红润。4
        ②夫妻星为木，主人长得高，发秀。3
        ③夫妻星为水，主人较胖，团活。面黑，人机灵，相貌一般．2
        ④夫妻星为土，主人长的敦厚结实，个头矮，较丑。1
        ⑤夫妻星为金，人长得白皙端庄。3
        上 8，7
        中上 6，5
        中等 4，3
        一般 2
        :return:
        """
        return self.element_appearance_mapping[self.primary_couple_gan_details['element']], self.element_appearance_mapping[self.secondary_couple_gan_details['element']]

    def calc_gan_zhi_appearance(self):
        result = f"""
        比如男命以财星为妻，女命以官星为夫，这个“财”和这个“官”，就是配偶星。同时官/财也分正偏（正式夫妻/情人（再婚））。
        命主为{'男' if self.is_male else '女'}
        所以以{'正财-偏财' if self.is_male else '正官-偏官（七杀）'}的顺序显示。
        正缘：「{self.gan_appearance[0]}{self.position_appearance}」
        次缘：「{self.gan_appearance[1]}{self.position_appearance}」
        """

        return result

    def calc_element_based_appearance(self):
        """
        如果官星为土，又为喜用的五行，则表示此人忠厚老实，身材较肥，面色较黄。反之则身材较瘦，面色黑黄。
        如果官星为金，又为喜用的五行，则表示此人原则性强，身材骨感，面色较白。反之则瘦骨嶙峋，面色稍青。
        如果官星为水，又为喜用的五行，则表示此人灵活圆滑，身材浑厚，面色稍白。反之则肥腻如猪，面色发黑。
        如果官星为木，又为喜用的五行，则表示此人耿直不阿，身材苗条，面色青白。反之则骨瘦如柴，面色黑黄。
        如果官星为火，又为喜用的五行，则表示此人疾恶如仇，身材适中，面色红润。反之则肥瘦不均，面色青紫。
        :return:
        """
        primary_couple_element = self.primary_couple_gan_details['element']
        secondary_couple_element = self.secondary_couple_gan_details['element']

        positive_conditions = {
            '土': '(+土)忠厚老实，身材较肥，面色较黄',
            '金': '(+金)原则性强，身材骨感，面色较白',
            '水': '(+水)灵活圆滑，身材浑厚，面色稍白',
            '木': '(+木)耿直不阿，身材苗条，面色青白',
            '火': '(+火)疾恶如仇，身材适中，面色红润',
        }

        negative_conditions = {
            '土': '(-土)身材较瘦，面色黑黄',
            '金': '(-金)瘦骨嶙峋，面色稍青',
            '水': '(-水)肥腻如猪，面色发黑',
            '木': '(-木)骨瘦如柴，面色黑黄',
            '火': '(-火)肥瘦不均，面色青紫',
        }

        result = f"""
        与此同时，从五行上来看：
        """

        if primary_couple_element in self.supporting_elements_sequence:
            result += f"""
        正宫的样貌{positive_conditions[primary_couple_element]}
            """
        else:
            result += f"""
        正宫的样貌{negative_conditions[primary_couple_element]}
            """

        if secondary_couple_element in self.supporting_elements_sequence:
            result += f"""
        次宫的样貌{positive_conditions[secondary_couple_element]}
            """
        else:
            result += f"""
        次宫的样貌{negative_conditions[secondary_couple_element]}
            """

        return result

    def calc_guan_position(self, **kwargs):
        """
        如果官星在年柱，则表示婚恋对象年龄较大，大约在一旬左右甚至以上；距离较远，有可能不是当地的或同城的;也有可能是上司或老板等。
        如果官星在月柱，则表示婚恋对象年龄稍大，大约在半旬左右甚至以上；距离稍近，有可能是当地或同城的熟人、同学、朋友等。
        如果官星在日支，则表示婚恋对象年龄相仿，大约在两三岁或是同龄人;也有可能稍小；距离很近，有可能是经常接触的熟人朋友等。
        如官星在时柱，则表示婚恋对象年龄较小，有可能相差半旬左右或以上;距稍远，也有可能是熟人朋友或下属等。
        :return:
        """

        couple_list = []

        """
        如果官星只出现一个，就按一个或两个来看;如果官星出现两个，就按两三个来看;如果官星出现三个以上，就按多个来看，都是根据所在的位置，分别来看，不能混淆。
        如果八字中官星没有出现，则从八字的地支暗藏中去找;如果地支暗藏中也没有，则以财星代替官星来看。如果财星也没有出现，则以桃花来看。
        """
        idx_lord_god_mapping_sequence = [
            "正财" if self.is_male else "正官",
            "正官" if self.is_male else "正财",
            "偏财" if self.is_male else "七杀",
            "七杀" if self.is_male else "偏财",
        ]
        all_gan = self.lord_gods_w_cang_gan_matrix[0]
        # 日主不算
        all_gan[2] = ''
        all_zhi = self.lord_gods_w_cang_gan_core_matrix[1]

        def find_lord_gods(trgt_lord_god):
            matched_list = []
            if trgt_lord_god in all_gan:
                for i, gan_load_god in enumerate(all_gan):
                    if gan_load_god == trgt_lord_god:
                        matched_list.append((trgt_lord_god, i, 0))
            elif trgt_lord_god in all_zhi:
                for i, zhi_load_god in enumerate(all_zhi):
                    if trgt_lord_god in zhi_load_god:
                        matched_list.append((trgt_lord_god, i, 1))
            return matched_list

        for check_lord in idx_lord_god_mapping_sequence:
            tmp = find_lord_gods(check_lord)
            if tmp:
                couple_list.extend(tmp)
                break

        if not couple_list:
            self.demigod = Demigod(**kwargs)

            idx_demigod = "桃花"
            if idx_demigod in self.demigod.all_demigod:
                for i, zhu_demigod in enumerate(self.demigod.all_demigod_matrix):
                    if idx_demigod in zhu_demigod:
                        couple_list.append((idx_demigod, i, 1))
                        break

        return couple_list

    def calc_finance_position(self):
        """
        如果官星为喜用的五行，旺而逢生，则表示此人事业有成，财运很好。反之则事业坎坷，财运不佳。
        如果官星为忌讳的五行，旺而逢生，则表示此人事业蹉跎，财运较差。反之则事业有成，财运很好。
        :return:
        """
        element_comments = []
        for position in self.guan_position:
            is_support = self.elements_matrix[position[2]][position[1]] in self.supporting_elements_sequence
            if self.self_strong:
                if is_support:
                    msg = "官星为喜用的五行，旺而逢生，则表示此人事业有成，财运很好。"
                else:
                    msg = "官星为忌讳的五行，旺而逢生，则表示此人事业蹉跎，财运较差。"
            else:
                if is_support:
                    msg = "官星为喜用的五行，弱而逢生，则表示此人事业蹉跎，财运较差。"
                else:
                    msg = "官星为忌讳的五行，弱而逢生，则表示此人事业有成，财运很好。"
            element_comments.append((msg, position[2], position[1]))

        return element_comments

    def calc_finance_columns(self):
        """
        官星在年柱的，不论喜忌与否，一般都有一定的事业基础和财富积累。
        官星在时柱的，不论喜忌与否，起码在你和他结婚的时候，一般都没有事业基础，财富也不够充裕。不过中年以后也或有改善。
        官星在月柱与日支的，一般是夫妻共同奋斗，同甘共苦，创立基业。
        :return:
        """
        result = []
        for position in self.finance_position:
            if position[2] == 0:
                result.append("官星在年柱的，一般都有一定的事业基础和财富积累。")
            elif position[2] == 3:
                result.append("官星在时柱的，在你和他结婚的时候，一般都没有事业基础，财富也不够充裕。不过中年以后也或有改善。")
            else:
                result.append("官星在月柱与日支的，一般是夫妻共同奋斗，同甘共苦，创立基业。")
        return result

    def calc_palace(self):
        """
        配偶宫为日主的喜用神的人，配偶多能富贵
        八字中的配偶宫，一般指的是日支。日支为日主的喜用之神，自然这个宫位所居之人，能为我所用，我会受益于她（他）；
        宫位所居之神，在八字中越是旺相，就表明能给自己带来的益处越大，富贵程度自然很高。
        反之，假如为忌，在八字中越旺，则表示富贵程度越低。
        这个也要结合日主的行运，行运中扶住夫妻宫位所居喜用之神的，这个阶段，配偶的富贵程度逾高；反之，则相反。
        另外一个方面，也可以从夫妻宫位所居十神看出富贵的类型：
        官星为喜用的，则表示配偶在社会上有名气、有身份、或者具有一定的社会地位；
        财星为喜用的，则表示配偶的家庭条件较好、生活富裕、以富为主；
        食伤为喜用的，则表示配偶是一个聪明、有才华、口碑很好的人；或者是文人、才子、或者靠口碑、技艺而扬名；
        印星为喜用的，则表示配偶好读书，多为书香门第，或者行善积德之人，为文人，多主贵；
        比劫为喜用的，则表示配偶多是白手起家，自己创业致富的人。
        :return:
        """
        result = ""
        ri_zhi_lord_gods_core = [self.ri_zhi_core_lord_gods] + self.lord_gods_w_cang_gan_core_matrix[1][2]
        if self.ri_zhi_element in self.supporting_elements_sequence:
            result += "配偶宫为日主的喜用神的人，配偶多能富贵。\n"
            if '正官' in ri_zhi_lord_gods_core or '七杀' in ri_zhi_lord_gods_core:
                result += '官星为喜用的，则表示配偶在社会上有名气、有身份、或者具有一定的社会地位'
            elif '正财' in ri_zhi_lord_gods_core or '偏财' in ri_zhi_lord_gods_core:
                result += '财星为喜用的，则表示配偶的家庭条件较好、生活富裕、以富为主'
            elif '食神' in ri_zhi_lord_gods_core or '伤官' in ri_zhi_lord_gods_core:
                result += '食伤为喜用的，则表示配偶是一个聪明、有才华、口碑很好的人；或者是文人、才子、或者靠口碑、技艺而扬名'
            elif '正印' in ri_zhi_lord_gods_core or '偏印' in ri_zhi_lord_gods_core:
                result += '印星为喜用的，则表示配偶好读书，多为书香门第，或者行善积德之人，为文人，多主贵'
            elif '比肩' in ri_zhi_lord_gods_core or '劫财' in ri_zhi_lord_gods_core:
                result += '比劫为喜用的，则表示配偶多是白手起家，自己创业致富的人'
        else:
            result += "配偶宫为日主的忌用神的人，配偶多不能富贵。"
        result += "\n"

        """
        配偶宫所居十神为“四善星”（正官、正印、食神、正财）的人，配偶一般个性较好；配偶宫所居十神为“四恶星”（七杀、枭印、伤官、劫财）的人，配偶一般脾气较差，个性不是很好。
        """
        four_positive_lord_gods = ['正官', '正印', '食神', '正财']
        four_negative_lord_gods = ['七杀', '枭印', '伤官', '劫财']
        positive = set(ri_zhi_lord_gods_core).intersection(set(four_positive_lord_gods))
        negative = set(ri_zhi_lord_gods_core).intersection(set(four_negative_lord_gods))
        if positive:
            result += f"""
        配偶宫所居十神（{list(positive)[0]}）为“四善星”（正官、正印、食神、正财）的人，配偶一般个性较好
            """
        elif negative:
            result += f"""
        配偶宫所居十神（{list(negative)[0]}）为“四恶星”（七杀、枭印、伤官、劫财）的人，配偶一般脾气较差，个性不是很好
        """

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

    args = parser.parse_args()

    print(f'Argument received: {args}')
    main_birthday = datetime.strptime(args.birthday, default_date_format)
    is_male = args.gander
    explain_append = args.explain
    prediction = PotentialCouple(
        base_datetime=main_birthday,
        explain_append=explain_append,
        is_male=is_male,
    )
    print(prediction)