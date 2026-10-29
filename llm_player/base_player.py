from abc import ABC, abstractmethod


class BasePlayer(ABC):

    @abstractmethod
    def get_prompt(self, previous_plan, action, enemy_pos) -> str:
        ...

    @abstractmethod
    def get_key_mapping(self) -> dict[str, str]:
        ...