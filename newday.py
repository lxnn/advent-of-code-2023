import sys, shutil, pathlib

ROOT = pathlib.Path(__file__).parent
TEMPLATE = ROOT / 'template.py'

def main():
    day = int(sys.argv[1])
    folder = ROOT / f"{day:02}"
    if folder.exists():
        print(f'day {day:02} already exists', file=sys.stderr)
        return 1
    folder.mkdir()
    shutil.copy(TEMPLATE, folder / 'solution.py')
    (folder / 'example').touch()
    return 0

if __name__ == '__main__':
    sys.exit(main())