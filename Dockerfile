FROM python:3.11

WORKDIR /app

# Install project python dependencies
ADD ["pyproject.toml", "poetry.lock", "./"]

RUN pip install --upgrade pip
RUN pip install poetry~=1.7.1 \
    && poetry config virtualenvs.in-project false \
    && poetry config virtualenvs.path /app/.venv-docker
RUN poetry install

ADD src src
RUN poetry install

ADD ["main.py", "./"]

CMD ["poetry", "run", "python", "main.py"]
