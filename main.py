import pymongo
from flask import Flask, jsonify, json
import cv2
import pytesseract
import re
from face_from_card import CropImageCard
from deepface import DeepFace
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from score import scoringClient,matching_score
from upload_image import upload_file

app = Flask(__name__)
UPLOAD_FOLDER = r'C:\Users\ahmed\PycharmProjects\deepFace_aml_cft\uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# database connection
client = pymongo.MongoClient("mongodb://aml_user:o0Eucdnbqf1rfidhj@vps-55aa3b4a.vps.ovh.net:19191/sanctions_db")
db = client["sanctions_db"]
collection = db["sanction_entities"]
collection_bank = db["bank_client"]

# initialise model face
model = DeepFace.build_model("Facenet")


@app.route("/verify", methods=['GET', 'POST'])
def verifyImage():
    global matching_score
    uploaded_image = upload_file()
    img_path = os.path.join(r'C:\Users\ahmed\PycharmProjects\deepFace_aml_cft\uploads', uploaded_image)
    CropImageCard(img_path)

    df = DeepFace.find('face.jpg'
                       , db_path=r'C:\Users\ahmed\PycharmProjects\deepFace_aml_cft\deepface\tests\dataset'
                       , model_name='Facenet'
                       , distance_metric='cosine'
                       , detector_backend='opencv', enforce_detection='true')

    print(df.head(10))
    print(df.size)
    if df.size == 0:
        print("No matching found")
    else:
        print("this match :  ", df['identity'][0])
        matching_score += 20
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    custom_config = r'-l ara --psm 6'
    img = cv2.imread(img_path)
    firstname = cv2.imread("firstname.jpg")
    firstname = cv2.cvtColor(firstname, cv2.COLOR_BGR2GRAY)
    data_extracted_firstname = pytesseract.image_to_string(firstname).strip().lower()
    print("firstname is :", data_extracted_firstname)
    lastname = cv2.imread("lastname.jpg")
    lastname = cv2.cvtColor(lastname, cv2.COLOR_BGR2GRAY)
    data_extracted_lastname = pytesseract.image_to_string(lastname).strip().lower()
    print("lastname is : ", data_extracted_lastname)

    cin = cv2.imread("cin.jpg")
    cin = cv2.cvtColor(cin, cv2.COLOR_BGR2GRAY)
    data_extracted_cin = pytesseract.image_to_string(cin).strip()
    data_extracted_cin = re.sub("[^0-9]", "", data_extracted_cin)
    print("cin is : ", data_extracted_cin)

    birthdate = cv2.imread("birthdate.jpg")
    birthdate = cv2.cvtColor(birthdate, cv2.COLOR_BGR2GRAY)
    data_extracted_birthdate = pytesseract.image_to_string(birthdate).strip()
    print("birthdate is : ", data_extracted_birthdate)

    conduct_id = cv2.imread("conductId.jpg")
    conduct_id = cv2.cvtColor(conduct_id, cv2.COLOR_BGR2GRAY)
    data_extracted_conductId = pytesseract.image_to_string(conduct_id).strip()

    finalScore = scoringClient(data_extracted_firstname, data_extracted_lastname, data_extracted_cin,
                               data_extracted_conductId)

    sanction_dict = dict()
    sanction_dict['firstname'] = data_extracted_firstname
    sanction_dict['lastname'] = data_extracted_lastname
    sanction_dict['birthdate'] = data_extracted_birthdate
    sanction_dict['cin'] = data_extracted_cin
    sanction_dict['permis'] = data_extracted_conductId
    sanction_dict['fear_index'] = str(finalScore)
    collection_bank.insert_one(sanction_dict)

    # Trying with text prediction
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
                print("cin found :", x)
                matching_cin = 20
                return "client suspected"
            else:
                print("cin not found")
        if re.search('^\d{4}\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01])$', all_predictions[i]) and i > 15:
            print("date de naissance :", all_predictions[i])
    return "client added"


if __name__ == '__main__':
    app.run(debug=True)
