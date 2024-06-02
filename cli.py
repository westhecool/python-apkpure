import argparse
import main
import re
def make_safe_filename(filename):
    invalid_chars = r'[<>:"/\\|?*]'
    safe_filename = re.sub(invalid_chars, '', filename)
    return safe_filename

args = argparse.ArgumentParser()
args.add_argument("command", choices=["download"])
args.add_argument("id")
args = args.parse_args()

if args.command == "download":
    info = main.get_info(args.id)
    print(f"Downloading {info['title']} v{info['versions'][0]['version']}...", end='')
    main.download(info["versions"][0]["url"], f"./{make_safe_filename(info['title'])} v{info['versions'][0]['version']}.{info['versions'][0]['type']}")
    print("done!")
