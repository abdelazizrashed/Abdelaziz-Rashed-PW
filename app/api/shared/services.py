from typing import List
from flask import Flask
from app.api.shared.helpers.services import HelperServices, rm_none_from_dict
from app.api.shared.models import IMGInfoModel, TechnologyModel, PlatformModel
from app.api.shared.helpers.services import HelperServices
from werkzeug.datastructures import FileStorage


class IMGInfoServices:
    @staticmethod
    def json(img_info: IMGInfoModel, storage) -> dict:
        if not img_info: return 
        return {
            "src": HelperServices.get_url_from_cloud_path(img_info.cloud_path, storage),
            "alt": img_info.alt,
            "caption": img_info.caption
        }

    @staticmethod
    def from_json(json: dict, file: FileStorage = None, app: Flask = None) -> IMGInfoModel:
        """
        The upload functionality of this method is deprecated and it will be removed.
        """
        if not json: return
        img_info = IMGInfoModel()
        #Todo: delete the upload functionality
        # if file and app:
        #     img_info.cloud_path = HelperServices.upload_file(file, app)
        # if file and not app:
        #     raise AttributeError("If you intend to upload an image you should include the flask app")
        # else:
        #     if json.get("img"):
        #         img_info.cloud_path = HelperServices.upload_file(file, app)
        #     elif json.get("couldPath"):
        img_info.cloud_path = json.get("cloudPath")

        img_info.alt = json.get("alt")
        img_info.caption = json.get("caption")
        return img_info

    @staticmethod
    def upload(img: FileStorage,app:Flask) -> str:
        cloud_path = HelperServices.upload_file(img, app)
        return cloud_path


class TechnologyServices:
    @staticmethod
    def json(technology: TechnologyModel) -> dict:
        if not technology: return 
        if not technology: return None
        return {
            "name": technology.name,
            "description": technology.description,
            "id": technology.id_,
        }

    @staticmethod
    def json_partial(technology: TechnologyModel) -> dict:
        if not technology: return 
        return {
            "name": technology.name,
            "id": technology.id_,
        }

    @staticmethod
    def from_json(json: dict) -> TechnologyModel:
        if not json: return
        technology = TechnologyModel()
        technology.name = json.get("name")
        technology.description = json.get("description")
        technology.id_ = json.get("id")

        return technology

    @staticmethod
    def create(attrs: dict, app: Flask) -> TechnologyModel:
        db = HelperServices.get_firebase_database(app)
        id_ = db.child("technologies").push(attrs)["name"]
        attrs["id"] = id_
        platform = TechnologyServices.from_json(attrs)
        return platform

    @staticmethod
    def update(updates: dict, id_: str, app: Flask) -> TechnologyModel:
        db = HelperServices.get_firebase_database(app)
        updates  = rm_none_from_dict(updates)
        attrs = db.child("technologies").child(id_).update(updates)
        if attrs == None:
            return None
        return TechnologyServices.from_json(attrs)


    @staticmethod
    def retrieve(id_: str, app: Flask) -> TechnologyModel:
        db = HelperServices.get_firebase_database(app)
        result = db.child("technologies").child(id_).get()
        if not result.val() or not result.key():
            return None
        attrs = dict(result.val())
        attrs["id"] = result.key()
        if attrs == None:
            return None
        return TechnologyServices.from_json(attrs)


    @staticmethod
    def delete(id_: str, app: Flask) -> int:
        db = HelperServices.get_firebase_database(app)
        return db.child("technologies").child(id_).remove()

class PlatformServices:
    @staticmethod
    def json_all(platform: PlatformModel) -> dict:
        if not platform: return  
        return {
            "name": platform.name,
            "description": platform.description,
            "id": platform.id_,
        }

    @staticmethod
    def json_partial(platform: PlatformModel) -> dict:
        if not platform: return
        return {
            "name": platform.name,
            "id": platform.id_,
        }

    @staticmethod
    def from_json(json: dict) -> PlatformModel:
        if not json: return
        platform = PlatformModel()
        platform.name = json.get("name")
        platform.description = json.get("description")
        platform.id_ = json.get("id")

        return platform

    @staticmethod
    def create(attrs: dict, app: Flask) -> PlatformModel:
        db = HelperServices.get_firebase_database(app)
        id_ = db.child("platforms").push(attrs)["name"]
        attrs["id"] = id_
        platform = PlatformServices.from_json(attrs)
        return platform

    @staticmethod
    def update(updates: dict, id_: str, app: Flask) -> PlatformModel:
        db = HelperServices.get_firebase_database(app)
        updates  = rm_none_from_dict(updates)
        attrs = db.child("platforms").child(id_).update(updates)
        if attrs == None:
            return None
        return PlatformServices.from_json(attrs)


    @staticmethod
    def retrieve(id_: str, app: Flask) -> PlatformModel:
        db = HelperServices.get_firebase_database(app)
        result = db.child("platforms").child(id_).get()
        if not result.val(): return None
        attrs = dict(result.val())
        attrs["id"] = result.key()
        if attrs == None:
            return None
        return PlatformServices.from_json(attrs)


    @staticmethod
    def delete(id_: str, app: Flask) -> int:
        db = HelperServices.get_firebase_database(app)
        return db.child("platforms").child(id_).remove()

