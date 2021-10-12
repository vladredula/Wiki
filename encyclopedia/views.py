from django.core.files import utils
from django.shortcuts import render
from markdown import Markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

from . import util

class EntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class':'form-control col-lg-5 col-md-6'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control col-lg-6 col-md-6'}))
    edit = forms.BooleanField(widget=forms.HiddenInput(), initial=False)

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

            if (util.get_entry(title) is None or form.cleaned_data["edit"] == True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "exist": True,
                    "title": title
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

def edit(request, entry):
    content = util.get_entry(entry)
    title = entry.capitalize()
    
    md = Markdown()

    if content is None:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": "<h1>Entry not found</h1>"
        })
    else:
        form = EntryForm()
        form.fields["title"].initial = entry
        form.fields['title'].widget.attrs['readonly'] = True
        form.fields["content"].initial = content
        form.fields["edit"].initial = True

        return render(request, "encyclopedia/create.html", {
            "form": form,
            "title": form.fields["title"].initial,
            "edit": form.fields["edit"].initial
        })