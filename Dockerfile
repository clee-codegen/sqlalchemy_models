FROM python:3.10.6 as builder

ENV PATH="/root/.local/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry self update --preview && \
    poetry config virtualenvs.in-project true


COPY pyproject.toml poetry.lock /venv/

WORKDIR /venv/

RUN poetry install

FROM python:3.10.6

LABEL version="0.1.0"
LABEL author="Chris Lee"
LABEL email="clee@codegen.com"
LABEL description="Cut from cookiecutter-poetry-py3-10"

ENV PYTHONPATH=/sqlalchemy_models PATH=/venv/.venv/bin:/sqlalchemy_models/bin:/sqlalchemy_models/scripts:${PATH}
COPY --from=builder /venv /venv

RUN apt update

WORKDIR /sqlalchemy_models
COPY . /sqlalchemy_models


ENTRYPOINT [ "bash" ]
