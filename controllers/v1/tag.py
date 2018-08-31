from flask import Response
from flask_restful import abort, reqparse, request
from flask_restful_swagger_2 import swagger, Resource

from data_access.tag import TagDataAccess
from view_models.tag import TagModel
from decorators.general import rest_method

class TagController(Resource):
    @rest_method
    def get(self, tag_id=None):
        if tag_id is None:
            tag_list = TagDataAccess().get_tag()
            return [TagModel._construct(tag) for tag in tag_list]
        else:
            tag = TagDataAccess().get_tag(tag_id)
            return TagModel._construct(tag)
    
    @rest_method
    def put(self, tag_id):
        tag_data = request.get_json()
        tag = TagModel(**tag_data)
        result = TagDataAccess().edit_tag(tag_id, tag)
        return TagModel._construct(result)
    
    @rest_method
    def post(self):
        tag_data = request.get_json()
        tag = TagModel(**tag_data)
        result = TagDataAccess().create_tag(tag)
        return TagModel._construct(result)

    @rest_method
    def delete(self, tag_id):
        if TagDataAccess().delete_tag(tag_id):
            return '', 204
        else:
            return 'Tag ID {} not found'.format(tag_id), 410