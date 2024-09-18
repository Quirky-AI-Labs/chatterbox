from dataclasses import dataclass
from typing import List

import pandas as pd

from ..utils.ocr_utils import BBoxMixins, DFMixins


@dataclass
class BBox(BBoxMixins):
    x0: float
    y0: float
    x2: float
    y2: float

    @classmethod
    def create_empty_bbox(cls):
        return cls(-1, -1, -1, -1)

    def to_tuple(self):
        return (self.x0, self.y0, self.x2, self.y2)

    def to_dict(self):
        return {
            "x0": self.x0,
            "y0": self.y0,
            "x2": self.x2,
            "y2": self.y2,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["x0"], data["y0"], data["x2"], data["y2"])

    def __str__(self) -> str:
        return f"({self.x0}, {self.y0}, {self.x2}, {self.y2})"

    def __repr__(self) -> str:
        return f"BBox({self.x0}, {self.y0}, {self.x2}, {self.y2})"

    @property
    def width(self):
        return self.x2 - self.x0

    @property
    def height(self):
        return self.y2 - self.y0

    @property
    def bbox(self):
        return self.to_tuple()


class Word(BBoxMixins):
    x0: float
    y0: float
    x2: float
    y2: float
    Text: str
    block: int
    page: int
    index_sort: int
    line: int
    confidence: float

    @classmethod
    def create_empty_word(cls):
        return cls(-1, -1, -1, -1, "", -1, -1, -1, "", -1, -1)

    def to_bbox(self):
        return BBox(self.x0, self.y0, self.x2, self.y2)

    def to_dict(self):
        return {
            "x0": self.x0,
            "y0": self.y0,
            "x2": self.x2,
            "y2": self.y2,
            "Text": self.Text,
            "block": self.block,
            "page": self.page,
            "index_sort": self.index_sort,
            "line": self.line,
            "confidence": self.confidence,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["x0"],
            data["y0"],
            data["x2"],
            data["y2"],
            data["Text"],
            data["block"],
            data["page"],
            data["index_sort"],
            data["line"],
            data["confidence"],
        )

    @classmethod
    def from_bbox(cls, bbox):
        return cls(bbox.x0, bbox.y0, bbox.x2, bbox.y2, "", -1, -1, -1, "", -1, -1)

    @property
    def Text(self):
        return self.Text

    @property
    def text(self):
        return self.Text

    def __str__(self) -> str:
        return f"{self.Text} - ({self.x0}, {self.y0}, {self.x2}, {self.y2}) - {self.block} - {self.page} - {self.index_sort} - {self.line}"


class WordList:
    word_list: List[Word]
    bbox: BBox

    @classmethod
    def from_df(cls, df: pd.DataFrame):
        word_list = [Word.from_dict(row) for index, row in df.iterrows()]
        bbox = BBoxMixins.combine([word.to_bbox() for word in word_list])
        return cls(word_list, bbox)

    @classmethod
    def from_dict(cls, data: dict):
        word_list = [Word.from_dict(row) for row in data["word_list"]]
        bbox = BBox.from_dict(data["bbox"])
        return cls(word_list, bbox)

    def to_df(self):
        data = [word.to_dict() for word in self.word_list]
        return pd.DataFrame(data)

    def to_dict(self):
        return {
            "word_list": [word.to_dict() for word in self.word_list],
            "bbox": self.bbox.to_dict(),
        }

    @property
    def words(self):
        return self.word_list

    @property
    def text(self):
        return " ".join([word.Text for word in self.word_list])

    @property
    def bbox(self):
        return BBoxMixins.combine([word.to_bbox() for word in self.word_list])

    @property
    def Text(self):
        return self.text

    def __len__(self):
        return len(self.word_list)

    def __getitem__(self, index):
        return self.word_list[index]

    def __iter__(self):
        return iter(self.word_list)

    def __repr__(self):
        return f"WordList({self.word_list})"

    def __str__(self):
        return str(self.word_list)


class OCRDATA(DFMixins):
    df: pd.DataFrame

    def __init__(self, df: pd.DataFrame):
        self.df = df

    @classmethod
    def from_df(cls, df: pd.DataFrame):
        return cls(df)

    @staticmethod
    def check_empty_ocrdata(ocrdata):
        if ocrdata is None or ocrdata.df.empty:
            return True
        return False

    @classmethod
    def create_empty_object(cls):
        return cls(pd.DataFrame())

    @property
    def text(self):
        return " ".join(self.df["Text"])


class DocOCR:
    def __init__(self, pages: List[OCRDATA]):
        self.pages = pages

    @classmethod
    def from_df(
        cls,
        dfs: List[pd.DataFrame],
    ):
        pages = [OCRDATA.from_df(df) for df in dfs]
        return cls(pages)

    def __len__(self):
        return len(self.pages)

    def __getitem__(self, index):
        return self.pages[index]

    def __iter__(self):
        return iter(self.pages)

    @property
    def text(self):
        return " ".join([page.text for page in self.pages])
