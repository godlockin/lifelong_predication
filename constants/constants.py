from datetime import datetime
import pytz

chinese_date_format = "yyyy-MM-dd"
default_date_format = "%Y-%m-%d %H:%M:%S"
BASE_DATE = datetime(1900, 1, 31, 0, 0, 0, tzinfo=pytz.timezone('Asia/Shanghai'))

# 干支，纳音，岁数，男，女
GAN_ZHI_SOUND_GANDER_MAPPING = [
    ["丙戌", "屋上土", "1", "3", "3"],
    ["乙酉", "泉中水", "2", "4", "2"],
    ["甲申", "泉中水", "3", "5", "1"],
    ["癸未", "杨柳木", "4", "6", "9"],
    ["壬午", "杨柳木", "5", "7", "8"],
    ["辛巳", "白蜡金", "6", "8", "7"],
    ["庚辰", "白蜡金", "7", "9", "6"],
    ["己卯", "城墙土", "8", "1", "5"],
    ["戊寅", "城墙土", "9", "2", "4"],
    ["丁丑", "涧下水", "10", "3", "3"],
    ["丙子", "涧下水", "11", "4", "2"],
    ["乙亥", "山头火", "12", "5", "1"],
    ["甲戌", "山头火", "13", "6", "9"],
    ["癸酉", "剑锋金", "14", "7", "8"],
    ["壬申", "剑锋金", "15", "8", "7"],
    ["辛未", "路旁土", "16", "9", "6"],
    ["庚午", "路旁土", "17", "1", "5"],
    ["己巳", "大林木", "18", "2", "4"],
    ["戊辰", "大林木", "19", "3", "3"],
    ["丁卯", "炉中火", "20", "4", "2"],
    ["丙寅", "炉中火", "21", "5", "1"],
    ["乙丑", "海中金", "22", "6", "9"],
    ["甲子", "海中金", "23", "7", "8"],
    ["癸亥", "大海水", "24", "8", "7"],
    ["壬戌", "大海水", "25", "9", "6"],
    ["辛酉", "石榴木", "26", "1", "5"],
    ["庚申", "石榴木", "27", "2", "4"],
    ["己未", "天上火", "28", "3", "3"],
    ["戊午", "天上火", "29", "4", "2"],
    ["丁巳", "沙中土", "30", "5", "1"],
    ["丙辰", "沙中土", "31", "6", "9"],
    ["乙卯", "大溪水", "32", "7", "8"],
    ["甲寅", "大溪水", "33", "8", "7"],
    ["癸丑", "桑松木", "34", "9", "6"],
    ["壬子", "桑松木", "35", "1", "5"],
    ["辛亥", "钗钏金", "36", "2", "4"],
    ["庚戌", "钗钏金", "37", "3", "3"],
    ["己酉", "大驿土", "38", "4", "2"],
    ["戊申", "大驿土", "39", "5", "1"],
    ["丁未", "天河水", "40", "6", "9"],
    ["丙午", "天河水", "41", "7", "8"],
    ["乙巳", "佛灯火", "42", "8", "7"],
    ["甲辰", "佛灯火", "43", "9", "6"],
    ["癸卯", "金箔金", "44", "1", "5"],
    ["壬寅", "金箔金", "45", "2", "4"],
    ["辛丑", "壁上土", "46", "3", "3"],
    ["庚子", "壁上土", "47", "4", "2"],
    ["己亥", "平地木", "48", "5", "1"],
    ["戊戌", "平地木", "49", "6", "9"],
    ["丁酉", "山下火", "50", "7", "8"],
    ["丙申", "山下火", "51", "8", "7"],
    ["乙未", "沙中金", "52", "9", "6"],
    ["甲午", "沙中金", "53", "1", "5"],
    ["癸巳", "长流水", "54", "2", "4"],
    ["壬辰", "长流水", "55", "3", "3"],
    ["辛卯", "松柏木", "56", "4", "2"],
    ["庚寅", "松柏木", "57", "5", "1"],
    ["己丑", "霹雳火", "58", "6", "9"],
    ["戊子", "霹雳火", "59", "7", "8"],
    ["丁亥", "屋上土", "60", "8", "7"],
]

# 甲子 -》 纳音
GAN_ZHI_SOUND_MAPPING = {item[0]: item[1] for item in GAN_ZHI_SOUND_GANDER_MAPPING}

# 甲子 -》 宫卦（分男女）
GAN_ZHI_SOUND_GONG_GUA_MAPPING = {item[0]: (item[3], item[4]) for item in GAN_ZHI_SOUND_GANDER_MAPPING}

