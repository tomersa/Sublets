import urllib2
import simplecrypt
import sys, os

DEBUG = True

class FacebookHandler:
    ENTER_PASSWORD_MESSAGE = "Enter password:"

    def __init__(self, key_path):
        self.ENCRYPTED_KEY_PATH = key_path

    def __read_encrypted_client_secret(self):
        handle = open(self.ENCRYPTED_KEY_PATH, "r")
        key_content = None
        try:
            key_content = handle.read()

        finally:
            handle.close()

        decrypted_key = simplecrypt.decrypt(raw_input(FacebookHandler.ENTER_PASSWORD_MESSAGE), key_content)

        return decrypted_key

    def read_from_api(self):
        encrypted_client_secret = self.__read_encrypted_client_secret()
        graph_api_request = "https://graph.facebook.com/oauth/access_token?client_id=490769394355273&client_secret=%s&grant_type=client_credentials" % encrypted_client_secret

        access_token = urllib2.urlopen(graph_api_request).read().replace("access_token=", "")

        write_access_token_to_file(access_token)

        return access_token


def read_access_token_from_file():
    try:
        handle = open(".access_token", "r")
        access_token = handle.read()

    finally:
        handle.close()

    return access_token

def write_access_token_to_file(access_token):
    try:
        handle = open(".access_token", "w")
        handle.write(access_token)

    finally:
        handle.close()

def main():
    facebook_handler = FacebookHandler(sys.argv[1])

    if DEBUG and os.path.exists(".access_token"):
        access_token = read_access_token_from_file()

    else:
        print facebook_handler.read_from_api()

if __name__ == "__main__":
    main()