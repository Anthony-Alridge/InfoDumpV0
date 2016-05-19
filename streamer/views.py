from django.shortcuts import render, redirect
from .models import Focus, Links, KeyWords
from .scraping.wiki import Wiki
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
#import pdb

# Create your views here.
@login_required
def user_page(request):
    focus_request = request.POST.get('query')
    delete_focus = request.POST.get('delete_focus')
    log_out_request = request.POST.get('log_out_request')
    user = request.user
    if focus_request:
        f1 = Focus(focus=focus_request)
        f1.save()
        user.profile.focus.add(f1)
    if delete_focus:
        foc = user.profile.focus.get(focus=delete_focus)
        user.profile.focus.remove(foc)
    if log_out_request:
        logout(request)
        return redirect(reverse('home:home_page'))
    context = {'focus_list': request.user.profile.focus.all()}
    return render(request, 'streamer/user_page.html', context)

@login_required
def focus_page(request):
    #pdb.set_trace() //for debugging
    #we should not allow duplicate links to be added to database
    focus = request.POST.get('focus_query')
    link = request.POST.get('link')
    keyword = request.POST.get('keyword')
    delete_note = request.POST.get('delete-note')
    delete_link =request.POST.get('delete-link')
    user_profile  = request.user.profile
    foc = user_profile.focus.get(focus=focus)
    log_out_request = request.POST.get('log_out_request')
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
    if log_out_request:
        logout(request)
        return redirect(reverse('home:home_page'))
    context = {'focus': focus,
               'summary': summary,
               'links': foc.links.all(),
               'keywords': foc.keywords.all()
               }
    return render(request, 'streamer/focus.html', context)
