# database connection
import pymongo


from score import scoringClient

client = pymongo.MongoClient("mongodb://aml_user:o0Eucdnbqf1rfidhj@vps-55aa3b4a.vps.ovh.net:19191/sanctions_db")
db = client["sanctions_db"]
collection = db["sanction_entities"]
collection_bank = db["bank_client"]
client_not_scored = {"fear_index": {"$exists": False}}

for client in collection_bank.find(client_not_scored):
    firstname = client['firstname']
    lastname = client['lastname']
    cin = client['cin']
    permis = client['permis']
    score = scoringClient(firstname,lastname,cin,permis)
    collection_bank.update_one({"_id": client['_id']}, {"$set": {"fear_index": score}})
