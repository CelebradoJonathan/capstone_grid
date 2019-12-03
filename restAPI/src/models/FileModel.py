from marshmallow import fields, Schema
from sqlalchemy import or_
from . import db


class FileModel(db.Model):
    """
    File Model
    """
    # table name
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer)
    filename = db.Column(db.String(128))
    sha1 = db.Column(db.String(128))
    md5 = db.Column(db.String(128))
    file_type = db.Column(db.String(5))

    # class constructor

    def __init__(self, data):
        """
        Class constructor
        """

        self.size = data.get('size')
        self.filename = data.get('filename')
        self.sha1 = data.get('sha1')
        self.md5 = data.get('md5')
        self.file_type = data.get('file_type')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_files():
        return FileModel.query.all()

    @staticmethod
    def get_one_file(hash_value):
        return FileModel.query.filter(or_(FileModel.sha1 == hash_value, FileModel.md5 == hash_value)).all()

    @staticmethod
    def get_one_file_only(hash_value):
        return FileModel.query.filter(or_(FileModel.sha1 == hash_value, FileModel.md5 == hash_value)).first()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class FileSchema(Schema):
    """
  File Schema
  """

    id = fields.Int(dump_only=True)
    size = fields.Int(required=True)
    filename = fields.Str(required=True)
    sha1 = fields.Str(required=True)
    md5 = fields.Str(required=True)
    file_type = fields.Str(required=False)
