from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

import pandas as pd
from langchain.schema import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from loguru import logger

from ..ocr.ocr import OCRParser
from ..structures.ocr import DocOCR


class DocumentMixins:
    @staticmethod
    def get_splitted_docs(documents: List[LangchainDocument]):
        logger.info("Splitting the documents into chunks ...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function=len)
        chunks = text_splitter.split_documents(documents)
        logger.info(f"Splitted into {len(chunks)} chunks.")
        return chunks


class BaseDocument(ABC):

    @classmethod
    @abstractmethod
    def load_document(cls, path: str, **kwargs) -> "BaseDocument":
        raise NotImplementedError

    @abstractmethod
    def get_contents(self, **kwargs) -> str:
        raise NotImplementedError

    def __str__(self):
        return self.get_contents()[:20]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.get_contents()[:20]})"

    def generate_document(self, **kwargs) -> List[LangchainDocument]:
        contents = self.get_contents()
        if not contents:
            logger.debug(f"Empty contents. Skipping document generation!!!")
            return []
        return [LangchainDocument(page_contents=self.get_contents())]


class OCRDocument(BaseDocument, DocumentMixins):
    def __init__(self, path: str, **kwargs):
        self.path = path
        self.doc_ocr = self._load_ocr(path, **kwargs)

    def _load_ocr(self, path: str, **kwargs):
        ocr_provider = kwargs.get("ocr_provider", "tesseract")
        parser = OCRParser(ocr_provider)
        df_lst = parser.parse(path)
        doc_ocr: DocOCR = DocOCR.from_df(df_lst)
        return doc_ocr

    @classmethod
    def load_document(cls, path: str, **kwargs):
        return cls(path, **kwargs)

    def get_contents(self, **kwargs) -> str:
        return self.doc_ocr.text

    def __len__(self):
        return len(self.doc_ocr)

    def __getitem__(self, index):
        return self.doc_ocr[index]

    def __iter__(self):
        return iter(self.doc_ocr)

    def __repr__(self):
        return f"OCRDocument({self.path})"

    def __str__(self):
        return self.get_contents()[:20]

    def generate_document(self, **kwargs) -> List[LangchainDocument]:
        documents = []
        for i, page in enumerate(self.doc_ocr):
            contents = page.text
            metadata = {"page_no": i + 1, "source": self.path}
            document = LangchainDocument(page_content=contents, metadata=metadata)
            documents.append(document)
        return documents


class CSVDocument(BaseDocument):
    def __init__(self, path: str, **kwargs):
        self.path = path
        self.data = self._load_csv(path, **kwargs)

    def _load_csv(self, path: str, **kwargs):
        return pd.read_csv(path)

    def get_contents(self, **kwargs) -> str:
        return self.data.to_string()

    def __repr__(self):
        return f"CSVDocument({self.path})"

    def __str__(self):
        return self.get_contents()[:20]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data.iloc[index]

    def __iter__(self):
        return iter(self.data)

    def __repr__(self):
        return f"CSVDocument({self.path})"

    def __str__(self):
        return self.get_contents()[:20]
