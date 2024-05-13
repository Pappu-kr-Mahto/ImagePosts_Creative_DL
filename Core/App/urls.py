from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


urlpatterns = [
    # path("",views.home, name='home'),

    # Drf Spectacular:
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Auth
    path('api/signup/',views.signup,name="signup"),
    path('api/login/',views.login,name="login"),

    # ImagePosts
    path('api/posts/',views.imagePost, name="imagePost"),
    path('api/posts/like_status/<int:post_id>/',views.like_unlikePost, name="like_status"),

    # UserProfile and ImagePosts
    path('api/users/',views.all_userprofile, name="users"),
    path('api/users/followed/',views.followed_userlist, name="followed_userlist"),
    path('api/users/followed_userposts/',views.followed_user_imagepost, name="followed_userposts"),
    path('api/users/follow_status/<int:user_id>/',views.follow_unfollow_user, name="follow_status"),

       
]