GONG_GUA = [["伏位", "绝命", "天医", "生气", "六煞", "祸害", "五鬼", "延年"],
            ["绝命", "伏位", "祸害", "五鬼", "延年", "天医", "生气", "六煞"],
            ["天医", "祸害", "伏位", "延年", "五鬼", "绝命", "六煞", "生气"],
            ["生气", "五鬼", "延年", "伏位", "祸害", "六煞", "绝命", "天医"],
            ["六煞", "延年", "五鬼", "祸害", "伏位", "生气", "天医", "绝命"],
            ["祸害", "天医", "绝命", "六煞", "生气", "伏位", "延年", "五鬼"],
            ["五鬼", "生气", "六煞", "绝命", "天医", "延年", "伏位", "祸害"],
            ["延年", "六煞", "生气", "天医", "绝命", "五鬼", "祸害", "伏位"], ]

GOD_LIST_PRIMARY = [
    ["碎", "狼籍", "飞天", "八败", "大狼籍", "大败", "相冲", "劫煞", "咸池", "头蒂", "再嫁", "女扫男家", "男扫女家",
     "女破男家", "男破女家", "生年"],
    ["四", "三", "二", "六", "五", "四", "八", "四", "八", "五", "五", "十二", "正", "六", "二", "子"],
    ["十二", "七", "正", "九", "八", "七", "九", "正", "五", "六", "六", "九", "六", "四", "三", "丑"],
    ["八", "六", "五", "十二", "十一", "十", "十", "十", "二", "七", "七", "七", "四", "三", "十", "寅"],
    ["四", "六", "五", "十二", "十二", "十", "十一", "七", "十一", "八", "八", "八", "二", "正", "五", "卯"],
    ["十二", "二", "三", "六", "五", "四", "十二", "四", "八", "九", "九", "十二", "正", "六", "十二", "辰"],
    ["八", "二", "三", "六", "五", "四", "正", "正", "五", "十", "十", "九", "六", "四", "正", "巳"],
    ["四", "六", "五", "十二", "十一", "十", "八", "十", "二", "十一", "十一", "七", "四", "三", "八", "午"],
    ["十二", "十一", "十", "三", "二", "正", "九", "七", "十一", "十二", "十二", "八", "二", "正", "九", "未"],
    ["八", "七", "正", "三", "八", "七", "十", "四", "八", "正", "正", "十二", "正", "六", "四", "申"],
    ["四", "七", "正", "三", "八", "七", "十一", "正", "五", "六", "六", "九", "六", "四", "十一", "酉"],
    ["十二", "十一", "十", "九", "二", "正", "十二", "十", "二", "四", "四", "七", "四", "三", "六", "戌"],
    ["八", "十一", "十", "九", "二", "正", "正", "七", "十一", "二", "二", "八", "二", "正", "七", "亥"], ]

GOD_LIST_SECONDARY = [
    ["旺门寡", "多厄", "女妨夫", "望门", "多厄", "男妨妻", "胞胎", "亡神", "脚踏", "绝房", "重婚", "寡宿", "孤辰",
     "小狼籍", "小狼籍", "生年"],
    ["十", "八九", "金", "七", "五六", "金", "二", "十", "四", "十一", "四", "九", "正", "九", "四", "子"],
    ["正", "十一十二", "无", "正", "二三", "木", "三", "七", "五", "二", "五", "九", "正", "十", "八", "丑"],
    ["四", "二三", "无", "十", "八九", "水", "四", "四", "六", "七", "六", "十二", "四", "十二", "十", "寅"],
    ["四", "五六", "无", "正", "十一十二", "火", "五", "正", "七", "十一", "七", "十二", "四", "九", "四", "卯"],
    ["七", "无", "土命", "四", "二三", "土", "六", "十", "八", "二", "八", "十二", "四", "九", "四", "辰"],
    ["无", "无", "无", "无", "无", "无", "七", "七", "九", "七", "九", "三", "七", "十二", "十", "巳"],
    ["无", "无", "无", "无", "无", "无", "二", "四", "十", "十一", "十", "三", "七", "六", "二", "午"],
    ["无", "无", "无", "无", "无", "无", "三", "正", "十一", "二", "十一", "三", "七", "十", "八", "未"],
    ["无", "无", "无", "无", "无", "无", "四", "十", "十二", "七", "十二", "六", "十", "十", "八", "申"],
    ["无", "无", "无", "无", "无", "无", "五", "七", "正", "十一", "正", "六", "十", "六", "二", "酉"],
    ["无", "无", "无", "无", "无", "无", "六", "四", "二", "二", "二", "六", "十", "六", "二", "戌"],
    ["无", "无", "无", "无", "无", "无", "七", "七", "三", "七", "三", "九", "正", "二", "十", "亥"], ]

CHINESE_MONTH_NAME = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "腊"]

CHINESE_WORD = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]

CHINESE_TEN = ["初", "十", "廿", "卅"]

# 天干五合（争合） 甲己合化土；乙庚合化金；丙辛合化水；丁壬合化木；戊癸合化火。
TIAN_GAN_HE = [
    ("甲己", "土"),
    ("乙庚", "金"),
    ("丙辛", "水"),
    ("丁壬", "木"),
    ("戊癸", "火"),
]

