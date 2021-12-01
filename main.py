import datetime
import random

import json

import pymongo as pym
from enum import IntEnum
from codicefiscale import codicefiscale

# CONNECTION_STRING = "mongodb+srv://andrea:Zx9KaBfRDniXeDD@cluster0.7h575.mongodb.net/test"
CONNECTION_STRING = "mongodb+srv://Piero_Rendina:R3nd1n%402021@cluster0.hns6k.mongodb.net/authSource=admin?ssl=true" \
                    "&tlsAllowInvalidCertificates=true"

NUMBER_OF_PEOPLE = 10

NAMES = []
SURNAMES = []
MUNICIPALITIES = []
ADDRESSES = []
ISSUERS = []
VACCINES = []
TESTS = []
"""
Dictionary used to bind each issuer with its ObjectId inside MongoDB
It is updated after the creation of each issuer inside the function create_and_insert_all_issuer_doc
"""
ISSUERS_TABLE = {}
"""
Dictionary used to bind each person with its ObjectId inside MongoDB
Is is updated after the creation of each person inside the function create_and_insert_people_doc
"""
PEOPLE_TABLE = {}


class TestAttributes(IntEnum):
    """
    Enum class to retrieve index of a given attribute for a test document.
    """
    ISSUER = 0
    DATE = 1
    RESULT = 2
    TYPE = 3
    DOCTOR = 4
    NURSE = 5

    @classmethod
    def create_test_document(cls, test_type, doctor, nurse):
        """
        Method to create a test document.
        :param test_type the type of the test
        :param doctor list containing all attributes for a doctor
        :param nurse list containing all attributes for a nurse
        """
        positivity = random.random()
        if positivity >= 0.5:
            result = "positive"
        else:
            result = "negative"
        test = {TestAttributes.ISSUER.name: ISSUERS_TABLE[random.randint(0, len(ISSUERS_TABLE) - 1)],
                TestAttributes.DATE.name: build_date("2019-01-01", days_ahead=730),
                TestAttributes.TYPE.name: test_type,
                TestAttributes.RESULT.name: result,
                TestAttributes.DOCTOR.name: EmbeddedDoctorAttributes.create_embedded_doctor(doctor),
                TestAttributes.NURSE.name: EmbeddedDoctorAttributes.create_embedded_doctor(nurse)
                }
        return test


class VaccinationAttributes(IntEnum):
    """
    Enum class to retrieve the index of a given attribute in a vaccine document
    """
    VACCINE = 0
    DATE = 1
    DOSE = 2
    ISSUER = 3
    DOCTOR = 4
    NURSE = 5

    @classmethod
    def create_vaccination_document(cls, vaccine, doctor, nurse):
        """
        Method to create a covid vaccination, given details about the issued vaccine.
        It ensures that the vaccine is issued after its production
        """
        vaccine_issued = EmbeddedVaccineAttributes.create_embedded_vaccine(vaccine)
        production_date = vaccine_issued['PRODUCTION_DATE']
        days = random.randint(0, 30)
        hours = random.randint(0, 24)
        minutes = random.randint(0, 60)
        injection_date = production_date + datetime.timedelta(days=days, hours=hours, minutes=minutes)
        vaccination = {
            VaccinationAttributes.VACCINE.name: vaccine_issued,
            VaccinationAttributes.DATE.name: injection_date,
            VaccinationAttributes.DOSE.name: 1,
            VaccinationAttributes.ISSUER.name: ISSUERS_TABLE[random.randint(0, len(ISSUERS_TABLE) - 1)],
            VaccinationAttributes.DOCTOR.name: EmbeddedDoctorAttributes.create_embedded_doctor(doctor),
            VaccinationAttributes.NURSE.name: EmbeddedDoctorAttributes.create_embedded_doctor(nurse),
        }
        return vaccination

    @classmethod
    def create_vaccination_doc_from_previous_one(cls, vaccination):
        """
        Method to create a vaccination document after one vaccination has been already done.
        """
        # The first element in the vaccination instance is a dictionary representing the last vaccine done.
        vaccine_details = list(vaccination[VaccinationAttributes.VACCINE.value].values())
        previous_dose = vaccination[VaccinationAttributes.DOSE.value]
        vaccine_name = vaccine_details[EmbeddedVaccineAttributes.NAME.value]
        # Handling of the case with single-dose vaccine Janssen
        if vaccine_name == "COVID-19 Vaccine Janssen":
            previous_dose = 2
            vaccine_details[EmbeddedVaccineAttributes.NAME.value:
                            EmbeddedVaccineAttributes.TYPE.value+1] = retrieve_vaccine(0, 1)
        if previous_dose == 1:
            days_to_wait = 30
            injection_date = vaccination[VaccinationAttributes.DATE.value] + datetime.timedelta(days=days_to_wait)
            vaccine_doc = EmbeddedVaccineAttributes. \
                create_embedded_vaccine_from_previous(vaccine_details, max_num_production_days=28)
        else:
            if previous_dose == 2:
                days_to_wait = 150
                injection_date = vaccination[VaccinationAttributes.DATE.value] + datetime.timedelta(days=days_to_wait)
                vaccine_doc = EmbeddedVaccineAttributes. \
                    create_embedded_vaccine_from_previous(vaccine_details, max_num_production_days=149)
            else:
                print("The person has already done all required vaccine doses")
                return None
        vaccination_document_to_add = {
            VaccinationAttributes.VACCINE.name: vaccine_doc,
            VaccinationAttributes.DATE.name: injection_date,
            VaccinationAttributes.DOSE.name: previous_dose + 1,
            # TODO decide whether or not taking the same ISSUER. Now it is randomly chosen.
            VaccinationAttributes.ISSUER.name: ISSUERS_TABLE[random.randint(0, len(ISSUERS_TABLE) - 1)],
            VaccinationAttributes.DOCTOR.name: EmbeddedDoctorAttributes.create_embedded_doctor(retrieve_person()),
            VaccinationAttributes.NURSE.name: EmbeddedDoctorAttributes.create_embedded_doctor(retrieve_person()),
        }
        return vaccination_document_to_add


