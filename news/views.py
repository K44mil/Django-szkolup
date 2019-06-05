from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Post, Author, PostComment, PostRate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import PostForm
# Create your views here.

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def searchPostResult(request):


    posts_list = Post.objects.all()
    context = {}
    query = request.GET.get('q')

    if query:
        queryset = posts_list.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()


        paginator = Paginator(queryset, 9)
        page_request_var = 'page'
        page = request.GET.get(page_request_var)

        try:
            paginated_queryset = paginator.page(page)
        except PageNotAnInteger:
            paginated_queryset = paginator.page(1)
        except EmptyPage:
            paginated_queryset = paginator.page(paginator.num_pages)


        context = {
            'queryset': paginated_queryset,
            'page_request_var': page_request_var,
            'q': query,
        }

    if not request.user.is_staff and not request.user.is_anonymous:
        if request.user.isProfilEdited == False:
            if request.user.role == 0:
                return redirect('/editStudentProfile')
            elif request.user.role == 1:
                return redirect('/editCompanyProfile')

    return render(request, 'searchPostResult.html', context)

def index(request):
    posts_list = Post.objects.filter(featured=True).order_by('-timestamp')[0:3]

    context = {
        'posts_list': posts_list,
    }

    if not request.user.is_staff and not request.user.is_anonymous:
        if request.user.isProfilEdited == False:
            if request.user.role == 0:
                return redirect('/editStudentProfile')
            elif request.user.role == 1:
                return redirect('/editCompanyProfile')

    return render(request, 'index.html', context)

def news(request):
    posts_list = Post.objects.all()

    paginator = Paginator(posts_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_posts_list = paginator.page(page)
    except PageNotAnInteger:
        paginated_posts_list = paginator.page(1)
    except EmptyPage:
        paginated_posts_list = paginator.page(paginator.num_pages)

    context = {
        'posts_list': paginated_posts_list,
        'page_request_var': page_request_var,
    }

    if not request.user.is_staff and not request.user.is_anonymous:
        if request.user.isProfilEdited == False:
            if request.user.role == 0:
                return redirect('/editStudentProfile')
            elif request.user.role == 1:
                return redirect('/editCompanyProfile')

    return render(request, 'news.html', context)

def post(request, id):

    post = get_object_or_404(Post, id=id)
    latest_post = Post.objects.order_by('-timestamp')[0:3]

    if request.method == 'POST':
        if request.POST['submit'] == 'addComment':
            commentAuthorName = request.POST['username']
            commentAuthorEmail = request.POST['useremail']
            commentContent = request.POST['comment']

            newComment = PostComment.objects.create(
                author_name=commentAuthorName,
                author_email=commentAuthorEmail,
                content=commentContent,
                post=post,
            )

            newComment.save()
            post.comment_count = post.comment_count + 1
            post.save()

    comments = PostComment.objects.filter(post=post)

    #Ocena artykułu
    sumRate = 0;
    post_rates = PostRate.objects.filter(post=post)

    if not post_rates:
        post_rate = '-'
    else:
        myPost_rates = iter(post_rates)
        for i in myPost_rates:
            sumRate += i.value

        post_rate = sumRate/post_rates.count()

    msg = ''

    if request.method == 'POST':
        if request.POST['submit'] == 'addRate':
            try:
                rate = request.POST['rate']
            except:
                rate = ''

            if rate == '' or rate is None:
                msg = ''
            else:
                rateExists = PostRate.objects.filter(post=post, user=request.user)

                if rateExists:
                    msg = 'Już oceniłeś ten artykuł.'
                else:
                    rateObj = PostRate.objects.create(
                        value=rate,
                        user=request.user,
                        post=post,
                    )

                    rateObj.save()
                    msg = 'Twoja ocena została zapisana'


    context = {
        'latest_posts': latest_post,
        'current_post': post,
        'comments': comments,
        'msg': msg,
        'post_rate': post_rate,
    }

    post.view_count = post.view_count + 1
    post.save()


    if not request.user.is_staff and not request.user.is_anonymous:
        if request.user.isProfilEdited == False:
            if request.user.role == 0:
                return redirect('/editStudentProfile')
            elif request.user.role == 1:
                return redirect('/editCompanyProfile')

    return render(request, 'post.html', context)

def post_update(request, id):
    title = 'Edytuj artykuł'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'form': form,
        'title': title,
    }

    return render(request, "post_create.html", context)

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("news"))

def post_create(request):

    title = 'Dodaj artykuł'
    form = PostForm(request.POST or None, request.FILES or None)
    if request.user.is_staff:
        author = get_author(request.user)
        if request.method == "POST":
            if form.is_valid():
                form.instance.author = author
                form.save()
                return redirect(reverse("post-detail", kwargs={
                    'id': form.instance.id
                }))
        context = {
            'form': form,
            'title': title,
        }
        return render(request, "post_create.html", context)

    return redirect('/')
