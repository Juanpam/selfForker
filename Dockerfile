# test argument
ARG test=FALSE

# set base image (host OS)
FROM python:3.7 as base

# set working dir to root of the django project
WORKDIR /home/selfForker/

# copy the requirements file to the working directory
COPY ./selfForker/requirements.txt .

# install python dependencies
RUN pip install -r requirements.txt
RUN pip install gunicorn==20.1.0

# copy the project to the working directory
ADD ./selfForker/ .

# setup gunicorn environment variables:
ENV WORKERS=1
ENV TIMEOUT=240

# port exposure
EXPOSE 8000

RUN echo "yes" | python manage.py collectstatic --settings selfForker.productionSettings
# command to run on container start when nothing else is run:
CMD gunicorn -b 0.0.0.0:8000 --timeout=$TIMEOUT --workers=$WORKERS --env DJANGO_SETTINGS_MODULE=selfForker.productionSettings selfForker.wsgi