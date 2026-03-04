from abc import ABC, abstractmethod


class ValidadorBase(ABC):

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def validar(self, df):
        pass
