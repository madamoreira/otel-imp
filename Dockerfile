
FROM python:3.12.2

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools wheel psutil

RUN pip install "poetry==1.8.2"

RUN poetry install
RUN opentelemetry-bootstrap -a install

EXPOSE 8008

# STOPSIGNAL SIGINT
RUN chmod +x ./run.sh
ENTRYPOINT [ "./run.sh" ]
