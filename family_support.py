from utils import *
from ba_zi_elements import BaZiElements


class FamilySupport(BaZiElements):

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
            self.spouse,
            self.primary_child,
            self.following_child,
        ] = [self.elements_relationships_mapping[item][0] for item in [self.nian_gan_element,
                                                                       self.nian_zhi_element,
                                                                       self.yue_gan_element,
                                                                       self.yue_zhi_element,
                                                                       self.ri_zhi_element,
                                                                       self.shi_gan_element,
                                                                       self.shi_zhi_element,
                                                                       ]
             ]

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        家庭支持：
        祖先宫：
        年干（父亲及家族）：{self.father_family}
        年支（母亲及家族）：{self.mother_family}
        
        父母/兄弟姐妹/社会关系宫：
        月干（哥哥姐姐）：{self.elder_family_members}
        月令（弟弟妹妹）：{self.younger_family_members}
          
        夫妻宫：
        日元（自己）
        日支（夫/妻）：{self.spouse}

        子女宫：
        时干（长子）：{self.primary_child}
        时支（次子）：{self.following_child}
        '''
        return msg
