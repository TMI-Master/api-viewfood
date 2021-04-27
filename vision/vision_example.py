import io
import os

# Imports the Google Cloud client library
from google.cloud import vision

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('wakeupcat.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)
    print(label.description, '(%.2f%%)' % (label.score * 100.))

image_uri = 'gs://cloud-vision-codelab/otter_crossing.jpg'

image = vision.Image()
image.source.image_uri = image_uri

response = client.text_detection(image=image)
texts = response.text_annotations

for text in texts:
    print('=' * 30)
    print(text.description)
    vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
    print('bounds:', ",".join(vertices))


# The name of the image file to annotate
file_name = os.path.abspath('menu_test.jpeg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations

print("Text:")
print(texts[0])
for text in texts:
    print('=' * 30)
    print(text.description)
    # vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
    # print('bounds:', ",".join(vertices))
