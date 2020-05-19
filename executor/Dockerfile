# Environment setter image
FROM python:3.8.3-buster AS environment

# Set up environmental variables
ENV LANG=C.UTF-8 \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.0.3

# Set up base workdir
WORKDIR /executor

# Install OS package dependencies
RUN apt-get update && \
    rm -rf /var/lib/apt/lists/* && \
    # Install poetry
    pip install "poetry==$POETRY_VERSION"

# Setup the virtualenv
RUN python -m venv /venv

# Copy project dependency files to image
COPY pyproject.toml poetry.lock ./

# Install dependencies (export as requirements.txt and install using pip)
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin

# --------------------------------------------------------

# Final image
FROM python:3.8.3-slim-buster AS final

# Set up environmental variables
ENV LANG=C.UTF-8

# Get virtual environment
COPY --from=environment /venv /venv

# Use executables from the virtual env
ENV PATH="/venv/bin:$PATH"

# Set up base workdir
WORKDIR /executor

# Copy files to image
COPY . .

# Add a script to be executed every time the container starts.
COPY entrypoint.sh /usr/bin/
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
EXPOSE 8000

# Run as non-root user
RUN useradd -m human
USER human

# Start the main process.
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000", "--reload"]
