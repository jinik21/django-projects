from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import util
from markdown2 import Markdown
from django import forms
import random

class Search(forms.Form):
    q= forms.CharField(max_length=100)
class Entry(forms.Form):
    title = forms.CharField(label= "Title")
    content = forms.CharField(widget=forms.Textarea(), label='Content')
class Edit(forms.Form):
    content = forms.CharField(widget=forms.Textarea(), label='Content')

markdowner = Markdown()

def index(request):
    if request.method=='POST':
        form = Search(request.POST)
        if form.is_valid():
            entries=util.list_entries()
            title=form.cleaned_data["q"]
            if title in entries:
                return redirect(f'/wiki/{title}')
            else:
                search_entry=[]
                for entry in entries:
                    if entry.find(title)!=-1:
                        search_entry.append(entry)
                if len(search_entry)==0:
                    return render(request, "encyclopedia/message.html",{
                        'title':"Results",
                        'Message_head':"No Matching Results Found."
                    })
                else:
                    return render(request, "encyclopedia/results.html", {"entries": search_entry})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def name(request,name):
    entries=util.list_entries()
    if request.method=='POST':
        form = Search(request.POST)
        search_entry=[]
        if form.is_valid():
            title=form.cleaned_data["q"]
            if title in entries:
                return redirect(f'/wiki/{title}')
            else:
                for entry in entries:
                    if entry.find(title)!=-1:
                        search_entry.append(entry)
                if len(search_entry)==0:
                    return render(request, "encyclopedia/message.html",{
                        'title':"Results",
                        'Message_head':"No Matching Results Found."})
                else:
                    return render(request, "encyclopedia/results.html", {"entries": search_entry})
    else:    
        if name in entries:
            return render(request,"encyclopedia/page.html",{
                "name":name,
                "entry": markdowner.convert(util.get_entry(name))
            })
        else:
            return render(request,"encyclopedia/message.html",{
                'title':'Error',
                'Message_head':"Error 404",
                'Message':"Page Not Found"
            })

def Random_Page(request):
    entries=util.list_entries()
    page_num=random.randint(0, len(entries) - 1)
    name=entries[page_num]
    return redirect(f'/wiki/{name}')

def Create_page(request):
    entries=util.list_entries()
    if request.method=='POST':
        form = Search(request.POST)
        if form.is_valid():
            entries=util.list_entries()
            title=form.cleaned_data["q"]
            if title in entries:
                return redirect(f'/wiki/{title}')
            else:
                search_entry=[]
                for entry in entries:
                    if entry.find(title)!=-1:
                        search_entry.append(entry)
                if len(search_entry)==0:
                    return render(request, "encyclopedia/message.html",{
                        'title':"Results",
                        'Message_head':"No Matching Results Found."
                    })

                else:
                    return render(request, "encyclopedia/results.html", {"entries": search_entry})
        form_markdown=Entry(request.POST)
        if form_markdown.is_valid():
            title=form_markdown.cleaned_data["title"].capitalize()
            content=form_markdown.cleaned_data["content"]
            if title in entries:
                return render(request, "encyclopedia/message.html",{
                    'title':"Already Exists",
                    'Message_head':"Title already exists"
                })
            util.save_entry(title,content)
            return redirect(f'/wiki/{title}')
    else:
        return render(request,"encyclopedia/create.html",{
            'form':Entry()
        })

def edit(request,name):
    title=name
    contents=util.get_entry(title)
    entries=util.list_entries()
    if request.method=='GET':
        return render(request,"encyclopedia/edit.html",{
            'form':Edit(initial={'content': contents}),
            'name':title
        })
    else:
        form = Search(request.POST)
        if form.is_valid():
            entries=util.list_entries()
            title=form.cleaned_data["q"]
            if title in entries:
                return redirect(f'/wiki/{title}')
            else:
                search_entry=[]
                for entry in entries:
                    if entry.find(title)!=-1:
                        search_entry.append(entry)
                if len(search_entry)==0:
                    return render(request, "encyclopedia/message.html",{
                        'title':"Results",
                        'Message_head':"No Matching Results Found."
                    })
                else:
                    return render(request, "encyclopedia/results.html", {"entries": search_entry})
        form_markdown=Edit(request.POST)
        if form_markdown.is_valid():
            content=form_markdown.cleaned_data["content"]
            util.save_entry(title,content)
            return redirect(f'/wiki/{title}')


def Error(request):
   entries=util.list_entries()
   if request.method=='POST':
       form = Search(request.POST)
       if form.is_valid():
           title=form.cleaned_data["q"]
           if title in entries:
               return redirect(f'/wiki/{title}')
           else:
               return render(request,"encyclopedia/error.html",{'name':title})
   else:
        return render(request,"encyclopedia/error.html",{'name':name})