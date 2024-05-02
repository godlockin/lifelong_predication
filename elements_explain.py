from constants import *


class ElementsExplain:
    def __init__(self, ba_zi_elements):

        self.ri_gan = ba_zi_elements.ri_gan
        self.ri_gan_element = ba_zi_elements.ri_gan_element
        self.supporting_elements_sequence = ba_zi_elements.supporting_elements_sequence
        self.elements_matrix = ba_zi_elements.elements_matrix

        self.self_element_analysis = self.self_analysis()

        self.elements_count = self.calc_elements_count()
        self.elements_healthy = self.calc_elements_healthy()
        self.elements_healthy_list = sorted(self.elements_healthy.items(), key=lambda x: -x[1]['score'])
        self.self_elements_healthy_analysis = self.elements_healthy_analysis()

    def __str__(self):
        msg = "### 解析"

        msg += self.self_elements_healthy_analysis

        msg += self.self_element_analysis

        return msg

    def calc_elements_count(self):
        elements_count = {
            '金': 0,
            '木': 0,
            '水': 0,
            '火': 0,
            '土': 0,
        }
        for row in self.elements_matrix:
            for element in row:
                elements_count[element] += 1
        return elements_count

    def calc_elements_healthy(self):
        conditions = {
            "木": {
                "organ": "肝",
                "emotion": "怒",
                "positive": "肝火旺盛、胆结石、胆固醇高、甘油三酯",
                "negative": "体力差、易疲劳、睡眠浅、难入睡、多梦、睡眠差（最好戒烟酒）",
            },
            "火": {
                "organ": "心脏、血液",
                "emotion": "喜",
                "positive": "高血压、高血脂、高血糖、心跳快、心血机能弱",
                "negative": "肠炎、贫血、血压低、心率慢、易疲劳、容易近视",
            },
            "土": {
                "organ": "脾胃",
                "emotion": "思",
                "positive": "腹胀、腹痛、腹泻、消化不良",
                "negative": "胃胀、胃炎、胃溃疡、食道炎、皮肤过敏、糖尿病",
            },
            "金": {
                "organ": "肺/呼吸道、大肠",
                "emotion": "忧",
                "positive": "呼吸不畅、胸闷、感冒咳嗽、气喘",
                "negative": "气虚、鼻炎、肠炎、大肠息肉、腹泻、便秘、肺炎",
            },
            "水": {
                "organ": "肾",
                "emotion": "恐",
                "positive": "肾虚、腰痛、尿频、尿急、尿不尽、体寒、体质弱",
                "negative": "肾结石、肾炎、肾病、尿路感染、尿毒症、泌尿系统炎症、思虑过多",
            },
        }

        elements_healthy = {}
        for element, count in self.elements_count.items():
            tmp = conditions[element]
            element_list = [
                element,
                SWAPPED_ELEMENTS_SUPPORTING[element],
                ELEMENTS_SUPPORTING[element],
                ELEMENTS_OPPOSING[element],
                SWAPPED_ELEMENTS_OPPOSING[element],
            ]

            score_list = [self.elements_count[e] * ELEMENTS_POSITION_DELTA[idx] for idx, e in enumerate(element_list)]
            score = round(sum(score_list), 2)

            if score > 3:
                elements_healthy[element] = {
                    "score": score,
                    'count': self.elements_count[element],
                    "status": "旺",
                    "organ": tmp["organ"],
                    "emotion": tmp["emotion"],
                    "hidden_danger": tmp["positive"],
                }
            elif score < 1:
                elements_healthy[element] = {
                    "score": score,
                    'count': self.elements_count[element],
                    "status": "衰",
                    "organ": tmp["organ"],
                    "emotion": tmp["emotion"],
                    "hidden_danger": tmp["negative"],
                }

        return elements_healthy

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
                'element_position': {
                    '金': '领导',
                    '木': '朋友',
                    '水': '贵人',
                    '火': '夫妻',
                    '土': '下属',
                },
            },
            '火': {
                'explain': "火主礼，名日炎上，为向上发光、发热、温暖之意。",
                'color': "红色、赤色、橋红色、粉红色、紫色",
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
                'element_position': {
                    '金': '下属',
                    '木': '贵人',
                    '水': '领导',
                    '火': '朋友',
                    '土': '夫妻',
                },
            },
            '土': {
                'explain': "土主信，土日稼穑，为生券万物、券育、孕育之意",
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
                'element_position': {
                    '金': '夫妻',
                    '木': '领导',
                    '水': '下属',
                    '火': '贵人',
                    '土': '朋友',
                },
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
                'element_position': {
                    '金': '朋友',
                    '木': '下属',
                    '水': '夫妻',
                    '火': '领导',
                    '土': '贵人',
                }
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
                'element_position': {
                    '金': '贵人',
                    '木': '夫妻',
                    '水': '朋友',
                    '火': '下属',
                    '土': '领导',
                },
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

    def self_analysis(self):
        gan_details = GAN_DETAILS[self.ri_gan]
        msg = f'''
        #### 干支五行：
        日主：{self.ri_gan}（{gan_details['yinyang']}{gan_details['element']}）
        {self.append_gan_details(self.ri_gan)}
            '''
        gan_element_details = self.append_element_details(self.ri_gan_element)
        msg += f'''
        {gan_element_details['explain']}
        最佳相处方式：{gan_element_details['company_with']}
        五行人际关系：{gan_element_details['element_position']}
            '''

        msg += f'''
        #### 喜用五行：
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

    def elements_healthy_analysis(self):

        msg = f"""
        五行对应五脏，金主肺，水主肾，木主干，火主心，土主脾。
        如果八字中某一属性过旺(3个或3个以上)，就会导致该五行克的属性太弱，这两个属性都会有对应的疾病隐患，同样如果一个五行没有，也是太弱。
        """
        for item in self.elements_healthy_list:
            details = item[1]
            msg += f"""
        {item[0]}（{details.get('count', 0)}/{details['score']}）：{details['status']}
        所属器官：{details['organ']}
        情绪：{details['emotion']}
        易感症状：{details['hidden_danger']}
            """

        return msg

