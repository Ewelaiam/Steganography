from parser import get_extract_arguments
from common import create_eocd_object

# create new file and put secret in it
if __name__ == "__main__":
    args = get_extract_arguments()

    # get EOCD record from ZIP file
    eocd = create_eocd_object(args.zip_file)

    with open(args.zip_file, 'rb') as zip_file, open(args.output_file, 'wb') as output_file:
        # get byte length of secret file
        zip_file.seek(eocd.offset_of_cd)
        # go back (-4) to read secret file
        zip_file.seek(-4, 1)
        secret_length = int.from_bytes(zip_file.read(4), 'little')

        # copy all data up to first CD header
        zip_file.seek(-(4 + secret_length), 1)
        # read secret
        data = zip_file.read(secret_length)
        # rm offset val from every byte
        bytes_with_offset = bytes((byte - args.byte_offset) % 256 for byte in data)
        output_file.write(bytes_with_offset)

