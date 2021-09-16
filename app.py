from api import api, app, docs
from api.resources.note import NoteResource, NotesListResource, NoteAddTagsResource, NoteRestoreResource
from api.resources.user import UserResource, UsersListResource
from api.resources.auth import TokenResource
from api.resources.tag import TagsResource, TagsListResource
from api.resources.file import UploadPictureResource
from config import Config
from api import Message, mail
from flask import send_from_directory


@app.route('/uploads/<path:filename>')
def download_file(filename):
    # FIXME: добавить проверку на существовании директории для загрузки, если нет ее - то создать
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


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

# api.add_resource(NotesListResource,
#                  '/notes',  # GET, POST
#                  )
# api.add_resource(NoteResource,
#                  '/notes/<int:note_id>',  # GET, PUT, DELETE
#                  )
api.add_resource(NoteRestoreResource,
                 '/notes/<int:note_id>/restore',  # PUT
                 )
api.add_resource(NoteAddTagsResource,
                 '/notes/<int:note_id>/tags',  # PUT
                 )
api.add_resource(TagsListResource,
                 '/tags'
                 )

docs.register(UserResource)
docs.register(UsersListResource)
docs.register(NoteResource)
docs.register(NoteRestoreResource)
docs.register(NotesListResource)
docs.register(NoteAddTagsResource)
docs.register(TagsListResource)
docs.register(UploadPictureResource)

msg = Message('test subject', sender=Config.ADMINS[0], recipients=Config.ADMINS)
msg.body = 'text body'
msg.html = '<b>HTML</b> body'

if __name__ == '__main__':
    # with app.app_context():
    #     mail.send(msg)
    app.run(debug=Config.DEBUG, port=Config.PORT)
