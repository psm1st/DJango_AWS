from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .forms import PostBasedForm,PostCreateForm,PostDetailForm
from .models import Post
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .serializers import PostModelSerializer
from django.views.generic import ListView
from .models import Posts,Post
from django.contrib.auth.decorators import login_required
def index(request):
    post_list = Post.objects.all().order_by('-created_at')
    context = {
        'post_list':post_list,
    }
    return render(request, 'index.html',context)

def post_list_view(request):
    post_list = Post.objects.filter(writer=request.user)
    context = {
        'post_list':post_list,
    }
    return render(request, 'posts/post_list.html', context)

def post_detail_view(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExit:
        return redirect('index')
    post = Post.objects.get(id=id)
    context = {
        'post' : post,
        'form' : PostDetailForm(),
    }
    return render(request, 'posts/post_detail.html', context)
@login_required
def post_create_view(request):
    if request.method == 'GET':
        return render(request, 'posts/post_form.html')
    else:
        image = request.FILES.get('image')
        content = request.POST.get('content')
        Post.objects.create(
            image = image,
            content = content,
            writer = request.user
        )
        return redirect('index')

@login_required
def post_update_view(request, id):
    #post = Post.objects.get(id=id)
    post = get_object_or_404(Post, id=id, writer = request.user)

    if request.method == 'GET':
        context = {'post':post}
        return render(request, 'posts/post_form.html',context)
    elif request.method == 'POST':
        new_image = request.FILES.get('image')
        content = request.POST.get('content')
        print(new_image)
        print(content)
        if new_image:
            post.image.delete()
            post.image = new_image
        post.content = content
        post.save()
        return redirect('posts:post-detail', post.id)
   
@login_required
def post_delete_view(request, id=id):
    post = get_object_or_404(Post, id=id)
    #post = get_object_or_404(Post, id=id,writer=request.user)
    if request.user != post.writer:
        raise Http404('잘못된 접근입니다')
    
    if request.method == 'GET':
        context = { 'post':post }
        return render(request, 'posts/post_confirm_delete.html',context)
    else:
        post.delete()
        return redirect('index')

def post_create_form_view(request):
    if request.method=="GET":
        form = PostCreateForm()
        context = {'form':form}
        return render(request, 'posts/post_form2.html',context)
    else:
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            Post.objects.create(
                image = form.cleaned_data['image'],
                content = form.cleaned_data['content'],
                writer = request.user
            )
        else:
            return redirect('post:post-create')
        return redirect('index')
        
class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer

class PostBase(APIView):
    def get(self, request, format=None):
        queryset = Post.objects.all()
        serializer = PostModelSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostModelSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostModelSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 

















class class_view(ListView):
    model = Post
    template_name = 'cbv_view.html'

def url_view(request):
    data = {'code': '001', 'msg': 'OK'}
    return HttpResponse('<h1>url_views</h1>')

def url_parameter_view(request, username):
    print(f'url_parameter_view()')
    print(f'username: {username}')
    print(f'request.GET: {request.GET}')
    return HttpResponse(username)

def function_view(request):
    print(f'request.method: {request.method}')

    if request.method == "GET":
        print(f'request.GET: {request.GET}')
    elif request.method == 'POST':
        print(f'request.POST: {request.POST}')
    return render(request, 'view.html')