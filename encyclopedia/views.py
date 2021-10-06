from django.core.files import utils
from django.shortcuts import render
from markdown import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

class EntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

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
    entries = util.list_entries()

    query = request.POST["q"].lower()

    if util.get_entry(query) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': query}))

    found = []
    for entry in entries:
        if query in entry.lower():
            found.append(entry)
    
    return render(request, "encyclopedia/index.html", {
        "entries": found,
        "search": True,
        "query": query
    })

def create(request):
    if request.method == "POST":
        form = EntryForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "exist": True
                })
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form,
                "exist": False
            })

    return render(request, "encyclopedia/create.html", {
        "form": EntryForm(),
        "exist": False
    })