from PIL import Image
from PIL.ExifTags import TAGS

def GetExif(image):
    exifdata = image.getexif()

    exifdict = {
        TAGS[k]: v
        for k, v in exifdata.items()
        if k in TAGS
    }
    # Get the ifd keys too
    ifddict = {
        TAGS[k]: v
        for k, v in exifdata.get_ifd(0x8769).items()
        if k in TAGS
    }

    # Flatten result
    exifdict.update(ifddict)
    return exifdict


if __name__ == "__main__":
    GetExif("https://s3.us-west-2.amazonaws.com/img.dump/image/DSC00011.jpg")