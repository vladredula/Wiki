from django.shortcuts import render
from markdown import Markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    content = util.get_entry(entry)

    return render(request, "encyclopedia/entry.html", {
        "title": entry.capitalize(),
        "entry": Markdown.convert(content)
    })