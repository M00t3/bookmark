sites_dict = lambda query: {
    "dj": f"https://docs.djangoproject.com/en/5.0/search//?q={query}",
    "db": f"https://wiki.debian.org/?action=fullsearch&value={query}",
    "ar": f"https://wiki.archlinux.org/index.php?search={query}",
    "yt": f"https://www.youtube.com/results?search_query={query}",
    "gt": f"https://github.com/search?q={query}&type=Repositories",
    "vi": f"https://vim.fandom.com/wiki/Special:Search?query={query}&scope=internal&contentType=&ns%5B0%5D=0",
    "chg": f"https://cheatography.com/explore/search/?q={query}",
}
