import os
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import File, UserProfile


def index(request):
    template = loader.get_template('login/myfirst.html')
    return HttpResponse(template.render())


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.method == 'GET':
        return render(request, 'login/register.html')
    
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    
    # Validation
    if not username or not email or not password:
        return render(request, 'login/register.html', {'error': 'All fields are required'})
    
    if password != confirm_password:
        return render(request, 'login/register.html', {'error': 'Passwords do not match'})
    
    if len(password) < 6:
        return render(request, 'login/register.html', {'error': 'Password must be at least 6 characters'})
    
    if User.objects.filter(username=username).exists():
        return render(request, 'login/register.html', {'error': 'Username already exists'})
    
    if User.objects.filter(email=email).exists():
        return render(request, 'login/register.html', {'error': 'Email already registered'})
    
    # Create user
    user = User.objects.create_user(username=username, email=email, password=password)
    UserProfile.objects.create(user=user)
    
    messages.success(request, 'Registration successful! Please log in.')
    return redirect('login')
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login/login.html')

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Check if request is AJAX (Django 6.0 removed is_ajax())
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        if is_ajax or request.content_type == 'application/json':
            return JsonResponse({'status': 'ok'})
        return redirect('dashboard')

    # Check if request is AJAX (Django 6.0 removed is_ajax())
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    if is_ajax or request.content_type == 'application/json':
        return JsonResponse({'status': 'error', 'message': 'invalid credentials'}, status=400)
    return render(request, 'login/login.html', {'error': 'Invalid credentials'})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    files = File.objects.filter(owner=request.user, is_deleted=False).order_by('-uploaded_at')
    return render(request, 'login/dashboard.html', {'files': files})


@login_required
def api_list_files(request):
    files = File.objects.filter(owner=request.user, is_deleted=False).order_by('-uploaded_at')
    data = []
    for f in files:
        data.append({
            'id': f.id,
            'name': f.name,
            'size': f.size,
            'uploaded_at': f.uploaded_at.isoformat(),
            'url': f.file.url if hasattr(f.file, 'url') else '',
        })
    return JsonResponse({'files': data})


@login_required
@require_http_methods(['POST'])
def api_upload_file(request):
    uploaded = request.FILES.get('file')
    if not uploaded:
        return JsonResponse({'error': 'no file provided'}, status=400)

    f = File(owner=request.user, name=uploaded.name, file=uploaded)
    f.save()
    return JsonResponse({'status': 'ok', 'id': f.id, 'name': f.name, 'size': f.size})


@login_required
@require_http_methods(['POST'])
def api_delete_file(request, pk):
    try:
        f = File.objects.get(pk=pk, owner=request.user)
    except File.DoesNotExist:
        return JsonResponse({'error': 'not found'}, status=404)

    try:
        if f.file:
            f.file.delete(save=False)
    except Exception:
        pass
    f.is_deleted = True
    f.save()
    return JsonResponse({'status': 'ok'})
