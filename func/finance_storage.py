from ba_zi_elements import BaZiElements


class FinanceStorage(BaZiElements):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)

        self.storage = self.calc_finance_storage()

    def __str__(self):
        pass

    def calc_finance_storage(self):
        conditions = {
            "甲乙": "戌",
            "丙丁": "丑",
            "戊己": "辰",
            "庚辛": "未",
            "壬癸": "戌"
        }

        return [value for key, value in conditions.items() if self.ri_gan_element in key][0]
