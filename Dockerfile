FROM python:3.13-slim-bookworm

RUN apt update && apt-get install -y \
	socat \
	&& rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash ctf
USER ctf
WORKDIR /home/ctf

COPY ./server/requirements.txt ./server/requirements.txt
RUN python3 -m venv venv
RUN /bin/bash -c "source venv/bin/activate && pip install -r server/requirements.txt"

COPY --chown=ctf:ctf ./server/ ./server/
COPY --chown=ctf:ctf --chmod=777 entrypoint.sh .

CMD ["/bin/bash", "entrypoint.sh"]