# 甲庚 乙辛 丙壬 丁癸（土无冲）
TIAN_GAN_CHONG = [
    "甲庚",
    "乙辛",
    "丙壬",
    "丁癸",
]
TIAN_GAN_CHONG_MAPPING = {
    "甲": "庚",
    "庚": "甲",
    "乙": "辛",
    "辛": "乙",
    "丙": "壬",
    "壬": "丙",
    "丁": "癸",
    "癸": "丁",
}

YIN_YANG = ["阳", "阴"]
YIN_YANG_SWAP = {
    "阳": "阴",
    "阴": "阳",
}

# |种类|方向|阴阳|五行|颜色|器官|身体部位|意象|寓意|解释|
GAN_MATRIX = [
    ["甲", "东", "阳", "木", "绿", "肝", "头", "大树", "大林之木", "有参天之势，其性坚质硬，可做栋梁之材，故为阳木。", ],
    ["乙", "东", "阴", "木", "绿", "胆", "肩", "花草", "花草之木", "有娇艳大地之美，其性柔质软，情满人间，故为阴木。", ],
    ["丙", "南", "阳", "火", "红", "小肠", "额", "太阳/圆形物品", "太阳火", "有光明天地之功，其性猛烈，欺雪侮霜，普照万物，故为阳火。", ],
    ["丁", "南", "阴", "火", "红", "心脏/血液", "齿舌", "蜡烛、灯泡、烟头", "太阴火", "有明照千家万户之功，其性柔质弱，为人不为己，故为阴火。", ],
    ["戊", "中间", "阳", "土", "黄", "胃", "鼻", "城墙土", "城垣之土", "为万物司令，其性高亢质，硬而向阳，生育万物，故为阳土。", ],
    ["己", "中间", "阴", "土", "黄", "脾", "面", "田地", "田园之土", "有培木止水之能。其性湿质软，低洼向阴，造福人间，故为阴土。", ],
    ["庚", "西", "阳", "金", "白/金", "大肠", "筋", "宝剑、大刀、汽车", "剑戟", "有刚健肃杀之力。其性刚质硬，肃杀万物，故为阳金。", ],
    ["辛", "西", "阴", "金", "白/金", "肺", "胸", "首饰、小型金属饰品", "珠玉", "有镶嵌珠宝之用。其性温柔，质温清韵，装饰人间，故为阴金。", ],
    ["壬", "北", "阳", "水", "黑/蓝", "膀胱", "胫", "(大水)江河湖海", "江、河、湖、海", "通天河而周流不息，其性猛质硬，灌溉万物，故为阳水。", ],
    ["癸", "北", "阴", "水", "黑/蓝", "肾", "足", "(小水)溪、井、小河、露水、下水道", "雨露之水", "润物无声，其性柔质软，润泽万物，故为阴水。",]
]
GAN_DETAILS = {line[0]: {
    "gan": line[0],
    "direction": line[1],
    "yinyang": line[2],
    "element": line[3],
    "color": line[4],
    "organ": line[5],
    "body_part": line[6],
    "image": line[7],
    "meaning": line[8],
    "explanation": line[9],
} for line in GAN_MATRIX}
GAN = list(GAN_DETAILS.keys())

GAN_ELEMENTS_MAPPING = {
    f"{line[2]}_{line[3]}": {
        "gan": line[0],
        "direction": line[1],
        "yinyang": line[2],
        "element": line[3],
        "color": line[4],
        "organ": line[5],
        "body_part": line[6],
        "image": line[7],
        "meaning": line[8],
        "explanation": line[9],
    } for line in GAN_MATRIX
}

# 子丑合土，寅亥合木，卯戌合火，辰酉合金，巳申合水，午未合土。
DI_ZHI_HE = [
    ("子丑", "土"),
    ("寅亥", "木"),
    ("卯戌", "火"),
    ("辰酉", "金"),
    ("巳申", "水"),
    ("午未", "土"),
]

# 子午相冲，丑未相冲，寅申相冲，卯酉相冲，辰戌相冲，巳亥相冲
# 是地支相克意思，它们之间可以相互制约。 冲库表示打开。冲 人际关系不合 突然间矛盾 突然间发生。
DI_ZHI_CHONG = [
    "子午",
    "丑未",
    "寅申",
    "卯酉",
    "辰戌",
    "巳亥",
]

# 子未相害，丑午相害，寅巳相害，卯辰相害，申亥相害，酉戌相害
# 穿害表示互相折磨，长期损耗。
DI_ZHI_HAI = [
    "子未",
    "丑午",
    "寅巳",
    "卯辰",
    "申亥",
    "酉戌",
]

# 地支相刑子卯相刑，丑未戌相刑，寅巳申相刑，辰午酉亥自刑。
# 吵架 很快能和好 对自己伤害小
DI_ZHI_XING = [
    "子卯",
    "丑未",
    "丑未戌",
    "寅巳申",
    "辰午酉亥",
]

