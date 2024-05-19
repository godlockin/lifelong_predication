from collections import Counter

from backend.func.lord_gods import LordGods


class Female(LordGods):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.meta_info_display = kwargs.get('meta_info_display', False)
        self.explain_append = kwargs.get('explain_append', False)
        
        self.easily_deceived = self.check_if_easily_deceived()

    def __str__(self):
        msg = f"{super().__str__() if self.meta_info_display else ''}"

        if self.easily_deceived:
            msg += f"""
        {self.easily_deceived}
            """

        return msg

    def check_if_easily_deceived(self):
        # 第一种是那种聪明反被聪明误的人，如果八字中的食伤星(智慧)为喜用神，但被被印星克制太过，就会容易造成判断失误，聪明一世偶尔糊涂一时，导致脑子一时受到蒙蔽而被骗。
        if not self.self_strong:
            if (
                    (self.lord_god_explain.single_explain_mapping['正印'].lord_gods_count
                     + self.lord_god_explain.single_explain_mapping['偏印'].lord_gods_count)
                    -
                    (self.lord_god_explain.single_explain_mapping['食神'].lord_gods_count
                     + self.lord_god_explain.single_explain_mapping['伤官'].lord_gods_count)
            ) > 2:
                return "聪明反被聪明误的人，如果八字中的食伤星(智慧)为喜用神，但被被印星克制太过，就会容易造成判断失误，聪明一世偶尔糊涂一时，导致脑子一时受到蒙蔽而被骗。"

            # 第二种是那种性格过于柔软没有主见的，如果八字中日干为阴干而又身弱的人性格阴柔软弱，没有主见，往往容易被人牵着鼻子走而上当受骗。
            if self.ri_gan in ['乙', '丁', '己', '辛', '癸']:
                return "性格过于柔软没有主见的，如果八字中日干为阴干而又身弱的人性格阴柔软弱，没有主见，往往容易被人牵着鼻子走而上当受骗。"

            # 第四种是那种脑子不好使容易招小人的人，身弱官杀混杂又旺而为忌的人一般不是很精明。男命容易被骗财受人欺负，女人容易被人骗财骗色。
            if (
                self.lord_god_explain.single_explain_mapping['正官'].lord_gods_count > 0
                and
                self.lord_god_explain.single_explain_mapping['七杀'].lord_gods_count > 0
            ):
                return "容易招小人的人，身弱官杀混杂又旺而为忌的人一般不是很精明。男命容易被骗财受人欺负，女人容易被人骗财骗色。"
        # 第七种是那种贪婪财色的人，八字或行运中食伤，财多为忌的人。食伤代表贪，财代表欲。为忌就会在这上面吃亏栽跟头。财多坏印，丢了原则就会坏了名声。
        else:
            if (
                (
                    (self.lord_god_explain.single_explain_mapping['食神'].lord_gods_count
                     + self.lord_god_explain.single_explain_mapping['伤官'].lord_gods_count)
                ) > 3
                or
                (
                    (self.lord_god_explain.single_explain_mapping['正财'].lord_gods_count
                     + self.lord_god_explain.single_explain_mapping['偏财'].lord_gods_count)
                ) > 3
            ):
                return "贪婪财色的人，八字或行运中食伤，财多为忌的人。食伤代表贪，财代表欲。为忌就会在这上面吃亏栽跟头。财多坏印，丢了原则就会坏了名声。"

        # 第三种是那种胆大心不细却又贪心的人，八字中比劫旺而无制财星弱的，就是比较贪心，喜欢投机取巧，不劳无获，异想天开。比劫旺之人胆大冲动头脑简单，喜欢贪小利冲动的去以小博大，往往会贪小利一时冲动做一些错误决定而因小失大被骗；比如好赌之徒，这种人一般多口舌是非，被朋友或小人所骗。
        if (
            (
                (
                    (self.lord_god_explain.single_explain_mapping['正官'].lord_gods_count
                     + self.lord_god_explain.single_explain_mapping['七杀'].lord_gods_count)
                    -
                    (self.lord_god_explain.single_explain_mapping['比肩'].lord_gods_count
                     + self.lord_god_explain.single_explain_mapping['劫财'].lord_gods_count)
                ) < 0
            )
            and
            (
                (
                    (self.lord_god_explain.single_explain_mapping['正财'].lord_gods_count
                     + self.lord_god_explain.single_explain_mapping['偏财'].lord_gods_count)
                ) < 3
            )
        ):
            return "胆大心不细却又贪心的人，八字中比劫旺而无制财星弱的，就是比较贪心，喜欢投机取巧，不劳无获，异想天开。比劫旺之人胆大冲动头脑简单，喜欢贪小利冲动的去以小博大，往往会贪小利一时冲动做一些错误决定而因小失大被骗；比如好赌之徒，这种人一般多口舌是非，被朋友或小人所骗。"

        # 第五种是那种心地善良单纯喜欢关心助人的热心人，八字中印星太旺或木太多的人心怀慈悲，同情心强，容易可怜别人，会因救助别人而被骗。印旺：八字印旺之人同情心重，喜欢助人。正印为我主动生助，正印旺容易同情相信别人在助人方面容易轻信别人而被骗。偏印为不情愿之生，虽也爱帮助别人，但心中总有预期的回报，倘若发现对方是虚伪不诚之人，内心的失落感就会很强烈。
        if (
            (
                self.lord_god_explain.single_explain_mapping['正印'].lord_gods_count >= 4
                or
                self.lord_god_explain.single_explain_mapping['偏印'].lord_gods_count >= 4
            )
            or
            self.elements_count['木'] > 3
        ):
            return "心地善良单纯喜欢关心助人的热心人，八字中印星太旺或木太多的人心怀慈悲，同情心强，容易可怜别人，会因救助别人而被骗。印旺：八字印旺之人同情心重，喜欢助人。正印为我主动生助，正印旺容易同情相信别人在助人方面容易轻信别人而被骗。偏印为不情愿之生，虽也爱帮助别人，但心中总有预期的回报，倘若发现对方是虚伪不诚之人，内心的失落感就会很强烈。"

        # 第六种是那种特讲信用、忠厚、说到做到的人，八字中土太多太旺的人愚钝诚实，容易相信别人而被骗。
        if self.elements_count['土'] > 3:
            return "特讲信用、忠厚、说到做到的人，八字中土太多太旺的人愚钝诚实，容易相信别人而被骗。"

        return ""
