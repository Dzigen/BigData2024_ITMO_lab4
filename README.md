# BigData2024_ITMO_lab1

Реализованный конвейер передачи данных между запускаемыми контейнерами (названия контейнеров соответствуют названиям run-директив в docker-compose.yaml):
* (modelapi) -> (kafka) -> (kafkadb_connector) -> (mongodb)
* (kafkadb_connector) -> (zookeeper)
* (mongodb) -> (mongoui)

Следующие директории соответствуют запускаемым docker-контейнерам:
* modelapi/ - API-сервис с обученной моделью; выполняет предсказания.
* mongodb/ - сервис с базой данных MongoDB.
* test_model_api/ - контейнер с окружением для проведения функционального тестирования API-сервиса (modelapi).
* kafka_db_connector/ - контейнер для передачи сообщений от контейнера с kafka (kafka) к контейнеру с MongoDB (mongodb) для логирования результатов предсказания в API-сервисе (modelapi).

asd
