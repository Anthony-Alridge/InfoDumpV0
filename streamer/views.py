from django.shortcuts import render, redirect
from .models import Focus, Links, KeyWords
from .scraping.wiki import Wiki
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
#import pdb

@login_required
def user_page(request):
    focus_request = request.POST.get('focus')
    delete_focus = request.POST.get('delete_focus')
    log_out_request = request.POST.get('log_out_request')
    user = request.user
    if log_out_request:
        logout(request)
        return redirect(reverse('home:home_page'))
    if focus_request:
        f1 = Focus(focus=focus_request)
        f1.save()
        user.profile.focus.add(f1)
    if delete_focus:
        foc = user.profile.focus.get(focus=delete_focus)
        user.profile.focus.remove(foc)
    context = {'focus_list': request.user.profile.focus.all()}
    return render(request, 'streamer/user_page.html', context)

@login_required
def focus_page(request):
    user_profile  = request.user.profile
    if request.POST.get('log_out_request'):
        log_out_request = request.POST.get('log_out_request')
        logout(request)
        return redirect(reverse('home:home_page'))
    if request.POST.get('focus_query'):
        #a user just came here from user page
        focus = request.POST.get('focus_query')
        foc = user_profile.focus.get(focus=focus)
        summary = Wiki(focus).summarise()
        request.session['current_focus'] = focus
    else:
        #a user did some action on the page and we need to know
        #what focus we need to return
        focus = request.session['current_focus']
        foc = user_profile.focus.get(focus=focus)
        #the wikipedia api handles caching so we'll just call summarise again
        #without caching ourselves.
        summary = Wiki(focus).summarise()
    if request.POST.get('link'):
        link = request.POST.get('link')
        db_link = Links(links=link)
        db_link.save()
        foc.links.add(db_link)
    if request.POST.get('note'):
        note = request.POST.get('note')
        db_note = KeyWords(keywords=note)
        db_note.save()
        foc.keywords.add(db_note)
    if request.POST.get('delete-note'):
        delete_note = request.POST.get('delete-note')
        note = KeyWords.objects.get(keywords=delete_note)
        foc.keywords.remove(note)
        note.delete()
    if request.POST.get('delete-link'):
        delete_link = request.POST.get('delete-link')
        link = Links.objects.get(links=delete_link)
        foc.links.remove(link)
        link.delete()
    context = {'focus': focus,
               'summary': summary,
               'links': foc.links.all(),
               'notes': foc.keywords.all()
               }
    return render(request, 'streamer/focus.html', context)
