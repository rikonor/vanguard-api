FROM python:2.7

ADD . /src

# Install seleniumapis
WORKDIR /src/seleniumapis
RUN python setup.py develop

# Install api
WORKDIR /src/api
RUN python setup.py develop

EXPOSE 5000

WORKDIR /src/api/api
ENTRYPOINT python api.py
