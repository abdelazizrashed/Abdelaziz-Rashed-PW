from flask import current_app as app
from flask_jwt_extended.view_decorators import jwt_required
from flask_restful import Resource, reqparse, request

from app.api.services.services import ServiceServices, ServicesServices
from app.api.shared.helpers.services import HelperServices, any2bool


_service_parser = reqparse.RequestParser()
_service_parser.add_argument("id", type=str)
_service_parser.add_argument("name", type=str)
_service_parser.add_argument("description", type=str)
_service_parser.add_argument("logo", type=dict)
_service_parser.add_argument("projectsIds", type=str, action="append")
_service_parser.add_argument("otherServicesIds", type=str, action="append")

_service_parser.add_argument("content", type=dict, action="append")
_service_parser.add_argument("technologies", type=dict, action="append")


class ServiceResources(Resource):

    @jwt_required()
    def post(self):
        data = _service_parser.parse_args()
        if not data.get("logo") or not data.get("logo").get("cloudPath"):
            return {
                "description": "The logo of the service is required as well as it's cloudPath",
                "error": "missing_info"
            }, 400
        
        if not HelperServices.check_if_file_exists(data.get("logo").get("cloudPath"), app):
            return {
                "description": "Image not found in the database. Please upload the image first using the url /shared/image, then attach the resulting cloudPath to the request.",
                "error": "not_found"
            }, 404

        service = ServiceServices.create(data, app)
        if not service:
            return {
                "description": "Faced unknown error while creating the service",
                "error": "unknown_error"
            }, 520
        storage = HelperServices.get_firebase_storage(app)
        return ServiceServices.json(service, storage), 201

    def get(self):
        id_ = request.args.get("id", type=str)
        partial = request.args.get("partial", type=any2bool)
        service = ServiceServices.retreive(id_, app)
        if not service:
            return {
                "description": f"Service with id:<{id_}> couldn't be found",
                "error": "not_found"
            }, 404
        storage = HelperServices.get_firebase_storage(app)
        print(f"partial  =   {partial}")
        if partial:
            res = ServiceServices.json_partial(service, storage)
        else: 
            res =  ServiceServices.json(service, storage)
        # print(res)
        return res, 200


    @jwt_required()
    def put(self):
        id_ = request.args.get("id", type=str)
        data = _service_parser.parse_args()
        
        if data.get("logo") and not data.get("logo").get("cloudPath"):
            return {
                "description": "If you are going to update the logo you need to upload the new logo to the database via /shared/image post request then add the cloudPath to the logo",
                "error": "missing_info"
            }, 400
        
        if data.get("logo") and not HelperServices.check_if_file_exists(data.get("logo").get("cloudPath"), app):
            return {
                "description": "Image not found in the database. Please upload the image first using the url /shared/image, then attach the resulting cloudPath to the request.",
                "error": "not_found"
            }, 404
        service = ServiceServices.update(data, id_, app)
        storage = HelperServices.get_firebase_storage(app)
        return ServiceServices.json(service, storage)


    @jwt_required()
    def delete(self):
        id_ = request.args.get("id", type=str)

        return ServiceServices.delete(id_, app), 200


class ServicesResources(Resource):

    @jwt_required()
    def post(self):
        #Todo: Check if you can make this request work
        return{
            "description": "You are not allowed to create multiple projects at once. Create them one by one",
            "error": "invalid_operation"
        }, 409

    def get(self):
        ids = request.args.getlist("id", type=str)
        partial = request.args.get("partial", type=any2bool)

        services = ServicesServices.retreive(app, ids)

        return {
            "services": ServicesServices.json_partial(services, app)if partial else ServicesServices.json(services, app)
        }, 200
        

    @jwt_required()
    def put(self):
        #Todo: Check if you can make this request work
        return{
            "description": "You are not allowed to create multiple projects at once. Update them one by one",
            "error": "invalid_operation"
        }, 409

    @jwt_required()
    def delete(self):
        ids = request.args.getlist("id")

        ServicesServices.delete(ids, app)

        
        return {
            "description": "Services deleted"
        }, 200