# 寅午戌三合火局，申子辰三合水局，亥卯未三合木局，巳酉丑三合金局
DI_ZHI_SAN_HE = [
    ('寅午戌', '火'),
    ('申子辰', '水'),
    ('亥卯未', '木'),
    ('巳酉丑', '金'),
]

# 寅卯辰东方木局，巳午未南方火局，申酉戌西方金局，亥子丑北方水局
# 三合三会是力量的聚集 牢不可破
DI_ZHI_SAN_HUI = [
    ('寅卯辰', '东方', '木'),
    ('巳午未', '南方', '火'),
    ('申酉戌', '西方', '金'),
    ('亥子丑', '北方', '水'),
]

# 寅辰拱会木局，巳未拱会火局，申戌拱会金局，亥丑拱会水局。
DI_ZHI_GONG_HUI = [
    ('寅辰', '木'),
    ('巳未', '火'),
    ('申戌', '金'),
    ('亥丑', '水'),
]

# 亥未拱木局，寅戌拱火局，巳丑拱金局，申辰拱水局。
DI_ZHI_GONG_HE = [
    ('亥未', '木'),
    ('寅戌', '火'),
    ('巳丑', '金'),
    ('申辰', '水'),
]

# |种类|方向|颜色|阴阳|五行|月份|时间|藏天干|生肖|器官|身体部位|
ZHI_MATRIX = [
    ["子", "正北", "黑/蓝", "阳", "水", "阴历11月", "23点～凌晨1点", "癸", "鼠", "膀胱", "耳", ],
    ["丑", "东北", "黄", "阴", "土", "阴历12月", "凌晨1～3点", "己辛癸", "牛", "脾", "胞肚", ],
    ["寅", "东北", "绿", "阳", "木", "阴历1月", "凌晨3～5点", "甲丙戊", "虎", "胆", "手", ],
    ["卯", "正东", "绿", "阴", "木", "阴历2月", "凌晨5～7点", "乙", "兔", "肝", "指", ],
    ["辰", "东南", "黄", "阳", "土", "阴历3月", "7～9点", "戊乙癸", "龙", "胃", "肩胸", ],
    ["巳", "东南", "红", "阴", "火", "阴历4月", "9～11点", "丙戊庚", "蛇", "心", "面/咽齿", ],
    ["午", "正南", "红", "阳", "火", "阴历5月", "11～13点", "丁己", "马", "小肠", "眼", ],
    ["未", "西南", "黄", "阴", "土", "阴历6月", "13～15点", "己丁乙", "羊", "脾", "脊梁", ],
    ["申", "西南", "白/金", "阳", "金", "阴历7月", "15～17点", "庚壬戊", "猴", "大肠", "经络", ],
    ["酉", "正西", "白/金", "阴", "金", "阴历8月", "17～19点", "辛", "鸡", "肺", "精血", ],
    ["戌", "西北", "黄", "阳", "土", "阴历9月", "19～21点", "戊辛丁", "狗", "胃", "命门、腿、足", ],
    ["亥", "西北", "蓝/黑", "阴", "水", "阴历10月", "21～23点", "壬甲", "猪", "肾", "头", ],
]
ZHI_DETAILS = {line[0]: {
    "zhi": line[0],
    "direction": line[1],
    "color": line[2],
    "yinyang": line[3],
    "element": line[4],
    "month": line[5],
    "time": line[6],
    "cang_tian_gan": line[7],
    "zodiac": line[8],
    "organ": line[9],
    "body_part": line[10],
} for line in ZHI_MATRIX}
ZHI = list(ZHI_DETAILS.keys())

ZHI_ELEMENTS_MAPPING = {
    f"{line[3]}_{line[4]}": {
        "zhi": line[0],
        "direction": line[1],
        "color": line[2],
        "yinyang": line[3],
        "element": line[4],
        "month": line[5],
        "time": line[6],
        "cang_tian_gan": line[7],
        "zodiac": line[8],
        "organ": line[9],
        "body_part": line[10],
    }
    for line in ZHI_MATRIX
}

CANG_GAN = {
    "子": ["癸", "", "", ],
    "卯": ["乙", "", "", ],
    "午": ["丁", "己", "", ],
    "酉": ["辛", "", "", ],
    "寅": ["甲", "丙", "戊", ],
    "巳": ["丙", "戊", "庚", ],
    "申": ["庚", "壬", "戊", ],
    "亥": ["壬", "甲", "", ],
    "丑": ["己", "癸", "辛", ],
    "辰": ["戊", "乙", "癸", ],
    "未": ["己", "丁", "乙", ],
    "戌": ["戊", "辛", "丁", ],
}

