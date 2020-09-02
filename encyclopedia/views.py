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