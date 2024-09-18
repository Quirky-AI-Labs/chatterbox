from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger

from ..ingress.channel import BaseDocument


class BaseDocumentSplitter(ABC):
    @abstractmethod
    def split(self, document: BaseDocument, **kwargs) -> List[BaseDocument]:
        raise NotImplementedError


class PageSplitter(BaseDocumentSplitter):
    name = "page"

    def split(self, documents: List[BaseDocument], **kwargs) -> List[BaseDocument]:
        logger.info("Splitting the documents into chunks ...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Splitted into {len(chunks)} chunks.")
        return chunks


class DocumentSplitterStrategy:
    STRATEGY_MAP = {"page": PageSplitter}

    def __init__(self):
        self.strategy = None

    def get_splitter(self, strategy) -> BaseDocumentSplitter:
        if strategy in self.STRATEGY_MAP:
            self.strategy = self.STRATEGY_MAP.get(strategy)()
        else:
            raise NotImplementedError(f"Splitter strategy {self.strategy} is not implemented yet!!!")
        return self.strategy

    def split(self, document: BaseDocument, **kwargs) -> List[BaseDocument]:
        splitter = self.get_splitter()
        return splitter.split(document, **kwargs)

    def __repr__(self):
        return f"DocumentSplitterStrategy - ({self.strategy})"
