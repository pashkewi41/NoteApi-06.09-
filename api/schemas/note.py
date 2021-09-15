from api import ma
from api.models.note import NoteModel
from api.schemas.user import UserSchema
from api.schemas.tag import TagSchema


#       schema        flask-restful
# object ------>  dict ----------> json

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel

    # id = ma.auto_field()
    # text = ma.auto_field()
    # private = ma.auto_field()
    # archive = ma.auto_field()
    author = ma.Nested(UserSchema())
    tags = ma.Nested(TagSchema(many=True))

    _links = ma.Hyperlinks({
        'self': ma.URLFor('noteresource', values=dict(note_id="<id>")),
        'collection': ma.URLFor('noteslistresource')
    })


class NoteRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteModel
        fields = ["text", "private"]

    # text = ma.auto_field()
    # private = ma.auto_field()


class NoteFilterSchema(ma.SQLAlchemySchema):
    private = ma.Boolean(required=False)
    tag = ma.String(required=False)
