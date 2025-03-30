from google.cloud import vision
from google.oauth2 import service_account
import io
import re


def extract_text_from_image(image_path, credentials_path):
    credentials = service_account.Credentials.from_service_account_file(credentials_path)

    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(f"API Error: {response.error.message}")

    texts = response.text_annotations
    if texts:
        print("Items list:\n")
        print(texts[0].description)  # Full extracted text
    else:
        print("No text found.")

def extract_rc_text_from_image(image_path, credentials_path):

    credentials = service_account.Credentials.from_service_account_file(credentials_path)

    client = vision.ImageAnnotatorClient(credentials=credentials)

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    if response.error.message:
        raise Exception(f"API Error: {response.error.message}")

    extracted_text = response.text_annotations[0].description if response.text_annotations else ""

    if extracted_text:
        maker = re.search(r"(?i)Maker[:\s]*(.*)", extracted_text)
        model = re.search(r"(?i)Model[:\s]*(.*)", extracted_text)
        registration_number = re.search(r"(?i)Regn. Number[:\s]*(.*)", extracted_text)
        color = re.search(r"(?i)Color[:\s]*(.*)", extracted_text)

        print("Maker:", maker.group(1).strip() if maker else "Not Found")
        print("Model:", model.group(1).strip() if model else "Not Found")
        print("Registration Number:", registration_number.group(1).strip() if registration_number else "Not Found")
        print("Colour :", color.group(1).strip() if color else "Not Found")

    else:
        print("No text found.")

if __name__ == "__main__":
    image_path = "/Users/a36014/Downloads/image.png"  # Update with your image path
    credentials_path = "quick-cache-170312-b7229e8d86dc.json"  # Path to your Google Cloud service account key

    image_path1 = "/Users/a36014/Downloads/imageRC.png"
    extract_text_from_image(image_path, credentials_path)
    print("\n---- RC Details ----\n")
    extract_rc_text_from_image(image_path1, credentials_path)
