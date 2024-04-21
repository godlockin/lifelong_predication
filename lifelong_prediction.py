from ba_zi_elements import BaZiElements
from demigod import Demigod
from family_support import FamilySupport
from intermarriage import Intermarriage
from life_stages_luck import LifeStagesLuck
from lord_gods import LordGods
from metainfo import MetaInfo
from potential_couple import PotentialCouple
from ten_years_luck import TenYearsLuck
from utils import *
from yearly_luck import YearlyLuck


class LifePrediction(MetaInfo):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kwargs['meta_info_display'] = False
        self.ba_zi_elements = BaZiElements(**kwargs)

        self.lord_gods = LordGods(**kwargs)
        self.demi_gods = Demigod(**kwargs)

        self.family_support = FamilySupport(**kwargs)
        self.life_stages_luck = LifeStagesLuck(**kwargs)

        self.ten_years_luck = TenYearsLuck(**kwargs)
        self.yearly_luck = YearlyLuck(**kwargs)

        if kwargs.get('is_male', True):
            man_birthday = self.birthday_normal
            woman_birthday = kwargs.get('couple_birthday', constants.BASE_DATE)
            self.primary_birthday = man_birthday
            self.couple_birthday = woman_birthday
        else:
            man_birthday = kwargs.get('couple_birthday', constants.BASE_DATE)
            woman_birthday = self.birthday_normal
            self.primary_birthday = woman_birthday
            self.couple_birthday = man_birthday

        if self.couple_birthday != constants.BASE_DATE:
            self.intermarriage = Intermarriage(
                man_birthday=man_birthday,
                woman_birthday=woman_birthday,
                marry_date=kwargs.get('marry_date', constants.BASE_DATE),
                explain_append=kwargs.get('explain_append', False)
            )
        else:
            self.potential_couple = PotentialCouple(**kwargs)

    def __str__(self):
        msg = f"{super().__str__()}"
        msg += self.ba_zi_elements.__str__()
        msg += self.lord_gods.__str__()
        msg += self.demi_gods.__str__()
        msg += self.family_support.__str__()
        msg += self.life_stages_luck.__str__()
        msg += self.ten_years_luck.__str__()
        msg += self.yearly_luck.__str__()

        if self.couple_birthday != constants.BASE_DATE:
            msg += self.intermarriage.__str__()
        else:
            msg += self.potential_couple.__str__()
        return msg

