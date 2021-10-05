from django.shortcuts import render
from markdown import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search": False
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

        query = request.POST["q"].lower()

        if util.get_entry(query) is not None:
            return HttpResponseRedirect(reverse("entry", kwargs={'entry': query}))

        for entry in entries:
            if query in entry.lower():
                found.append(entry)
        
        return render(request, "encyclopedia/index.html", {
            "entries": found,
            "search": True,
            "query": query
        })