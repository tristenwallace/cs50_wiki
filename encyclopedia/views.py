from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
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

class AddPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")

def add(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new-page.html", {
            "form": AddPageForm()
        })

    if request.method == "POST":
        form = AddPageForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            
            for entry in entries:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/error.html", {
                        "message": "Wiki page already exits"
                    })
            util.save_entry(title, content)
            
            return HttpResponseRedirect(reverse("index"))
    