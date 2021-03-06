import random
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
import markdown
from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="New Title")
    content = forms.CharField(label="Adding Content", widget=forms.Textarea)


entries = util.list_entries()

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):

    result = util.get_entry(title)
    if result:
        entry = util.get_entry(title)
        #html = markdown.markdown(entry)
        md = markdown.Markdown()
        html = md.convert(entry)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": html
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": None
        })
        

def search(request):
    newEntriesList = []
    if request.method == "GET":
        title = request.GET.get('q')
        for newEntry in entries :
            if newEntry == util.get_entry(title):
                return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": util.get_entry(title)
            })

        for searchItem in entries:
            if title in searchItem:
                newEntriesList.append(searchItem),
    return render(request, "encyclopedia/index.html", {
        "entries": newEntriesList
    })

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            newEntry = util.save_entry(title, content)
            if newEntry:
                try:
                    entries.append(newEntry)
                    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
                finally:
                    return HttpResponseRedirect(reverse("encyclopedia:entry", args=[None]))
            else:
                return render(request, "encyclopedia/entry.html", {
                    "entry": None
                })

    return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm()
    }) 


def edit(request, title):
    if request.method =="POST":
        newContent = request.POST['content']
        newEntry = util.edit_entry(title, newContent)
        if newEntry:
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[title]))
        else:
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=[None]))
    else:
        return render(request, "encyclopedia/edit.html", {
        "title": title,
        "entry": util.get_entry(title)
        })

def random_entry(request):
    title = random.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": util.get_entry(title)
        })

