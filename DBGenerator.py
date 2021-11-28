from enum import IntEnum


class TestAttributes(IntEnum):
    """
    Enum class to retrieve index of a given attribute for a test sample.
    """
    # Names corresponding to a key in the dictionary
    DATE = 0
    RESULT = 1
    TYPE = 2
    ISSUER_NAME = 3
    ISSUER_ADDRESS = 4
    P_NAME = 5
    P_SURNAME = 6
    P_BIRTHDATE = 7
    P_FISCAL_CODE = 8
    D_NAME = 9
    D_SURNAME = 10
    D_MAIL = 11
    N_NAME = 12
    N_SURNAME = 13
    N_MAIL = 14

    # Name just for the pleasure of my eyes
    PERSON = -1
    ISSUER = -2
    DOCTOR = -3
    NURSE = -4

    @classmethod
    def number_of_attribute(cls):
        """
        Method used to get the number of useful parameters for the creation of the array
        Example of usage:
            test = [None] * TestAttribute.number_of_attribute()
            test[TestAttribute.NAME] = name
            ...
        :return: the number of useful parameters
        """
        numAttribute = 0
        for name in TestAttributes:
            if name.value >= 0:
                numAttribute += 1
        return numAttribute

    @classmethod
    def get_test_structure(cls , params):
        """
        Method that builds the dictionary containing the whole structure of the test document
        :param params: is a list containing all the params
        :return: the complete dictionary
        """
        issuerDictionary = {
            TestAttributes.ISSUER_NAME.name : params[TestAttributes.ISSUER_NAME.value] ,
            TestAttributes.ISSUER_ADDRESS.name : params[TestAttributes.ISSUER_ADDRESS]
        }

        personDictionary = {
            TestAttributes.P_NAME.name : params[TestAttributes.P_NAME.value] ,
            TestAttributes.P_SURNAME.name : params[TestAttributes.P_SURNAME.value] ,
            TestAttributes.P_BIRTHDATE.name : params[TestAttributes.P_BIRTHDATE.value] ,
            TestAttributes.P_FISCAL_CODE.name : params[TestAttributes.P_FISCAL_CODE.value]
        }

        doctorDictionary = {
            TestAttributes.D_NAME.name: params[TestAttributes.D_NAME.value],
            TestAttributes.D_SURNAME.name: params[TestAttributes.D_SURNAME.value],
            TestAttributes.D_MAIL.name : params[TestAttributes.D_MAIL.value]
        }

        nurseDictionary = {
            TestAttributes.N_NAME.name: params[TestAttributes.N_NAME.value],
            TestAttributes.N_SURNAME.name: params[TestAttributes.N_SURNAME.value],
            TestAttributes.N_MAIL.name : params[TestAttributes.N_MAIL.value]
        }

        dictionary = {
            TestAttributes.TYPE.name : params[TestAttributes.TYPE.value] ,
            TestAttributes.DATE.name : params[TestAttributes.DATE.value] ,
            TestAttributes.RESULT.name : params[TestAttributes.RESULT.value] ,
            TestAttributes.PERSON.name : personDictionary ,
            TestAttributes.ISSUER.name : issuerDictionary ,
            TestAttributes.DOCTOR.name : doctorDictionary ,
            TestAttributes.NURSE.name : nurseDictionary
        }

        return dictionary


