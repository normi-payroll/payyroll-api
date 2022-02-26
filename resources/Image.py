from flask.views import MethodView
from flask import jsonify, request, abort
import uuid
import os

from werkzeug.utils import secure_filename

class UploadAPI(MethodView):

    def __init__(self):
        if not request.files:
            abort(400)

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

    def allowed_file(self,filename):
	    return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

def post(self):
    file = request.files['file']
    if file.filename == '':
        error = 'No file selected for uploading'
        return jsonify({"error":error}), 400

    if file and self.allowed_file(file.filename):
        # generate unique filename
        filename = str(uuid.uuid4()) + '.' + filename.rsplit('.', 1)[1].lower()
                
        filename = secure_filename(file.filename)
                
        # filepath to save image                 
        file.save(os.path.join(os.getcwd(), 'static', 'upload', 'image', '', filename))

        response = 'File successfully uploaded'
        return jsonify({"message": response, "body":{"image_id":filename}}), 201
    else:
        error = 'Allowed file types are png, jpg, jpeg, gif'
        return jsonify({"error": error}), 400