from django.shortcuts import render

from django import forms
from . import util
import markdown2


class SearchForm(forms.Form):
    q = forms.CharField(label="q")

def index(request):
    if (request.method == "POST"):
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['q']
            entry = util.get_entry(search.lower())
            if not entry:
                # TODO in new page show available results
                terms = []
                for term in util.list_entries():
                    term = term.lower()
                    search_key = search.lower()
                    if search_key in term:
                        terms.append(term)
                    if term in search_key:
                        terms.append(term)
                
                print(terms)
                return render(request, "encyclopedia/search.html", {
                    "search": search,
                    "terms": terms,
                    "entries": util.list_entries()
                })
            else:
                html = markdown2.markdown(entry)
            print(html, entry, form)
            return render(request, "encyclopedia/entry_page.html", {
                "title": search.capitalize(),
                "html": html,
                "entries": util.list_entries()
            })
        else:
            return render(request, "encyclopedia/index.html", {
                "title": search.capitalize(),
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entry):
    entry_exists = util.get_entry(entry)
    if not entry_exists:
        # display to user that this entry does not exist
        html = "<h1>This entry does not exist!</h1>"
    else:
        # display HTML content from this .md entry
        html = markdown2.markdown(entry_exists)

    
    
    return render(request, "encyclopedia/entry_page.html", {
        "title": entry.capitalize(),
        "html": html,
        "entries": util.list_entries()
    })

# searching for an entry
def search(request):
    if (request.method == "POST"):
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data['q']
            entry = util.get_entry(search)
            html = markdown2.markdown(entry)
            return render(request, "encyclopedia/index.html", {
                "title": request.POST.dict().get('q'),
                "html": html
            })