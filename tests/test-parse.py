# test parse.py 
import parse

def main():

    # get some data from tests/data, load it and parse it
    fname = "test/data/test-multiple-documents.nc"
    parse.parse(fname)


if __name__ == "__main__":
    main()