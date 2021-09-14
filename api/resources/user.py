from api import Resource, abort, reqparse, auth
from api.models.user import UserModel
from api.schemas.user import user_schema, users_schema, UserSchema, UserRequestSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields
import logging


# @doc(
#     summary="Get user by id",
#     description="Returns user",
#     produces=[
#         'application/json'
#     ],
#     params={'user_id': {'description': 'user id'}},
#     responses={
#         "404": {
#             "description": "User not found"
#         }
#     },
#     security=[{"basicAuth": []}]
# )
@doc(tags=['Users'])
class UserResource(MethodResource):
    @doc(summary="Get user by id", description="Returns user")
    @doc(responses={404: {"description": 'User not found'}})
    @marshal_with(UserSchema, code=200)
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id={user_id} not found")
        return user, 200

    @auth.login_required(role="admin")
    @doc(description='Edit user by id')
    @marshal_with(UserSchema)
    @use_kwargs({"username": fields.Str()})
    @doc(security=[{"basicAuth": []}])
    def put(self, user_id, **kwargs):
        user = UserModel.query.get(user_id)
        user.username = kwargs["username"]
        user.save()
        return user, 200

    @auth.login_required(role="admin")
    @doc(description='Delete user by id')
    @doc(responses={401: {"description": "Not authorization"}})
    @doc(responses={404: {"description": "Not found"}})
    @marshal_with(UserSchema)
    @doc(security=[{"basicAuth": []}])
    def delete(self, user_id):
        user = UserModel.query.get(user_id)
        if not user:
            abort(404, error=f"User with id:{user_id} not found")
        user.delete()
        return user, 200


@doc(tags=['Users'])
class UsersListResource(MethodResource):
    @marshal_with(UserSchema(many=True), code=200)
    def get(self):
        users = UserModel.query.all()
        return users, 200

    @use_kwargs(UserRequestSchema, location='json')
    @marshal_with(UserSchema, code=201)
    def post(self, **kwargs):
        user = UserModel(**kwargs)
        user.save()
        if not user.id:
            abort(400, error=f"User with username:{user.username} already exist")
        logging.info("User create!!!")
        return user, 201
