import base64
from io import BytesIO
from PIL import Image


def get_image_type(file_path):
    import filetype
    
    pil_formats = {
        'png': 'PNG',
        'jpg': 'JPEG',
        'jpeg': 'JPEG',
        'gif': 'GIF',
        'bmp': 'BMP'
    }

    kind = filetype.guess(file_path)
    if kind is None:
        return "Unknown file type"
    return pil_formats[kind.mime.split("/")[-1]]

def convert_to_base64(image_path:str):
    """
    Convert PIL images to Base64 encoded strings

    :param pil_image: PIL image
    :return: Re-sized Base64 string
    """
    pil_image = Image.open(image_path)
    buffered = BytesIO()
    pil_image.save(buffered, format=get_image_type(image_path))  # You can change the format if needed
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str
