from api import auth, abort, g, Resource, reqparse, api
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.tag import TagModel
from api.schemas.note import NoteSchema, NoteCreateSchema, NoteEditSchema, NoteFilterSchema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields
from sqlalchemy.orm.exc import NoResultFound


@doc(tags=['Notes'])
@api.resource('/notes/<int:note_id>')
class NoteResource(MethodResource):
    @auth.login_required
    @doc(summary="Get note by id", security=[{"basicAuth": []}])
    @marshal_with(NoteSchema)
    def get(self, note_id):
        author = g.user
        try:
            note = NoteModel.get_all_for_user(author).filter_by(id=note_id).one()
            return note, 200
        except NoResultFound:
            abort(404, error=f"Note with id={note_id} not found")

    @auth.login_required
    @doc(summary="Edit note by id", security=[{"basicAuth": []}])
    @use_kwargs(NoteEditSchema)
    @marshal_with(NoteSchema)
    def put(self, note_id, **kwargs):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        if kwargs.get("text") is not None:
            note.text = kwargs.get("text")
        if kwargs.get("private") is not None:
            note.private = kwargs.get("private")
        note.save()
        return note, 200

    @auth.login_required
    @doc(description='Delete note by id', security=[{"basicAuth": []}])
    @doc(responses={401: {"description": "Not authorization"}})
    @doc(responses={404: {"description": "Not found"}})
    @marshal_with(NoteSchema, code=200)
    def delete(self, note_id):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id:{note_id} not found")
        # FIXME: добавить удаление только своих заметок
        note.delete()
        return note, 200


@doc(tags=['Notes'])
@api.resource('/notes')
class NotesListResource(MethodResource):
    @auth.login_required
    @doc(summary="Get notes list", security=[{"basicAuth": []}])
    @marshal_with(NoteSchema(many=True), code=200)
    @use_kwargs(NoteFilterSchema, location='query')
    def get(self, **kwargs):
        author = g.user
        notes = NoteModel.get_all_for_user(author)
        if kwargs.get("tag") is not None:
            notes = notes.filter(NoteModel.tags.any(name=kwargs['tag']))
        if kwargs.get("private") is not None:
            notes = notes.filter_by(private=kwargs['private'])
        return notes, 200

    @auth.login_required
    @doc(summary="Create note", security=[{"basicAuth": []}])
    @marshal_with(NoteSchema, code=201)
    @use_kwargs(NoteCreateSchema)
    def post(self, **kwargs):
        author = g.user
        note = NoteModel(author_id=author.id, **kwargs)
        note.save()
        return note, 201


@doc(tags=['Notes'])
class NoteRestoreResource(MethodResource):
    # PUT: /notes/{id}/restore
    @doc(summary="Restore note")
    @marshal_with(NoteSchema, code=200)
    def put(self, note_id):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error="Not found")

        if not note.archive:
            return {}, 304

        note.restore()
        return note, 200


@doc(tags=['Notes'])
class NoteAddTagsResource(MethodResource):
    # PUT: / notes / {id}
    @doc(summary="Add tags to note")
    @use_kwargs({"tags": fields.List(fields.Int())}, location="json")
    @marshal_with(NoteSchema, code=200)
    def put(self, note_id, **kwargs):
        note = NoteModel.query.get(note_id)
        for tag_id in kwargs["tags"]:
            tag = TagModel.query.get(tag_id)
            note.tags.append(tag)
        note.save()
        return note, 200


# @doc(tags=['NotesFilter'])
# class NoteFilterResource(MethodResource):
#     # GET: /notes/filter?tag=<tag_name>
#     # GET: /notes?tag=<tag_name>
#     @use_kwargs({"tag": fields.Str()}, location='query')
#     @marshal_with(NoteSchema(many=True), code=200)
#     def get(self, **kwargs):
#         notes = NoteModel.query.filter(NoteModel.tags.any(name=kwargs["tag"]))
#         return notes, 200


# @doc(tags=['NotesFilter'])
# class NoteFilterByUsernameResource(MethodResource):
#     # GET: /notes/public/filter?username=<un>
#     # GET: /notes?public=True&username=<un>
#     # GET: /notes?public=True&tag=<tag_name>
#     @use_kwargs({"username": fields.Str()}, location='query')
#     @marshal_with(NoteSchema(many=True), code=200)
#     def get(self, **kwargs):
#         print("query=", kwargs)
#         notes = NoteModel.query.filter(NoteModel.author.has(username=kwargs["username"]))
#         return notes, 200
