from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse, HttpResponseForbidden
from . models import *
from django.contrib.auth. forms import UserCreationForm
from django.contrib.auth.decorators import login_required,user_passes_test



# Create your views here.


# def student_list(request):
#     return HttpResponse("List of Students")


def hello_world(request):
     return HttpResponse("Welcome to University Hub!")


@login_required
def course_list(request):
     all_courses = Course.objects.all()
     context = {
          'courses' : all_courses,
          'page_title' : 'Available Courses'
     }
     return render (request, 'academic/course_list.html', context)


def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def delete_student(request,id):
    student = Student.objects.get(id=id)
    if student.user:
        student.user.delete()
    else:
        student.delete()
    return redirect('course_list')


@login_required
def student_profile(request,id):
    profile = Student.objects.get(id=id)
    if request.user!= profile.user:
        return HttpResponseForbidden("You are not authorized to view this profile.")
    return HttpResponse('Profile allowed')
    

def student_create(request):

    if request.method == 'POST':
        form = StudentForm(request.POST)

        if form.is_valid():

            # get login fields safely
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            email = request.POST.get('email', '').strip()

            # validate login fields first
            if not username or not password or not email:
                return render(request, 'academic/student_form.html', {
                    'form': form,
                    'error': 'All login fields required'
                })

            # prevent duplicate username crash
            if user.objects.filter(username=username).exists():
                return render(request, 'academic/student_form.html', {
                    'form': form,
                    'error': 'Username already exists'
                })

            # create user first
            user = user.objects.create_user(
                username=username,
                password=password,
                email=email
            )

            # THEN create student object
            student = form.save(commit=False)
            student.user = user
            student.save()

            form.save_m2m()

            return redirect('course_list')

    else:
        form = StudentForm()

    return render(request, 'academic/student_form.html', {'form': form})








def register_user(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():
            form. save()
            return redirect('login')

    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html',{'form': form})




from django.http import JsonResponse

def api_course_list(request):
  
    courses = Course.objects.all()


    data = {
        'count': courses.count(),
        'results': list(courses.values('name', 'code', 'credits'))
    }

    return JsonResponse(data)



from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from .models import *
from .serializers import *

@api_view(['POST'])
def login_api(request):
    """Custom login endpoint for React frontend"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=400)
    
    user = authenticate(username=username, password=password)
    
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=401)
    
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
    })

class courseViewSets(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = courseSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]

class studentViewSets(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = studentserializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [AllowAny]
