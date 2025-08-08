FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y binutils && \
    rm -rf /var/lib/apt/lists/*
COPY ./source /source

WORKDIR /usr/bin/numerology

RUN pip install pyinstaller && \
    pip install -r /source/numerology/requirements.txt && \
    ls /source/numerology -al && \
    pyinstaller /source/numerology/build/docker/numerology.spec

RUN ln -s /usr/bin/numerology/dist/numerology/numerology /usr/local/bin/numerology

RUN rm -rf /source

WORKDIR /app

ENTRYPOINT ["numerology"]
CMD ["--help"]