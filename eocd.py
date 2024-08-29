class EOCD:

    def __init__(self, eocd, eocd_position):
        self.eocd = eocd
        self.eocd_position = eocd_position

        self.total_num_of_cd_records = int.from_bytes(eocd[10:12], byteorder='little')
        self.size_of_cd = int.from_bytes(eocd[12:16], byteorder='little')
        self.offset_of_cd = int.from_bytes(eocd[16:20], byteorder='little')

        self.print_EOCD_info()

    def print_EOCD_info(self):
        print("-------------------------------------------------------------------------")
        print('Total number of central directory records: {}'.format(self.total_num_of_cd_records))
        print('Size of central directory (bytes): {}'.format(self.size_of_cd))
        print('Offset of start of central directory, relative to start of archive: {}'.format(self.offset_of_cd))
        print("-------------------------------------------------------------------------")