class EmbeddedVaccineAttributes(IntEnum):
    """
    Enum class containing all the attributes for an embedded vaccine
    """
    NAME = 0
    PRODUCER = 1
    TYPE = 2
    BATCH = 3
    PRODUCTION_DATE = 4

    @classmethod
    def create_embedded_vaccine(cls, vaccine_details):
        """
        Method to build the first vaccine as an embedded MongoDB document.
        """
        batch = random.randint(0, 10000)
        starting_possible_date = "2021-04-01"
        vaccine = {EmbeddedVaccineAttributes.NAME.name: vaccine_details[EmbeddedVaccineAttributes.NAME.value],
                   EmbeddedVaccineAttributes.PRODUCER.name: vaccine_details[EmbeddedVaccineAttributes.PRODUCER.value],
                   EmbeddedVaccineAttributes.TYPE.name: vaccine_details[EmbeddedVaccineAttributes.TYPE.value],
                   EmbeddedVaccineAttributes.BATCH.name: batch,
                   EmbeddedVaccineAttributes.PRODUCTION_DATE.name: build_date(starting_possible_date, days_ahead=210)}
        return vaccine

    @classmethod
    def create_embedded_vaccine_from_previous(cls, previous_vaccine_details, max_num_production_days):
        """
        Method to build further instances of vaccine for the same person.
        :param previous_vaccine_details list containing all information about the previous vaccine
        :param max_num_production_days maximum number of days within which the vaccine can be produced,
        given the last production.
        """
        previous_batch = previous_vaccine_details[EmbeddedVaccineAttributes.BATCH.value]
        batch = random.randint(previous_batch, previous_batch + 5000)
        starting_date = previous_vaccine_details[EmbeddedVaccineAttributes.PRODUCTION_DATE.value]
        production_date = build_date(starting_date, days_ahead=max_num_production_days, is_random=False)
        vaccine = {EmbeddedVaccineAttributes.NAME.name: previous_vaccine_details[EmbeddedVaccineAttributes.NAME.value],
                   EmbeddedVaccineAttributes.PRODUCER.name: previous_vaccine_details[
                   EmbeddedVaccineAttributes.PRODUCER.value],
                   EmbeddedVaccineAttributes.TYPE.name: previous_vaccine_details[EmbeddedVaccineAttributes.TYPE.value],
                   EmbeddedVaccineAttributes.BATCH.name: batch,
                   EmbeddedVaccineAttributes.PRODUCTION_DATE.name: production_date}
        return vaccine


class IssuerAttributes(IntEnum):
    TYPE = 0
    NAME = 1
    LOCATION_DETAILS = 2

    @classmethod
    def create_embedded_issuer(cls, params, add_location_details):
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
                    EmbeddedPositionDetails.create_embedded_location_details(
                        params[IssuerAttributes.LOCATION_DETAILS.value:])
            }
        return issuer


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
        embedded_location = {
            EmbeddedPositionDetails.LATITUDE.name: location_details[EmbeddedPositionDetails.LATITUDE.value],
            EmbeddedPositionDetails.LONGITUDE.name: location_details[EmbeddedPositionDetails.LONGITUDE.value],
            EmbeddedPositionDetails.ADDRESS.name: location_details[EmbeddedPositionDetails.ADDRESS.value],
            EmbeddedPositionDetails.CITY.name: location_details[EmbeddedPositionDetails.CITY.value],
            EmbeddedPositionDetails.PROVINCE.name: location_details[EmbeddedPositionDetails.PROVINCE.value],
            EmbeddedPositionDetails.ZIP.name: location_details[EmbeddedPositionDetails.ZIP.value]}
        return embedded_location


