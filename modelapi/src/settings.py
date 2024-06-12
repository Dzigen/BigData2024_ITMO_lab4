import os 
from ansible_vault import Vault
from pathlib import Path
from dataclasses import dataclass

SECRETS_FILE = Path.joinpath(Path(__file__).parent.parent.resolve(), 'vault.yaml')

PWD_FILE = Path.joinpath(Path(__file__).parent.parent.resolve(), '.vault_pass')
PWD_ENV_VAR = 'MODELAPI_VAULT_PASS'

@dataclass
class Secrets:
    KAFKA_TOPIC_NAME: str = None
    KAFKA_BOOTSTRAP_SERVER: str = None
    KAFKA_VERSION: tuple = None
    KAFKA_PARTITIONS_COUNT: int = None
    KAFKA_REPLICATION_COUNT: int = None

    @classmethod
    def load(cls) -> None:
        try:
            vault = Vault(Path(PWD_FILE).read_text())
        except FileNotFoundError:
            try:
                vault = Vault(os.environ[PWD_ENV_VAR])
            except KeyError:
                raise AttributeError

        data = vault.load(open(SECRETS_FILE).read())
        return cls(**data)

secrets = Secrets().load()

if __name__ == "__main__":
    print(secrets)