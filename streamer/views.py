from django.shortcuts import render
from .models import Focus, Links, KeyWords
from .scraping.wiki import Wiki
#import pdb

# Create your views here.
def user_page(request):
    focus_request = request.POST.get('query')
    if focus_request:
        f1 = Focus(focus=focus_request)
        f1.save()
    context = {'focus_list': Focus.objects.all()}
    return render(request, 'streamer/user_page.html', context)


def focus_page(request):
    #pdb.set_trace() //for debugging
    #we should not allow duplicate links to be added to database
    focus = request.POST.get('focus_query')
    link = request.POST.get('link')
    keyword = request.POST.get('keyword')
    delete_note = request.POST.get('delete-note')
    delete_link =request.POST.get('delete-link')
    foc = Focus.objects.get(focus=focus)
    if focus:
        summary = Wiki(focus).summarise()
    if link:
        db_link = Links(links=link)
        db_link.save()
        foc.links.add(db_link)
    if keyword:
        db_kw = KeyWords(keywords=keyword)
        db_kw.save()
        foc.keywords.add(db_kw)
    if delete_note:
        note = KeyWords.objects.get(keywords=delete_note)
        foc.keywords.remove(note)
        note.delete()
    if delete_link:
        link = Links.objects.get(links=delete_link)
        foc.links.remove(link)
        link.delete()
    context = {'focus': focus,
               'summary': summary,
               'links': foc.links.all(),
               'keywords': foc.keywords.all()
               }
    return render(request, 'streamer/focus.html', context)
