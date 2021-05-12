import io
import math
from enum import Enum

import six
from google.cloud import translate_v2 as translate
from google.cloud import vision
from PIL import Image, ImageDraw
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.menu import serializers
from apps.menu.models import Menu
from conf.settings import MEDIA_ROOT


class FeatureType(Enum):
    PAGE = 1
    BLOCK = 2
    PARA = 3
    WORD = 4
    SYMBOL = 5


def translate_text_print(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: \
        {}".format(result["detectedSourceLanguage"]))


def translate_all_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    translate_client = translate.Client()

    result_text = []

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    n_text = len(text)
    # print(n_text)
    num_executions = math.ceil(n_text / 120)
    # print(num_executions)
    for i in range(0, num_executions):
        # print(i)
        pos = i * 120
        # print(pos)
        end_pos = pos + 120
        if (pos + 120) > n_text:
            end_pos = n_text
        else:
            end_pos = pos + 120
        # print(end_pos)
        text_to_translate = text[(pos):(end_pos)]
        result = translate_client.translate(
            text_to_translate, target_language=target
        )
        # print(result)
        for t in result:
            result_text.append(t["translatedText"])

    return result_text


def translate_text(target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """

    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language=target)

    return result["translatedText"]


def draw_boxes(image, bounds, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)

    aux = 0
    for bound in bounds:
        if aux != 0:
            draw.polygon([
                bound.vertices[0].x, bound.vertices[0].y,
                bound.vertices[1].x, bound.vertices[1].y,
                bound.vertices[2].x, bound.vertices[2].y,
                bound.vertices[3].x, bound.vertices[3].y],
                fill=(255, 255, 255, 128), outline=color
            )
        aux = 1
    return image


def draw_text(image, bounds, texts, color):
    """Draw text in the image """
    draw = ImageDraw.Draw(image)

    aux = 0
    for bound in bounds:
        if (aux != 0):
            draw.text(
                (bound.vertices[0].x, bound.vertices[0].y),
                str(texts[aux]).encode('utf-8'),
                fill="black", anchor="ms"
            )
        aux += 1

    return image


def get_document_bounds(image_file, feature, lang):
    """Returns document bounds given an image."""
    client = vision.ImageAnnotatorClient()

    bounds = []
    texts = []
    texts_ = []
    translates = []

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    datas = response.text_annotations

    # general_description = datas[0].description
    # print(datas)
    # print(general_description)

    # translate_text_print(lang, general_description)

    for text in datas:
        texts_.append(text.description)
        texts.append(text.description)
        bounds.append(text.bounding_poly)

    translates = translate_all_text(lang, texts_)

    # The list `bounds` contains the coordinates of the bounding boxes.
    return bounds, texts, translates


def render_doc_text(filein, fileout, lang):
    image = Image.open(filein)
    bounds, texts, translates = get_document_bounds(
        filein, FeatureType.WORD, lang
    )
    draw_boxes(image, bounds, 'yellow')
    draw_text(image, bounds, translates, 'yellow')

    if fileout != 0:
        image.save(fileout)
    else:
        image.show()
    return translates, texts


class MenuViewSet(viewsets.ModelViewSet):
    """Manage menu in the database"""
    serializer_class = serializers.MenuImageSerializer
    queryset = Menu.objects.all()

    @action(methods=['POST'], detail=False, url_path='upload')
    def upload(self, request):
        serializer = self.get_serializer(
            data=request.data
        )

        if serializer.is_valid():
            # print(request.data)
            serializer.save()
            # print(serializer.data['id'])

            image_ = Menu.objects.get(id=serializer.data['id'])
            image_path = image_.image.path
            image_name = image_.image.name

            lang = serializer.data['lang']

            # print(image_path)
            # print(image_name)

            r_lang, r_text = render_doc_text(
                image_path, MEDIA_ROOT + '/' + image_name, lang
            )

            image_.description = r_lang[0]
            image_.original = r_text[0]
            image_.save()

            seria = serializers.MenuImageSerializer(image_)

            return Response(
                seria.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
