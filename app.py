from api import api, app, docs
from api.resources.note import NoteResource, NotesListResource, NoteFilterResource, NoteAddTagsResource
from api.resources.user import UserResource, UsersListResource
from api.resources.auth import TokenResource
from api.resources.tag import TagsResource, TagsListResource
from config import Config

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
docs.register(TagsListResource)
if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
