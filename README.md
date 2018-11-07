1) Build the docker environment by running docker build. This should set up 3 services web, db (postgres) and redis
2) run the following commands from the project root /GenomicPrediction
  a) to build the database tables:
      docker-compose exec web python /code/GenomicPrediction/manage.py migrate
  b) to create the admin user admin/password:
     docker-compose exec web python /code/GenomicPrediction/manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'benzyp@yahoo.com', 'password')"
  c) to start the redis worker process:
     docker-compose exec web python /code/GenomicPrediction/manage.py rqworker low
3) To get started import the endpoints from Genomic-Prediction_2018-11-01.json into Insomnia
4) Configure the Authenticate endpoint to point to the target server. It will return the admin user token
5) Configure the other endpoints to point to the target server and paste the token into the Bearer value
6) Create a patient, several enbryos and send the email report.
