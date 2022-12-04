# https://www.digitalocean.com/community/tutorials/how-to-build-and-deploy-a-flask-application-using-docker-on-ubuntu-20-04
FROM tiangolo/uwsgi-nginx-flask:latest

RUN apt-get update
RUN apt-get install -y bash nano vim default-jdk wget

ENV STATIC_URL static
ENV STATIC_PATH app/static

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# RUN wget http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server/1.24/tika-server-1.24.jar -P /tika-server.jar
# RUN wget http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server/1.24/tika-server-1.24.jar.md5 -P /tika-server.jar.md5
