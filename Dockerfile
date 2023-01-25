FROM python:3.9.16-slim

# Install curl.
RUN apt-get update && \
    apt-get -y install \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Install poetry.
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH /root/.local/bin:$PATH

# Install essential python packages.
RUN pip install \
    ipykernel==6.20.2 \
    jupyterlab==3.5.3