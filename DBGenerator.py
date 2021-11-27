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
            test[TestAttribute.P_NAME] = name
            ...
        :return: the number of useful parameters
        """
        numAttribute = 0
        for name in TestAttributes:
            if name.value >= 0:
                numAttribute += 1
        return numAttribute

    @classmethod
    def get_test_structure(cls, params):
        """
        Method that builds the dictionary containing the whole structure of the test document
        :param params: is a list containing all the params
        :return: the complete dictionary
        """
        issuerDictionary = {
            TestAttributes.ISSUER_NAME.name : params[TestAttributes.ISSUER_NAME.value] ,
            TestAttributes.ISSUER_ADDRESS.name : params[TestAttributes.ISSUER_ADDRESS.value]
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
        Method that builds the dictionary containing the whole structure vaccine document
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


if __name__ == '__main__':

    testDict = TestAttributes.get_test_structure(["0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" , "10" ,
                                                  "11" , "12" , "13" , "14"])

    vaccineDict = VaccineAttributes.get_test_structure(["0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" ,
                                                        "10" , "11" , "12" , "13" , "14" , "15" , "16" , "17" , "18"])
    print(testDict)
    print(vaccineDict)
    print("Size of TestAttribute is: " , TestAttributes.number_of_attribute())
    print("Size of VaccineAttribute is: ", VaccineAttributes.number_of_attribute())
