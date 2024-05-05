import argparse

from ba_zi_elements import BaZiElements
from bone_weight import BoneWeight
from demigod import Demigod
from family_support import FamilySupport
from finance_storage import FinanceStorage
from intermarriage import Intermarriage
from life_stages_luck import LifeStagesLuck
from lord_gods import LordGods
from lord_gods_structure import LordGodsStructure
from metainfo import MetaInfo
from potential_couple import PotentialCouple
from ten_years_luck import TenYearsLuck
from utils import *
from yearly_luck import YearlyLuck
from zodiac_explain import ZodiacExplain


class LifePrediction(MetaInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs['meta_info_display'] = False
        self.ba_zi_elements = BaZiElements(**kwargs)

        self.enabled_labels = self.calc_enabled_labels(**kwargs)

        self.bone_weight = BoneWeight(**kwargs)

        self.lord_gods = LordGods(**kwargs)
        self.lord_gods_structure = LordGodsStructure(**kwargs)

        self.finance_storage = FinanceStorage(**kwargs)

        self.family_support = FamilySupport(**kwargs)
        self.life_stages_luck = LifeStagesLuck(**kwargs)

        self.demigods = Demigod(**kwargs)

        self.ten_years_luck = TenYearsLuck(**kwargs)
        self.yearly_luck = YearlyLuck(**kwargs)

        if kwargs.get('is_male', True):
            man_birthday = self.input_datetime
            woman_birthday = kwargs.get('couple_birthday', constants.BASE_DATE)
            self.primary_birthday = man_birthday
            self.couple_birthday = woman_birthday
        else:
            man_birthday = kwargs.get('couple_birthday', constants.BASE_DATE)
            woman_birthday = self.input_datetime
            self.primary_birthday = woman_birthday
            self.couple_birthday = man_birthday

        self.intermarriage = Intermarriage(
            man_birthday=man_birthday,
            woman_birthday=woman_birthday,
            marry_date=kwargs.get('marry_date', constants.BASE_DATE),
            ru_zhui=kwargs.get('ru_zhui', False),
            explain_append=kwargs.get('explain_append', False),
        )
        self.potential_couple = PotentialCouple(**kwargs)

        self.zodiac_explain = ZodiacExplain(self.ba_zi_elements)

    def __str__(self):
        msg = f"{super().__str__()}"
        msg += self.ba_zi_elements.__str__()

        conditions = {
            'bone_weight': self.bone_weight.__str__(),
            'lord_gods': self.lord_gods.__str__(),
            'lord_gods_structure': self.lord_gods_structure.__str__(),
            'finance_storage': self.finance_storage.__str__(),
            'demigods': self.demigods.__str__(),
            'family_support': self.family_support.__str__(),
            'life_stages_luck': self.life_stages_luck.__str__(),
            'ten_years_luck': self.ten_years_luck.__str__(),
            'yearly_luck': self.yearly_luck.__str__(),
            'intermarriage': self.intermarriage.__str__(),
            'potential_couple': self.potential_couple.__str__(),
            'zodiac_explain': self.zodiac_explain.__str__(),
        }

        msg += "".join([conditions[label] for label in self.enabled_labels])

        return msg

    def calc_enabled_labels(self, **kwargs):
        enabled_labels = []
        enabled_labels_str = kwargs.get('enabled_labels', "")
        enabled_labels_items = [item.strip().lower() for item in enabled_labels_str.split(',') if item]
        if not enabled_labels_items or 'all' in enabled_labels_items:
            return constants.LIFE_PREDICTION_LABELS
        for item in enabled_labels_items:
            if item in constants.LIFE_PREDICTION_LABELS:
                enabled_labels.append(item)

        return enabled_labels


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This is a calc project of BaZi.')
    parser.add_argument('-b', '--birthday',
                        help='The birthday of yourself, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"',
                        required=True)
    parser.add_argument('-g', '--gander', help='The gander of yourself, default as male', action='store_true',
                        default=True)
    parser.add_argument('-e', '--explain', help='To check whether append explain details on different attributes',
                        action='store_true', default=False)
    parser.add_argument('-c', '--couple_birthday',
                        help='The birthday of your couple, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"',
                        required=False, default="2014-01-03 05:20:00")
    parser.add_argument('-md', '--marry_date',
                        help='The date which you couples prepare to get marriage, in the format of "YYYY-MM-DD HH:MM:SS", e.g. "2014-01-03 05:20:00"',
                        required=False)
    parser.add_argument('-rz', '--ru_zhui',
                        help='Set male as primary info to do calculation, and there were a special case on male\'s marriage is [ru zhui], default as False',
                        action='store_true', default=False)

    args = parser.parse_args()

    print(f'Argument received: {args}')

    main_birthday = datetime.strptime(args.birthday, default_date_format)
    is_male = args.gander
    explain_append = args.explain
    couple_birthday = datetime.strptime(args.couple_birthday, default_date_format)
    marry_date = datetime.strptime(args.marry_date, default_date_format) if args.marry_date else constants.BASE_DATE
    ru_zhui = args.ru_zhui

    prediction = LifePrediction(
        base_datetime=main_birthday,
        meta_info_display=True,
        explain_append=explain_append,
        couple_birthday=couple_birthday,
        marry_date=marry_date,
        ru_zhui=ru_zhui,
    )
    print(prediction)
