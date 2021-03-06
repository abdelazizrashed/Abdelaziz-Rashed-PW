from flask import current_app as app #request
from flask_restful import Resource, reqparse, request
from flask_jwt_extended import jwt_required

# from typing import List

from app.api.shared.helpers.services import HelperServices, any2bool

from .services import ProjectServices, ProjectsServices



_project_parser = reqparse.RequestParser()
_project_parser.add_argument("name", type=str)
_project_parser.add_argument("id", type=str)
_project_parser.add_argument("platformsIds", type=str, action="append")
_project_parser.add_argument("technologiesIds", type=str, action="append")
_project_parser.add_argument("img", type=dict)
_project_parser.add_argument("description", type=str)
_project_parser.add_argument("githubUrl", type=str)
_project_parser.add_argument("appStoreUrl", type=str)
_project_parser.add_argument("googlePlayStoreUrl", type=str)
_project_parser.add_argument("websiteUrl", type=str)
_project_parser.add_argument("youtubeVid", type=dict)
_project_parser.add_argument("servicesIds", type=str, action="append")
_project_parser.add_argument("imgs", type=dict, action="append")
_project_parser.add_argument("relatedProjectsIds", type=str, action="append")
_project_parser.add_argument("detailedServices", type=dict, action="append")
_project_parser.add_argument("detailedTechnologies", type=dict, action="append")
_project_parser.add_argument("detailedPlatforms", type=dict, action="append")


class ProjectResources(Resource):
    
    def get(self):
        id_ = request.args.get("id", type=str)
        partial = request.args.get("partial", type=any2bool)
        project = ProjectServices.retrieve(id_, app)
        if not project:
            return {
                "description": f"Project with id:<{id_}> couldn't be found",
                "error": "not_found"
            }, 404
        storage = HelperServices.get_firebase_storage(app)
        j =  ProjectServices.json(project, app, storage) if not partial else ProjectServices.json_partial(project, app, storage)
        return j,  200

    @jwt_required()
    def post(self):
        import time
        print("project post request")
        t0 =  time.time()
        data = _project_parser.parse_args()
        if not HelperServices.check_if_file_exists(data.get("img").get("cloudPath"), app):
            cp = data.get("img").get("cloudPath")
            return {
                "description": f"Image {cp} not found in the database. Please upload the image first using the url /shared/image, then attach the resulting cloudPath to the request.",
                "error": "not_found"
            }, 404
        for img in data.get("imgs"):
            if not HelperServices.check_if_file_exists(img.get("cloudPath"), app):
                cp = img.get("cloudPath")
                return {
                    "description": f"Image {cp} not found in the database. Please upload the image first using the url /shared/image, then attach the resulting cloudPath to the request.",
                    "error": "not_found"
                }, 404
        project = ProjectServices.create(data, app)
        t1  = time.time()
        print(f"got project from db after {t1-t0}s")

        if not project:
            return {
                "description": "Faced unknown error while creating the project",
                "error": "unknown_error"
            }, 520
        storage = HelperServices.get_firebase_storage(app)
        j =  ProjectServices.json(project, app, storage), 201
        t2= time.time()
        print(f"jsoned the project after {t2-t1}s")
        return j

    @jwt_required()
    def put(self):
        #*Data Validation
        data = _project_parser.parse_args()
        id_ = request.args.get("id", type=str)
        if data.get("img") and data.get("img").get("cloudPath") and not HelperServices.check_if_file_exists(data.get("img").get("cloudPath"), app):
            cp = data.get('img').get("cloudPath")
            return {
                "description": f"Image {cp} not found in the database. Please upload the image first using the url /shared/image, then attach the resulting cloudPath to the request.",
                "error": "not_found"
            }, 404
        if data.get("imgs"):
            if isinstance(data.get("imgs"), list):
                for img in data.get("imgs"):
                    if not HelperServices.check_if_file_exists(img.get("cloudPath"), app):
                        cp = img.get('cloudPath')
                        return {
                            "description": f"Image {cp} not found in the database. Please upload the image first using the url /shared/image, then attach the resulting cloudPath to the request.",
                            "error": "not_found"
                        }, 404
            elif HelperServices.check_if_file_exists(data.get("imgs").get("cloudPath"), app):
                cp = data.get("imgs").get("cloudPath")
                return {
                    "description": f"Image {cp} not found in the database. Please upload the image first using the url /shared/image, then attach the resulting cloudPath to the request.",
                    "error": "not_found"
                }, 404

        project = ProjectServices.update(data, id_, app)

        if not project:
            return {
                "description": "Faced unknown error while updating the project",
                "error": "unknown_error"
            }, 520
        storage = HelperServices.get_firebase_storage(app)
        return ProjectServices.json(project, app, storage), 200

    @jwt_required()
    def delete(self):
        id_ = request.args.get("id", type=str)

        return ProjectServices.delete(id_, app), 200


class ProjectsResources(Resource):
    
    def get(self):
        print("recieved get request at /projects")
        ids = request.args.getlist("id")
        partial = request.args.get("partial", type=any2bool)
        service = request.args.get("service", type=str)
        platform = request.args.get("platform", type=str)
        technology = request.args.get("technology", type=str)
        from time import time
        t0 = time()
        projects = ProjectsServices.retrieve(app, ids, service, platform, technology)
        t1 = time()
        print(f"retrieved data in {t1-t0} seconds")
        j = ProjectsServices.json_partial(projects, app) if partial else ProjectsServices.json(projects, app)
        t3 = time()
        print(f"jsonified data in {t3-t1} seconds")
        # print(j)
        return j, 200

    @jwt_required()
    def post(self):
        #Todo: Check if you can make this request work
        return{
            "description": "You are not allowed to create multiple projects at once. Create them one by one",
            "error": "invalid_operation"
        }, 409

    @jwt_required()
    def put(self):
        #Todo: Check if you can make this request work
        return{
            "description": "You are not allowed to create multiple projects at once. Update them one by one",
            "error": "invalid_operation"
        }, 409
        # data = _project_parser.parse_args()

        # projects = ProjectsServices.update(data, app)

        # return ProjectsServices.json(projects), 200

    @jwt_required()
    def delete(self):
        ids = request.args.getlist("id")

        status_codes = ProjectsServices.delete(ids, app)

        return {
            "description": "Projects deleted",
            "statusCodes": status_codes
        }, 200