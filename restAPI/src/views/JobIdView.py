from flask import request, json, Response, Blueprint, g

from ..models.JobModel import JobModel, JobSchema
from ..models.JobIdModel import JobIdModel, JobIdSchema

# from ..shared.Authentication import Auth

jobid_api = Blueprint('jobid', __name__)

jobid_schema = JobIdSchema()


@jobid_api.route('/', methods=['POST'])
def create():
    """
    Create Job Function
    """

    req_data = request.get_json()
    data, error = jobid_schema.load(req_data)
    if error:
        return custom_response(error, 400)
    jobid = JobIdModel(data)
    jobid.save()
    jobid_message = jobid_schema.dump(jobid)

    return custom_response(jobid_message, 201)


def custom_response(res, status_code):
    """
    Custom Response Function
    """

    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )


@jobid_api.route('/<string:job_id>', methods=['GET'])
def get_a_job(job_id):
    """
    Get a single jobid and corresponding jobs
    """

    jobid = JobIdModel.get_one_jobid(job_id)
    if not jobid:
        return custom_response({'error': 'jobId not found'}, 404)

    jobid_message = jobid_schema.dump(jobid, many=True)
    return custom_response(jobid_message, 200)




