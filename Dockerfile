FROM python:3.7
RUN apt-get update && apt-get upgrade -y && apt-get clean
RUN curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
   python get-pip.py --force-reinstall && \
    rm get-pip.py
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
COPY ./app /app
WORKDIR "/app"
EXPOSE 8050
ENTRYPOINT [ "python3" ]
CMD [ "index.py" ]
#FROM tiangolo/uwsgi-nginx-flask:python3.7
#COPY requirements.txt /tmp/requirements.txt
#RUN pip3 install -r /tmp/requirements.txt
#COPY ./app /app