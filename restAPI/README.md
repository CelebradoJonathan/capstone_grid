INSTRUCTIONS:

1.
$ export FLASK_ENV=development
$ export DATABASE_URL= postgres://name:password@host.docker.internal:5432/dbname

2.Then run "python manage.py db init"
3.Then run "python manage.py db migrate"
4.Then run "python manage.py db update". Now you must have the tables jobs and jobid.
5.Then run "python run.py"

CRUD FUNCTIONS
POST /modulelogid/ - create a job_id (referenced in job table)
GET /modulelogid/<string:job_id> - get a job_id and corresponding jobs 

POST /modulelog/ - create a job
GET /modulelog/<string:job_id> - get jobs according to job_id
GET /modulelog - get all jobs
PUT /modulelog/<int:id>/<string:job_id> - update a specific job, accepts the id and the job_id
PUT /modulelog/<string:job_id> - update all jobs with given job_id
DELETE /modulelog/<string:job_id> - delete all jobs with given job_id