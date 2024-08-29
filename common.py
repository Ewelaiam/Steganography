from eocd import EOCD  # Import of EOCD class


EOCD_SIGNATURE = b'\x50\x4b\x05\x06'

def get_eocd_position(zip_file):
    with open(zip_file, 'rb') as f:  # open in binary mode
        data = f.read()
        pos = data.rfind(EOCD_SIGNATURE)  # find the first appearance of EOCD_SOGNATURE - else -1
        return pos


def create_eocd_object(zip_file):
    eocd_position_value = get_eocd_position(zip_file)

    if eocd_position_value == -1:
        raise ValueError("EOCD position not found")

    with open(zip_file, "rb") as f:
        f.seek(eocd_position_value)
        eocd = f.read()  # read EOCD record
        eocd_record = EOCD(eocd, eocd_position_value)

    return eocd_record