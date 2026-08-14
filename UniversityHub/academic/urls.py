
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from academic import views
from django.views.generic import RedirectView

router = DefaultRouter()

router.register(r'courses', views.courseViewSets)
router.register(r'students', views.studentViewSets)

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='course_list', permanent=False), name='home'),
    # path('students/', views.student_list),
    path('hello/', views.hello_world, name='hello'),
    path('courses/', views.course_list, name='course_list'),
    path("register-student/", views.student_create, name="student_create"),
    path("register/", views.register_user, name="register"),
    # path('api/courses/',views.api_course_list,name='api_course_list'),
    path('api/login/', views.login_api, name='login_api'),
    path('api/', include(router.urls)),
]
