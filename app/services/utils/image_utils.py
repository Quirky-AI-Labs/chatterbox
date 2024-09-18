from PIL import Image


class ImageMixins:
    def load_image_from_path(self, path: str) -> Image:
        return Image.open(path)
