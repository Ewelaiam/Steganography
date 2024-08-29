import os
from parser import get_inject_arguments
from common import create_eocd_object

# create new file and hide secret in it
if __name__ == "__main__":
    # get arguments
    args = get_inject_arguments()

    # get EOCD record from ZIP file
    eocd = create_eocd_object(args.zip_file)

    # length of the file
    length_of_the_file_to_hide = 4

    with open(args.zip_file, 'rb') as zip_file, open(args.output_file, 'wb') as output_file, open(args.secret_file, 'rb') as secret:
        # copy all data from files up to first CD header
        files = zip_file.read(eocd.offset_of_cd)
        output_file.write(files)

        # reads the secret file and modifies its bytes by adding the byte_offset value, ensuring the result is within byte range (0-255) using modulo 256.
        files = secret.read()
        bytes_with_offset = bytes((byte + args.byte_offset) % 256 for byte in files)

        # copy the file we want to hide
        output_file.write(bytes_with_offset)

        # write the length of the file on 4 bytes
        output_file.write(os.path.getsize(args.secret_file).to_bytes(length_of_the_file_to_hide, 'little'))

        # copy and writes the central directory headers from the original ZIP file to the output file
        zip_file.seek(eocd.offset_of_cd)
        central_directory_headers = zip_file.read(eocd.eocd_position - eocd.offset_of_cd)
        output_file.write(central_directory_headers)

        # calculates the new offset for the Central Directory in the EOCD, modifies the EOCD with this new offset.
        new_offset = eocd.offset_of_cd + os.path.getsize(args.secret_file) + length_of_the_file_to_hide
        to_byte_array = bytearray(eocd.eocd)
        to_byte_array[16:20] = new_offset.to_bytes(length_of_the_file_to_hide, 'little')

        # copy modified eocd header (converts it back to bytes)
        output_file.write(bytes(to_byte_array))
