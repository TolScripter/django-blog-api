from django.contrib.auth.models import User 
from rest_framework import serializers
from .models import Tag, Category, Like, Post, View, Collection

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_superuser']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)

        if password:
            user.set_password(password)
            user.save()
        
        return user
    

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title', 'code', 'description', 'at']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'at']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'img', 'category', 'tags', 'at']

class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = View
        fields = ['id', 'user', 'post', 'at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'at']

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'user', 'post', 'at']