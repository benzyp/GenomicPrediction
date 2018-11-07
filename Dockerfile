FROM python:3.7
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt

ADD . /code/

#CMD [ "python", "manage.py migrate"]
#CMD [ "python", "manage.py createsuperuser --username admin --password password --noinput --email benzyp@gmail.com"]
