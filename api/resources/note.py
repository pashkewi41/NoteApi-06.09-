from api import auth, abort, g, Resource, reqparse
from api.models.note import NoteModel
from api.schemas.note import note_schema, notes_schema
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from webargs import fields


@doc(tags=['Notes'])
class NoteResource(MethodResource):
    @auth.login_required
    def get(self, note_id):
        author = g.user
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id={note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        return note_schema.dump(note), 200

    @auth.login_required
    def put(self, note_id):
        author = g.user
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        parser.add_argument("private", type=bool)
        note_data = parser.parse_args()
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"note {note_id} not found")
        if note.author != author:
            abort(403, error=f"Forbidden")
        note.text = note_data["text"]

        note.private = note_data.get("private") or note.private
        # if note_data["private"]:
        #     note.private = note_data["private"]

        note.save()
        return note_schema.dump(note), 200

    def delete(self, note_id):
        note = NoteModel.query.get(note_id)
        if not note:
            abort(404, error=f"Note with id:{note_id} not found")
        note_dict = note_schema.dump(note)
        note.delete()
        return note_dict, 200


@doc(tags=['Notes'])
class NotesListResource(MethodResource):
    @auth.login_required
    @doc(security=[{"basicAuth": []}])
    def get(self):
        author = g.user
        notes = NoteModel.query.filter_by(author_id=author.id)
        return notes_schema.dump(notes), 200

    @auth.login_required
    def post(self):
        author = g.user
        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True)
        parser.add_argument("private", type=bool)
        note_data = parser.parse_args()
        note = NoteModel(author_id=author.id, **note_data)
        note.save()
        return note_schema.dump(note), 201

