FROM dzigen/base_model_api:v1

ARG APP_DIR=/home/app
ARG LOG_DIR=/home/logs
ARG APP_PORT=4567

ENV PYTHONPATH "${PYTHONPATH}:${APP_DIR}"
RUN echo $PYTHONPATH
RUN mkdir "${LOG_DIR}"

WORKDIR "${APP_DIR}"
COPY src/ src/
COPY models/ models/
COPY tests/unit tests/unit
COPY vault.yaml vault.yaml

RUN pytest
RUN rm -rf tests

WORKDIR "${APP_DIR}/src/"

ENTRYPOINT ["sh", "-c", "uvicorn api:app --reload --host 0.0.0.0 --port 4567"]