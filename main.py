import datetime
import pprint
import random

import json
import pymongo as pym
from enum import IntEnum
from codicefiscale import codicefiscale


CONNECTION_STRING = "mongodb+srv://Piero_Rendina:R3nd1n%402021@cluster0.hns6k.mongodb.net/authSource=admin?ssl=true"\
                   "&tlsAllowInvalidCertificates=true"

NAMES = []
SURNAMES = []
MUNICIPALITIES = []
ADDRESSES = []
ISSUERS = []


class TestAttributes(IntEnum):
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


class VaccineAttributes(IntEnum):
    """
    Enum class to retrieve the index of a given attribute in a vaccine document
    """
    DATE = 0
    VACCINE = 1
    DOSE = 2
    PERSON = 3
    ISSUER = 4
    DOCTOR = 5
    NURSE = 6


class IssuerAttributes(IntEnum):
    TYPE = 0
    NAME = 1
    LOCATION_DETAILS = 2


class EmbeddedPositionDetails(IntEnum):
    """
    Enum class to map attribute for embedded location to their index.
    """
    LATITUDE = 0
    LONGITUDE = 1
    ADDRESS = 2
    CITY = 3
    PROVINCE = 4
    ZIP = 5

    @classmethod
    def create_embedded_location_details(cls, location_details):
        """
        Method to create a complete address for a location.
        :param location_details is the list containing all the attributes
        """
        embedded_location = {EmbeddedPositionDetails.LATITUDE.name: location_details[EmbeddedPositionDetails.LATITUDE.value],
                             EmbeddedPositionDetails.LONGITUDE.name: location_details[EmbeddedPositionDetails.LONGITUDE.value],
                             EmbeddedPositionDetails.ADDRESS.name: location_details[EmbeddedPositionDetails.ADDRESS.value],
                             EmbeddedPositionDetails.CITY.name: location_details[EmbeddedPositionDetails.CITY.value],
                             EmbeddedPositionDetails.PROVINCE.name: location_details[EmbeddedPositionDetails.PROVINCE.value],
                             EmbeddedPositionDetails.ZIP.name: location_details[EmbeddedPositionDetails.ZIP.value]}
        return embedded_location


class EmbeddedVaccineAttributes(IntEnum):
    """
    Enum class containing all the attributes for an embedded vaccine
    """
    NAME = 0
    PRODUCER = 1
    TYPE = 2
    BATCH = 3
    PRODUCTION_DATE = 4

    #TODO change the way the number of the batch and the type are chosen
    @classmethod
    def create_embedded_vaccine(cls, name, producer):
        vaccine = {EmbeddedVaccineAttributes.NAME.name: name,
                   EmbeddedVaccineAttributes.PRODUCER.name: producer,
                   EmbeddedVaccineAttributes.TYPE.name: "mRNA",
                   EmbeddedVaccineAttributes.BATCH.name: 1234,
                   EmbeddedVaccineAttributes.PRODUCTION_DATE.name: build_date("2021-04-01", days_ahead=210)}
        return vaccine


class EmbeddedDoctorAttributes(IntEnum):
    """
    Enum class to retrieve the index of a given attribute for a doctor embedded in a document
    """
    NAME = 0
    SURNAME = 1
    MAIL = 2

    @classmethod
    def create_embedded_doctor(cls, name, surname):
        """
        Method that creates a dictionary representing an embedded doctor
        """
        doctor = {EmbeddedDoctorAttributes.NAME.name: name,
                  EmbeddedDoctorAttributes.SURNAME.name: surname,
                  EmbeddedDoctorAttributes.MAIL.name: (name + '.' + surname + "@polipass.it").lower()}
        return doctor


class EmbeddedPersonAttributes(IntEnum):
    """
    Enum class to retrieve the index of a given attribute for an embedded person
    """
    NAME = 0
    SURNAME = 1
    BIRTHDATE = 2
    FISCAL_CODE = 3

    @classmethod
    def create_embedded_person(cls, name, surname, birthdate, fiscal_code):
        """
        Method that creates a dictionary representing an embedded person
        """
        person = {EmbeddedPersonAttributes.NAME.name: name,
                  EmbeddedPersonAttributes.SURNAME.name: surname,
                  EmbeddedPersonAttributes.BIRTHDATE.name: birthdate,
                  EmbeddedPersonAttributes.FISCAL_CODE.name: fiscal_code}
        return person


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


def read_municipalities():
    """
    Method to read all italian municipalities from the file comuni.json and store them in the global variable
    """
    f = open("files/comuni.json")
    data = json.load(f)
    for i in range(len(data)):
        MUNICIPALITIES.append(data[i]["nome"])
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


