from marshmallow import fields, Schema
from sqlalchemy.dialects.postgresql import UUID
import datetime
import enum
from . import db
from .JobModel import JobSchema


class JobIdModel(db.Model):
    """
    JobId Model
    """
    # table name
    __tablename__ = 'jobid'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    jobs = db.relationship('JobModel', backref='jobs', lazy=True)

    # class constructor

    def __init__(self, data):
        """
        Class constructor
        """

        self.job_id = data.get('job_id')

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
    def get_all_jobids():
        return JobIdModel.query.all()

    @staticmethod
    def get_one_jobid(job_id):
        return JobIdModel.query.filter(JobIdModel.job_id == job_id).all()

    def __repr__(self):
        return '<id {}>'.format(self.id)


class JobIdSchema(Schema):
    """
  JobId Schema
  """

    id = fields.Int(dump_only=True)
    job_id = fields.UUID(required=True)
    jobs = fields.Nested(JobSchema, many=True)


