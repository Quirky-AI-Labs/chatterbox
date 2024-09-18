from abc import ABC, abstractmethod


class BaseParser(ABC):

    @abstractmethod
    def parse(self, **kwargs):
        raise NotImplementedError


class BaseExtractor(ABC):

    @abstractmethod
    def extract(self):
        raise NotImplementedError


class BaseHandler(ABC):

    @abstractmethod
    def handle(self):
        raise NotImplementedError
