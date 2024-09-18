import re
from typing import List

import fitz
import pandas as pd
from loguru import logger
from pydantic import BaseModel


class BBoxMixins:

    @staticmethod
    def iou(bbox1, bbox2):
        """
        Calculate Intersection over Union (IoU) of two bounding boxes.
        """
        x1, y1, x2, y2 = bbox1
        x3, y3, x4, y4 = bbox2
        x5, y5 = max(x1, x3), max(y1, y3)
        x6, y6 = min(x2, x4), min(y2, y4)
        intersection = max(0, x6 - x5) * max(0, y6 - y5)
        area1 = (x2 - x1) * (y2 - y1)
        area2 = (x4 - x3) * (y4 - y3)
        union = area1 + area2 - intersection
        return intersection / union if union else 0

    @staticmethod
    def bbox_area(bbox):
        x1, y1, x2, y2 = bbox
        return (x2 - x1) * (y2 - y1)

    @staticmethod
    def bbox_center(bbox):
        x1, y1, x2, y2 = bbox
        return (x1 + x2) / 2, (y1 + y2) / 2

    @staticmethod
    def combine(bboxes):
        x1 = min(bbox[0] for bbox in bboxes)
        y1 = min(bbox[1] for bbox in bboxes)
        x2 = max(bbox[2] for bbox in bboxes)
        y2 = max(bbox[3] for bbox in bboxes)
        return (x1, y1, x2, y2)

    @staticmethod
    def bbox_from_points(points):
        x = [point[0] for point in points]
        y = [point[1] for point in points]
        return (min(x), min(y), max(x), max(y))

    @staticmethod
    def bbox_from_image(image):
        return (0, 0, image.width, image.height)


class OCRMixins:
    COLUMNS: List[str] = [
        "x0",
        "y0",
        "x2",
        "y2",
        "Text",
        "block",
        "page",
        "index_sort",
        "line",
        "confidence",
    ]

    @staticmethod
    def _pdf_text_extract_page(page: fitz.Page) -> List:
        words = page.get_text("words")
        data = []
        for i, w in enumerate(words):
            x0, y0, x2, y2, text, block, line, _word = w
            try:
                ntext, nblock, nline = words[i + 1][4:7]
                if (nblock != block) or (nline != line) or ntext.startswith(":"):
                    raise IndexError
                brk = 1
            except IndexError:
                brk = 2
            data.append((text, x0, y0, x2, y2, block, line, brk))
        return data


class DFMixins:
    @staticmethod
    def combine(df: pd.DataFrame, horizontal_thresh: float) -> pd.DataFrame:
        """
        Combine the words in the DataFrame that are adjacent to each other.
        """
        if df.empty:
            return df

        df = df.sort_values(["y0", "x0"]).reset_index(drop=True)
        return df
