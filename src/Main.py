import simplecrypt
import sys
import eatiht.v2 as v2

def readContent(input_file_path):
    content = None

    try:
        handle = open(input_file_path)
        content = handle.read()

    finally:
        handle.close()

    return content


def main():
    input_file_path = sys.argv[1]

    content = readContent(input_file_path)

    print v2.extract(content)


if __name__ == "__main__":
    main()
