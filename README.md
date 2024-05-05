# Bookmark Manager

This is a Python script that helps you manage and open your bookmarked websites.
It uses `rofi` for site selection and can open sites in your preferred browser.
It also supports switching workspaces in `i3wm` or `dwm` window managers.

## Features

- Open a bookmarked site from a list
- Open an important site
- Switch workspace after opening a site (for `i3wm` or `dwm` users)
- Search functionality for important sites

## Requirements

- `rofi`

## Usage

First, clone the repository and navigate to the project directory:

```bash
git clone https://github.com/mooteee/bookmark.git
cd bookmark-manager
```

To open a bookmarked site:

```bash
python bookmark.py --open-site
```

To open an important site:

```bash
python bookmark.py --important-site
```

## Configuration

You can customize the script to suit your needs by modifying the `.sites.txt` and `.important_site.txt` files. These files contain the list of bookmarked and important sites respectively.

## TODO

- [x] add config file for customizing the script
- [ ] way to add sites to the list
- [ ] way to remove sites from the list
- [ ] add config file for quick search links

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

These script is licensed under the GPL3 License - see the [LICENSE.txt](LICENSE.txt) file for details.