class EmbeddedDoctorAttributes(IntEnum):
    """
    Enum class to retrieve the index of a given attribute for a doctor embedded in a document
    """
    NAME = 0
    SURNAME = 1
    MAIL = 2

    @classmethod
    def create_embedded_doctor(cls, doctor_details):
        """
        Method that creates a dictionary representing an embedded doctor
        """
        name = doctor_details[EmbeddedDoctorAttributes.NAME.value]
        surname = doctor_details[EmbeddedDoctorAttributes.SURNAME.value]
        doctor = {EmbeddedDoctorAttributes.NAME.name: name,
                  EmbeddedDoctorAttributes.SURNAME.name: surname,
                  EmbeddedDoctorAttributes.MAIL.name: (name + '.' + surname + "@polipass.it").lower()}
        return doctor


class PersonAttributes(IntEnum):
    """
    Enum class to retrieve the index of a given attribute for an embedded person
    """
    NAME = 0
    SURNAME = 1
    BIRTHDATE = 2
    FISCAL_CODE = 3
    TESTS = 4
    VACCINATIONS = 5

    @classmethod
    def create_embedded_person(cls, person_details):
        """
        Method that creates a dictionary representing an embedded person
        """
        person = {PersonAttributes.NAME.name: person_details[PersonAttributes.NAME.value],
                  PersonAttributes.SURNAME.name: person_details[PersonAttributes.SURNAME.value],
                  PersonAttributes.BIRTHDATE.name: person_details[PersonAttributes.BIRTHDATE.value],
                  PersonAttributes.FISCAL_CODE.name: person_details[PersonAttributes.FISCAL_CODE.value],
                  PersonAttributes.TESTS.name: [],
                  PersonAttributes.VACCINATIONS.name: []
                  }
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


def read_vaccines():
    """
    Method to read all the vaccines from the file vaccines.txt.
    """
    with open("files/vaccines.txt", 'r', encoding='utf8') as file:
        for line in file:
            if line == "\n":
                continue
            vaccine = line.rstrip('\n').rstrip().lstrip().split(',')
            VACCINES.append(vaccine)


def read_tests():
    """
    Method to read all the tests from the file tests.txt.
    """
    with open("files/tests.txt", 'r', encoding='utf8') as file:
        for line in file:
            if line == "\n":
                continue
            TESTS.append((line.rstrip('\n').rstrip().lstrip()))


def create_index_function(collection_name):
    """
    Method that creates a textual index inside a MongoDB collection.
    :param collection_name: collection in which the index is created
    :return:
    """
    collection_name.create_index([('FISCAL_CODE', 'text')])


def retrieve_person():
    """
    Method that initializes a list containing all the attributes for a generic person (only name and surname so far)
    """
    name_index = random.randint(0, len(NAMES) - 1)
    surname_index = random.randint(0, len(SURNAMES) - 1)
    return [NAMES[name_index], SURNAMES[surname_index]]


def retrieve_detailed_person():
    """
    Method that initializes a list containing all the attributes for a generic person
    """
    name_index = random.randint(0, len(NAMES) - 1)
    surname_index = random.randint(0, len(SURNAMES) - 1)
    birthdate = build_date("1950-01-01", days_ahead=12775)
    fiscal_code = codicefiscale.encode(SURNAMES[surname_index], NAMES[name_index], 'M', str(birthdate),
                                       random.choice(MUNICIPALITIES))
    return [NAMES[name_index], SURNAMES[surname_index], birthdate, fiscal_code]


def build_date(start_date, days_ahead, is_random=True):
    """
    Method that provides a datetime structure
    :param start_date the starting date to which we add the number of days
    :param days_ahead the maximum number of days we can add
    :param is_random tells whether or not the date should be built randomly.
    """
    if is_random:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        result_date = start_date + datetime.timedelta(days=random.randint(0, days_ahead))
    else:
        result_date = start_date + datetime.timedelta(days=days_ahead)
    return result_date


def retrieve_issuer(issuer_index):
    """
    Method to retrieve a list containing all the attributes for an issuer.
    If an index is provided, it will be used to enable the search, otherwise a random index will be chosen.
    """
    try:
        return ISSUERS[issuer_index]
    except IndexError:
        print("Index out of bound, please insert a valid index!")


