from collections import Counter

from metainfo import MetaInfo
from utils import *


class BaZiElements(MetaInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.primary_element = get_heavenly_stem_element(self.ri_gan)
        self.support_element = SWAPPED_WU_XING_XIANG_SHENG[self.primary_element]
        self.self_strong = self.calc_element_strength()

        self.elements_relationships = self.calc_element_relationship()
        self.elements_weight = self.calc_element_weight()
        elements_weight_rounded = {element: round(weight, 2) for element, weight in self.elements_weight.items()}

        self.elements_relationships_mapping = {
            element: (ELEMENTS_RELATIONS[i], elements_weight_rounded[element])
            for i, element in enumerate(self.elements_relationships)
        }

        self.elements_matrix = [
            [
                self.nian_gan_element, self.yue_gan_element, self.ri_gan_element, self.shi_gan_element
            ],
            [
                self.nian_zhi_element, self.yue_zhi_element, self.ri_zhi_element, self.shi_zhi_element
            ]
        ]

        if self.self_strong:
            self.supporting_elements_sequence = self.elements_relationships[:3]
            self.opposing_elements_sequence = self.elements_relationships[3:]
        else:
            self.supporting_elements_sequence = self.elements_relationships[:2]
            self.opposing_elements_sequence = self.elements_relationships[2:]

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"
        msg += f'''
        五行强弱：{"强" if self.self_strong else "弱"}
        喜用：{self.supporting_elements_sequence}
        忌凶：{self.opposing_elements_sequence}
        '''

        elements_relations = [f"{key}:{value}" for key, value in self.elements_relationships_mapping.items()]
        msg += f'''
        五行运气：
        {"  ".join(elements_relations)}
        '''

        if self.explain_append:
            gan_details = GAN_DETAILS[self.ri_gan]
            msg += f'''
        干支五行解析：
        日主：{self.ri_gan}（{gan_details['yinyang']}{gan_details['element']}）
        {self.append_gan_details(self.ri_gan)}
            '''
            gan_element_details = self.append_element_details(self.ri_gan_element)
            msg += f'''
        {gan_element_details['explain']}
        最佳相处方式：{gan_element_details['company_with']}
            '''

            msg += f'''
        喜用五行：
            '''
        for item in self.supporting_elements_sequence:
            element_details = self.append_element_details(item)
            msg += f'''
        五行：{item}
        幸运色：{element_details['color']}
        幸运数字：{element_details['number']}
        幸运方位：{element_details['direction']}
        适应行业：{element_details['industry']}
            '''

        return msg

    def calc_element_strength(self):
        """
        五行相生记正分，相同记正分，相克记负分
        如果八字的加分大于50则为身强，扣分大于50则为身弱。
        :return:
        """

        positive_weight = 0
        negative_weight = 0
        for row in range(len(self.element_matrix)):
            for col in range(len(self.element_matrix[row])):
                if self.element_matrix[row][col] in [self.primary_element, self.support_element]:
                    positive_weight += GAN_ZHI_WU_XING_WEIGHT[row][col]
                else:
                    negative_weight -= GAN_ZHI_WU_XING_WEIGHT[row][col]

        if positive_weight > 50:
            return True
        elif negative_weight < -50:
            return False
        return False

    def calc_element_relationship(self):
        """
        运气公式：
        |名称|变化|身强|身弱|
        |:-:|:-:|:-:|:-:|
        |旺|快涨|我生的|同我的|
        |相|慢涨|我克的|生我的|
        |休|横盘|克我的|我生的|
        |囚|慢跌|生我的|我克的|
        |死|快跌|同我的|克我的|
        :return:
        """
        elements_sequence = []
        if self.self_strong:
            elements_sequence.append(WU_XING_XIANG_SHENG[self.primary_element])
            elements_sequence.append(WU_XING_XIANG_KE[self.primary_element])
            elements_sequence.append(SWAPPED_WU_XING_XIANG_KE[self.primary_element])
            elements_sequence.append(SWAPPED_WU_XING_XIANG_SHENG[self.primary_element])
            elements_sequence.append(self.primary_element)
        else:
            elements_sequence.append(self.primary_element)
            elements_sequence.append(SWAPPED_WU_XING_XIANG_SHENG[self.primary_element])
            elements_sequence.append(WU_XING_XIANG_SHENG[self.primary_element])
            elements_sequence.append(SWAPPED_WU_XING_XIANG_KE[self.primary_element])
            elements_sequence.append(WU_XING_XIANG_KE[self.primary_element])

        return elements_sequence

    def calc_element_weight(self):
        ba_zi_elements_list = [
            self.nian_gan_element, self.nian_zhi_element,
            self.yue_gan_element, self.yue_zhi_element,
            self.ri_gan_element, self.ri_zhi_element,
            self.shi_gan_element, self.shi_zhi_element
        ]

        elements_count = Counter(ba_zi_elements_list)

        elements_weight = {}
        element_to_index = {element: idx for idx, element in enumerate(self.elements_relationships)}
        for element, idx in element_to_index.items():
            elements_weight[element] = round((elements_count[element] / 8), 2)
            elements_weight[element] += ELEMENTS_POSITION_DELTA[idx]
            elements_weight[element] += ZODIAC_ELEMENT_WEIGHT if element == self.zodiac_element else 0

        return elements_weight

    def append_element_details(self, zhu):
        conditions = {
            '木': {
                'explain': "木主慈，以仁为主。名日曲直，体形曲而直立。",
                'color': "绿色/青色",
                'number': "3/8",
                'direction': "东",
                'symbol': '长方形',
                'industry': '“湿柔滋生仁正”\n特点:文教性、宗教性、新生性、恻隐性、植物性\n'
                            '举例：文化文艺、文学作家、书画雕刻艺术家、印刷出版、教育培训、\n'
                            '教员院校、文具书籍、山林纸业、植物种植、农作物、蔬菜果品、繁殖种子、\n'
                            '木器木材、包装、纸竹藤业、花艺园艺、宗教业界及用品、香料店、中医中药、\n'
                            '素食品店、纺织制衣、布面料、报纸杂志、社工护理、护士、刺青纹眉、妇幼保健、\n'
                            '免疫防疫、医疗医务、妇产科。',
                'company_with': '装可怜、共情、卖惨、吃软不吃硬',
            },
            '火': {
                'explain': "火主礼，名日炎上，为向上发光、发热、温暖之意。",
                'color': "红色、赤色、橋红色、粉红色",
                'number': "2/7",
                'direction': "南",
                'symbol': '三角形',
                'industry': '“明热旺熟礼仪”\n特点:热能性、光电性、燃热性、礼仪性、火爆性\n'
                            '举例：煤炭电力、石油煤气、易燃品、化工原料制品、爆破炸药、\n'
                            '冶炼焊镀热加工、加油站、电机电源电池、电气电工、电线光纤电缆、\n'
                            '光电产品、玻璃光学类、照相影印、灯饰照明类、热水器、食用油、\n'
                            '油炸热饮食小吃、酒楼饭店快餐、食品加工、理烫发美容、手工艺品、\n'
                            '服饰衣帽物品、化妆品礼品、婚庆礼仪、家用电器电脑、公关、培训。',
                'company_with': '夸赞，彩虹屁，避免硬碰硬',
            },
            '土': {
                'explain': "土主信， 土日稼穑，为生券万物、券育、孕育之意",
                'color': "黄色、咖啡色、茶色、褐色",
                'number': "5/10（0）",
                'direction': "中",
                'symbol': '方形',
                'industry': '“含实通转信用”\n特点:包含性、稳定性、基础性、土地性、中介性\n'
                            '举例：房地产、建筑业、不动产业及其保险、挖掘采矿业、水泥石沙砖瓦、\n'
                            '土地开垦、山地农村、农蓄牧业及其人员、饲料肥料业、土特产、粮食经营、\n'
                            '营养师、考古、陶瓷业、古玩业、各种中介业、代理咨询、经纪人、律师会计行、\n'
                            '鉴定、服务业、仓储业、丧事墓地业、慈善福利业、托儿养老业、纪念馆。',
                'company_with': '遵守承诺，给与足够的信任',
            },
            '金': {
                'explain': "金主义，金日从革，为变革、肃清之意。",
                'color': "白色、金色",
                'number': "4/9",
                'direction': "西",
                'symbol': '圆形',
                'industry': '“强燥敛收裁决”\n特点:金属性、机器加工性、决断性、权威性、操控性\n'
                            '举例：金属材料及制品、冶金五金、机械及加工、工具仪器、电子零器件、\n'
                            '通讯器材、钟表、制造工程、汽車业、造船业、珠宝玉石加工、金融财会、\n'
                            '股票债券、保险投资、证券信托、军警保卫、武术、公检法、企业领导、\n'
                            '节目主持、导演、制片商、演说家、评论家、编辑。',
                'company_with': '主动承担责任，讲义气，动之以情，不要晓之以理',
            },
            '水': {
                'explain': "水主智，水称为润下，为滋润万物、寒冷向下之意",
                'color': "黑色",
                'number': "1/6",
                'direction': "北",
                'symbol': '波浪形',
                'industry': '“寒虚伏藏聪慧”\n特点:智慧性、流动性、娱乐性、水属性、寒散性\n'
                            '举例：各类设计、科研开发、策划创作、软件业、广告传媒业、贸易商务、\n'
                            '商业百货、会展业、流动贩售、运输仓储、快递搬家、交通航空航运、导游旅游、\n'
                            '运动体育、音乐舞蹈、影歌星演艺圈、声乐、戏剧院、歌舞厅、茶室咖啡厅、河湖池塘、\n'
                            '水利水务、打捞码头、涉水产类、钓具、冷藏速冻、酒业饮料、印染业、清洁环保、\n'
                            '洗衣洗车、泳池浴池、洗涤剂、化妆品、旅社酒店、电子商务、通讯通信经营业。',
                'company_with': '多包容、以理服人、温和处事',
            },
        }
        return conditions[zhu]

    def append_gan_details(self, gan):
        conditions = {
            '甲': '有恻隐之心、上进心、有情有义、喜欢为人挺身而出、说话直、善良，但缺乏应变能力、做事多劳苦',
            '乙': '富有同情心、温柔、苗条、但内心占有欲强、独立性差、多虑',
            '丙': '朝气蓬勃、热情开朗、适合社交活动、懂礼貌、爱面子、没耐心、易被误解为好大喜功',
            '丁': '外静内进、思想缜密、讲文明、给人启示、但是多疑与心机',
            '戊': '诚实、厚重沉稳、为人憨直、有主见、有持久力、但是固执',
            '己': '重视内涵、多才多艺、行事依规蹈矩、但度量欠广，易生疑心',
            '庚': '精神粗旷豪爽、意气轻燥、性情刚烈而重义气，个性好胜、具有破坏性、人缘佳、易相处',
            '辛': '阴沉，温润秀气、重感情、虛荣心强而爱好面子、有强烈的自尊心、但缺乏坚强的意志',
            '壬': '清浊并容，宽宏大度、能潜伏和包容，富于勇气、但依赖性强、漫不经心',
            '癸': '平静柔和、内向、勤勉力行、但爱好猜臆、注重原则不务实际、时有破坏性、重情调、喜钻牛角尖',
        }
        return conditions[gan]
