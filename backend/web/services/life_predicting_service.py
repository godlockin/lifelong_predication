from backend.func.lifelong_prediction import LifePrediction
from backend.web.entity.bone_weight_info import BoneWeightDto
from backend.web.entity.lord_gods_structure_info import LordGodsStructureDto
from backend.web.entity.meta_info import MetaInfoDto, BaZiElementsDto
from backend.web.entity.process_request import QueryDto
from backend.web.entity.process_response import PredictionDto


class LifePredictionOperator:
    def __init__(self, query: QueryDto):
        self.query = query
        predict_req = {
            "name": query.name,
            "base_datetime": query.selfBirthday,
            "meta_info_display": True,
            "explain_append": query.addDetails,
            "couple_birthday": query.partnerBirthday,
            "marry_date": query.marriageDate,
            "ru_zhui": query.isBridegroom,
            "is_male": query.gender == "male",
            "enabled_features": query.enabledFeatures,
        }
        self.life_prediction = LifePrediction(**predict_req)

    def do_predict(self):
        return PredictionDto(
            queryDto=self.display_query_info(),
            metaInfo=self.build_meta_info(),
            baziElements=self.build_bazi_elements(),
            boneWeight=self.build_bone_weight(),
            lordGodsStructure=self.build_lord_gods_structure()
        )

    def display_query_info(self):
        return QueryDto(
            name=self.query.name,
            selfBirthday=self.query.selfBirthday,
            gender='男' if self.query.gender == 'male' else '女',
            partnerBirthday=self.query.partnerBirthday,
            marriageDate=self.query.marriageDate,
            isBridegroom=self.query.isBridegroom,
            addDetails=self.query.addDetails,
            enabledFeatures=self.query.enabledFeatures
        )

    def build_meta_info(self):
        metainfo = self.life_prediction
        return MetaInfoDto(
            name=self.query.name,
            birthdate=metainfo.input_datetime_str,
            lunar_birthday=metainfo.lunar_of_input_datetime_str,
            lunar_birthday_hour=metainfo.shi_chen,
            bazi=metainfo.ba_zi,
            zodiac=metainfo.zodiac,
            zodiac_cn=f"{metainfo.zodiac_zhi}({metainfo.zodiac_element})",
            year_gan=metainfo.nian_gan,
            year_gan_element=metainfo.nian_gan_element,
            year_zhi=metainfo.nian_zhi,
            year_zhi_element=metainfo.nian_zhi_element,
            month_gan=metainfo.yue_gan,
            month_gan_element=metainfo.yue_gan_element,
            month_zhi=metainfo.yue_zhi,
            month_zhi_element=metainfo.yue_zhi_element,
            day_gan=metainfo.ri_gan,
            day_gan_element=metainfo.ri_gan_element,
            day_zhi=metainfo.ri_zhi,
            day_zhi_element=metainfo.ri_zhi_element,
            hour_gan=metainfo.shi_gan,
            hour_gan_element=metainfo.shi_gan_element,
        )

    def build_bazi_elements(self):
        ba_zi_elements = self.life_prediction.ba_zi_elements
        return BaZiElementsDto(
            isStrong=ba_zi_elements.self_strong,
            isPositive=ba_zi_elements.self_positive,
            supportingElements=ba_zi_elements.supporting_elements_sequence,
            opposingElements=ba_zi_elements.opposing_elements_sequence,
            elementsInfluenceWeight={key: value[1] for key, value in
                                     ba_zi_elements.elements_relationships_mapping.items()},
            elementsInfluence={key: value[0] for key, value in ba_zi_elements.elements_relationships_mapping.items()},
        )

    def build_bone_weight(self):
        bone_weight = self.life_prediction.bone_weight
        return BoneWeightDto(
            boneWeight=bone_weight.bone_weight,
            description=bone_weight.description,
            details=bone_weight.bone_weight_map
        )

    def build_lord_gods_structure(self):
        lord_gods_structure = self.life_prediction.lord_gods_structure
        return LordGodsStructureDto(
            structure=lord_gods_structure.structure,
            structureAppend=f"身{'强' if lord_gods_structure.self_strong else '弱'}",
            structureDescription=f"{lord_gods_structure.strength_comment['comment']}",
            structureImagery=f"{lord_gods_structure.strength_comment['imagery']}",
            comment=f"{lord_gods_structure.strength_comment['strength_comment']}",
            isStructurePositive=lord_gods_structure.is_positive_overall[0],
            structureFix=lord_gods_structure.is_positive_overall[1],
        )
