import jwt
from datetime import timedelta, datetime
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse 
from django.contrib.auth.models import User 
from rest_framework.exceptions import AuthenticationFailed
from .serializers import TagSerializer, PostSerializer, CategorySerializer, LikeSerializer, ViewSerializer, CollectionSerializer
from .models import Tag, Category, Post, Like, View, Collection
from django.shortcuts import get_object_or_404

def auth_middleware(request):
    try:
        token = request.headers['Authorization'].split('Bearer')[1].strip()
        decoded_jwt = jwt.decode(token, 'secret', algorithms=['HS256'])
        current_time = datetime.utcnow().timestamp()
        token_lt = decoded_jwt['exp']

        if current_time < token_lt:
            user = User.objects.get(id=decoded_jwt['id'])
            serializer = UserSerializer(user)
        else:
            raise AuthenticationFailed('The token is dead')
        
        return serializer.data
    except:
        raise AuthenticationFailed('Authentication required')


#Users
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']
    
    user = User.objects.filter(email=email).first()
    
    if user is None:
        raise AuthenticationFailed('User not found')
    
    if not user.check_password(password):
        raise AuthenticationFailed('Bad password')
    

    payload = {
        'id' : user.id,
        'exp' : datetime.utcnow() + timedelta(minutes=30)
    }

    encoded_jwt = jwt.encode(payload, 'secret', algorithm='HS256')
    # usr = {
    #     'id': user.id,
    #     'username': user.username,
    #     'email': user.email,
    #     'is_superuser':user.is_superuser
    # }
    return JsonResponse({"token": encoded_jwt})


@api_view(['DELETE', 'PUT', 'GET'])
def account_details(request, id):
    check_user = auth_middleware(request)
    if check_user['id'] is None or check_user['is_superuser'] is False:
        raise AuthenticationFailed('You are not authorized')
    
    user = get_object_or_404(User, pk=id)
    
    if request.method == 'PUT':
        serializer = UserSerializer(user, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'The serializer is invalid'}, status=status.HTTP_304_NOT_MODIFIED)
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

#Tags
@api_view(['POST', 'GET'])
def tags_list(request):
    if request.method == 'POST':
        check_user = auth_middleware(request)
        if check_user['is_superuser'] is True:
            serializer = TagSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data={'message': 'The serializer is invalid'}, status=status.HTTP_406_NOT_ACCEPTABLE)    
        else:
            return Response(data={'message': 'You are not superuser'}, status=status.HTTP_401_UNAUTHORIZED)    
    elif request.method == 'GET':
        all_tags = Tag.objects.all()
        serializer = TagSerializer(all_tags, many=True)
        return JsonResponse({'tags': serializer.data})


@api_view(['PUT', 'GET', 'DELETE'])
def tag_details(request, id):
    tag = get_object_or_404(Tag, pk=id)
    if request.method == 'GET':
        serializer = TagSerializer(tag)
        return JsonResponse(serializer.data)
    
    if request.method == 'PUT' or request.method == 'DELETE':
        check_user = auth_middleware(request)
        if check_user['is_superuser'] is not True:
            raise AuthenticationFailed('You are not superuser')
    
    if request.method == 'PUT':
        serializer = TagSerializer(tag, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(data={'message': 'The serializer is invalid'}, status=status.HTTP_304_NOT_MODIFIED)
    elif request.method == 'DELETE':
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Categories
@api_view(['POST', 'GET'])
def categories_list(request):
    if request.method == 'GET':
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return JsonResponse({'categories': serializer.data})
    elif request.method == 'POST':
        check_user = auth_middleware(request)
        if check_user['is_superuser'] is True:
            serializer = CategorySerializer(request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data={'message': 'The serializer is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'message': 'You are not superuser'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT', 'GET', 'DELETE'])
def category_details(request, id):
    category = get_object_or_404(Category, pk=id)

    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return JsonResponse(serializer.data)
    
    check_user = auth_middleware(request)

    if request.method == 'PUT' or request.method == 'DELETE' and check_user is not True:
        raise AuthenticationFailed('You are not authorized')
    
    
    if request.method == 'PUT':
        serializer = CategorySerializer(category, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'The serializer is invalid'}, status=status.HTTP_304_NOT_MODIFIED)
    elif request.method == 'DELETE':        
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  

#Posts
@api_view(['POST', 'GET'])
def posts_list(request):
    if request.method == 'GET':
        all_posts = Post.objects.all()
        serializer = PostSerializer(all_posts, many=True)
        return JsonResponse({'posts': serializer.data})
    elif request.method == 'POST':
        check_user = auth_middleware(request)
        if check_user['is_superuser'] is True:
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data={'message': 'The serializer is invalid'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'message': 'You are not superuser'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['PUT', 'GET', 'DELETE'])
def post_details(request, id):
    post = Post.objects.get(id)

    check_user = auth_middleware(request)

    if request.data == 'PUT' or request.data == 'DELETE' and check_user is not True:
        raise AuthenticationFailed('You are not authorized')
    
    if request.data == 'GET':
        return JsonResponse(post)
    
    if request.data == 'PUT':
        serializer = PostSerializer(post, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'The serializer is invalid'}, status=status.HTTP_304_NOT_MODIFIED)
    elif request.data == 'DELETE':        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#Likes
@api_view(['POST', 'GET'])
def likes_list(request):
    if request.method == 'GET':
        all_likes = Like.objects.all()
        serializer = LikeSerializer(all_likes, many=True)
        return JsonResponse({'likes': serializer.data})
    elif request.method == 'POST':
        check_user = auth_middleware(request)
        if check_user['id'] is None:
            raise AuthenticationFailed('You are not authorized')
        
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': 'The serializer is invalid'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'DELETE'])
def like_details(request, id):
    like = get_object_or_404(Like, pk=id)

    check_user = auth_middleware(request)

    if request.method == 'DELETE' and check_user['id'] is None:
        raise AuthenticationFailed('You are not authorized')
    
    if request.method == 'GET':
        serializer = LikeSerializer(like)
        return JsonResponse(serializer.data)
    
    if request.method == 'DELETE':        
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Views
@api_view(['POST', 'GET'])
def views_list(request):
    if request.method == 'GET':
        all_views = View.objects.all()
        serializer = ViewSerializer(all_views, many=True)
        return JsonResponse({'views': serializer.data})
    elif request.method == 'POST':
        serializer = ViewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': 'The serializer is invalid'}, status=status.HTTP_400_BAD_REQUEST)



#Collections
@api_view(['POST', 'GET'])
def collection_list(request):
    if request.method == 'GET':
        all_collections = Collection.objects.all()
        serializer = CollectionSerializer(all_collections, many=True)
        return JsonResponse({'collections': serializer.data})
    elif request.method == 'POST':
        check_user = auth_middleware(request)
        if check_user['id'] is None:
            raise AuthenticationFailed('You are not authorized')
        
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data={'message': 'The serializer is invalid'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def collection_details(request, id):
    collection = get_object_or_404(Collection, pk=id)

    check_user = auth_middleware(request)

    if request.data == 'DELETE' and check_user['id'] is None:
        raise AuthenticationFailed('You are not authorized')
    
    if request.data == 'GET':
        serializer = CollectionSerializer(collection)
        return JsonResponse(serializer.data)
    
    if request.data == 'DELETE':        
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)