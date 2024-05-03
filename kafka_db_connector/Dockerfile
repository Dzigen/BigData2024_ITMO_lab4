FROM dzigen/base_model_api:v1

ENV PYTHONPATH "${PYTHONPATH}:${APP_DIR}"
RUN echo $PYTHONPATH

COPY src/ src/
COPY tests/unit tests/unit
COPY vault.yaml vault.yaml

RUN mkdir /home/logs

RUN pytest
RUN rm -rf tests

WORKDIR "${APP_DIR}/src/"

ENTRYPOINT ["sh", "-c", "python main.py"]