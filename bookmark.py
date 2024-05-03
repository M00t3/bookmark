import os
import subprocess
import time
import argparse


def switch_workspace():
    # Check if i3 or dwm is running and switch workspace
    if subprocess.run(["pgrep", "i3wm"], stdout=subprocess.DEVNULL).returncode == 0:
        subprocess.run(["i3-msg", "workspace", "2"], stdout=subprocess.DEVNULL)
    elif subprocess.run(["pgrep", "dwm"], stdout=subprocess.DEVNULL).returncode == 0:
        subprocess.run(["xdotool", "key", "Super_L+2"], stdout=subprocess.DEVNULL)


def open_site(browser="chromium", file_path=".sites.txt"):

    # Read the file and filter out comments and empty lines
    with open(file_path, "r") as f:
        lines = [
            line.strip()
            for line in f.readlines()
            if not line.startswith("#") and line.strip()
        ]

    # Convert lines to a string with each item on a new line
    lines_str = "\n".join(lines)

    # Use rofi for site selection
    result = subprocess.run(
        ["rofi", "-dmenu", "-i", "-p", "Choose site"],
        input=lines_str,
        text=True,
        capture_output=True,
    )

    # The selected line is in result.stdout
    name = result.stdout.strip()

    if not name in lines:
        exit()

    # Open the site in the browser
    subprocess.run([browser, name])

    time.sleep(0.3)
    switch_workspace()


def open_important_site(browser="chromium", important_site="./.important_site.txt"):

    # Define the help_script function
    def help_script():
        with open(important_site, "r") as file:
            content = file.read()
        subprocess.run(
            [
                "notify-send",
                "-t",
                "30000",
                "-u",
                "low",
                "{abbreviation} {search for}",
                content,
            ]
        )
        print("{abbreviation} {search for}", content)

    # Define the open_site function
    def open_site(site):
        is_browser_up = subprocess.run(
            ["pgrep", browser], stdout=subprocess.DEVNULL
        ).returncode

        if is_browser_up != 0:
            subprocess.Popen(
                [browser], start_new_session=True, stdout=subprocess.DEVNULL
            )
            time.sleep(2.5)

        subprocess.Popen(
            [browser, site], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )

    # Use rofi for site selection
    input = subprocess.run(
        ["rofi", "-dmenu", "-i", "-p", "Search to: "],
        text=True,
        capture_output=True,
    )
    inputs = input.stdout.strip().split()

    if inputs:
        # The first part of the input, usually the command or site name
        first_part = inputs[0]

        # If there are two parts in the input, the second part is considered as the search term
        if len(inputs) == 2:
            search_to = " ".join(inputs[1:])

        else:
            search_to = None

        # Open the file containing important sites
        with open(important_site, "r") as file:
            lines = file.readlines()
        # Find the site name that starts with the first part of the input
        site_name = next(
            (line.split()[1] for line in lines if line.startswith(first_part)), None
        )

        site_dict = {
            "dj": f"https://docs.djangoproject.com/en/5.0/search//?q={search_to}",
            "db": f"https://wiki.debian.org/?action=fullsearch&value={search_to}",
            "ar": f"https://wiki.archlinux.org/index.php?search={search_to}",
            "yt": f"https://www.youtube.com/results?search_query={search_to}",
            "gt": f"https://github.com/search?q={search_to}&type=Repositories",
            "vi": f"https://vim.fandom.com/wiki/Special:Search?query={search_to}&scope=internal&contentType=&ns%5B0%5D=0",
            "chg": f"https://cheatography.com/explore/search/?q={search_to}",
        }

        if first_part in site_dict and search_to:
            open_site(site_dict[first_part])
        elif first_part not in site_dict and site_name and search_to:
            open_site(
                f"https://www.startpage.com/sp/search?query=site:{site_name} {search_to}"
            )
        elif site_name and not search_to and site_name:
            open_site(site_name)

        else:
            subprocess.run(
                [
                    "notify-send",
                    "-t",
                    "2000",
                    "-u",
                    "critical",
                    "search to site",
                    "error",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            help_script()


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

    # Set the browser and file path
    browser = "chromium"
    file_path = f"{script_dir}/.sites.txt"
    important_site_file = f"{script_dir}/.important_site.txt"

    parser = argparse.ArgumentParser(description="Open bookmark sites")

    parser.add_argument(
        "-i", "--important-site", action="store_true", help="Open important site"
    )
    parser.add_argument("-o", "--open-site", action="store_true", help="Open site")

    args = parser.parse_args()

    if args.important_site:
        open_important_site(browser, important_site_file)
    elif args.open_site:
        open_site(browser, file_path)
    else:
        print("No flags passed !")
        parser.print_help()
