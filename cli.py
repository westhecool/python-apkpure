import argparse
import main

args = argparse.ArgumentParser()
args.add_argument("command", choices=["download"])
args.add_argument("id")
args = args.parse_args()

if args.command == "download":
    info = main.get_info(args.id)
    print(f"Downloading {info['title']} v{info['versions'][0]['version']}...")
    main.download(info["versions"][0]["url"], f"./{args.id} v{info['versions'][0]['version']}.{info['versions'][0]['type']}")
