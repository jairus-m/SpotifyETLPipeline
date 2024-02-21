FROM python:3.9.18

WORKDIR /spotify_etl

COPY ./src ./src
COPY ./configs ./configs
COPY ./token.txt ./token.txt
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock

ENV PYTHONPATH "${PYTHONPATH}:/spotify_etl"

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

CMD python src/main.py configs/config.yml