try:
    from urllib import quote_plus #python 2
except:
    pass

try:
    from urllib.parse import quote_plus #python 3
except: 
    pass

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment

from .forms import PostForm
from .models import Post

@login_required
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
        
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        instance      = form.save(commit=False)
        instance.user = request.user
        instance.save()
        # message success
        messages.success(request, "Creación correcta!")
        return HttpResponseRedirect(instance.get_absolute_url())
    
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)

'''
 Created for Django Code Review
'''

from django.views.generic import DetailView

class PostDetailView(DetailView):
    template_name = 'post_detail.html' 
    
    def get_object(self, *args, **kwargs):
        slug    = self.kwargs.get("slug")
        instance= get_object_or_404(Post, slug=slug)
        
        if instance.publish > timezone.now().date() or instance.draft:
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                raise Http404
        return instance
    
    def get_context_data(self, *args, **kwargs):
        context                = super(PostDetailView, self).get_context_data(*args, **kwargs)
        instance               = context['object']
        context['share_string']= quote_plus(instance.content)

        return context
    
# in urls.py --> PostDetailView.as_view() instead of post_detail


def post_detail(request, slug=None):
    #instance = get_object_or_404(Post, slug=slug)
    try:
        instance = Post.objects.get(slug=slug)
    except:
        raise Http404

    if instance.publish > timezone.now().date() or instance.draft:
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404

    share_string      = quote_plus(instance.content)
    initial_data      = {
        "content_type": instance.get_content_type,
        "object_id"   : instance.id,
    }

    form = CommentForm(request.POST or None, initial=initial_data)

    if form.is_valid() and request.user.is_authenticated:
        c_type      = form.cleaned_data.get("content_type")
        content_type= ContentType.objects.get(model=c_type)
        obj_id      = form.cleaned_data.get("object_id")
        content_data= form.cleaned_data.get("content")
        parent_obj  = None

        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_id = None

        if parent_id:
            parent_qs = Comment.objects.filter(id=parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj = parent_qs.first()

        new_comment, created = Comment.objects.get_or_create(
                                    user        = request.user,
                                    content_type= content_type,
                                    object_id   = obj_id,
                                    content     = content_data,
                                    parent      = parent_obj
                                )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    comments = instance.comments #Comment.objects.filter_by_instance(instance)

    context = {
        "title"       : instance.title,
        "object"      : instance,
        "share_string": share_string,
        "comments"    : comments,
        "comment_form": form,
    }
    return render(request, "post_detail.html", context)

def post_list(request):
    today        = timezone.now().date()
    queryset_list= Post.objects.active() #.order_by("-timestamp")

    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()

    paginator       = Paginator(queryset_list, 8) # Show 25 contacts per page
    page_request_var= "page"
    page            = request.GET.get(page_request_var)

    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)


    context = {
        "object_list"     : queryset, 
        "title"           : "Blog cíclica itinerante",
        "page_request_var": page_request_var,
        "today"           : today,
    }
    return render(request, "post_list.html", context)

@login_required
def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance= get_object_or_404(Post, slug=slug)
    form    = PostForm(request.POST or None, request.FILES or None, instance=instance)

    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Se actualizó el siguiente <a href='#' class='alert-link'>Ítem</a>", extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title"   : instance.title,
        "instance": instance,
        "form"    : form,
    }
    return render(request, "post_form.html", context)


@login_required
def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    try:
        obj = Post.objects.get(slug=slug)
    except:
        raise Http404

    if obj.user != request.user:
        response = HttpResponse("No tienes permiso para eliminar este Post.")
        response.status_code = 403
        return response

    if request.method == "POST":
        obj.delete()
        messages.success(request, "El post fue eliminado.")
        return redirect("posts:list")

    context = {
        "object": obj,
        "title_post": obj.title,
    }
    return render(request, "confirm_delete.html", context)


    # #instance = get_object_or_404(Post, slug=slug)
    # instance.delete()
    # messages.success(request, "Eliminación completa")
    # return redirect("posts:list")