def retrieve_vaccine(start_index, end_index):
    """
    Method to randomly retrieve a list containing all the attributes for a vaccine.
    """
    vaccine_index = random.randint(start_index, end_index)
    return VACCINES[vaccine_index]


def retrieve_test():
    """
    Method to randomly retrieve a test.
    """
    test_index = random.randint(0, len(TESTS) - 1)
    return TESTS[test_index]


def insert_document(collection, document):
    """
    Method to insert a test document inside the collection.
    :param collection MongoDB collection to update
    :param document MongoDB document to insert in the collection
    """
    collection.insert_one(document)


def create_and_insert_all_issuer_doc(collection):
    """
    Method to insert all the issuers document and to initialize a local dictionary to avoid queries for
    retrieving ObjectIds.
    """
    for i in range(len(ISSUERS)):
        issuer_document = IssuerAttributes.create_embedded_issuer(retrieve_issuer(i), add_location_details=True)
        print("Inserting the issuer: " + retrieve_issuer(i)[IssuerAttributes.TYPE.value] + '\t'
              + retrieve_issuer(i)[IssuerAttributes.NAME.value])
        insert_document(collection, issuer_document)
        identifier = collection.find_one({'NAME': retrieve_issuer(i)[IssuerAttributes.NAME.value]},
                                         {'ObjectId': 1})['_id']
        ISSUERS_TABLE.update({i: identifier})


def create_and_insert_people_doc(collection):
    """
    Method to inside the chosen collection NUMBER OF PEOPLE instances of person documents.
    Furthermore, it updates the dictionary adding the pair (index, id) for each person.
    """
    for index in range(NUMBER_OF_PEOPLE):
        person_details = retrieve_detailed_person()
        person_document = PersonAttributes.create_embedded_person(person_details)
        print("Inserting the person: " + person_details[PersonAttributes.NAME.value] +
              ' ' + person_details[PersonAttributes.SURNAME.value])
        insert_document(collection, person_document)
        identifier = collection.find_one({'FISCAL_CODE': person_document['FISCAL_CODE']},
                                         {'ObjectId': 1})
        PEOPLE_TABLE.update({index: identifier['_id']})


def insert_ordered_vaccination(collection, person_index):
    """
    Method to insert a vaccination for the chosen person_id.
    It checks whether the person has already done any vaccination. If yes, it retrieves the vaccine name, producer and
    type to guarantee consistency among all the doses.
    """
    person_id = PEOPLE_TABLE[person_index]
    vaccinations_list = collection.find_one({'_id': person_id}, {'VACCINATIONS': 1})['VACCINATIONS']
    print(vaccinations_list)
    if len(vaccinations_list) == 0:
        collection.find_one_and_update({'_id': PEOPLE_TABLE[person_index]},
                                       {'$push': {'VACCINATIONS': {
                                           '$each': [
                                               VaccinationAttributes.
                                               create_vaccination_document
                                               (retrieve_vaccine(0, len(VACCINES)-1), retrieve_person(),
                                                retrieve_person())],
                                           '$sort': {'DATE': -1}}}})
    else:
        vaccination_details = list(vaccinations_list[0].values())
        new_vaccination_doc = VaccinationAttributes.create_vaccination_doc_from_previous_one(vaccination_details)
        if new_vaccination_doc is not None:
            collection.find_one_and_update({'_id': PEOPLE_TABLE[person_index]},
                                           {'$push': {'VACCINATIONS': {
                                               '$each': [new_vaccination_doc],
                                               '$sort': {'DATE': -1}
                                           }}})


if __name__ == '__main__':
    cluster = pym.MongoClient(CONNECTION_STRING)
    db = cluster['polipass']
    db.drop_collection('covid_certificates')
    db.drop_collection('issuers')
    covid_certificates_collection = db['covid_certificates']
    issuers_collection = db['issuers']

    # Initialization of all the global variables
    read_names()
    read_surnames()
    read_municipalities()
    read_addresses()
    read_issuers()
    read_vaccines()
    read_tests()

    # Insertion of the documents
    create_and_insert_people_doc(covid_certificates_collection)
    create_and_insert_all_issuer_doc(issuers_collection)
    print("People to vaccinate: " + str(PEOPLE_TABLE[0]))

    for i in range(len(PEOPLE_TABLE)):
        insert_ordered_vaccination(covid_certificates_collection, i)
        insert_ordered_vaccination(covid_certificates_collection, i)
        insert_ordered_vaccination(covid_certificates_collection, i)

    cluster.close()
