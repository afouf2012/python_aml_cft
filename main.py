from deepface import DeepFace
import pymongo
from face_from_card import CropImageCard
import cv2
import pytesseract
import re

client = pymongo.MongoClient("mongodb://aml_user:o0Eucdnbqf1rfidhj@vps-55aa3b4a.vps.ovh.net:19191/sanctions_db")
db = client["sanctions_db"]
collection = db["sanction_entities"]


model = DeepFace.build_model("Facenet")

img_path = r'C:\Users\ahmed\PycharmProjects\deepFace_aml_cft\ahmed_card.jpg'
CropImageCard(img_path)

df = DeepFace.find('face.jpg'
                   , db_path='deepface/tests/dataset'
                   , model_name='Facenet'
                   , distance_metric='cosine'
                   , detector_backend='opencv', enforce_detection='true')

print(df.head(10))
print(df.size)
if df.size == 0:
    print("No matching found")
else:
    print("this match :  ", df['identity'][0])

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

custom_config = r'-l ara --psm 6'
img = cv2.imread("ahmed_card.jpg")
# pytesseract accepte que BRG donc on doit convertir
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

data_extracted = pytesseract.image_to_data(img, config=custom_config, output_type='data.frame')
print("data_extracted :", data_extracted)
img_conf_text = data_extracted[["conf", "text"]]
img_valid = img_conf_text[img_conf_text["text"].notnull()]
img_words = img_valid[img_valid["text"].str.len() > 1]
all_predictions = img_words["text"].to_list()
print(all_predictions)
for i in range(len(all_predictions)):
    if len(all_predictions[i]) == 8 and all_predictions[i].isdigit():
        print("cin is : ", all_predictions[i])
        myquery = {"list_docs.id_number": all_predictions[i]}
        mydoc = collection.find(myquery)
        for x in mydoc:
            print("cin found :",x)
        else:
            print("cin not found")
    if re.search('^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$', all_predictions[i]) and i > 15:
        print("date de naissance :", all_predictions[i])


