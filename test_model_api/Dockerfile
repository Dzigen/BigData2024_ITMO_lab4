FROM dzigen/base_model_api:v1

ARG APP_DIR=/home/app
EXPOSE 4567

ENV PYTHONPATH "${PYTHONPATH}:${APP_DIR}"
RUN echo $PYTHONPATH

WORKDIR ${APP_DIR}
COPY tests/functional tests/functional

ENTRYPOINT ["pytest"]