def read_issuers():
    """
    Method to read all the issuers from the file issuers.txt.
    """
    with open("files/locations.txt", 'r', encoding='utf8') as file:
        for line in file:
            if line == "\n":
                continue
            location_details = line.rstrip('\n').rstrip().lstrip().split(',')
            ISSUERS.append(location_details)


def create_index_function(collection_name):
    """
    Method that creates a textual index inside a MongoDB collection.
    :param collection_name: collection in which the index is created
    :return:
    """
    collection_name.create_index([('vaccine name', 'text')])


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
    birthdate = build_date("1950-01-01", days_ahead=12775)
    fiscal_code = codicefiscale.encode(SURNAMES[surname_index], NAMES[name_index], 'M', str(birthdate), random.choice(MUNICIPALITIES))
    return [NAMES[name_index], SURNAMES[surname_index], birthdate, fiscal_code]


def build_date(start_date, days_ahead):
    """
    Method that provides a datetime structure
    :param start_date the starting date to which we add the number of days
    :param days_ahead the maximum number of days we can add
    """
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    result_date = start_date + datetime.timedelta(days=random.randint(0, days_ahead))
    return result_date


def retrieve_issuer():
    """
    Method to randomly retrieve a list containing all the attributes for an issuer.
    """
    issuer_index = random.randint(0, len(ISSUERS) - 1)
    return ISSUERS[issuer_index]


def create_embedded_issuer(params, add_location_details):
    """
    Method to create an issuer given a list of attributes.
    :param params list with all fields mapped according to IssuerAttributes enum
    :param add_location_details is a boolean variable to assess if the details about the issuer position are required.
    """
    if not add_location_details:
        issuer = {
            IssuerAttributes.TYPE.name: params[IssuerAttributes.TYPE.value],
            IssuerAttributes.NAME.name: params[IssuerAttributes.NAME.value],
        }
    else:
        issuer = {
            IssuerAttributes.TYPE.name: params[IssuerAttributes.TYPE.value],
            IssuerAttributes.NAME.name: params[IssuerAttributes.NAME.value],
            IssuerAttributes.LOCATION_DETAILS.name:
                EmbeddedPositionDetails.create_embedded_location_details(params[IssuerAttributes.LOCATION_DETAILS.value:])
        }
    return issuer


def create_test_document(person, doctor, nurse):
    """
    Method to create a test document.
    :param person list containing all attributes for a person
    :param doctor list containing all attributes for a doctor
    :param nurse list containing all attributes for a nurse
    """
    positivity = random.random()
    if positivity >= 0.5:
        result = "positive"
    else:
        result = "negative"
    test = {TestAttributes.ISSUER.name: create_embedded_issuer(retrieve_issuer(), add_location_details=False),
            TestAttributes.DATE.name: build_date("2019-01-01", days_ahead=730),
            TestAttributes.RESULT.name: result,
            TestAttributes.PERSON.name: EmbeddedPersonAttributes.create_embedded_person(
                                                                       person[int(EmbeddedPersonAttributes.NAME)],
                                                                       person[int(EmbeddedPersonAttributes.SURNAME)],
                                                                       person[int(EmbeddedPersonAttributes.BIRTHDATE)],
                                                                       person[int(EmbeddedPersonAttributes.FISCAL_CODE)]
                                                                       ),
            TestAttributes.TYPE.name: "PCR",
            TestAttributes.DOCTOR.name: EmbeddedDoctorAttributes.create_embedded_doctor(
                                            doctor[int(EmbeddedDoctorAttributes.NAME)],
                                            doctor[int(EmbeddedDoctorAttributes.SURNAME)]),
            TestAttributes.NURSE.name: EmbeddedDoctorAttributes.create_embedded_doctor(
                                           nurse[int(EmbeddedDoctorAttributes.NAME)],
                                           nurse[int(EmbeddedDoctorAttributes.SURNAME)])
            }
    return test


def insert_test(collection, test):
    """
    Method to insert a test document inside the collection.
    :param collection
    """
    collection.insert_one(test)


if __name__ == '__main__':

    cluster = pym.MongoClient(CONNECTION_STRING)
    db = cluster['polipass']
    db.drop_collection('covid_certificates')
    collection = db['covid_certificates']
    read_names()
    read_surnames()
    read_municipalities()
    read_addresses()
    read_issuers()

    test = create_test_document(build_detailed_person(), build_person(), build_person())
    insert_test(collection, test)

    pprint.pp(collection.find_one())
