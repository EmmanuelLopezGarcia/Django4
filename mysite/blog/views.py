from django.shortcuts import render, get_object_or_404
from .models import Post
# Adding the Django Paginator class
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Adding class-based views
from django.views.generic import ListView
# Adding forms.py
from .forms import EmailPostForm
# Adding send_email library
from django.core.mail import send_mail


# A Class-Based view

class PostListView(ListView):

    # Alternative post list view

    queryset = Post.published.all()

    context_object_name = 'posts'

    paginate_by = 3

    template_name = 'blog/post/list.html'

# Create your views here.

def post_list(request):

    post_list = Post.published.all()

    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)

    page_number = request.GET.get('page', 1)

    try:

        posts = paginator.page(page_number)

    except PageNotAnInteger:

        # if the page_number is not an integer retrieve the first page
        posts = paginator.page(1)

    except EmptyPage:

        #If page_number is out of range deliver last page of result

        # We get the total number of pages using "num_pages" and the total number of pages
        # is the same as the last page.
        posts = paginator.page(paginator.num_pages)


    return render(request, 'blog/post/list.html', {'posts': posts})

# Form's view

def post_share(request, post_id):

    # Using get_object_or_404 shortcut to retrieve a published post by its id.

    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)

    sent = False

    # Using request.method POST to differentiate that the form has been sent and if not, it means that is GET mehtod (form is empty)

    if request.method == 'POST':

        # When the user fills in the form and submits it via POST, a form instance is created using the sumbitted data
        # CONTAINED IN "request.POST"

        form = EmailPostForm(request.POST)

        """
        After this, the data submitted is validated using the form's is_valid() method. This method validates the data
        introduced in the form and returns True if all fields contain valid data. If any field contains invalid data, 
        then is_valid() return False. The list of validation errors can be obtained with form.errors.

        If the form is not valid, the form is rendered in the template again, including the data submitted. Validation
        errors will be displayed in the template.

        If the form is valid, the validated data is retrieved with form.cleaned_data. This attribute is a dictionary of 
        form fields and their values.

        """

        # When the user fills in the 
        if form.is_valid():

            cd = form.cleaned_data
            
            # Form fields passed validation

            # This request.build_absolute_uri retrieves the absolute path of the post using its
            # absolute get_absolute_url() method
            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you read {cd['post.title']}"

            message = f"Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']}"
            
            send_mail(subject, message, 'minoz199618@gmail.com', [cd['to']])

            sent = True

    else:

        form = EmailPostForm()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


def post_detail(request, year, month, day, post):

    """ 
    This modified the post_detail view to take the year, month, day, and post arguments and
    retrieve a published post with the given slug and publication date. By adding unique_for_date='publish'
    to the slug field of the Post model before, we ensured that there will be only one post with a slug for a
    given date. Thus, you can retrieve single posts using the date and slug.

    """

    post = get_object_or_404(Post, status = Post.Status.PUBLISHED, slug = post, publish__year = year, publish__month = month, publish__day = day)
    
    return render(request, 'blog/post/detail.html', {'post': post})