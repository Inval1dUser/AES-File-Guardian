#local imports
import crypt
import secrets
import os

seperator = '$'

def validate_password():
    password = None
    valid_pass = False
    while valid_pass == False:
        password = input("Enter a file password: ")
        if password.__contains__('$'):
            print("password cannot contain '$', try again or exit")
        else:
            valid_pass = True
            break
    return password


def validate_path():
    file = None
    valid_path = False
    while valid_path == False:
        path = input("Enter a file path to encrypt, make sure the is not surrounded by quotations: ")
        if os.path.exists(path):
            file = open(path, 'rb')
            valid_path = True
        else:
            print("File not found, try again or exit")
    return file

def save_encrypted_file(encrypted_data, file):
    output_filename = file.name + '.enc'
    is_dir_valid = False

    while not is_dir_valid:
        if not os.path.join(os.curdir, output_filename) in os.listdir(os.curdir):
            output_directory = input(f"Enter a directory to store '{output_filename}': ")
        else:
            output_directory = os.curdir

        output_full_path = os.path.join(output_directory, output_filename)
        original_extension = file.name.split('.')[-1]


        if not os.path.exists(output_directory):
            print(f"Error: Directory '{output_directory}' does not exist. Please try again.")
        elif not os.path.isdir(output_directory):
            print(f"Error: Path '{output_directory}' exists but is not a directory. Please try again.")
        else:
            try:
                with open(output_full_path, 'wb') as encrypted_file:
                    encrypted_file.write(encrypted_data[1])
                print(f"Encrypted file saved successfully to: {output_full_path}")
                is_dir_valid = True
            except IOError as e:
                print(f"Error writing file to '{output_full_path}': {e}. Please try again.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}. Please try again.")

if __name__ == '__main__':
    #get and validate password
    password = validate_password()

    #get and validate path
    file = validate_path()


    #generate salt
    salt = secrets.token_hex(16)
    salted_password = password + (seperator + salt)

    #encrypt password and retrieve key and token from response
    encrypted = crypt.encrypt_string(salted_password)

    if not os.path.exists('key.key'):
        enc_key = encrypted[0]
    else:
        enc_key = open('key.key', 'rb').read()


    enc_token = encrypted[1]

    #dec_pass = crypt.decrypt_string(enc_key, enc_token)
    #unsalted_pass = crypt.unsalt_data(dec_pass, salt)

    #open file and encrypt data
    original_data = file.read()
    encrypted_data = crypt.encrypt_string(original_data, key=enc_key)

    file.close()

    save_encrypted_file(encrypted_data, file)



    #encrypt file