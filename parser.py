import argparse

def get_inject_arguments():
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument('zip_file',
                             type=str,
                             help='hide a secret in this archive')

    args_parser.add_argument('secret_file',
                             type=str,
                             help='secret to hide')

    args_parser.add_argument('output_file',
                             type=str,
                             nargs='?',
                             default="output.zip",
                             help='output ZIP archive')

    args_parser.add_argument('byte_offset',
                             type=int,
                             nargs='?',
                             default=0,
                             help='bytes offset of secret file')

    return args_parser.parse_args()

def get_extract_arguments():
    args_parser = argparse.ArgumentParser()

    args_parser.add_argument('zip_file',
                        type=str,
                        help='hide a secret in this archive')

    args_parser.add_argument('output_file',
                        type=str,
                        help='output ZIP archive')

    args_parser.add_argument('byte_offset',
                        type=int,
                        nargs='?',
                        default=0,
                        help='bytes offset of secret file')

    return args_parser.parse_args()