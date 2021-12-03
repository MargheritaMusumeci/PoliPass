import datetime
import hashlib
import random
import json
import pymongo as pym
from enum import IntEnum
from codicefiscale import codicefiscale
import qrcode
 from PIL import Image
import io

CONNECTION_STRING = "mongodb+srv://zucco:zucco@cluster0.fn8v8.mongodb.net/test"
# CONNECTION_STRING = "mongodb+srv://Piero_Rendina:R3nd1n%402021@cluster0.hns6k.mongodb.net/authSource=admin?ssl=true" \
     # "&tlsAllowInvalidCertificates=true"
#CONNECTION_STRING = "mongodb+srv://andrea:Zx9KaBfRDniXeDD@cluster0.7h575.mongodb.net/test"

# Constants
NUMBER_OF_PEOPLE = 10
MAX_NUMBER_OF_DOSES = 3
MAX_NUMBER_OF_TESTS = 5
PROB_BEING_DOCTOR_OR_NURSE = 0.5

# Global variables
NAMES = []
SURNAMES = []
MUNICIPALITIES = []
ADDRESSES = []
ISSUERS = []
VACCINES = []
TESTS = []
MOBILE_PREFIXES = []
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
# TODO use DOCTORS_TABLE and NURSES_TABLE to retrieve their data when building vaccinations and tests
"""
Dictionary used to bind each doctor with its ObjectId inside MongoDB
Is is updated after the creation of each doctor inside the function create_and_insert_people_doc 
"""
DOCTORS_TABLE = {}
"""
Dictionary used to bind each nurse with its ObjectId inside MongoDB
Is is updated after the creation of each nurse inside the function create_and_insert_people_doc 
"""
NURSES_TABLE = {}


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
                TestAttributes.DATE.name: build_date("2021-06-01", days_ahead=365),
                TestAttributes.TYPE.name: test_type,
                TestAttributes.RESULT.name: result,
                TestAttributes.DOCTOR.name: EmbeddedDoctorAttributes.create_doctor(retrieve_doctor()),
                TestAttributes.NURSE.name: EmbeddedDoctorAttributes.create_doctor(retrieve_nurse())
                }
        return test

    @classmethod
    def create_test_document_from_previous_one(cls, test_type, doctor, nurse, previous_test):
        """
        Method to create a test document after one test has already been done.
        :param test_type the type of the test
        :param doctor list containing all attributes for a doctor
        :param nurse list containing all attributes for a nurse
        :param previous_test the last test done
        """
        previous_date = str(datetime.datetime.date(previous_test['DATE']))
        positivity = random.random()
        if positivity >= 0.5:
            result = "positive"
        else:
            result = "negative"
        test = {TestAttributes.ISSUER.name: ISSUERS_TABLE[random.randint(0, len(ISSUERS_TABLE) - 1)],
                # TODO set the date between previous date and current date
                TestAttributes.DATE.name: build_date(previous_date, days_ahead=30),
                TestAttributes.TYPE.name: test_type,
                TestAttributes.RESULT.name: result,
                TestAttributes.DOCTOR.name: EmbeddedDoctorAttributes.create_doctor(retrieve_doctor()),
                TestAttributes.NURSE.name: EmbeddedDoctorAttributes.create_doctor(retrieve_nurse())
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
        hours = random.randint(8, 24)
        minutes = random.randint(0, 60)
        injection_date = production_date + datetime.timedelta(days=days, hours=hours, minutes=minutes)
        vaccination = {
            VaccinationAttributes.VACCINE.name: vaccine_issued,
            VaccinationAttributes.DATE.name: injection_date,
            VaccinationAttributes.DOSE.name: 1,
            VaccinationAttributes.ISSUER.name: ISSUERS_TABLE[random.randint(0, len(ISSUERS_TABLE) - 1)],
            VaccinationAttributes.DOCTOR.name: EmbeddedDoctorAttributes.create_doctor(retrieve_doctor()),
            VaccinationAttributes.NURSE.name: EmbeddedDoctorAttributes.create_doctor(retrieve_nurse()),
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
        if vaccine_name == "COVID-19 Vaccine Janssen" or (vaccine_name == "Vaxzevria" and previous_dose == 2):
            previous_dose = 2
            vaccine_details[EmbeddedVaccineAttributes.NAME.value:
                            EmbeddedVaccineAttributes.TYPE.value + 1] = retrieve_vaccine(0, 1)
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
            VaccinationAttributes.DOCTOR.name: EmbeddedDoctorAttributes.create_doctor(retrieve_doctor()),
            VaccinationAttributes.NURSE.name: EmbeddedDoctorAttributes.create_doctor(retrieve_nurse()),
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
        :param add_location_details is a boolean variable to assess
        if the details about the issuer position are required.
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
    FISCAL_CODE = 2

    @classmethod
    def create_embedded_doctor(cls, doctor_details):
        """
        Method that creates a dictionary representing an embedded doctor
        """
        name = doctor_details[EmbeddedDoctorAttributes.NAME.value]
        surname = doctor_details[EmbeddedDoctorAttributes.SURNAME.value]
        doctor = {EmbeddedDoctorAttributes.NAME.name: name,
                  EmbeddedDoctorAttributes.SURNAME.name: surname
        }
        return doctor

    @classmethod
    def create_doctor(cls, fiscal_code):
        """
        Method to create an embedded doctor/nurse given his/her fiscal code.
        :param fiscal_code fiscal code to enable the searching inside NURSES_TABLE or DOCTOR_TABLES
        """
        try:
            name = NURSES_TABLE[fiscal_code][0]
            surname = NURSES_TABLE[fiscal_code][1]
        except KeyError:
            try:
                name = DOCTORS_TABLE[fiscal_code][0]
                surname = DOCTORS_TABLE[fiscal_code][1]
            except KeyError:
                name = None
                surname = None
        if name is not None and surname is not None:
            caregiver_doc = {
                EmbeddedDoctorAttributes.NAME.name: name,
                EmbeddedDoctorAttributes.SURNAME.name: surname,
                EmbeddedDoctorAttributes.FISCAL_CODE.name: fiscal_code,
            }
            return caregiver_doc


class PersonAttributes(IntEnum):
    """
    Enum class to retrieve the index of a given attribute for an embedded person
    """
    NAME = 0
    SURNAME = 1
    BIRTHDATE = 2
    FISCAL_CODE = 3
    BIRTH_PLACE = 4
    PHONE_NUMBER = 5
    EMAIL = 6
    ADDRESS = 7
    EMERGENCY_CONTACT = 8
    TESTS = 9
    VACCINATIONS = 10
    GREEN_PASS = 11
    PASSWORD = 12
    ROLE = 13

    @classmethod
    def create_person(cls, person_details):
        """
        Method that creates a dictionary representing an embedded person
        """
        emergency_contact = EmergencyContactAttributes.create_embedded_emergency_contact(retrieve_person())
        person = {PersonAttributes.NAME.name: person_details[PersonAttributes.NAME.value],
                  PersonAttributes.SURNAME.name: person_details[PersonAttributes.SURNAME.value],
                  PersonAttributes.BIRTHDATE.name: person_details[PersonAttributes.BIRTHDATE.value],
                  PersonAttributes.FISCAL_CODE.name: person_details[PersonAttributes.FISCAL_CODE.value],
                  PersonAttributes.BIRTH_PLACE.name: person_details[PersonAttributes.BIRTH_PLACE.value],
                  PersonAttributes.PHONE_NUMBER.name: person_details[PersonAttributes.PHONE_NUMBER.value],
                  PersonAttributes.EMAIL.name: person_details[PersonAttributes.EMAIL.value],
                  PersonAttributes.ADDRESS.name: person_details[PersonAttributes.ADDRESS.value],
                  PersonAttributes.EMERGENCY_CONTACT.name: emergency_contact,
                  PersonAttributes.PASSWORD.name: encode_password("password")
                  }
        probability = random.random()
        role = None
        if PROB_BEING_DOCTOR_OR_NURSE >= probability:
            role = random.choice(["doctor", "nurse"])
        if role is not None:
            person[PersonAttributes.ROLE.name] = role
            if role == "doctor":
                DOCTORS_TABLE.update(
                    {person[PersonAttributes.FISCAL_CODE.name]:
                        [person[PersonAttributes.NAME.name], person[PersonAttributes.SURNAME.name]]})
            if role == "nurse":
                NURSES_TABLE.update(
                    {person[PersonAttributes.FISCAL_CODE.name]:
                        [person[PersonAttributes.NAME.name], person[PersonAttributes.SURNAME.name]]})
        return person


def encode_password(string):
    """
    Encodes a password using SHA-256 algorithm.
    """
    # Converts the string into bytes
    encoded_string = string.encode()
    # Create the SHA-256 object
    result = hashlib.sha256(encoded_string)
    # Get the hexadecimal format of the encoded data
    hex_string = result.hexdigest()
    return hex_string


class GreenPassAttributes(IntEnum):
    """
    Enum class to retrieve the index of an attribute for a green pass embedded instance.
    """
    QR_CODE = 0
    ISSUE_DATE = 1
    EXPIRATION_DATE = 2

    @classmethod
    def create_green_pass_from_vaccination(cls, vaccination):
        date = vaccination[VaccinationAttributes.DATE.name]
        dose_number = vaccination[VaccinationAttributes.DOSE.name]
        vaccine = vaccination[VaccinationAttributes.VACCINE.name]
        if dose_number == 1:
            if vaccine[EmbeddedVaccineAttributes.NAME.name] == "COVID-19 Vaccine Janssen":
                days_ahead = 270
            else:
                days_ahead = 30
        else:
            if dose_number == 2:
                days_ahead = 270
            else:
                days_ahead = 365
        expiration_date = date + datetime.timedelta(days=days_ahead)
        green_pass = {GreenPassAttributes.QR_CODE.name: build_green_pass_qrcode(str(expiration_date)),
                      GreenPassAttributes.ISSUE_DATE.name: date,
                      GreenPassAttributes.EXPIRATION_DATE.name: expiration_date
                      }
        return green_pass

    @classmethod
    def create_green_pass_from_test(cls, test):
        date = test[TestAttributes.DATE.name]
        expiration_date = date + datetime.timedelta(days=2)
        green_pass = {GreenPassAttributes.QR_CODE.name: build_green_pass_qrcode(str(expiration_date)),
                      GreenPassAttributes.ISSUE_DATE.name: date,
                      GreenPassAttributes.EXPIRATION_DATE.name: expiration_date
                      }
        return green_pass


class EmergencyContactAttributes(IntEnum):
    """
    Enum class to retrieve the index of an attribute for an emergency contact embedded instance.
    """
    NAME = 0
    SURNAME = 1
    PHONE_NUMBER = 2

    @classmethod
    def create_embedded_emergency_contact(cls, person_details):
        phone_number = random.choice(MOBILE_PREFIXES) + str(random.randint(1111111, 9999999))
        contact = {EmergencyContactAttributes.NAME.name: person_details[EmergencyContactAttributes.NAME.value],
                   EmergencyContactAttributes.SURNAME.name: person_details[EmergencyContactAttributes.SURNAME.value],
                   EmergencyContactAttributes.PHONE_NUMBER.name: phone_number
                   }
        return contact


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
            address_line = line.rstrip('\n').rstrip().lstrip().split(',')
            address = ""
            for i in range(len(address_line)):
                if i > 0:
                    address = address + " " + address_line[i]
                else:
                    address = address + address_line[i]
            ADDRESSES.append(address)
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


def read_mobile_prefixes():
    """
    Method to read all the italian mobile prefixes from the file mobile_prefixes.txt.
    """
    with open("files/mobile_prefixes.txt", 'r', encoding='utf8') as file:
        for line in file:
            if line == "\n":
                continue
            MOBILE_PREFIXES.append((line.rstrip('\n').rstrip().lstrip()))


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


def retrieve_nurse():
    fiscal_code = random.choice(list(NURSES_TABLE.keys()))
    try:
        return fiscal_code
    except KeyError:
        print("Error, no nurse available")


def retrieve_doctor():
    fiscal_code = random.choice(list(DOCTORS_TABLE.keys()))
    try:
        return fiscal_code
    except KeyError:
        print("Error, no doctor available")


def build_detailed_person():
    """
    Method that initializes a list containing all the attributes for a generic person
    """
    name_index = random.randint(0, len(NAMES) - 1)
    surname_index = random.randint(0, len(SURNAMES) - 1)
    name = NAMES[name_index]
    surname = SURNAMES[surname_index]
    if name[len(name) - 1] == 'a':
        sex = 'F'
    else:
        sex = 'M'
    birthdate = build_date("1950-01-01", days_ahead=12775)
    birth_place = random.choice(MUNICIPALITIES)
    fiscal_code = codicefiscale.encode(surname, name, sex, str(birthdate),
                                       birth_place)
    address = ADDRESSES[random.randint(0, len(ADDRESSES) - 1)]
    number = "+393"
    for i in range(0, 9):
        number += str(random.randint(0, 9))
    email = (name + '.' + surname + "@polipass.it").lower()
    return [name, surname, birthdate, fiscal_code, birth_place, number, email, address]


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


def build_green_pass_qrcode(expiration_date):
    """
    Method that saves an image representing a green pass qr code and returns it as a binary file.
    """
    green_pass_img = qrcode.make(expiration_date)
    green_pass_img.save("green_pass.png")
    green_pass_img = Image.open("green_pass.png")
    green_pass_qr_bytes = io.BytesIO()
    green_pass_img.save(green_pass_qr_bytes, format='PNG')
    return green_pass_qr_bytes.getvalue()


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
        person_details = build_detailed_person()
        person_document = PersonAttributes.create_person(person_details)
        print("Inserting the person: " + person_details[PersonAttributes.NAME.value] +
              ' ' + person_details[PersonAttributes.SURNAME.value])
        insert_document(collection, person_document)
        identifier = collection.find_one({'FISCAL_CODE': person_document['FISCAL_CODE']},
                                         {'ObjectId': 1})
        PEOPLE_TABLE.update({index: identifier['_id']})
        """
        try:
            role = person_document['ROLE']
            if role == "doctor":
                DOCTORS_TABLE.update({index: identifier['_id']})
            elif role == "nurse":
                NURSES_TABLE.update({index: identifier['_id']})
        except KeyError:
            pass
        """


def insert_ordered_vaccination(collection, person_index):
    """
    Method to insert a vaccination for the chosen person_id.
    It checks whether the person has already done any vaccination. If yes, it retrieves the vaccine name, producer and
    type to guarantee consistency among all the doses.
    :return the vaccination document that has been just created.
    """
    person_id = PEOPLE_TABLE[person_index]
    vaccinations_list = collection.find_one({'_id': person_id}, {'VACCINATIONS': 1})

    try:
        vaccinations_list = vaccinations_list['VACCINATIONS']
    except KeyError:
        vaccinations_list = []

    print(vaccinations_list)
    if len(vaccinations_list) == 0:
        new_vaccination_doc = VaccinationAttributes.create_vaccination_document \
            (retrieve_vaccine(0, len(VACCINES) - 1), retrieve_person(), retrieve_person())
        collection.find_one_and_update({'_id': person_id},
                                       {'$push': {'VACCINATIONS': {
                                           '$each': [new_vaccination_doc],
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
    if new_vaccination_doc is not None:
        insert_green_pass(collection, new_vaccination_doc, person_index)


def insert_green_pass(collection, vaccination, person_index):
    """
    Method used to create and update the green pass for a given person.
    """
    person_id = PEOPLE_TABLE[person_index]
    collection.find_one_and_update({'_id': person_id},
                                   {'$set': {'GREEN_PASS':
                                                 GreenPassAttributes.create_green_pass_from_vaccination(vaccination)
                                             }
                                    })


def insert_ordered_test(collection, person_index):
    """
    Method to insert a test for the chosen person_id. If the person has an active green pass and the test result is
    positive, the green pass gets deleted. If the test result is negative and the person has an active vaccine, it
    recreates the green pass from the vaccine details. Otherwise, if the test result is negative a new green pass
    is created when the person has not gotten the vaccine or when their vaccine is eligible for a green pass.
    """
    person_id = PEOPLE_TABLE[person_index]
    info = collection.find_one({'_id': person_id}, {"VACCINATIONS": 1, "TESTS": 1, "GREEN_PASS": 1})



    try:
        green_pass = info['GREEN_PASS']
    except KeyError:
        green_pass = None

    # if the green pass is expired, remove it
    if green_pass is not None and datetime.datetime.today() >= green_pass['EXPIRATION_DATE']:
        collection.find_one_and_update({'_id': PEOPLE_TABLE[person_index]},
                                       {'$unset': {'GREEN_PASS': ""},
                                        })
    try:
        tests_list = info['TESTS']
    except KeyError:
        tests_list = []

    # create a new test
    if len(tests_list) == 0:
        test = TestAttributes.create_test_document(random.choice(TESTS), retrieve_person(), retrieve_person())
    else:
        last_test = collection.find_one({'_id': PEOPLE_TABLE[person_index]},
                                        {'TESTS': {
                                            '$slice': 1
                                        }})['TESTS'][0]
        test = TestAttributes.create_test_document_from_previous_one(random.choice(TESTS), retrieve_person(),
                                                                     retrieve_person(), last_test)
    result = test['RESULT']
    try:
        vaccinations_list = info['VACCINATIONS']
    except KeyError:
        vaccinations_list = []


    # handle the case where the person got a vaccine
    if len(vaccinations_list) != 0:
        last_vaccination = collection.find_one({'_id': PEOPLE_TABLE[person_index]},
                                               {'VACCINATIONS': {
                                                   '$slice': 1
                                               }})['VACCINATIONS'][0]
        if result == "positive":
            if green_pass is not None and green_pass['ISSUE_DATE'] <= test['DATE'] <= green_pass['EXPIRATION_DATE']:
                collection.find_one_and_update({'_id': PEOPLE_TABLE[person_index]},
                                               {'$push': {'TESTS': {
                                                   '$each': [test],
                                                   '$sort': {'DATE': -1}}},
                                                   '$unset': {'GREEN_PASS': ""}
                                               })
            elif green_pass is not None:
                collection.find_one_and_update({'_id': PEOPLE_TABLE[person_index]},
                                               {'$push': {'TESTS': {
                                                   '$each': [test],
                                                   '$sort': {'DATE': -1}
                                               }}})
            else:
                collection.find_one_and_update({'_id': PEOPLE_TABLE[person_index]},
                                               {'$push': {'TESTS': {
                                                   '$each': [test],
                                                   '$sort': {'DATE': -1}
                                               }}})
        elif result == "negative":
            # TODO handle the case where the last vaccination is not eligible for a green pass
            collection.find_one_and_update({'_id': PEOPLE_TABLE[person_index]},
                                           {'$push': {'TESTS': {
                                               '$each': [test],
                                               '$sort': {'DATE': -1}}},
                                               '$set': {'GREEN_PASS':
                                                   GreenPassAttributes.create_green_pass_from_vaccination(
                                                       last_vaccination)
                                               }
                                           })

    # handle the case where the person did not get a vaccine
    else:
        if result == "positive":
            if green_pass is None:
                collection.find_one_and_update({'_id': PEOPLE_TABLE[person_index]},
                                               {'$push': {'TESTS': {
                                                   '$each': [test],
                                                   '$sort': {'DATE': -1}
                                               }}})
            else:
                collection.find_one_and_update({'_id': PEOPLE_TABLE[person_index]},
                                               {'$push': {'TESTS': {
                                                   '$each': [test],
                                                   '$sort': {'DATE': -1}}},
                                                   '$unset': {'GREEN_PASS': ""}
                                               })
        elif result == "negative":
            collection.find_one_and_update({'_id': PEOPLE_TABLE[person_index]},
                                           {'$push': {'TESTS': {
                                               '$each': [test],
                                               '$sort': {'DATE': -1}}},
                                               '$set': {'GREEN_PASS':
                                                        GreenPassAttributes.create_green_pass_from_test(test)
                                                        }
                                           })



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
    read_mobile_prefixes()

    # Insertion of people and issuers
    create_and_insert_people_doc(covid_certificates_collection)
    create_and_insert_all_issuer_doc(issuers_collection)

    for key in DOCTORS_TABLE.keys():
        print("Doctor: " + str(key))
    for key in NURSES_TABLE.keys():
        print("Nurse: " + str(key))

    # Insertion of vaccines
    for j in range(len(PEOPLE_TABLE)):
        doses = random.randint(0, MAX_NUMBER_OF_DOSES)
        for k in range(doses):
            insert_ordered_vaccination(covid_certificates_collection, j)
    # Insertion of tests
    for j in range(len(PEOPLE_TABLE)):
        tests = random.randint(0, MAX_NUMBER_OF_TESTS)
        for k in range(tests):
            insert_ordered_test(covid_certificates_collection, j)
    cluster.close()