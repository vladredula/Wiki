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

def search(request):
    if request.method == "POST":
        entries = util.list_entries()
        found = []

        query = request.POST["query"]

        for entry in entries:
            if query.lower() == entry.lower():
                content = util.get_entry(entry)
                md = Markdown()

                return render(request, "encyclopedia/entry.html", {
                    "title": entry,
                    "entry": md.convert(content)
                })
            elif query.lower() in entry.lower():
                found.append(entry)
        
        return render(request, "encyclopedia/index.html", {
            "entries": found
        })