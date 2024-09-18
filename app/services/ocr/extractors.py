from typing import List

import numpy as np
import pandas as pd
import pytesseract
from loguru import logger
from pdf2image import convert_from_path
from PIL import Image
from pytesseract import Output

from ..utils.ocr_utils import DFMixins, OCRMixins
from .base import BaseExtractor


class TesseractExtractor(BaseExtractor, OCRMixins, DFMixins):

    def split_filename_and_ext(self):
        file = self.file_path.split("/")[-1].rsplit(".", 1)
        if len(file) == 1:
            file_name = file[0]
            file_ext = ""
        elif len(file) == 2:
            file_name = file[0]
            file_ext = file[1].strip()
        else:
            file_name = ""
            file_ext = ""
        return file_name, file_ext

    def get_standard_format(self, df):
        df["x0"] = df["left"]
        df["y0"] = df["top"]
        df["x2"] = df["x0"] + df["width"]
        df["y2"] = df["y0"] + df["height"]
        df["block"] = df["block_num"]
        df["line"] = df["line_num"]
        df["page"] = df["page_num"]
        df["Text"] = df["text"]
        df["confidence"] = df["conf"] / 100
        df["index_sort"] = df["word_num"]
        df_standard = df[OCRMixins.COLUMNS]
        return df_standard

    def extract(self, file: str, parallelize: bool = False) -> List[pd.DataFrame]:
        df_list = []
        if file.lower().endswith(".pdf"):
            files = convert_from_path(file)
            files = [np.array(img) for img in files]
        else:
            img_ = Image.open(file)
            files = [np.array(img_)]
        for img in files:
            df = self.get_ocr_dataframe(img)
            df_list.append(df)

        return df_list

    def get_ocr_dataframe(self, img):
        df = pytesseract.image_to_data(img, output_type=Output.DATAFRAME)
        df = df.dropna(subset=["text"])
        try:
            df = df[~df["text"].str.isspace()]
        except:
            logger.warning("Skipping space removal")
        df = self.get_standard_format(df)
        return df


class OCRProvider:
    EXTRACTOR_MAP = {"tesseract": TesseractExtractor}

    @staticmethod
    def get_extractor(provider: str) -> BaseExtractor:
        if provider not in OCRProvider.EXTRACTOR_MAP:
            raise Exception("Provider not found in the extractor map")
        return OCRProvider.EXTRACTOR_MAP.get(provider)()
