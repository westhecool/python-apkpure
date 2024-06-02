import argparse
import main
import re
import os
def make_safe_filename(filename):
    invalid_chars = r'[<>:"/\\|?*]'
    safe_filename = re.sub(invalid_chars, '', filename)
    return safe_filename

args = argparse.ArgumentParser()
args.add_argument("command", choices=["download"])
args.add_argument("id")
args.add_argument("--output-dir", "-d", default=".", help="Output directory")
args.add_argument("--output-file", "-f", default=None, help="Output file name")
args = args.parse_args()

os.makedirs(args.output_dir, exist_ok=True)

if args.command == "download":
    info = main.get_info(args.id)
    print(f"Downloading {info['title']} v{info['versions'][0]['version']}...", end='', flush=True)
    main.download(info["versions"][0]["url"], f"{args.output_dir}/{make_safe_filename(info['title']) if not args.output_file else args.output_file} {'v' + info['versions'][0]['version'] if not args.output_file else ''}.{info['versions'][0]['type'] if not args.output_file else ''}")
    print("done!", flush=True)