LUNAR_INFO = [0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0, 0x09ad0, 0x055d2,
              0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540, 0x0d6a0, 0x0ada2, 0x095b0, 0x14977,
              0x04970, 0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970,
              0x06566, 0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
              0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2, 0x0a950, 0x0b557,
              0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5d0, 0x14573, 0x052d0, 0x0a9a8, 0x0e950, 0x06aa0,
              0x0aea6, 0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0,
              0x096d0, 0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b5a0, 0x195a6,
              0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46, 0x0ab60, 0x09570,
              0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58, 0x055c0, 0x0ab60, 0x096d5, 0x092e0,
              0x0c960, 0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5,
              0x0a950, 0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
              0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260, 0x0ea65, 0x0d530,
              0x05aa0, 0x076a3, 0x096d0, 0x04bd7, 0x04ad0, 0x0a4d0, 0x1d0b6, 0x0d250, 0x0d520, 0x0dd45,
              0x0b5a0, 0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0
              ]

JIA_ZI_NAME = [
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉",
    "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午", "癸未",
    "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳",
    "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑", "壬寅", "癸卯",
    "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑",
    "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申", "辛酉", "壬戌", "癸亥"
]

SHENG_XIAO = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# 专门为了计算勾绞煞用的地支序列
DI_ZHI = ["　", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

TIAN_GAN_SHENG_SI_JUE_WANG = ["甲", "丙", "戊", "庚", "壬", "乙", "丁", "己", "辛", "癸"]

LORD_GODS_MATRIX = [
    ["日/干", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],
    ["甲", "比肩", "劫财", "食神", "伤官", "偏财", "正财", "七杀", "正官", "偏印", "正印"],
    ["乙", "劫财", "比肩", "伤官", "食神", "正财", "偏财", "正官", "七杀", "正印", "偏印"],
    ["丙", "偏印", "正印", "比肩", "劫财", "食神", "伤官", "偏财", "正财", "七杀", "正官"],
    ["丁", "正印", "偏印", "劫财", "比肩", "伤官", "食神", "正财", "偏财", "正官", "七杀"],
    ["戊", "七杀", "正官", "偏印", "正印", "比肩", "劫财", "食神", "伤官", "偏财", "正财"],
    ["己", "正官", "七杀", "正印", "偏印", "劫财", "比肩", "伤官", "食神", "正财", "偏财"],
    ["庚", "偏财", "正财", "七杀", "正官", "偏印", "正印", "比肩", "劫财", "食神", "伤官"],
    ["辛", "正财", "偏财", "正官", "七杀", "正印", "偏印", "劫财", "比肩", "伤官", "食神"],
    ["壬", "食神", "伤官", "偏财", "正财", "七杀", "正官", "偏印", "正印", "比肩", "劫财"],
    ["癸", "伤官", "食神", "正财", "偏财", "正官", "七杀", "正印", "偏印", "劫财", "比肩"],
]
LORD_GODS_DETAILS = {item[0]: {
    item[1]: LORD_GODS_MATRIX[0][1],
    item[2]: LORD_GODS_MATRIX[0][2],
    item[3]: LORD_GODS_MATRIX[0][3],
    item[4]: LORD_GODS_MATRIX[0][4],
    item[5]: LORD_GODS_MATRIX[0][5],
    item[6]: LORD_GODS_MATRIX[0][6],
    item[7]: LORD_GODS_MATRIX[0][7],
    item[8]: LORD_GODS_MATRIX[0][8],
    item[9]: LORD_GODS_MATRIX[0][9],
    item[10]: LORD_GODS_MATRIX[0][10],
} for item in LORD_GODS_MATRIX[1:]}

SHENG_SI_JUE_WANG_MAPPING = [
    ["天干", "长生", "沐浴", "冠带", "临官", "帝旺", "衰", "病", "死", "墓", "绝", "胎", "养"],
    ["甲", "亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌"],
    ["丙", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"],
    ["戊", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"],
    ["庚", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑", "寅", "卯", "辰"],
    ["壬", "申", "酉", "戌", "亥", "子", "丑", "寅", "卯", "辰", "巳", "午", "未"],
    ["乙", "午", "巳", "辰", "卯", "寅", "丑", "子", "亥", "戌", "酉", "申", "未"],
    ["丁", "酉", "申", "未", "午", "巳", "辰", "卯", "寅", "丑", "子", "亥", "戌"],
    ["己", "酉", "申", "未", "午", "巳", "辰", "卯", "寅", "丑", "子", "亥", "戌"],
    ["辛", "子", "亥", "戌", "酉", "申", "未", "午", "巳", "辰", "卯", "寅", "丑"],
    ["癸", "卯", "寅", "丑", "子", "亥", "戌", "酉", "申", "未", "午", "巳", "辰"],
]

JIE_QI = ["春分", "清明", "谷雨", "立夏", "小满", "芒种", "夏至", "小暑", "大暑", "立秋", "处暑", "白露",
          "秋分", "寒露", "霜降", "立冬", "小雪", "大雪", "冬至", "小寒", "大寒", "立春", "雨水", "惊蛰"]

# 金主义 木主仁 水主智 土主信 火主礼
WU_XING_ZHU_YI = {
    "金": "义",
    "木": "仁",
    "水": "智",
    "土": "信",
    "火": "礼",
}

# 相生关系为：金生水，水生木，木生火，火生土，土生金
ELEMENTS_SUPPORTING = {
    "金": "水",
    "水": "木",
    "木": "火",
    "火": "土",
    "土": "金",
}
SWAPPED_ELEMENTS_SUPPORTING = {value: key for key, value in ELEMENTS_SUPPORTING.items()}

# 相克关系为：火克金，金克木，木克土，土克水，水克火
ELEMENTS_OPPOSING = {
    "火": "金",
    "金": "木",
    "木": "土",
    "土": "水",
    "水": "火",
}
SWAPPED_ELEMENTS_OPPOSING = {value: key for key, value in ELEMENTS_OPPOSING.items()}

GAN_ZHI_POSITION_WEIGHT = [
    [8, 12, 0, 12],
    [4, 40, 12, 12]
]

ELEMENTS_RELATIONS = ["快涨", "慢涨", "横盘", "慢跌", "快跌"]
ELEMENTS_POSITION_DELTA = [1.4, 1.2, 0.9, -0.8, -1.2]

ZODIAC_ELEMENT_WEIGHT = 0.1

ELEMENTS_ORGAN_STRENGTH = ["强壮", "较强壮", "一般", "较弱", "弱"]

CANG_GAN_WEIGHT = [1, 0.6, 0.2]

POSITION_WEIGHT = [
    [2, 2, 0, 2],
    [1, 4, 1, 1],
]

POSITION_NAMES = [
    ["年干", "月干", "日干", "时干"],
    ["年支", "月令", "日支", "时支"],
]

POSITION_COLUMN_NAMES = ['年柱', '月柱', '日柱', '时柱']

LIFE_WEIGHT_MAPPING = {"2.1": "短命非业谓大凶，平生灾难事重重，凶祸频临限逆境，终世困苦事不成",
                       "2.2": "身寒骨冷苦伶仃，此命推来行乞人，劳劳碌碌无度日，中年打拱过平生",
                       "2.3": "此命推来骨轻轻，求谋做事事难成，妻儿兄弟应难许，别处他乡作散人",
                       "2.4": "此命推来福禄无，门庭困苦总难荣，六亲骨肉皆无靠，流到他乡作老人",
                       "2.5": "此命推来祖业微，门庭营度似希奇，六亲骨肉如水炭，一世勤劳自把持",
                       "2.6": "平生一路苦中求，独自营谋事不休，离祖出门宜早计，晚来衣禄自无忧",
                       "2.7": "一生做事少商量，难靠祖宗作主张，独马单枪空作去，早年晚岁总无长",
                       "2.8": "一生作事似飘蓬，祖宗产业在梦中，若不过房并改姓，也当移徒二三通",
                       "2.9": "初年运限未曾亨，纵有功名在后成，须过四旬方可上，移居改姓使为良",
                       "3": "劳劳碌碌苦中求，东走西奔何日休，若能终身勤与俭，老来稍可免忧愁",
                       "3.1": "忙忙碌碌苦中求，何日云开见日头，难得祖基家可立，中年衣食渐无忧",
                       "3.2": "初年运错事难谋，渐有财源如水流，到的中年衣食旺，那时名利一齐来",
                       "3.3": "早年做事事难成，百计徒劳枉费心，半世自如流水去，后来运到始得金",
                       "3.4": "此命福气果如何，僧道门中衣禄多，离祖出家方得妙，终朝拜佛念弥陀",
                       "3.5": "生平福量不周全，祖业根基觉少传，营事生涯宜守旧，时来衣食胜从前",
                       "3.6": "不须劳碌过平生，独自成家福不轻，早有福星常照命，任君行去百般成",
                       "3.7": "此命般般事不成，弟兄少力自孤成，虽然祖业须微有，来的明时去的暗",
                       "3.8": "一生骨肉最清高，早入学门姓名标，待看年将三十六，蓝衣脱去换红袍",
                       "3.9": "此命少年运不通，劳劳做事尽皆空，苦心竭力成家计，到得那时在梦中",
                       "4": "平生衣禄是绵长，件件心中自主张，前面风霜都受过，从来必定享安泰",
                       "4.1": "此命推来事不同，为人能干异凡庸，中年还有逍遥福，不比前年云未通",
                       "4.2": "得宽怀处且宽怀，何用双眉总不开，若使中年命运济，那时名利一齐来",
                       "4.3": "为人心性最聪明，做事轩昂近贵人，衣禄一生天数定，不须劳碌是丰亨",
                       "4.4": "来事由天莫苦求，须知福禄胜前途，当年财帛难如意，晚景欣然便不忧",
                       "4.5": "福中取贵格求真，明敏才华志自伸，福禄寿全家道吉，桂兰毓秀晚荣臻",
                       "4.6": "东西南北尽皆通，出姓移名更觉隆，衣禄无亏天数定，中年晚景一般同",
                       "4.7": "此命推来旺末年，妻荣子贵自怡然，平生原有滔滔福，可有财源如水流",
                       "4.8": "幼年运道未曾享，苦是蹉跎再不兴，兄弟六亲皆无靠，一身事业晚年成",
                       "4.9": "此命推来福不轻，自立自成显门庭，从来富贵人亲近，使婢差奴过一生",
                       "5": "为利为名终日劳，中年福禄也多遭，老来是有财星照，不比前番目下高",
                       "5.1": "一世荣华事事通，不须劳碌自亨通，兄弟叔侄皆如意，家业成时福禄宏",
                       "5.2": "一世亨通事事能，不须劳思自然能，宗施欣然心皆好，家业丰亨自称心",
                       "5.3": "此格推来气象真，兴家发达在其中，一生福禄安排定，却是人间一富翁",
                       "5.4": "此命推来厚且清，诗书满腹看功成，丰衣足食自然稳，正是人间有福人",
                       "5.5": "走马扬鞭争名利，少年做事废筹论，一朝福禄源源至，富贵荣华显六亲",
                       "5.6": "此格推来礼仪通，一生福禄用无穷，甜酸苦辣皆尝过，财源滚滚稳且丰",
                       "5.7": "福禄盈盈万事全，一生荣耀显双亲，名扬威震人钦敬，处世逍遥似遇春",
                       "5.8": "平生福禄自然来，名利兼全福禄偕，雁塔提名为贵客，紫袍金带走金鞋",
                       "5.9": "细推此格妙且清，必定才高礼仪通，甲第之中应有分，扬鞭走马显威荣",
                       "6": "一朝金榜快提名，显祖荣宗立大功，衣食定然原欲足，田园财帛更丰盈",
                       "6.1": "不做朝中金榜客，定为世上一财翁，聪明天赋经书熟，名显高克自是荣",
                       "6.2": "此名生来福不穷，读书必定显亲荣，紫衣金带为卿相，富贵荣华皆可同",
                       "6.3": "命主为官福禄长，得来富贵定非常，名题金塔传金榜，定中高科天下扬",
                       "6.4": "此格权威不可当，紫袍金带坐高堂，荣华富贵谁能及，积玉堆金满储仓",
                       "6.5": "细推此命福不轻，安国安邦极品人，文绣雕梁政富贵，威声照耀四方闻",
                       "6.6": "此格人间一福人，堆金积玉满堂春，从来富贵由天定，正笏垂绅谒圣君",
                       "6.7": "此名生来福自宏，田园家业最高隆，平生衣禄丰盈足，一世荣华万事通",
                       "6.8": "富贵由天莫苦求，万金家计不须谋，十年不比前番事，祖业根基水上舟",
                       "6.9": "君是人间衣禄星，一生福贵众人钦，纵然福禄由天定，安享荣华过一生",
                       "7": "此命推来福不轻，不须愁虑苦劳心，一生天定衣与禄，富贵荣华过一生",
                       "7.1": "此名生来大不同，公侯卿相在其中，一生自有逍遥福，富贵荣华极品隆",
                       "7.2": "此格世界罕有生，十代积善产此人，天上紫微来照命，统治万民乐太平"}

LIFE_WEIGHT_YEAR_RATIO = {'壬申': 0.7, '乙亥': 0.9, '己巳': 0.5,
                          '甲申': 0.5, '丁亥': 1.6, '辛巳': 0.6,
                          '丙申': 0.5, '己亥': 0.9, '癸巳': 0.7,
                          '戊申': 1.4, '辛亥': 1.7, '乙巳': 0.7,
                          '庚申': 0.8, '癸亥': 0.6, '丁巳': 0.6,
                          '甲子': 1.2, '丁卯': 0.7, '庚午': 0.9,
                          '丙子': 1.6, '己卯': 1.9, '壬午': 0.8,
                          '戊子': 1.5, '辛卯': 1.2, '甲午': 1.5,
                          '庚子': 0.7, '癸卯': 1.2, '丙午': 1.3,
                          '壬子': 0.5, '乙卯': 0.8, '戊午': 1.9,
                          '癸酉': 0.8, '乙丑': 0.9, '戊辰': 1.2,
                          '乙酉': 1.5, '丁丑': 0.8, '庚辰': 1.2,
                          '丁酉': 1.4, '己丑': 0.7, '壬辰': 1.0,
                          '己酉': 0.5, '辛丑': 0.7, '甲辰': 0.8,
                          '辛酉': 1.6, '癸丑': 0.7, '丙辰': 0.8,
                          '辛未': 0.8, '甲戌': 1.5, '丙寅': 0.6,
                          '癸未': 0.7, '丙戌': 0.6, '戊寅': 0.8,
                          '乙未': 0.6, '戊戌': 1.4, '庚寅': 0.9,
                          '丁未': 0.5, '庚戌': 0.9, '壬寅': 0.9,
                          '己未': 0.6, '壬戌': 1.0, '甲寅': 1.2,
                          }

LIFE_WEIGHT_MONTH_RATIO = {'11': 0.9, '10': 0.8, '12': 0.5, '1': 0.6, '3': 1.8, '2': 0.7, '5': 0.5, '4': 0.9, '7': 0.9,
                           '6': 1.6,
                           '9': 1.8, '8': 1.5}

LIFE_WEIGHT_DAY_RATIO = {'24': 0.9, '25': 1.5, '26': 1.8, '27': 0.7, '20': 1.5, '21': 1, '22': 0.9, '23': 0.8,
                         '28': 0.8, '29': 1.6,
                         '1': 0.5, '3': 0.8, '2': 1, '5': 1.6, '4': 1.5, '7': 0.8, '6': 1.5, '9': 0.8, '8': 1.6,
                         '11': 0.9, '10': 1.6,
                         '13': 0.8, '12': 1.7, '15': 1, '14': 1.7, '17': 0.9, '16': 0.8, '19': 0.5, '18': 1.8,
                         '30': 0.6}

LIFE_WEIGHT_HOUR_RATIO = {'24': 1.6, '20': 0.6, '21': 0.6, '22': 0.6, '23': 1.6, '1': 0.6, '3': 0.7, '2': 0.6, '5': 1,
                          '4': 0.7, '7': 0.9,
                          '6': 1, '9': 1.6, '8': 0.9, '11': 1, '10': 1.6, '13': 0.8, '12': 1, '15': 0.8, '14': 0.8,
                          '17': 0.9, '16': 0.8,
                          '19': 0.6, '18': 0.9}

LIFE_PREDICTION_LABELS = [
    'bone_weight',
    'zodiac_explain',
    'lord_gods',
    'lord_gods_structure',
    'demigods',
    'family_support',
    'life_stages_luck',
    'ten_years_luck',
    'yearly_luck',
    'intermarriage',
    'potential_couple',
]

CORE_LIFE_PREDICTION_LABELS = [
    'lord_gods',
    'family_support',
    'life_stages_luck',
]

ZHI_ATTRIBUTES = {
    "子": {"冲": "午", "刑": "卯", "被刑": "卯", "合": ("申", "辰"), "会": ("亥", "丑"), '害': '未', '破': '酉',
           "六": "丑", "暗": "", },
    "丑": {"冲": "未", "刑": "戌", "被刑": "未", "合": ("巳", "酉"), "会": ("子", "亥"), '害': '午', '破': '辰',
           "六": "子", "暗": "寅", },
    "寅": {"冲": "申", "刑": "巳", "被刑": "申", "合": ("午", "戌"), "会": ("卯", "辰"), '害': '巳', '破': '亥',
           "六": "亥", "暗": "丑", },
    "卯": {"冲": "酉", "刑": "子", "被刑": "子", "合": ("未", "亥"), "会": ("寅", "辰"), '害': '辰', '破': '午',
           "六": "戌", "暗": "申", },
    "辰": {"冲": "戌", "刑": "辰", "被刑": "辰", "合": ("子", "申"), "会": ("寅", "卯"), '害': '卯', '破': '丑',
           "六": "酉", "暗": "", },
    "巳": {"冲": "亥", "刑": "申", "被刑": "寅", "合": ("酉", "丑"), "会": ("午", "未"), '害': '寅', '破': '申',
           "六": "申", "暗": "", },
    "午": {"冲": "子", "刑": "午", "被刑": "午", "合": ("寅", "戌"), "会": ("巳", "未"), '害': '丑', '破': '卯',
           "六": "未", "暗": "亥", },
    "未": {"冲": "丑", "刑": "丑", "被刑": "戌", "合": ("卯", "亥"), "会": ("巳", "午"), '害': '子', '破': '戌',
           "六": "午", "暗": "", },
    "申": {"冲": "寅", "刑": "寅", "被刑": "巳", "合": ("子", "辰"), "会": ("酉", "戌"), '害': '亥', '破': '巳',
           "六": "巳", "暗": "卯", },
    "酉": {"冲": "卯", "刑": "酉", "被刑": "酉", "合": ("巳", "丑"), "会": ("申", "戌"), '害': '戌', '破': '子',
           "六": "辰", "暗": "", },
    "戌": {"冲": "辰", "刑": "未", "被刑": "丑", "合": ("午", "寅"), "会": ("申", "酉"), '害': '酉', '破': '未',
           "六": "卯", "暗": "", },
    "亥": {"冲": "巳", "刑": "亥", "被刑": "亥", "合": ("卯", "未"), "会": ("子", "丑"), '害': '申', '破': '寅',
           "六": "寅", "暗": "午", },
}
