import os.path

SCRIPT_DIR = os.path.dirname(os.path.relpath(__file__))


def main() -> None:
    with open(f'{SCRIPT_DIR}/input.txt', 'r') as f:
        for line in f.readlines():
            print(line.strip())


if __name__ == "__main__":
    main()
