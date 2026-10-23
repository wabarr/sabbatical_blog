from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from sabbatical_blog.models import Post, Category
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_not_required

class CategoryListView(ListView):
    model = Category

class CategoryView(ListView):
    model = Post
    paginate_by = 100
    template_name = "sabbatical_blog/categories.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs["category"]
        return context
    def get_queryset(self):
        return Post.objects.filter(category__name=self.kwargs['category'])

class PostDetailView(DetailView):
    model = Post

class AboutView(TemplateView):
    template_name = 'sabbatical_blog/about.html'

class MapView(TemplateView):
    template_name = "sabbatical_blog/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(map_latitude__isnull=False, map_longitude__isnull=False)
        return context

class HomeView(ListView):
    model = Post
    paginate_by = 10

@login_not_required
def login_view(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      urlForRedirect = request.GET.get('next')
      return redirect(urlForRedirect)
  else:
    form = AuthenticationForm()

  return render(request, "sabbatical_blog/login.html", {"form": form})

