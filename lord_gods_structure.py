import argparse
import copy

from constants import *
from lord_gods import LordGods


class LordGodsStructure(LordGods):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.structure = self.calc_structure()
        self.strength_comment = self.calc_structure_expansion()
        self.is_positive_overall = self.calc_is_positive_overall()

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"

        msg += f"""
        ### 命格
        命主为：{self.structure}格（身{'强' if self.self_strong else '弱'}）
        {self.strength_comment['structure']}
        因为，{self.strength_comment['comment']}
        形象：{self.strength_comment['imagery']}
        由于命主身{'强' if self.self_strong else '弱'}，所以：{self.strength_comment['strength_comment']}
        整体来看，命主命格{'正' if self.is_positive_overall[0] else '负'}向。
        {self.is_positive_overall[1]}
        """
        return msg

    def calc_structure(self):
        # 月令藏干十神为本气根、中气根、余气根
        # 月令食神中有根，天干中透出者为格
        # 如果不存在，则以本气根为格
        yue_zhi_lord_gods = self.lord_gods_core_matrix[1][1]
        for item in yue_zhi_lord_gods:
            if item in self.lord_gods_matrix[0]:
                return item

        return yue_zhi_lord_gods[0]

    def calc_structure_expansion(self):
        conditions = {
            '正财': {
                'comment': '正财是纯物质型十神。重现实、讲实际、脚踏实地、诚实可信。',
                'structure': '正财格的人，一步一个脚印，坚信成功在于勤奋',
                'male': '正财格的男人有着不错的事业发展，这种命格的人往往都很注重于自己的事业因为他们是不会走偏财运的，如果想要有钱的话，都会依靠自己的努力，他们就是那种一分耕耘一分收获的人，因此，这样的人在事业上面是会花费很多精力，但是也能够在事业道路上有很不错的发展，他们一般都是踏实肯干的人。',
                'female': '对于正财格女命来说，财星往往代表丈夫和婚姻，假如一个女命为正财格的话，那么其人婚姻美满，勤俭持家品性温顺，丈夫本人也品德高尚。不过如果女命正财过旺，婆婆、小姑掌家权，那么很有可能婆媳有失和之象，这样来反为贫命。',
                'imagery': '钱财、身体、工作、事业、固定资产、妻子（男命）',
                'positive': '富裕、健康、事业有成',
                'negative': '贫困、新款、疾病、婚灾',
            },
            '偏财': {
                'comment': '偏财是偏向于物质型十神，其本性偏向于吉神。偏财之人深谙理财处事的诀窍，头脑灵活，多才多艺，为人处事圆滑干练；豪爽仗义，注重物质的享受。',
                'structure': '偏财格的人，对任何事情拿得起放得下',
                'imagery': '钱财、才华、事业、吃喝玩乐',
                'positive': '事业有成、多才多艺',
                'negative': '贫困、疾病、婚灾、玩世不恭、铺张浪费',
            },
            '正官': {
                'comment': '正官是物质型十神，是最理想的十神。习惯在法律、法规、社会习俗、规章制度允许的前提下求名、求发展。',
                'structure': '正官格的人，一身正气崇尚正义。',
                'male': '正官格男命的特征非常明显，他们聪明、有才华、有领导能力，但同时也有点固执已见。他们的命运多半与职业、事业密切相关，因此，他们常常会成为领导者、管理者、企业家等职业的佼佼者。如果你是一位正官格男命，那么你应该好好利用自己的优势，不断追求更高的成就。',
                'female': '正官格女命的特点是品行端正、聪明机智、重视事业、重情重义、有才华等这种女命的人往往能够在事业和人际关系上取得良好的成就，同时在艺术领域也有一定的天赋。当然，不同的人有不同的命局，也会有不同的特点和优缺点。因此，我们应该在了解自己的命局特点的同时，也要发挥自己的优势克服自己的缺点，不断提升自己。',
                'imagery': '工作、地位。权利、压力、阻力、丈夫（女命）、子女（男命）',
                'positive': '名声、地位、权力、事业',
                'negative': '压力、阻力、慢性病、贫贱、官灾',
            },
            '七杀': {
                'comment': '七杀是物质型十神。名声、地位是七杀之人终生的追求，他们能为名利舍弃一切，包括家庭、生命。',
                'structure': '偏官（七杀）格的人，相信胜者为王，败者为寇。',
                'male': '七杀格男命，做事相当果断坚决，绝对不会优柔寡断，拖泥带水。脑子很活络思维也很跳跃，一旦决定了的事情，就不会轻易改变。他们特别有韧劲儿，吃苦耐劳的能力，不是常人能够想象的。他们事业心很强，为了取得重大成绩，会牺牲很多东西。比如说家庭以及健康等等。在他们眼中，只有取得重大成绩实现人生抱负，才算是圆满而无憾的。',
                'female': '女人七杀，事业心强，性格坚强。她们对事业非常重视，愿意付出心血和精力，有很强的毅力和决心，能够取得事业上的突破和成功。她们在事业上可以有突破，比如能够创办自己的事业，或者担任领导职位。此外，她们在家庭中也能够付出很多，家庭打理得并并有条，但最忌官杀混杂。',
                'imagery': '伤残、疾病、夭折、牢狱、名声、权威',
                'positive': '名声、地位、权力、事业',
                'negative': '伤残、疾病、牢狱、斗争、小人、贫贱',
            },
            '正印': {
                'comment': '正印是纯精神型十神。淡泊名利、注重荣誉、好学多思、博爱无私。',
                'structure': '正印格的人，善于思考、疏于实践。',
                'imagery': '学习、荣誉、工作、靠山、贵人、福气',
                'positive': '学历、荣誉、地位。靠山、贵人',
                'negative': '休学、失业、损名、贫穷、懒惰、疾病',
            },
            '偏印': {
                'comment': '偏印是精神型十神。思想怪异，深具创造力。精明能干，缺少人情味。',
                'structure': '偏印（枭神）格的人，排斥他人他物，偏业之人。',
                'male': '偏印格的男命在事业发展的过程之中，还是需要进行更多的努力，因为如果没有更多勤奋刻苦的了解的话，那么，这类男人并不对事业产生兴趣，也没有意识到工作对自己人生发展的重要性。所以在一些贵人帮助的情况之下，其实这-种类型的男孩子未来的生活之中还是能够达到一定的事业成就的。',
                'female': '偏印格女命的人具有独立自主、活泼开朗、富有创造力、理性冷静和追求完美等特点。这些优秀的品质让她们在职场和生活中表现得更加出色，也让她们在人际关系中更容易得到他人的认可和支持。',
                'imagery': '不稳定性、偏业性工作、副职、病灾、破财、休学、失业',
                'positive': '偏业、思想上的成就，学术、荣誉、地位',
                'negative': '病灾、不雅的胎记/疤痕/痣。破财、休学、失业、伤克于女',
            },
            '食神': {
                'comment': '食神是精神型十神。聪明仁慈、通情达理、乐于奉献。',
                'structure': '食神格的人，悠游自足、随遇而安、和气生财、与世无争。',
                'male': '食神格的男人，内心世界是非常丰富的，他们有自己的抱负和抱负。他们不仅有远大志向，而且他们会不断实现自身价值，所以他们也是人生的赢家。但是食神太多时，则变成好吃懒做，游手好闲之徒，贪图享受，没有理想的工作，并且经常为金钱所困。',
                'female': '女命者，食伤代表子女。食神格最忌偏印，因此以食神为主的命大运遇上偏印的，容易遇见各种倒霉之事。食神格的女命往往会有比较好的事业运和财运，因为这个命格的女命很容易就能够使得自己具备不错的气场，而且也具有很强的正气。',
                'imagery': '平安、福气、口福。娱乐、运动、才华、财源',
                'positive': '平安、福气、多才多艺、经济富裕、身体健康',
                'negative': '疾病、劳累、贫困',
            },
            '伤官': {
                'comment': '伤官是精神和物质矛盾型十神。才华横溢，大胆泼辣，斗志昂扬，狂傲乖张。刚愎自用，言语尖锐，气量狭小。',
                'structure': '伤官格的人，欲望强烈永不满足。',
                'male': '伤官格的男人，自己的事业运势是不错的，因此，在事业发展的过程中会比较顺利，虽然这种人可能和同事的关系不是很好，但是其本人却具有很不错的能力以及自信心，这样的人自然最终地位也会挺高。伤官格男命的人缘一般都比较差，主要是因为本身性格就比较强势，比较霸道。',
                'female': '伤官格女命一般来说对人是很热忱的，也很有同情心，可是就是有一点，就是自己做了善事就理所当然的认为别人也要协助自己，这样可能会发生了反效果的，反而别人感到其不怎么好相处。伤官格女命都是虚荣心比较强的，不喜欢遭就任何的束缚的，大部分的时分都是不会听从管理的，自身的才能也是很出众的，这类人生活喜欢做自由职业的比较多。',
                'imagery': '才华、技艺、降职、免位、休学、失业、伤病灾',
                'positive': '多才多艺、技术成果、升职、富裕',
                'negative': '官灾、降职失业、病退休学、伤病灾',
            },
            '比肩': {
                'comment': '比肩是物质型十神。其本性偏，向于凶神。比肩之人自信自尊，好攀比，不服输，有自知之明。',
                'structure': '比肩格的人，人不犯我我不犯人。',
                'imagery': '竞争、耗财、口舌官非、婚姻不顺',
                'positive': '多得兄弟姐妹、朋友助益，竞争中得名得利，富裕',
                'negative': '官非口舌、破财、病灾、婚灾',
            },
            '劫财': {
                'comment': '劫财是物质型十神。自信、武断，斗志高昂，以行动解决问题；投机取巧，野心勃勃；人不犯我，我也犯人。',
                'structure': '劫财格的人，办事不达目的誓不罢休。',
                'imagery': '打架斗殴，官灾牢狱，破财，克妻、克夫、克父，竞争奋斗',
                'positive': '意志坚强、竞争得利、事业有成',
                'negative': '打架斗殴、偷盗抢劫、官灾牢狱、破财病灾、克妻克夫克父、贫寒',
            },
        }

        # 身强 + 喜用
        positive_supporting_list = ['正财', '偏财', '正官', '偏官', '食神', '伤官']
        negative_supporting_list = ['正印', '偏印', '比肩', '劫财']

        details = copy.deepcopy(conditions[self.structure])
        if self.self_strong:
            if self.structure in positive_supporting_list:
                strength_comment = details['positive']
            else:
                strength_comment = details['negative']
        else:
            if self.structure in negative_supporting_list:
                strength_comment = details['positive']
            else:
                strength_comment = details['negative']

        del details['positive']
        del details['negative']
        details['strength_comment'] = strength_comment
        return details

    def calc_is_positive_overall(self):
        structure_gan, structure_element = "", ""
        for gan, element, lord_god in self.yue_zhi_lord_gods:
            if self.structure == lord_god:
                structure_gan, structure_element = gan, element
                break

        structure_gan_details = GAN_DETAILS[structure_gan]
        self_lord_god_details = LORD_GODS_DETAILS[self.ri_gan]

        is_finance_exists = any(item in self.all_lord_gods for item in ['正财', '偏财'])
        is_yin_exists = any(item in self.all_lord_gods for item in ['正印', '偏印'])
        is_shi_shang_exists = any(item in self.all_lord_gods for item in ['食神', '伤官'])
        is_harmful_exists = (
                TIAN_GAN_CHONG_MAPPING.get(structure_gan, '') in self.all_gan
                or
                any(ZHI_ATTRIBUTES[self.yue_zhi][item] in self.all_zhi for item in ['冲', '刑', '害', '破'])
        )
        fix_func = self.calc_fix_func(structure_element, structure_gan_details)

        # 正官
        if '正官' == self.structure:
            if (
                    # 日干强，又有财来生官
                    (
                            self.self_strong
                            and is_finance_exists
                    )
                    or
                    # 日干弱，正官强，有印生身
                    (
                            not self.self_strong
                            and self.elements_weight.get(structure_element, 0) > 1
                            and is_yin_exists
                    )
                    or
                    # 正官不见七杀混杂
                    (
                            '七杀' not in self.lord_gods_core_matrix[1][1]
                    )
            ):
                return True, ""

            if (
                    # 见伤官而无印
                    (
                            '伤官' in self.all_lord_gods and not is_yin_exists
                    )
                    or
                    # 杀来混杂
                    (
                            '七杀' in self.lord_gods_core_matrix[1][1]
                    )
                    or
                    # 刑冲破害
                    (
                            is_harmful_exists
                    )
            ):
                return False, fix_func

        # 食神
        if '食神' == self.structure:

            if (
                    self.self_strong
                    and
                    (
                            # 日干强，食亦强，再见财
                            (
                                    self.elements_weight.get(structure_element, 0) > 1
                                    and is_finance_exists
                            )
                            or
                            # 日干强，杀尤过之，食神制杀而不见财
                            (
                                    self.elements_weight.get(structure_element, 0) < self.elements_weight.get(GAN_DETAILS[LORD_GODS_DETAILS[self.ri_gan]['七杀']]['element'], 0)
                                    and not is_finance_exists
                            )
                            or
                            # 日干强，食神泄气太过，见印护身
                            (
                                    self.elements_weight.get(structure_element, 0) > 1.5
                                    and is_yin_exists
                            )
                    )
            ):
                return True, ""

            if (
                    # 日干强，食轻又逢枭
                    (
                            self.self_strong
                            and self.elements_weight.get(structure_element, 0) < 1
                            and '偏印' in self.all_lord_gods
                    )
                    or
                    # 日干弱，食神生财，而又露杀
                    (
                            not self.self_strong
                            and is_finance_exists
                            and '七杀' in self.all_lord_gods
                    )
                    or
                    # 逢刑冲破害
                    (
                            is_harmful_exists
                    )
            ):
                return False, fix_func

        # 正偏财
        if any(item == self.structure for item in ['正财', '偏财']):
            if (
                # 日干强，财亦强，再见官星
                    (
                        self.self_strong
                        and self.elements_weight.get(structure_element, 0) > 1
                        and '正官' in self.all_lord_gods
                    )
                or
                # 日干弱，财星强，有印比护身
                    (
                        not self.self_strong
                        and self.elements_weight.get(structure_element, 0) > 1
                        and is_yin_exists
                        and '比肩' in self.all_lord_gods
                    )
                or
                # 日干强，财星弱，有食伤生财
                    (
                        self.self_strong
                        and self.elements_weight.get(structure_element, 0) < 1
                        and is_shi_shang_exists
                    )
            ):
                return True, ""

            if (
                # 日干强，财轻，比劫又重
                    (
                        self.self_strong
                        and self.elements_weight.get(structure_element, 0) < 1
                        and (
                                self.elements_weight.get(GAN_DETAILS[self_lord_god_details['比肩']]['element'], 0) > 1
                                or
                                self.elements_weight.get(GAN_DETAILS[self_lord_god_details['劫财']]['element'], 0) > 1
                        )
                    )
                or
                # 日干弱，七杀重，财又生杀
                    (
                        not self.self_strong
                        and self.elements_weight.get(GAN_DETAILS[self_lord_god_details['七杀']]['element'], 0) > 1
                    )
                or
                # 逢刑冲破害
                    (
                        is_harmful_exists
                    )
            ):
                return False, fix_func

        # 伤官
        if '伤官' == self.structure:
            if (
                # 日干强，伤官生财
                    (
                        self.self_strong
                        and is_finance_exists
                    )
                or
                # 日干弱，伤官泄气，有印护身
                    (
                        not self.self_strong
                        and is_yin_exists
                    )
                or
                # 日干弱，伤官强，而印杀双透
                    (
                        not self.self_strong
                        and self.elements_weight.get(structure_element, 0) > 1
                        and all((item in self.lord_gods_matrix[0]) and (item in self.lord_gods_matrix[1]) for item in ['正印', '七杀'])
                    )
                or
                # 日干强，杀重，伤官驾杀
                    (
                        self.self_strong
                        and self.elements_weight.get(GAN_DETAILS[self_lord_god_details['七杀']]['element'], 0) > 1
                        and '七杀' in self.lord_gods_core_matrix[1][1]
                    )
            ):
                return True, ""

            if (
                # 见官
                    (
                        '正官' in self.lord_gods_core_matrix[0] or '正官' in self.lord_gods_core_matrix[1]
                    )
                or
                # 日干弱，又多财
                    (
                        not self.self_strong
                        and is_finance_exists
                        and self.elements_count.get(ELEMENTS_OPPOSING[self.ri_gan_element], 0) > 3
                    )
                or
                # 日干强，伤官轻，而又多印
                    (
                        self.self_strong
                        and self.elements_weight.get(GAN_DETAILS[self_lord_god_details['伤官']]['element'], 0) < 1.01
                        and self.all_lord_gods_counter['正印'] > 3
                    )
                or
                    # 逢刑冲破害
                    (
                            is_harmful_exists
                    )
            ):
                return False, fix_func

        # 七杀
        if '七杀' == self.structure:
            if (
                # 身强
                #     (
                #         self.self_strong
                #     )
                # or
                # 日干强，杀尤过之，有食制杀
                    (
                        self.self_strong
                        and 1 < self.elements_weight.get(GAN_DETAILS[self_lord_god_details['七杀']]['element'], 0) < self.elements_weight.get(GAN_DETAILS[self_lord_god_details['食神']]['element'], 0)
                    )
                or
                # 日干弱，杀旺，有印生身
                    (
                        not self.self_strong
                        and self.elements_weight.get(GAN_DETAILS[self_lord_god_details['七杀']]['element'], 0) > 1
                        and is_yin_exists
                    )
                or
                # 身杀两停，无官混杀
                    (
                        self.self_strong
                        and '正官' not in self.lord_gods_core_matrix[1][1]
                    )
            ):
                return True, ""

            if (
                # 财当杀而无制
                    (
                        is_finance_exists
                        and '正官' not in self.all_lord_gods
                    )
                or
                # 日干弱
                    (
                        not self.self_strong
                    )
                or
                    # 逢刑冲破害
                    (
                            is_harmful_exists
                    )
            ):

                return False, fix_func

        return True, fix_func

    def calc_fix_func(self, structure_element, structure_gan_details):
        structure_supporting_element = SWAPPED_ELEMENTS_SUPPORTING[structure_element]
        opposing_yin_yang = YIN_YANG_SWAP[structure_gan_details['yinyang']]
        if self.self_strong:
            yin_details = GAN_ELEMENTS_MAPPING[f"{opposing_yin_yang}_{structure_supporting_element}"]
        else:
            yin_details = GAN_ELEMENTS_MAPPING[f"{structure_gan_details['yinyang']}_{structure_supporting_element}"]
        return "建议多接触「{}」，以增强{}的正能量".format(yin_details['meaning'], self.structure)


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
    prediction = LordGodsStructure(
        base_datetime=main_birthday,
        explain_append=explain_append,
        is_male=is_male,
    )
    print(prediction)
