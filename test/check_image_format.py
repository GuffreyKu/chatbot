import os




def check_image_info(path):
    import imghdr
    # Get file extension
    ext = os.path.splitext(path)[1].lower()
    # print(f"File Extension: {ext}")
    
    # Guess format using imghdr
    fmt = imghdr.what(path)
    # print(f"MIME Type: {fmt if fmt else 'unknown'}")
    
    # Common PIL formats based on extension
    pil_formats = {
        '.png': 'PNG',
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.gif': 'GIF',
        '.bmp': 'BMP'
    }
    
    # print("\nCommon PIL-compatible formats:")
    for ext, fmt in pil_formats.items():
        if os.path.splitext(path)[1].lower() == ext:
            # print(f"{ext} → {fmt}")
            return fmt
  

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

# Example usage
if __name__ == "__main__":
    format = get_image_type("/Users/guffrey/dataset/archive/card_dataset/test/cam_image2.jpg")
    print(type(format))
    print(f"format : {format}")

