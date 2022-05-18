
# database connection
import pymongo

client = pymongo.MongoClient("mongodb://aml_user:o0Eucdnbqf1rfidhj@vps-55aa3b4a.vps.ovh.net:19191/sanctions_db")
db = client["sanctions_db"]
collection = db["sanction_entities"]
collection_bank = db["bank_client"]

matching_face = 10
matching_cin = 100
matching_permis = 100
matching_firstname = 40
matching_lastname = 40
matching_birthday = 10
matching_score = 0

def scoringClient(firstname, lastname, cin, permis):
    global matching_score
    query_firstname = {"first_name": firstname}
    doc_firstname = collection.find(query_firstname)
    if doc_firstname is None:
        print("doesn't match")
    else:
        matching_score += matching_firstname

    query_lastname = {"last_name": lastname}
    doc_lastname = collection.find(query_lastname)
    if doc_lastname is None:
        print("doesn't match")
    else:
        matching_score += matching_lastname
    query_conduct_id = {"list_docs.id_number": permis}
    doc_conduct_id = collection.find(query_conduct_id)
    if doc_conduct_id is None:
        print("doesn't match concudt id ")
    else:
        matching_score += matching_permis

    query_cin_id = {"list_docs.id_number": cin}
    doc_cin_id = collection.find(query_cin_id)
    if doc_cin_id is None:
        print("doesn't match")
    else:
        matching_score += matching_cin
    if matching_score >= 100:
        matching_score = 100
    return matching_score