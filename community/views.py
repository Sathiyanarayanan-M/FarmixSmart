from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

from .models import Document
from .forms import DocumentForm

@login_required
def feed(request):
    form = DocumentForm()
    documents = Document.objects.all()
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, "feed.html", {"documents": documents, "form": form})
    else:
        return render(request, "feed.html", {"form": form, "documents": documents})
