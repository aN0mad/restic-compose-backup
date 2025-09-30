FROM restic/restic:0.9.6

RUN apk update && apk add python3 \ 
    dcron \
    mariadb-client \
    postgresql-client \
    mariadb-connector-c-dev \ 
    bash

ADD . /restic-compose-backup
WORKDIR /restic-compose-backup
# RUN pip3 install -U pip setuptools wheel && pip3 install -e .
RUN python3 -m pip install --user pipx
RUN echo export PATH="/root/.local/bin:$PATH" >> ~/.bashrc
RUN /root/.local/bin/pipx install .
ENV XDG_CACHE_HOME=/cache

ENTRYPOINT []
CMD ["./entrypoint.sh"]
