import os
import sys


def main():
    try:
        __file__
    except NameError:
        this_file = os.path.abspath(sys.argv[0])
    else:
        this_file = os.path.abspath(__file__)
    test_dir = os.path.join(os.path.dirname(this_file), "test")
    sys.path.insert(0, test_dir)
    try:
        import warnings
    except ImportError:
        pass
    else:
        warnings.filterwarnings(
            action="ignore", message="import \* only allowed at module level")
    execfile(os.path.join(test_dir, "test_clientform.py"))


if __name__ == "__main__":
    main()
