import argparse

from backend.constants import constants
from backend.func.lifelong_prediction import LifePrediction
from backend.utils.utils import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is a calc project of BaZi.')
    parser.add_argument('-b', '--birthday', help='The birthday of yourself, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"', required=True)
    parser.add_argument('-g', '--gander', help='The gander of yourself, default as male', default=False)
    parser.add_argument('-e', '--explain', help='To check whether append explain details on different attributes', default=False)
    parser.add_argument('-c', '--couple_birthday', help='The birthday of your couple, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"', required=False, default=BASE_DATE_STR)
    parser.add_argument('-md', '--marry_date', help='The date which you couples prepare to get marriage, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"', required=False, default=BASE_DATE_STR)
    parser.add_argument('-rz', '--ru_zhui', help='Set male as primary info to do calculation, and there were a special case on male\'s marriage is [ru zhui], default as False', default=False)

    args = parser.parse_args()

    print(f'Argument received: {args}')

    main_birthday = datetime.strptime(args.birthday, default_date_format)
    is_male = bool(args.gander)
    explain_append = bool(args.explain)
    couple_birthday = datetime.strptime(args.couple_birthday, default_date_format)
    marry_date = datetime.strptime(args.marry_date, default_date_format) if args.marry_date else constants.BASE_DATE
    ru_zhui = bool(args.ru_zhui)

    life = LifePrediction(
        base_datetime=main_birthday,
        meta_info_display=True,
        explain_append=explain_append,
        couple_birthday=couple_birthday,
        marry_date=marry_date,
        ru_zhui=ru_zhui,
    )
    print(life)