class VaccineAttributes(IntEnum):
    """
    Enum class to retrieve index of a given attribute for a vaccine sample.
    """
    # Names corresponding to a key in the dictionary
    DATE = 0
    TYPE = 1
    NAME = 2
    PRODUCER = 3
    LOT = 4
    PRODUCTION_DATE = 5
    DOSE = 6
    P_NAME = 7
    P_SURNAME = 8
    P_BIRTHDATE = 9
    P_FISCAL_CODE = 10
    ISSUER_NAME = 11
    ISSUER_ADDRESS = 12
    D_NAME = 13
    D_SURNAME = 14
    D_MAIL = 15
    N_NAME = 16
    N_SURNAME = 17
    N_MAIL = 18

    # Name just for the pleasure of my eyes
    PERSON = -1
    ISSUER = -2
    DOCTOR = -3
    NURSE = -4
    VACCINE_DETAILS = -5

    @classmethod
    def number_of_attribute(cls):
        """
        Method used to get the number of useful parameters for the creation of the array
        :return: the number of useful parameters
        """
        numAttribute = 0
        for name in VaccineAttributes:
            if name.value >= 0:
                numAttribute += 1
        return numAttribute

    @classmethod
    def get_test_structure(cls , params):
        """
        Method that builds the dictionary containing the whole structure of the vaccine document
        :param params: is a list containing all the params
        :return: the complete dictionary
        """
        issuerDictionary = {
            VaccineAttributes.ISSUER_NAME.name : params[VaccineAttributes.ISSUER_NAME.value] ,
            VaccineAttributes.ISSUER_ADDRESS.name : params[VaccineAttributes.ISSUER_ADDRESS]
        }

        personDictionary = {
            VaccineAttributes.P_NAME.name : params[VaccineAttributes.P_NAME.value] ,
            VaccineAttributes.P_SURNAME.name : params[VaccineAttributes.P_SURNAME.value] ,
            VaccineAttributes.P_BIRTHDATE.name : params[VaccineAttributes.P_BIRTHDATE.value] ,
            VaccineAttributes.P_FISCAL_CODE.name : params[VaccineAttributes.P_FISCAL_CODE.value]
        }

        doctorDictionary = {
            VaccineAttributes.D_NAME.name: params[VaccineAttributes.D_NAME.value],
            VaccineAttributes.D_SURNAME.name: params[VaccineAttributes.D_SURNAME.value],
            VaccineAttributes.D_MAIL.name : params[VaccineAttributes.D_MAIL.value]
        }

        nurseDictionary = {
            VaccineAttributes.N_NAME.name: params[VaccineAttributes.N_NAME.value],
            VaccineAttributes.N_SURNAME.name: params[VaccineAttributes.N_SURNAME.value],
            VaccineAttributes.N_MAIL.name : params[VaccineAttributes.N_MAIL.value]
        }

        vaccineDetailsDictionary = {
            VaccineAttributes.NAME.name: params[VaccineAttributes.NAME.value],
            VaccineAttributes.PRODUCER.name: params[VaccineAttributes.PRODUCER.value],
            VaccineAttributes.DOSE.name: params[VaccineAttributes.DOSE.value],
            VaccineAttributes.LOT.name: params[VaccineAttributes.LOT.value],
            VaccineAttributes.PRODUCTION_DATE.name: params[VaccineAttributes.PRODUCTION_DATE.value],
        }

        dictionary = {
            VaccineAttributes.TYPE.name : params[VaccineAttributes.TYPE.value] ,
            VaccineAttributes.DATE.name : params[VaccineAttributes.DATE.value] ,
            VaccineAttributes.VACCINE_DETAILS.name : vaccineDetailsDictionary ,
            VaccineAttributes.PERSON.name : personDictionary ,
            VaccineAttributes.ISSUER.name : issuerDictionary ,
            VaccineAttributes.DOCTOR.name : doctorDictionary ,
            VaccineAttributes.NURSE.name : nurseDictionary
        }

        return dictionary


class IssuerAttributes(IntEnum):
    """
    Enum class to retrieve index of a given attribute for am issuer sample.
    """
    # Names corresponding to a key in the dictionary
    NAME = 0
    TYPE = 1
    GPS_COORDINATES = 2
    OPENING_HOURS = 3
    ADDRESS = 4
    CITY = 5
    COUNTRY = 6
    ZIP = 7

    # Name just for the pleasure of my eyes
    LOCATION_DETAILS = -1

    @classmethod
    def number_of_attribute(cls):
        """
        Method used to get the number of useful parameters for the creation of the array
        :return: the number of useful parameters
        """
        numAttribute = 0
        for name in IssuerAttributes:
            if name.value >= 0:
                numAttribute += 1
        return numAttribute

    @classmethod
    def get_test_structure(cls , params):
        """
        Method that builds the dictionary containing the whole structure of the issuer document
        :param params: is a list containing all the params
        :return: the complete dictionary
        """
        locationDetailsDictionary = {
            IssuerAttributes.ADDRESS.name : params[IssuerAttributes.ADDRESS.value],
            IssuerAttributes.CITY.name: params[IssuerAttributes.CITY.value],
            IssuerAttributes.ZIP.name: params[IssuerAttributes.ZIP.value],
            IssuerAttributes.COUNTRY.name: params[IssuerAttributes.COUNTRY.value]
        }

        dictionary = {
            IssuerAttributes.NAME.name: params[IssuerAttributes.NAME.value],
            IssuerAttributes.TYPE.name : params[IssuerAttributes.TYPE.value] ,
            IssuerAttributes.GPS_COORDINATES.name : params[IssuerAttributes.GPS_COORDINATES.value] ,
            IssuerAttributes.OPENING_HOURS.name : params[IssuerAttributes.OPENING_HOURS.value] ,
            IssuerAttributes.LOCATION_DETAILS.name : locationDetailsDictionary
        }

        return dictionary


