from flask import request, json, Response, Blueprint
from sqlalchemy import or_
import os
import hashlib
from ..models.FileModel import FileModel, FileSchema


file_api = Blueprint('files', __name__)

file_schema = FileSchema()


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


@file_api.route('/', methods=['POST'])
def create():
    """
    Create file Function
    """

    req_data = request.files["file"]
    binary = req_data.read()
    filename = req_data.filename
    # print(str(req_data.filename))
    # print(type(req_data.tell()))
    # print(str(get_md5(binary)))
    # print(str(get_sha1(binary)))

    insert_data = {"filename": filename,
                   "size": req_data.tell(),
                   "sha1": get_sha1(binary),
                   "md5": get_md5(binary),
                   "file_type": req_data.filename.split(".")[-1]}
    data, error = file_schema.load(insert_data)
    if error:
        return custom_response(error, 404)

    file_result = FileModel.get_one_file(get_sha1(binary))
    if not file_result:
        file = FileModel(data)
        file.save()
        download_file(binary, filename)
        file_message = file_schema.dump(file)
    else:
        file_message = {'message': 'file already exists!'}

    return custom_response(file_message, 201)


def download_file(binary, filename):
    with open("{}{}{}{}{}".format(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__name__)))),
                                  os.sep, "downloads", os.sep, filename), "wb") as file:
        # response = get(url)
        file.write(binary)


def get_md5(binary):
    buf = binary
    md5_hasher = hashlib.md5()
    md5_hasher.update(buf)

    return md5_hasher.hexdigest()


def get_sha1(binary):
    buf = binary
    sha1_hasher = hashlib.sha1()
    sha1_hasher.update(buf)

    return sha1_hasher.hexdigest()


@file_api.route('/<string:hash_value>', methods=['GET'])
def get_a_file(hash_value):
    """
    Get files according to hash_value
    """

    file = FileModel.get_one_file(hash_value)
    if not file:
        return custom_response({'error': 'file not found'}, 404)

    file_message = file_schema.dump(file, many=True)
    return custom_response(file_message, 200)


@file_api.route('', methods=['GET'])
def get_all_file():
    """
    Get all files
    """
    file = FileModel.get_all_files()

    if not file:
        return custom_response({'error': 'no file found'}, 404)
    file_message = file_schema.dump(file, many=True)
    return custom_response(file_message, 200)


@file_api.route('/<string:hash_value>', methods=['PUT'])
def update(hash_value):
    """
    Update a file based on hash
    """
    req_data = request.get_json()
    file = FileModel.get_one_file_only(hash_value)
    print(file)
    if not file:
        return custom_response({'error': 'file not found'}, 404)

    data, error = file_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    file.update(data)

    file_message = file_schema.dump(file)
    return custom_response(file_message, 200)
    # return "stuff"


@file_api.route('/<string:file_id>', methods=['PUT'])
def update_all(file_id):
    """
    Update a file based on id anf file_id
    """
    req_data = request.get_json()
    file = FileModel.get_one_file(file_id)
    if not file:
        return custom_response({'error': 'file not found'}, 404)

    data, error = file_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)

    for afile in file:
        afile.update(data)
        file_message = file_schema.dump(afile)

    return custom_response(file_message, 200)


@file_api.route('/<string:hash_value>', methods=['DELETE'])
def delete(hash_value):
    """
    Delete all files based on the given file_id
    """

    file = FileModel.get_one_file_only(hash_value)
    data, error = file_schema.dump(file)
    if not file:
        return custom_response({'error': 'file not found'}, 404)
    delete_file(data["filename"])
    file.delete()
    # print(FileModel.query.filter(FileModel.sha1 == hash_value))

    return custom_response({'message': 'deleted'}, 204)


def delete_file(file):
    location = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__name__))))+os.sep+"downloads"
    path = os.path.join(location, file)
    if os.path.exists(path):
        os.remove(path)
    else:
        print("The file does not exist")



