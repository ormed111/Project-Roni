from Universal.constants import DataTransmissionConstants as consts


class Crypto(object):
    """
        class handles all aspects of data encryption/decryption for hq and kli communications.
    """

    @classmethod
    def encrypt_data(cls, data):
        """
            method gets data encrypts it..
                for now it is just encoding it to base64 but this can be easily changed
        """
        return data.encode(consts.BASE64)

    @classmethod
    def decrypt_data(cls, data):
        return data.decode(consts.BASE64)