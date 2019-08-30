FROM pinellolab/stream:0.3.8

RUN mkdir /stream
COPY transition_command_line.py /stream/transition_command_line.py

ENTRYPOINT []
