INSTRUCTIONS:

1.
$ export FLASK_ENV=development/production
$ export DATABASE_URL= postgres://name:password@host:port/dbname

2.Then run "python manage.py db init"
3.Then run "python manage.py db migrate"
4.Then run "python manage.py db update". Now you must have the table files
5.Then run "python run.py"

CRUD FUNCTIONS
POST /filelog/ - insert a file 
GET /filelog/<string:hash> - get a file and corresponding metadata 
GET /filelog - get all files
PUT /filelog/<string:hash> - update a specific file
DELETE /filelog/<string:hash> - delete a file 