from enum import IntEnum


class TestAttributes(IntEnum):
    """
    Eum class to retrieve index of a given attribute for a test sample.
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

    # Name just for the pleasure of my eye
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


if __name__ == '__main__':

    testDict = TestAttributes.get_test_structure(["0" , "1" , "2" , "3" , "4" , "5" , "6" , "7" , "8" , "9" , "10" ,
                                                  "11" , "12" , "13" , "14"])
    print(testDict)
    print("Size of TestAttribute is: " , TestAttributes.number_of_attribute())