class GreenPassAttributes(IntEnum):
    """
    Enum class to retrieve index of a given attribute for a green pass sample.
    """
    # Names corresponding to a key in the dictionary
    QR_CODE = 0
    VALIDITY_DATE = 1
    STATE = 2

    @classmethod
    def number_of_attribute(cls):
        """
        Method used to get the number of useful parameters for the creation of the array
        :return: the number of useful parameters
        """
        numAttribute = 0
        for name in GreenPassAttributes:
            if name.value >= 0:
                numAttribute += 1
        return numAttribute

    @classmethod
    def get_test_structure(cls , params):
        """
        Method that builds the dictionary containing the whole structure of the green pass document
        :param params: is a list containing all the params
        :return: the complete dictionary
        """

        dictionary = {
            GreenPassAttributes.QR_CODE.name : params[GreenPassAttributes.QR_CODE.value] ,
            GreenPassAttributes.VALIDITY_DATE.name : params[GreenPassAttributes.VALIDITY_DATE.value] ,
            GreenPassAttributes.STATE.name : params[GreenPassAttributes.STATE.value]
        }

        return dictionary


class PersonAttributes(IntEnum):
    """
    Enum class to retrieve index of a given attribute for a person sample.
    """
    # Names corresponding to a key in the dictionary
    NAME = 0
    SURNAME = 1
    BIRTHDATE = 2
    FISCAL_CODE = 3
    TELEPHONE_NUMBER = 4
    EMAIL = 5
    EC_TELEPHONE_NUMBER = 6
    EC_EMAIL = 7
    ADDRESS = 8
    CITY = 9
    COUNTRY = 10
    ZIP = 11

    # Name just for the pleasure of my eyes
    EMERGENCY_CONTACT = -1
    LOCATION_DETAILS = -2

    @classmethod
    def number_of_attribute(cls):
        """
        Method used to get the number of useful parameters for the creation of the array
        :return: the number of useful parameters
        """
        numAttribute = 0
        for name in PersonAttributes:
            if name.value >= 0:
                numAttribute += 1
        return numAttribute

    @classmethod
    def get_test_structure(cls , params):
        """
        Method that builds the dictionary containing the whole structure of the vaccine document
        :param params: is a list containing all the params
        :return: the complete dictionary
        """
        locationDetailsDictionary = {
            PersonAttributes.ADDRESS.name : params[PersonAttributes.ADDRESS.value],
            PersonAttributes.CITY.name: params[PersonAttributes.CITY.value],
            PersonAttributes.ZIP.name: params[PersonAttributes.ZIP.value],
            PersonAttributes.COUNTRY.name: params[PersonAttributes.COUNTRY.value]
        }

        emergencyContactDictionary = {
            PersonAttributes.EC_EMAIL.name : params[PersonAttributes.EC_EMAIL.value] ,
            PersonAttributes.EC_TELEPHONE_NUMBER.name: params[PersonAttributes.EC_TELEPHONE_NUMBER.value]
        }

        dictionary = {
            PersonAttributes.NAME.name: params[PersonAttributes.NAME.value],
            PersonAttributes.SURNAME.name : params[PersonAttributes.SURNAME.value] ,
            PersonAttributes.BIRTHDATE.name : params[PersonAttributes.BIRTHDATE.value] ,
            PersonAttributes.FISCAL_CODE.name : params[PersonAttributes.FISCAL_CODE.value] ,
            PersonAttributes.EMAIL.name : params[PersonAttributes.EMAIL.value] ,
            PersonAttributes.LOCATION_DETAILS.name : locationDetailsDictionary ,
            PersonAttributes.EMERGENCY_CONTACT.name : emergencyContactDictionary
        }

        return dictionary


if __name__ == '__main__':

    testDict = TestAttributes.get_test_structure(["0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" , "10" ,
                                                  "11" , "12" , "13" , "14"])

    vaccineDict = VaccineAttributes.get_test_structure(["0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" ,
                                                        "10" , "11" , "12" , "13" , "14" , "15" , "16" , "17" , "18"])

    issuerDict = IssuerAttributes.get_test_structure(["0" , "1" , "2" , "3" , "4" , "5" , "6" , "7"])

    greenPassDict = GreenPassAttributes.get_test_structure(["0" , "1" , "2"])

    personDict = PersonAttributes.get_test_structure(["0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" ,
                                                      "10" , "11"])

    print(testDict)
    print(vaccineDict)
    print(issuerDict)
    print(greenPassDict)
    print(personDict)
    print("Size of TestAttribute is: " , TestAttributes.number_of_attribute())
    print("Size of VaccineAttribute is: ", VaccineAttributes.number_of_attribute())
    print("Size of IssuerAttribute is: ", IssuerAttributes.number_of_attribute())
    print("Size of GreenPassAttribute is: ", GreenPassAttributes.number_of_attribute())
    print("Size of PersonAttribute is: ", PersonAttributes.number_of_attribute())
