from flask import request, json, Response, Blueprint

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

    req_data = request.get_json()
    print(str(req_data))
    data, error = file_schema.load(req_data)
    if error:
        return custom_response(error, 404)
    file = FileModel(data)
    file.save()
    file_message = file_schema.dump(file)

    return custom_response(file_message, 201)


@file_api.route('/<string:file_id>', methods=['GET'])
def get_a_file(hash_value):
    """
    Get files according to file_id
    """

    file = FileModel.get_one_file(hash_value)
    if not file:
        return custom_response({'error': 'file not found'}, 404)

    file_message = file_schema.dump(file, many=True)
    return custom_response(file_message, 200)


@file_api.route('', methods=['GET'])
def get_all_file():
    """
    Get a all files
    """
    file = FileModel.get_all_files()

    if not file:
        return custom_response({'error': 'no file found'}, 404)
    file_message = file_schema.dump(file, many=True)
    return custom_response(file_message, 200)


@file_api.route('/<int:id>/<string:file_id>', methods=['PUT'])
def update(id, file_id):
    """
    Update a file based on id anf file_id
    """
    req_data = request.get_json()
    file = FileModel.get_one_file_only(id, file_id)
    if not file:
        return custom_response({'error': 'file not found'}, 404)

    data, error = file_schema.load(req_data, partial=True)
    if error:
        return custom_response(error, 400)
    file.update(data)

    file_message = file_schema.dump(file)
    return custom_response(file_message, 200)


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


@file_api.route('/<string:file_id>', methods=['DELETE'])
def delete(file_id):
    """
    Delete all files based on the given file_id
    """

    file = FileModel.get_one_file(file_id)

    if not file:
        return custom_response({'error': 'file not found'}, 404)

    FileModel.query.filter(FileModel.file_id == file_id).delete()

    return custom_response({'message': 'deleted'}, 204)



