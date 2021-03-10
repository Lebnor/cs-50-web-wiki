from django.shortcuts import render

from . import util
import markdown2


def index(request):
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