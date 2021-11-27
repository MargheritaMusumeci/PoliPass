import datetime
import pprint
import random

import isodate
import pymongo as pym
from bson import ObjectId
from enum import IntEnum


CONNECTION_STRING = "mongodb+srv://Piero_Rendina:R3nd1n%402021@cluster0.hns6k.mongodb.net/authSource=admin?ssl=true" \
                   "&tlsAllowInvalidCertificates=true"

NAMES = []
SURNAMES = []
ADDRESSES = []

class Test_Attributes(IntEnum):
    """
    Enum class to retrieve index of a given attribute for a test document.
    """
    ISSUER = 0
    DATE = 1
    RESULT = 2
    PERSON = 3
    TYPE = 4
    DOCTOR = 5
    NURSE = 6

class Embedded_Doctor_Attributes(IntEnum):
    """
    Enum class to retrieve the index of a given attribute for a doctor embedded in a document
    """
    D_NAME = 0
    D_SURNAME = 1
    D_MAIL = 2

class Embedded_Issuer_Attributes(IntEnum):
    """
    Enum class to retrieve the index of a given attribute for an issuer embedded in a document
    """
    ISSUER_NAME = 0
    ISSUER_ADDRESS = 1

class Embedded_Person_Attributes(IntEnum):
    """
    Enum class to retrieve the index of a given attribute for an embedded person
    """
    P_NAME = 0
    P_SURNAME = 1
    BIRTHDATE = 2
    FISCAL_CODE = 3


def read_names():
    """
    Method to read all the names from the file names.txt and store them in the global variable
    """
    with open("files/people_names.txt", 'r', encoding='utf8') as f:
        for line in f:
            if line == "\n":
                continue
            NAMES.append(line.rstrip('\n').rstrip().lstrip())
    f.close()


def read_surnames():
    """
    Method to read all the surnames from the file surnames.txt and store them in the global variable
    """
    with open("files/people_surnames.txt", 'r', encoding='utf8') as f:
        for line in f:
            if line == "\n":
                continue
            SURNAMES.append(line.rstrip('\n').rstrip().lstrip())
    f.close()


def read_addresses():
    """
    Method to read all the addresses from the file house_addresses.txt and store them in the global variable
    """
    with open("files/house_addresses.txt", 'r', encoding='utf8') as f:
        for line in f:
            if line == "\n":
                continue
            ADDRESSES.append(line.rstrip('\n').rstrip().lstrip())
    f.close()


def create_index_function(collection_name):
    """
    Method that creates a textual index inside a MongoDB collection.
    :param collection_name: collection in which the index is created
    :return:
    """
    collection_name.create_index([('vaccine name', 'text')])


def create_embedded_issuer(name, address):
    """
    Method that creates a dictionary representing an embedded issuer
    """
    issuer = {Embedded_Issuer_Attributes.ISSUER_NAME.name: name,
              Embedded_Issuer_Attributes.ISSUER_ADDRESS.name: address}
    return issuer


def create_embedded_person(name, surname, birthdate, fiscal_code):
    """
    Method that creates a dictionary representing an embedded person
    """
    person = {Embedded_Person_Attributes.P_NAME.name: name,
              Embedded_Person_Attributes.P_SURNAME.name: surname,
              Embedded_Person_Attributes.BIRTHDATE.name: birthdate,
              Embedded_Person_Attributes.FISCAL_CODE.name: fiscal_code}
    return person


def create_embedded_doctor(name, surname):
    """
    Method that creates a dictionary representing an embedded doctor
    """
    doctor = {Embedded_Doctor_Attributes.D_NAME.name: name,
              Embedded_Doctor_Attributes.D_SURNAME.name: surname,
              Embedded_Doctor_Attributes.D_MAIL.name: name + '.' + surname + "@polipass.it"}
    return doctor


def insert_test(collection, issuer, person, doctor, nurse):
    """
    Method to insert a test document inside the collection.
    :param collection
    """
    positivity = random.random()
    if positivity >= 0.5:
        result = "positive"
    else: result = "negative"
    collection.insert_one({Test_Attributes.ISSUER.name: create_embedded_issuer
                                                            (issuer[int(Embedded_Issuer_Attributes.ISSUER_NAME)],
                                                            issuer[int(Embedded_Issuer_Attributes.ISSUER_ADDRESS)]),
                           Test_Attributes.DATE.name: build_date(),
                           Test_Attributes.RESULT.name: result,
                           Test_Attributes.PERSON.name: create_embedded_person(person[int(Embedded_Person_Attributes.P_NAME)],
                                                            person[int(Embedded_Person_Attributes.P_SURNAME)],
                                                            person[int(Embedded_Person_Attributes.BIRTHDATE)],
                                                            person[int(Embedded_Person_Attributes.FISCAL_CODE)]
                                                            ),
                           Test_Attributes.TYPE.name: "PCR",
                           Test_Attributes.DOCTOR.name: create_embedded_doctor(doctor[int(Embedded_Doctor_Attributes.D_NAME)], doctor[int(Embedded_Doctor_Attributes.D_SURNAME)]),
                           Test_Attributes.NURSE.name: create_embedded_doctor(nurse[int(Embedded_Doctor_Attributes.D_NAME)], nurse[int(Embedded_Doctor_Attributes.D_SURNAME)])
                           })


def build_person():
    """
    Method that initializes a list containing all the attributes for a generic person (only name and surname so far)
    """
    name_index = random.randint(0, len(NAMES)-1)
    surname_index = random.randint(0, len(SURNAMES)-1)
    return [NAMES[name_index], SURNAMES[surname_index]]


def build_detailed_person():
    """
    Method that initializes a list containing all the attributes for a generic person
    """

    #TODO change the fiscal code field
    name_index = random.randint(0, len(NAMES) - 1)
    surname_index = random.randint(0, len(SURNAMES) - 1)
    birthdate = build_date()
    fiscal_code = "RNDPRI99P30G942C"
    return [NAMES[name_index], SURNAMES[surname_index], birthdate, fiscal_code]


def build_date():
    """
    Method that provides a datetime structure with hours and minutes set to 0 to comply with Date type in MongoDB
    """
    start_date = datetime.datetime.strptime("2020-06-01", "%Y-%m-%d")
    result_date = start_date + datetime.timedelta(random.randint(0, 365))
    return result_date


def build_issuer():
    """
    Method to build an issuer given
    """
    return ["Hospital", "Via Niguarda 25, 20154, Milano, MI"]


if __name__ == '__main__':
    cluster = pym.MongoClient(CONNECTION_STRING)
    db = cluster['my_database']
    db.drop_collection('my_collection')
    collection = db['my_collection']
    read_names()
    read_surnames()
    read_addresses()
    insert_test(collection, build_issuer(), build_detailed_person(), build_person(), build_person())