class TechnologiesServices:

    @staticmethod
    def json_all(technologies: List[TechnologyModel]) -> dict:
        if not technologies: return []
        techs_key = "technologies"
        technologies_dict = {techs_key: []}
        for tech in technologies:
            technologies_dict[techs_key].append(TechnologyServices.json(tech))
        return technologies_dict

    @staticmethod
    def json_partial(technologies: List[TechnologyModel]) -> dict:
        if not technologies: return []
        techs_key = "technologies"
        technologies_dict = {techs_key: []}
        for tech in technologies:
            technologies_dict[techs_key].append(TechnologyServices.json_partial(tech))
        return technologies_dict

    @staticmethod
    def from_json(json: dict) -> List[TechnologyModel]:
        if not json: return
        techs = []
        for json_dict in json["technologies"]:
            techs.append(TechnologyServices.from_json(json_dict))

        return techs

    @staticmethod
    def create(attrs: dict, app: Flask) -> List[TechnologyModel]:
        techs = []
        for tech in attrs["technologies"]:
            techs.append(TechnologyServices.create(tech, app))
        return techs

    @staticmethod
    def update(updates: dict, app: Flask) -> List[TechnologyModel]:
        techs = []
        for tech in updates["technologies"]:
            id_ = tech.pop("id")
            tech  = rm_none_from_dict(tech)
            techs.append(TechnologyServices.update(tech, id_, app))

        return techs


    @staticmethod
    def retrieve(app: Flask, ids: List[str] = None) -> List[TechnologyModel]:
        
        db =  HelperServices.get_firebase_database(app)
        results = db.child("technologies").get()
        technologies = []
        if not results.each(): return None
        for result in results.each():
            if ids and not result.key() in ids:
                continue
            attrs = result.val()
            attrs["id"] = result.key()
            technologies.append(TechnologyServices.from_json(attrs))
        return technologies

    @staticmethod
    def delete(ids: List[str], app: Flask) -> dict:
        res = {"result": []}
        is_success = False
        for id_ in ids:
            TechnologyServices.delete(id_, app)
            res["result"].append({"message": "Succeeded", "id": id_})
            is_success = True
        sc = 200 if is_success else 520
        return res, sc


class PlatformsServices:

    @staticmethod
    def json_all(platforms: List[PlatformModel]) -> dict:
        if  not platforms: return []
        plat_key = "platforms"
        plat_dict = {plat_key: []}
        for platform in platforms:
            plat_dict[plat_key].append(PlatformServices.json_all(platform))
        return plat_dict

    @staticmethod
    def json_partial(platforms: List[PlatformModel]) -> dict:
        if not platforms: return []
        plat_key = "platforms"
        plat_dict = {plat_key: []}
        for platform in platforms:
            plat_dict[plat_key].append(PlatformServices.json_partial(platform))
        return plat_dict

    @staticmethod
    def from_json(json: dict) -> List[PlatformModel]:
        if not json: return
        plats = []
        for plat_json in json["platforms"]:
            plats.append(PlatformServices.from_json(plat_json))

        return plats

    @staticmethod
    def create(attrs: dict, app: Flask) -> List[PlatformModel]:
        platforms = []
        for platform in attrs["platforms"]:
            platforms.append(PlatformServices.create(platform, app))
        return platforms

    @staticmethod
    def update(updates: dict, app: Flask) -> List[PlatformModel]:
        platforms = []
        for platform in updates["platforms"]:
            id_ = platform.pop("id")
            platform  = rm_none_from_dict(platform)
            platforms.append(PlatformServices.update(platform, id_, app))
        return platforms


    @staticmethod
    def retrieve(app: Flask, ids: List[str] = None) -> List[PlatformModel]:
        # if ids:
        #     return [PlatformServices.retrieve(id_, app) for id_ in ids]
        # else:
        db =  HelperServices.get_firebase_database(app)
        results = db.child("platforms").get()
        platforms = []
        if not results.each(): return None
        for result in results.each():
            if ids and not result.key() in ids:
                continue
            attrs = result.val()
            attrs["id"] = result.key()
            platforms.append(PlatformServices.from_json(attrs))
        return platforms

    @staticmethod
    def delete(ids: List[str], app: Flask) -> dict:
        return [PlatformServices.delete(id_, app) for id_ in ids]