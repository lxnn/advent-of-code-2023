import os, sys, shutil, pathlib, requests, dotenv

dotenv.load_dotenv()

ROOT = pathlib.Path(__file__).parent
TEMPLATE = ROOT / 'template.py'
TOKEN = os.getenv('TOKEN')

assert TOKEN is not None

def main():
    day = int(sys.argv[1])
    folder = ROOT / f"{day:02}"
    if folder.exists():
        print(f'day {day:02} already exists', file=sys.stderr)
        return 1
    folder.mkdir()
    shutil.copy(TEMPLATE, folder / 'solution.py')
    (folder / 'example').touch()
    (folder / 'input').write_text(get_input(2023, day))
    return 0

def get_input(year: int, day: int) -> str:
    response = requests.get(
        f'https://adventofcode.com/{year}/day/{day}/input',
        cookies=dict(session=TOKEN),
    )
    response.raise_for_status()
    return response.text

if __name__ == '__main__':
    sys.exit(main())