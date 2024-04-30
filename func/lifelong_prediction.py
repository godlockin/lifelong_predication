from func.ba_zi_elements import BaZiElements
from func.bone_weight import BoneWeight
from func.demigod import Demigod
from func.family_support import FamilySupport
from func.intermarriage import Intermarriage
from func.life_stages_luck import LifeStagesLuck
from func.lord_gods import LordGods
from func.lord_gods_structure import LordGodsStructure
from func.metainfo import MetaInfo
from func.potential_couple import PotentialCouple
from func.ten_years_luck import TenYearsLuck
from func.yearly_luck import YearlyLuck
from func.zodiac_explain import ZodiacExplain
from constants.constants import *


class LifePrediction(MetaInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs['meta_info_display'] = False
        self.ba_zi_elements = BaZiElements(**kwargs)

        self.bone_weight = BoneWeight(**kwargs)

        self.lord_gods = LordGods(**kwargs)
        self.lord_gods_structure = LordGodsStructure(**kwargs)
        self.demigods = Demigod(**kwargs)

        self.family_support = FamilySupport(**kwargs)
        self.life_stages_luck = LifeStagesLuck(**kwargs)

        self.ten_years_luck = TenYearsLuck(**kwargs)
        self.yearly_luck = YearlyLuck(**kwargs)

        self.enabled_labels = self.calc_enabled_labels(**kwargs)

        if kwargs.get('is_male', True):
            man_birthday = self.input_datetime
            woman_birthday = kwargs.get('couple_birthday', BASE_DATE)
            self.primary_birthday = man_birthday
            self.couple_birthday = woman_birthday
        else:
            man_birthday = kwargs.get('couple_birthday', BASE_DATE)
            woman_birthday = self.input_datetime
            self.primary_birthday = woman_birthday
            self.couple_birthday = man_birthday

        self.intermarriage = Intermarriage(
            man_birthday=man_birthday,
            woman_birthday=woman_birthday,
            marry_date=kwargs.get('marry_date', BASE_DATE),
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
        if not enabled_labels_items or 'core' in enabled_labels_items:
            return CORE_LIFE_PREDICTION_LABELS
        if 'all' in enabled_labels_items:
            return LIFE_PREDICTION_LABELS
        for item in enabled_labels_items:
            if item in LIFE_PREDICTION_LABELS:
                enabled_labels.append(item)

        return enabled_labels
