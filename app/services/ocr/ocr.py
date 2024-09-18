import os
from typing import List, Union

import fitz
import pandas as pd
from loguru import logger
from pypdf import PdfReader

from ..utils.ocr_utils import OCRMixins
from ..utils.utils import log_traceback
from .base import BaseParser
from .extractors import OCRProvider

OCR_PROVIDER = os.getenv("OCR_PROVIDER", "tesseract")


class DigitalOCRParser(BaseParser, OCRMixins):
    def parse(self, file: str, **kwargs):
        doc = fitz.open(file)
        df_list = []
        for pageno, page in enumerate(doc):
            page_word_detail_list = self._pdf_text_extract_page(page)
            COLUMNS = [
                "Text",
                "x0",
                "y0",
                "x2",
                "y2",
                "block",
                "line",
            ]
            df = pd.DataFrame(page_word_detail_list, columns=COLUMNS)
            df["page"] = pageno
            df_list.append(df)

        return df_list


class NonDigitalOCRParser(BaseParser, OCRMixins):

    def __init__(self, provider: str = OCR_PROVIDER):
        self.provider = provider

    def parse(self, files: str, **kwargs) -> List[pd.DataFrame]:
        logger.info(f"STARTING {self.__class__.__name__}!!!")
        ocr_extractor = OCRProvider.get_extractor(self.provider)

        df_lst = ocr_extractor.extract(files)
        return df_lst


class OCRParser(BaseParser, OCRMixins):
    def __init__(self, provider: str = OCR_PROVIDER):
        self.parsers = (DigitalOCRParser(), NonDigitalOCRParser(provider))

    def parse(self, files: str, **kwargs) -> List[pd.DataFrame]:
        df_lst = []
        for parser in self.parsers:
            try:
                df_lst = parser.parse(files, **kwargs)
            except Exception as e:
                logger.error(f"Error in {parser.__class__.__name__}: {e}")
                log_traceback()
            if df_lst:
                return df_lst
        return df_lst
