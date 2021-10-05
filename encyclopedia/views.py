from django.shortcuts import render
from markdown import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    content = util.get_entry(entry)
    title = entry.capitalize()
    
    md = Markdown()

    if content is None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": "<h1>Entry not found</h1>"
        })

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": md.convert(content)
    })