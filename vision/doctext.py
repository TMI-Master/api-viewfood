import argparse
import io
from enum import Enum

from google.cloud import vision
from PIL import Image, ImageDraw, ImageFont


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    for bound in bounds:
        draw.polygon([
            bound.vertices[0].x, bound.vertices[0].y,
            bound.vertices[1].x, bound.vertices[1].y,
            bound.vertices[2].x, bound.vertices[2].y,
            bound.vertices[3].x, bound.vertices[3].y], None, color)
    return image

def draw_text(image, bounds, texts, color):
    """Draw text in the image """
    draw = ImageDraw.Draw(image)

    aux = 0
    #print(texts)
    #print(bounds)
    for bound in bounds:
        if (aux != 0):
            #print(bound.vertices[0].x)
            draw.text((bound.vertices[0].x, bound.vertices[0].y), str(texts[aux]).encode('utf-8'), fill="black", anchor="ms")
        aux += 1

    return image

def get_document_bounds(image_file, feature):
    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient()

    bounds = []
    texts = []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation
    datas = response.text_annotations

    for text in datas:
        #print('=' * 30)
        #print(text.description)
        #vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
        texts.append(text.description)
        bounds.append(text.bounding_poly)

        #print('bounds:', ",".join(vertices))
    #print(document)

    # Collect specified feature bounds by enumerating all document features
    """
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if (feature == FeatureType.SYMBOL):
                            bounds.append(symbol.bounding_box)

                    if (feature == FeatureType.WORD):
                        bounds.append(word.bounding_box)

                if (feature == FeatureType.PARA):
                    bounds.append(paragraph.bounding_box)

            if (feature == FeatureType.BLOCK):
                bounds.append(block.bounding_box)
    """
    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds , texts


def render_doc_text(filein, fileout):
    image = Image.open(filein)
    #bounds, texts = get_document_bounds(filein, FeatureType.BLOCK)
    #draw_boxes(image, bounds, 'blue')
    #bounds, texts = get_document_bounds(filein, FeatureType.PARA)
    #draw_boxes(image, bounds, 'red')
    bounds, texts = get_document_bounds(filein, FeatureType.WORD)
    draw_boxes(image, bounds, 'yellow')
    draw_text(image, bounds, texts, 'yellow')

    if fileout != 0:
        image.save(fileout)
    else:
        image.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('detect_file', help='The image for text detection.')
    parser.add_argument('-out_file', help='Optional output file', default=0)
    args = parser.parse_args()

    render_doc_text(args.detect_file, args.out_file)
