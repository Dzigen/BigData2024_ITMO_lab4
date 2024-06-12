FROM dzigen/base_model_api:v1

ARG APP_DIR=/home/app

ENV PYTHONPATH "${PYTHONPATH}:${APP_DIR}"
RUN echo $PYTHONPATH

RUN mkdir /home/logs

WORKDIR "${APP_DIR}"
COPY src/ src/
COPY vault.yaml vault.yaml

WORKDIR "${APP_DIR}/src/"

ENTRYPOINT ["sh", "-c", "python main.py"]