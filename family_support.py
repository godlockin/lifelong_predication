import argparse

from lord_gods import LordGods
from utils import *


class FamilySupport(LordGods):

    """
    喜用就关系好，能得到六亲的帮助
    忌凶则关系不好，得不到六亲的帮助

    |祖先宫|父母/兄弟姐妹/社会关系宫|夫妻宫|子女宫|
    |:-:|:-:|:-:|:-:|
    |年干|月干|日元|时干|
    |*父亲/父亲家族（叔叔伯伯姑姑爷爷奶奶）*|*父亲/哥哥姐姐/社会上的哥哥姐姐*|*自己*|*长子（第一个孩子）*|
    |年支|月令|日支|时支|
    |*母亲/母亲家族（舅舅阿姨外公外婆）*|*母亲/弟弟妹妹/社会上的弟弟妹妹*|*夫妻/夫妻家族（如果本人是男则代表妻子的家族，反之亦然）*|*次子（第二个开始后面的孩子）*|
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)

        [
            self.father_family,
            self.mother_family,
            self.elder_family_members,
            self.younger_family_members,
            _, # 日主自己的不用计算
            self.spouse,
            self.primary_child,
            self.following_child,
        ] = [self.elements_relationships_mapping[item][0] for item in self.all_elements]

        self.family_relations = self.calc_family_relations()

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        ## 家庭支持：
        年柱祖先宫                  月柱父母/兄弟姐妹/社会关系宫        日柱夫妻宫         时柱子女宫
        年干（父亲及家族）           月干（哥哥姐姐）                   日元（自己）       时干（长子）
        {self.father_family}                       {self.elder_family_members}                                             {self.primary_child}
        年支（母亲及家族）           月令（弟弟妹妹）                   日支（夫/妻）      时支（次子）
        {self.mother_family}                       {self.younger_family_members}                             {self.spouse}             {self.following_child}
        '''

        if self.family_relations:
            msg += f'''
        {self.family_relations}
            '''
        return msg

    def calc_family_relations(self):
        result = []
        # 年柱
        result.extend(self.calc_nian_zhu())
        # 月柱
        result.extend(self.calc_yue_zhu())
        # 日柱
        result.extend(self.calc_ri_zhu())
        # 时柱
        result.extend(self.calc_shi_zhu())

        return "\n".join(result) if result else ""

    def calc_nian_zhu(self):
        result = []
        result.append("年柱代表祖先宫和父母。")
        nian_positive = 0
        if self.nian_gan_element in self.supporting_elements_sequence:
            result.append(f"年干（{self.nian_zhi_element}）为喜用，代表父亲家族对自己有促进作用。({self.elements_relationships_mapping[self.nian_gan_element]})")
            nian_positive += 1
        if self.nian_zhi_element in self.supporting_elements_sequence:
            result.append(f"年支（{self.nian_zhi_element}）为喜用，代表母亲家族对自己有促进作用。({self.elements_relationships_mapping[self.nian_zhi_element]})")
            nian_positive += 1
        if nian_positive == 2:
            result.append(f"年柱（{self.nian_zhi_element}/{self.nian_zhi_element}）双喜用，代表祖上为名门望族，有钱有势。面相上，额头（福德宫）上比较饱满。")

        nian_negative = 0
        if self.nian_gan_element in self.opposing_elements_sequence:
            result.append(f"年干（{self.nian_gan_element}）为忌凶，代表父亲家族会拖累自己。({self.elements_relationships_mapping[self.nian_gan_element]})")
            nian_negative += 1
        if self.nian_zhi_element in self.opposing_elements_sequence:
            result.append(f"年支（{self.nian_zhi_element}）为忌凶，代表母亲家族会拖累自己。({self.elements_relationships_mapping[self.nian_zhi_element]})")
            nian_negative += 1
        if nian_negative == 2:
            result.append(f"年柱（{self.nian_zhi_element}/{self.nian_zhi_element}）双忌凶，代表祖上情况比较一般，对自己没有帮助甚至需要消耗自己。")

        if ELEMENTS_SUPPORTING[self.nian_gan_element] == self.nian_zhi_element or SWAPPED_ELEMENTS_SUPPORTING[self.nian_gan_element] == self.nian_zhi_element:
            result.append(f"年柱（{self.nian_gan_element}/{self.nian_zhi_element}）五行相生，代表父母关系良好。")
            if ELEMENTS_SUPPORTING[self.nian_gan_element] == self.nian_zhi_element:
                result.append(f"「{self.nian_gan_element}」生「{self.nian_zhi_element}」，母亲会促进父亲。")
            else:
                result.append(f"「{self.nian_zhi_element}」生「{self.nian_gan_element}」，父亲会促进母亲。")

        elif ELEMENTS_OPPOSING[self.nian_gan_element] == self.nian_zhi_element or SWAPPED_ELEMENTS_OPPOSING[self.nian_gan_element] == self.nian_zhi_element:
            result.append(f"年柱（{self.nian_gan_element}/{self.nian_zhi_element}）五行相克，代表父母关系不好。")
            if ELEMENTS_OPPOSING[self.nian_gan_element] == self.nian_zhi_element:
                result.append(f"「{self.nian_gan_element}」克「{self.nian_zhi_element}」，父亲会压制母亲。")
            else:
                result.append(f"「{self.nian_zhi_element}」克「{self.nian_gan_element}」，母亲会压制父亲。")

        return result

    def calc_yue_zhu(self):
        result = []
        result.append("月柱代表成长环境和兄弟姐妹。")
        yue_positive = 0
        if self.yue_gan_element in self.supporting_elements_sequence:
            result.append(f"月干（{self.yue_gan_element}）为喜用，代表哥哥姐姐对自己有促进作用。({self.elements_relationships_mapping[self.yue_gan_element]})")
            yue_positive += 1
        if self.yue_zhi_element in self.supporting_elements_sequence:
            result.append(f"月支（{self.yue_zhi_element}）为喜用，代表弟弟妹妹对自己有促进作用。({self.elements_relationships_mapping[self.yue_zhi_element]})")
            yue_positive += 1
        if yue_positive == 2:
            result.append(f"月柱（{self.yue_gan_element}/{self.yue_zhi_element}）双喜用，代表同辈兄弟姐妹感情深厚，对命主多有帮助。")

        yue_negative = 0
        if self.yue_gan_element in self.opposing_elements_sequence:
            result.append(f"月干（{self.yue_gan_element}）为忌凶，代表哥哥姐姐会拖累自己。({self.elements_relationships_mapping[self.yue_gan_element]})")
            yue_negative += 1
        if self.yue_zhi_element in self.opposing_elements_sequence:
            result.append(f"月支（{self.yue_zhi_element}）为忌凶，代表弟弟妹妹会拖累自己。({self.elements_relationships_mapping[self.yue_zhi_element]})")
            yue_negative += 1
        if yue_negative == 2:
            result.append(f"月柱（{self.yue_gan_element}/{self.yue_zhi_element}）双忌凶，代表命主与兄弟姐妹不和，无法相互依靠，同时月柱也代表命主成长环境波折多阻。")

        return result

    def calc_ri_zhu(self):
        result = []
        result.append(f"日柱为夫妻宫代表对象。({self.elements_relationships_mapping[self.ri_zhi_element]})")
        if self.ri_zhi_element in self.supporting_elements_sequence:
            result.append(f"日支（{self.ri_zhi_element}）为喜用，可以{'娶贤妻' if self.is_male else '嫁贤夫'}，婚姻美满。")
            if self.is_male and '正财' in [item[2] for item in self.ri_zhi_lord_gods]:
                result.append(f"同时正财在日支，比较适合让老婆管钱，能让整体生活水平上升。性生活较和谐，双方需求都能满足。")

        if self.ri_zhi_element in self.opposing_elements_sequence:
            result.append(f"日支（{self.ri_zhi_element}）为忌凶，代表婚姻波折、口角纷争多，甚至可能离婚。性生活不太和谐。")

        if ELEMENTS_SUPPORTING[self.ri_gan_element] == self.ri_zhi_element or SWAPPED_ELEMENTS_SUPPORTING[self.ri_gan_element] == self.ri_zhi_element:
            result.append(f"日柱（{self.ri_gan_element}/{self.ri_zhi_element}）五行相生，代表夫妻相敬如宾情深意切。")
            if ELEMENTS_SUPPORTING[self.ri_gan_element] == self.ri_zhi_element:
                result.append(f"「{self.ri_gan_element}」生「{self.ri_zhi_element}」，对象促进自己。")
            else:
                result.append(f"「{self.ri_zhi_element}」生「{self.ri_gan_element}」，自己促进对象。")

        elif ELEMENTS_OPPOSING[self.ri_gan_element] == self.ri_zhi_element or SWAPPED_ELEMENTS_OPPOSING[self.ri_gan_element] == self.ri_zhi_element:
            result.append(f"日柱（{self.ri_gan_element}/{self.ri_zhi_element}）五行相克，代表夫妻反目，视如仇敌。")
            if ELEMENTS_OPPOSING[self.ri_gan_element] == self.ri_zhi_element:
                result.append(f"「{self.ri_gan_element}」克「{self.ri_zhi_element}」，自己压制对象。")
            else:
                result.append(f"「{self.ri_zhi_element}」克「{self.ri_gan_element}」，对象压制自己。")

        return result

    def calc_shi_zhu(self):
        result = []
        result.append("时柱代表学业、事业、子女。")
        if self.shi_gan_element in self.supporting_elements_sequence:
            result.append(f"时干（{self.shi_gan_element}）为喜用，晚年幸福，儿孙抱膝。({self.elements_relationships_mapping[self.shi_gan_element]})")
        if self.shi_zhi_element in self.supporting_elements_sequence:
            result.append(f"时支（{self.shi_zhi_element}）为喜用，学业、事业可以凭自己努力成功。({self.elements_relationships_mapping[self.shi_zhi_element]})")

        if self.shi_gan_element in self.opposing_elements_sequence:
            result.append(f"时干（{self.shi_gan_element}）为忌凶，子女难管、难养。年纪大了之后，小孩不太来看你，你们没啥交流。({self.elements_relationships_mapping[self.shi_gan_element]})")
        if self.shi_zhi_element in self.opposing_elements_sequence:
            result.append(f"时支（{self.shi_zhi_element}）为忌凶，子女孝顺，亲近{'父亲' if self.is_male else '母亲'}。学业、事业很难凭自己努力成功。({self.elements_relationships_mapping[self.shi_zhi_element]})")

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
    prediction = FamilySupport(
        base_datetime=main_birthday,
        meta_info_display=True,
        explain_append=explain_append,
        is_male=is_male,
    )
    print(prediction)
