from api import api, app, docs
from api.resources.note import NoteResource, NotesListResource, \
    NoteFilterResource, NoteAddTagsResource, NoteFilterByUsernameResource
from api.resources.user import UserResource, UsersListResource
from api.resources.auth import TokenResource
from api.resources.tag import TagsResource, TagsListResource
from config import Config
from api import Message, mail

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE
api.add_resource(UsersListResource,
                 '/users')  # GET, POST
api.add_resource(UserResource,
                 '/users/<int:user_id>')  # GET, PUT, DELETE

api.add_resource(TokenResource,
                 '/auth/token')  # GET

api.add_resource(NotesListResource,
                 '/notes',  # GET, POST
                 )
api.add_resource(NoteResource,
                 '/notes/<int:note_id>',  # GET, PUT, DELETE
                 )
api.add_resource(NoteAddTagsResource,
                 '/notes/<int:note_id>/tags',  # PUT
                 )
api.add_resource(NoteFilterResource,
                 '/notes/filter',  # GET
                 )
api.add_resource(NoteFilterByUsernameResource,
                 '/notes/public/filter',  # GET
                 )

api.add_resource(TagsListResource,
                 '/tags'
                 )

docs.register(UserResource)
docs.register(UsersListResource)
docs.register(NoteResource)
docs.register(NotesListResource)
docs.register(NoteFilterResource)
docs.register(NoteAddTagsResource)
docs.register(NoteFilterByUsernameResource)
docs.register(TagsListResource)

msg = Message('test subject', sender=Config.ADMINS[0], recipients=Config.ADMINS)
msg.body = 'text body'
msg.html = '<b>HTML</b> body'

if __name__ == '__main__':
    with app.app_context():
        mail.send(msg)
    app.run(debug=Config.DEBUG, port=Config.PORT)
