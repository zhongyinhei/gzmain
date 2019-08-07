FROM python:3.7
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN mkdir /code
WORKDIR /code
COPY . /code
COPY docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
RUN apt-get install uwsgi
RUN apt-get install libfontconfig
CMD /code/docker-entrypoint.sh
