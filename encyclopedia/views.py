from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if not util.get_entry(title):
        return render(request, "encyclopedia/error.html", {
            "message": "title does not exist"
        })

    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry(title)
    })

def search(request):
    if 'search' in request.GET:
        search_term = request.GET['search']
    
    entries = util.list_entries()
    results = []
    
    for entry in entries:
        if entry.lower().find(search_term.lower()) != -1:
            results.append(entry)
    
    if not results:
        return render(request, "encyclopedia/error.html", {
            "message": "No search results found"
        })
    if len(results) is 1:
        return render(request, "encyclopedia/entry.html", {
            "title": results[0],
            "content": util.get_entry(results[0])
        })
    
    return render(request, "encyclopedia/search.html", {
        "results": results
    })