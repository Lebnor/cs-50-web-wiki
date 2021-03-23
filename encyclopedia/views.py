from django.shortcuts import render

from django import forms
from . import util
import markdown2
import numpy as np


class SearchForm(forms.Form):
    q = forms.CharField(label="q")

class EntryForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(label="content")

# home page
def index(request):
    entries = util.list_entries()
    if (request.method == "POST"):
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['q']
            entry = util.get_entry(search.lower())
            if not entry:
                terms = []
                for term in entries:
                    term = term.lower()
                    search_key = search.lower()
                    if search_key in term:
                        terms.append(term)
                    if term in search_key:
                        terms.append(term)
                
                return render(request, "encyclopedia/search.html", {
                    "search": search,
                    "terms": terms,
                    "entries": entries,
                    "exists": False
                })
            else:
                html = markdown2.markdown(entry)
            return render(request, "encyclopedia/entry_page.html", {
                "title": search.capitalize(),
                "html": html,
                "entries": entries,
                "exists": True
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "title": search.capitalize(),
            })

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

# display an entry
def entry_page(request, entry):
    entry_exists = util.get_entry(entry)
    if not entry_exists:
        # display to user that this entry does not exist
        # html = "<h1>This entry does not exist!</h1>"
        return render(request, "encyclopedia/entry_page.html", {
            "title": entry.capitalize(),
            "entries": util.list_entries(),
            "exists": False
        })
    else:
        # display HTML content from this .md entry
        html = markdown2.markdown(entry_exists)

    return render(request, "encyclopedia/entry_page.html", {
        "title": entry.capitalize(),
        "html": html,
        "entries": util.list_entries(),
        "exists": True
    })

# edit an existing entry
def edit(request, title):
    # user submitted an edit
    if (request.method == "POST"):
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            html = markdown2.markdown(content)
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry_page.html", {
                "title": title.capitalize(),
                "html": html,
                "entries": util.list_entries(),
                "exists": True
            })
    
    # load the form to edit an entry
    content = util.get_entry(title)
    return render(request, "encyclopedia/new.html", {
        "entries": util.list_entries(),
        "title": title,
        "content": content,
        "edit": True
    })

# add a new entry to the list
def new(request):
    entries = util.list_entries()

    if (request.method == "POST"):
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title'].lower()

            # the entry already exists
            if title in entries:
                html = "<h1 class='text-danger'> This title already exists.</h1>"
                html += "<p class='text-center fs-light text-danger'> Please select it from the sidebar</p>"
                
                return render(request, "encyclopedia/entry_page.html", {
                    "title": title.capitalize(),
                    "html": html,
                    "entries": entries
                })

            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry_page.html", {
            "title": title.capitalize(),
            "html": content,
            "entries": entries,
            "exists": True
        })

    return render(request, "encyclopedia/new.html", {
        "entries": entries
    })

# load a random entry's page
def random(request):

    choice = np.random.choice(util.list_entries(), 1)[0]
    return entry_page(request, choice)