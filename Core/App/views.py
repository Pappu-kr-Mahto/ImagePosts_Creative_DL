from django.shortcuts import HttpResponse
from .serializers import * 
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema

# Create your views here.

# def home(request):
#     return HttpResponse("<h1>hello! Server is Live</h1>")

@extend_schema(
        request=UserSerializer,
        responses={201: None},
        description="Enter the username, email, dob, password to create an account."
    )
@api_view(['POST'])
def signup(request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success":"Account Created successfully","username":request.data['username'],"email":request.data['email']},status=status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error":'Internal server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
        request=LoginSerializer,
        responses={200: None},
        description="Enter the email and password for login. And Authorize with the access key given after login."
    )  
@api_view(['POST'])
def login(request):
    try:
        email= request.data.get('email')
        password = request.data.get('password')
        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        if user is not None:
            temp = authenticate(username=user.username, password=password)
            if temp is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                        'user':email,
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    })
        return Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({"error":"Invalid Credentials"},status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
        request={'multipart/form-data': GetImagePostSerilizer},
        responses={201: None},
        description="upload a image (note: use multipart/form-data)"
    )
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def imagePost(request):
    if request.method == 'POST':
        try:
            user = UserProfile.objects.get(user=request.user)
            if user:
                ImagePost.objects.create(user=user,image=request.data['image'])
                return Response({'success':'Image posted successfully.'},status=status.HTTP_201_CREATED)
            else:
                return Response({'error':'Something Went Wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:
            user = UserProfile.objects.get(user=request.user)
            queryset = ImagePost.objects.filter(user=user)
            serializer = ImagePostSerializer(queryset , many=True)
            return Response({'success':serializer.data})
        except Exception as e:
            return Response({'error':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
        responses={200: None},
        description=" Enter the post id for like/unlike "
    )  
@api_view(['GET'])    
@permission_classes([IsAuthenticated])
def like_unlikePost(request,post_id):
    try:
        user = UserProfile.objects.get(user=request.user)
        post = get_object_or_404(ImagePost, id=post_id)
        if post.likes.filter(id = user.id).exists():
            msg='unliked'
            post.likes.remove(user)
        else:
            msg='liked'
            post.likes.add(user)
        post.save()
        return Response({'success':f'Post {msg} successfully'},status=status.HTTP_200_OK)
    except Exception as e:
            return Response({'error':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
        responses=UserProfileSerializer,
        description="This API  gives you all the list of users."
    )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_userprofile(request):
    try:
        queryset = UserProfile.objects.all()
        serializer = UserProfileSerializer(queryset,many=True)
        return Response({'success':serializer.data})
    except Exception as e:
            return Response({'error':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
        responses=UserProfileSerializer,
        description="This API  gives you all the list of users whom you follow."
    )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def followed_userlist(request):
    try:
        user = UserProfile.objects.get(user=request.user)
        queryset = UserProfile.objects.filter(followers = user.id)
        serializer = UserProfileSerializer(queryset,many=True)
        return Response({'success': serializer.data})
    except Exception as e:
            return Response({'error':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
        responses=ImagePostSerializer,
        description=" This API gives you the list of posts from all followed users in descending order of their created time."
    )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def followed_user_imagepost(request):
    try:
        user = UserProfile.objects.get(user=request.user)
        followed_userlist = UserProfile.objects.filter(followers = user.id).values('id')
        temp=[]
        for i in followed_userlist:
            temp.append(i['id'])
        queryset = ImagePost.objects.filter(user_id__in = temp).order_by('-createdAt')
        serializer = ImagePostSerializer(queryset,many=True)
        return Response({'success':serializer.data})
    except Exception as e:
            return Response({'error':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
        responses={200: None},
        description="Enter User id. This API used to follow/unfollow the user. "
    )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def follow_unfollow_user(request, user_id):
    try:
        user = UserProfile.objects.get(user=request.user)
        user_profile = get_object_or_404(UserProfile, id = user_id)
        if user_profile.followers.filter(id = user.id).exists():
            msg="unfollowed"
            user_profile.followers.remove(user)
        else:
            msg='followed'
            user_profile.followers.add(user)
        user_profile.save()
        return Response({'success':f'User {msg} successfully'},status=status.HTTP_200_OK)
    except Exception as e:
            return Response({'error':'Internal Server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    