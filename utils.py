import constants
from constants import *


def parse_input_datetime_info(config):
    return config.get('base_datetime', constants.BASE_DATE)


def get_calendar_from_string(year, date_format):
    return datetime.strptime(year, date_format)


def get_gong_gua_for_gan_zhi(gan_zhi, is_man=True):
    pair = GAN_ZHI_SOUND_GONG_GUA_MAPPING.get(gan_zhi, ('', ''))
    return pair[0] if is_man else pair[1]


def get_sound_for_gan_zhi(gan_zhi):
    return GAN_ZHI_SOUND_MAPPING.get(gan_zhi, '')


def get_month_chinese_name(month):
    return CHINESE_MONTH_NAME[month - 1]


def get_year_chinese_name(year):
    ys = ""
    index = int(year / 1000)
    ys += CHINESE_WORD[index]
    year = int(year % 1000)
    index = int(year / 100)
    ys += CHINESE_WORD[index]
    year = int(year % 100)
    index = int(year / 10)
    ys += CHINESE_WORD[index]
    year = int(year % 10)
    index = year
    ys += CHINESE_WORD[index]
    return ys


def get_year_index(year):
    return (year - 4) % 12


def get_day_chinese_name(day):
    n = day % 10
    if n == 0:
        n = 9
    else:
        n = day % 10 - 1

    if day > 30:
        return ""

    if day != 10:
        return CHINESE_TEN[int(day / 10)] + CHINESE_MONTH_NAME[n]
    else:
        return "初十"


def get_shi_chen_idx(hour):
    """
    :param hour: 23~1: 0, 1~3: 1, 3~5: 2, 5~7: 3, 7~9: 3 ... 21~23: 11
    :return:
    """
    return (hour + 1) % 24 // 2
    # return hour // 2


def get_gan_zhi_for_year(lunar_year):
    # 1864年是甲子年，每隔六十年一个甲子
    idx = (lunar_year - 1864) % 60
    # 没有过春节的话那么年还算上一年的，此处求的年份的干支
    return JIA_ZI_NAME[idx]


def get_ba_zi_for_datetime(lunar_year, lunar_month, birthday_normal):
    if not birthday_normal:
        birthday_normal = datetime.now()

    # 1864年是甲子年，每隔六十年一个甲子
    idx = (lunar_year - 1864) % 60
    # 没有过春节的话那么年还算上一年的，此处求的年份的干支
    nian_zhu = JIA_ZI_NAME[idx]

    idx = idx % 5
    """
    年上起月
    甲己之年丙作首，乙庚之岁戊为头，
    丙辛必定寻庚起，丁壬壬位顺行流，
    更有戊癸何方觅，甲寅之上好追求。
    """
    idx_month = (idx + 1) * 2
    idx_month = 0 if idx_month == 10 else idx_month
    # 求的月份的干支
    yue_zhu = GAN[(idx_month + lunar_month - 1) % 10] + ZHI[(lunar_month + 2 - 1) % 12]

    # 求出和1900年1月31日甲辰日相差的天数
    # 甲辰日是第四十天
    offset = (birthday_normal - BASE_DATE).days
    offset = (offset + 40) % 60
    # 求的日的干支
    ri_zhu = JIA_ZI_NAME[offset]

    """
    日上起时
    甲己还生甲，乙庚丙作初，
    丙辛从戊起，丁壬庚子居，
    戊癸何方发，壬子是真途。
    """
    offset = (offset % 5) * 2
    shichen_idx = get_shi_chen_idx(birthday_normal.hour)
    # 求得时辰的干支
    ganzhi_shichen = GAN[(int(offset + shichen_idx) % 10)] + ZHI[shichen_idx]

    # 在此处输出我们的年月日时的天干地支
    return f"{nian_zhu},{yue_zhu},{ri_zhu},{ganzhi_shichen}"


# 传回农历 y年的总天数
def year_days(y):
    i, days_sum_of_year = 0x8000, 348
    while i > 0x8:
        if (LUNAR_INFO[y - 1900] & i) != 0:
            days_sum_of_year += 1
        i >>= 1
    return days_sum_of_year + leap_days(y)


# 传回农历 y年闰月的天数
def leap_days(y):
    if leap_month_num(y) != 0:
        if (LUNAR_INFO[y - 1900] & 0x10000) != 0:
            return 30
        else:
            return 29
    else:
        return 0


# 传回农历 y年闰哪个月 1-12 , 没闰传回 0
def leap_month_num(y):
    return LUNAR_INFO[y - 1900] & 0xf


# 传回农历 y年m月的总天数
def month_days(y, m):
    if (LUNAR_INFO[y - 1900] & (0x10000 >> m)) == 0:
        return 29
    else:
        return 30


# 传回农历 y年的生肖地支
def get_zhi_of_year(year):
    return ZHI[(year - 4) % 12]


# 传回农历 y年的生肖
def get_zodiac_of_year(year):
    return SHENG_XIAO[(year - 4) % 12]


# 传入 月日的offset 传回干支, 0=甲子
def cyclicalm(num):
    return GAN[num % 10] + ZHI[num % 12]


# 传入 offset 传回干支, 0=甲子
def cyclical(year):
    num = year - 1900 + 36
    return cyclicalm(num)
