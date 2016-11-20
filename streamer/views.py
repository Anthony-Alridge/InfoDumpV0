from django.shortcuts import render, redirect
from .models import Focus, Links, KeyWords, FileModel
from .forms import UploadForm
from .scraping.wiki import Wiki
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
import os
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
        try:
            foc = user.profile.focus.get(focus=delete_focus)
            user.profile.focus.remove(foc)
        except KeyError:
            #the focus has already been deleted, maybe they reloaded the page.
            pass
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
        links = [str(link_object) for link_object in foc.links.all()]
        if link not in links:
            db_link = Links(links=link)
            db_link.save()
            foc.links.add(db_link)
    if request.POST.get('note'):
        note = request.POST.get('note')
        notes = [str(note_object) for note_object in foc.keywords.all()]
        if note not in notes:
            db_note = KeyWords(keywords=note)
            db_note.save()
            foc.keywords.add(db_note)
    if request.POST.get('delete-note'):
        try:
            delete_note = request.POST.get('delete-note')
            note = KeyWords.objects.get(keywords=delete_note)
            foc.keywords.remove(note)
            note.delete()
        except:
            #user reloaded page so resubmitted delete request
            pass
    if request.POST.get('delete-link'):
        try:
            delete_link = request.POST.get('delete-link')
            link = Links.objects.get(links=delete_link)
            foc.links.remove(link)
            link.delete()
        except:
            #user reloaded page so resubmitted delete request
            pass
    context = {'focus': focus,
               'summary': summary,
               'links': foc.links.all(),
               'notes': foc.keywords.all()
               }
    return render(request, 'streamer/focus.html', context)

@login_required
def uploads(request):
    user_profile = request.user.profile
    focus = request.session['current_focus']
    foc = user_profile.focus.get(focus=focus)
    if request.method =='POST':
        if request.POST.get('delete_file'):
            try:
                delete_file = request.POST.get('delete_file')
                _file = FileModel.objects.get(file_field = delete_file)
                foc.files.remove(_file)
                _file.delete()
            except:
                pass

        else:
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                _file = FileModel(file_field = request.FILES['docfile'])
                _file.save()
                foc.files.add(_file)
            #return HttpResponseRedirect('..')
            #return render(request, 'streamer/uploads.html', {'form':form, 'num':num})
    else:
        form = UploadForm()

    files = foc.files.all()
    navlinks = [{'name':'FocusPage', 'link':'streamer/focusPage'}]
    return render(request, 'streamer/uploads.html', {'form':form, 'files':files, 'navlinks':navlinks})
