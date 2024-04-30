import argparse
from datetime import datetime

from fastapi import FastAPI, APIRouter

import constants.constants as constants
from func.lifelong_prediction import LifePrediction
from web.api import app as api

app = FastAPI()
api_router = APIRouter()
api_router.include_router(api, prefix="")
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8082, log_level="info", reload=True)

    parser = argparse.ArgumentParser(description='This is a calc project of BaZi.')
    parser.add_argument('-b', '--birthday', help='The birthday of yourself, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"', required=True)
    parser.add_argument('-m', '--meta_info', help='The bazi info for yourself, default as True', action='store_true', default=True)
    parser.add_argument('-g', '--gander', help='The gander of yourself, default as male', action='store_true', default=True)
    parser.add_argument('-e', '--explain', help='To check whether append explain details on different attributes', action='store_true', default=False)
    parser.add_argument('-c', '--couple_birthday', help='The birthday of your couple, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"', required=False, default="2014-01-03 05:20:00")
    parser.add_argument('-md', '--marry_date', help='The date which you couples prepare to get marriage, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"', required=False)
    parser.add_argument('-rz', '--ru_zhui', help='Set male as primary info to do calculation, and there were a special case on male\'s marriage is [ru zhui], default as False', action='store_true', default=False)
    parser.add_argument('-o', '--option', default='core', help='Choose an option from: bone_weight, zodiac_explain, lord_gods, lord_gods_structure, demigods, family_support, life_stages_luck, ten_years_luck, yearly_luck, intermarriage, potential_couple. Default is "core".')
    args = parser.parse_args()

    print(f'Argument received: {args}')

    main_birthday = datetime.strptime(args.birthday, constants.default_date_format)
    meta_info = args.meta_info
    is_male = args.gander
    explain_append = args.explain
    couple_birthday = datetime.strptime(args.couple_birthday, constants.default_date_format)
    marry_date = datetime.strptime(args.marry_date, constants.default_date_format) if args.marry_date else constants.BASE_DATE
    ru_zhui = args.ru_zhui
    option = args.option
    print(option)

    life = LifePrediction(
        base_datetime=main_birthday,
        meta_info_display=meta_info,
        explain_append=explain_append,
        couple_birthday=couple_birthday,
        marry_date=marry_date,
        ru_zhui=ru_zhui,
        enabled_labels=option,
    )
    print(life)
