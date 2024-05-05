import os
import subprocess
import time
import platform

import argparse
import configparser

from quick_search_config import sites_dict

# read config file
config = configparser.ConfigParser()
config.read("config.ini")

browser = config["open_link"].get("browser", fallback="chromium")
default_flag = config["default"].get("default_flag")
use_rofi = config["default"].getboolean("use_rofi", fallback=True)
dwm_workspace = config["default"].get("dwm_workspace", fallback="2")
i3wm_workspace = config["default"].get("i3wm_workspace", fallback="2")


def switch_workspace(dwm_workspace="2", i3wm_workspace="2"):
    # Check if the operating system is Linux
    if platform.system() != "Linux":
        return

    # Check if i3 or dwm is running and switch workspace
    if subprocess.run(["pgrep", "i3wm"], stdout=subprocess.DEVNULL).returncode == 0:
        subprocess.run(
            ["i3-msg", "workspace", i3wm_workspace], stdout=subprocess.DEVNULL
        )
    elif subprocess.run(["pgrep", "dwm"], stdout=subprocess.DEVNULL).returncode == 0:
        subprocess.run(
            ["xdotool", "key", f"Super_L+{dwm_workspace}" ], stdout=subprocess.DEVNULL
        )


def open_site(use_rofi, browser, file_path=".sites.txt"):
    def select_site(lines, use_rofi):
        if use_rofi:
            # Use rofi for site selection
            selected_site = subprocess.run(
                ["rofi", "-dmenu", "-i", "-p", "Choose site"],
                input=lines,
                text=True,
                capture_output=True,
            )

            return selected_site.stdout.strip()
        else:
            # Run fzf and pass the sites to it through the standard input
            process = subprocess.Popen(
                ["fzf"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
            )

            # Send the sites to fzf and get the selected site
            selected_site, _ = process.communicate(lines)

            return selected_site.split()

    # Read the file and filter out comments and empty lines
    with open(file_path, "r") as f:
        lines = [
            line.strip()
            for line in f.readlines()
            if not line.startswith("#") and line.strip()
        ]

    # Convert lines to a string with each item on a new line
    lines_str = "\n".join(lines)

    # The selected line is in result.stdout
    site = select_site(use_rofi=use_rofi, lines=lines_str)

    if not site in lines:
        exit()

    # Open the site in the browser
    subprocess.run([browser, site])

    time.sleep(0.3)
    switch_workspace(i3wm_workspace=i3wm_workspace, dwm_workspace=dwm_workspace)


def quick_search(use_rofi, browser, important_site="./.important_site.txt"):

    def get_site(use_rofi):
        if use_rofi:
            # Use rofi for site selection
            search_query = subprocess.run(
                ["rofi", "-dmenu", "-i", "-p", "Search to: "],
                text=True,
                capture_output=True,
            )
            return search_query.stdout.strip().split()
        else:
            search_query = input("Search to: ")
        return search_query.split()

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
    def open_with_browser(site):
        # TODO: handle this in windows
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

    inputs = get_site(use_rofi=use_rofi)

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

        sites = sites_dict(search_to)
        if first_part in sites and search_to:
            open_with_browser(sites[first_part])
        elif first_part not in sites and site_name and search_to:
            open_with_browser(
                f"https://www.startpage.com/sp/search?query=site:{site_name} {search_to}"
            )
        elif site_name and not search_to and site_name:
            open_with_browser(site_name)

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
            return

        time.sleep(0.3)
        switch_workspace(i3wm_workspace=i3wm_workspace, dwm_workspace=dwm_workspace)
        

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_dir)

    sites_file = f"{script_dir}/.sites.txt"
    important_site_file = f"{script_dir}/.important_site.txt"

    parser = argparse.ArgumentParser(description="Open bookmark sites")

    parser.add_argument(
        "-i", "--important-site", action="store_true", help="Open important site"
    )
    parser.add_argument("-o", "--open-site", action="store_true", help="Open site")

    args = parser.parse_args()

    if args.important_site:
        quick_search(use_rofi, browser, important_site_file)
    elif args.open_site:
        open_site(use_rofi, browser, sites_file)
    elif default_flag:
        if default_flag == "important":
            quick_search(use_rofi, browser, important_site_file)
        elif default_flag == "open-site":
            print(default_flag)
            open_site(use_rofi, browser, sites_file)
    else:
        print("No flags passed !")
        parser.print_help()
