from django.shortcuts import render

# Create your views here.
def login_view(request):
    return render(request, 'biblioteca_app/login.html')

def admin_view(request):
    return render(request, 'biblioteca_app/admin.html')