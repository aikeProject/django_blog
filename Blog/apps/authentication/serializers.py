#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@Author  :   成雨
@Contact :   1121352970@qq.com
@Software:   PyCharm
@File    :   serializers.py
@Time    :   2019-10-14 19:48
@Desc    :
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from Blog.apps.articles.models import Tag, Category
from .models import Blog

# 拿到在 setting AUTH_USER_MODEL 配置中中指定的模型
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """注册序列化"""

    username = serializers.CharField(
        label='用户名',
        help_text='请填写用户名',
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")],
        error_messages={
            'blank': '请输入用户名',
            'required': '请输入用户名'
        }
    )

    email = serializers.EmailField(
        label='邮箱',
        help_text='请填写邮箱',
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all(), message="邮箱已经存在")],
        error_messages={
            'blank': '请输入邮箱',
            'required': '请输入邮箱',
            'invalid': '邮箱格式错误'
        }
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        help_text='请输入密码',
        error_messages={
            'blank': '请输入密码',
            'required': '请输入密码',
            'min_length': '密码必须大于8个字符'
        }
    )

    class Meta:
        model = User
        # 需要序列化的字段
        fields = ['email', 'username', 'password']


class UserBlogUpdateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(
        required=False,
        min_length=2,
        max_length=25,
        error_messages={
            'min_length': '个人博客标题不少于2个字',
            'max_length': '个人博客标题不能超多25个人'
        }
    )

    site_name = serializers.CharField(
        required=False,
        min_length=5,
        max_length=50,
        error_messages={
            'min_length': '个人博客签名不少于5个字',
            'max_length': '个人博客签名不能超多25个人'
        }
    )

    class Meta:
        model = Blog
        fields = ('title', 'site_name',)


class UserUpdateSerializer(serializers.ModelSerializer):
    # allow_blank 将空值设置为有效值
    username = serializers.CharField(
        label='用户名',
        help_text='请填写用户名',
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all(), message="用户已经存在")],
        error_messages={
            'blank': '请输入用户名',
            'required': '请输入用户名'
        }
    )

    blog = UserBlogUpdateSerializer(required=False)

    class Meta:
        model = User
        fields = ('username', 'image', 'blog')

    def update(self, instance, validated_data):
        blog_data = validated_data.pop('blog', None)
        blog = instance.blog

        instance.username = validated_data.get('username', instance.username)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        if blog_data:
            blog.title = blog_data.get('title', blog.title)
            blog.site_name = blog_data.get('site_name', blog.site_name)
            blog.save()

        return instance


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    categories = CategorySerializer(many=True, source='category_by')

    class Meta:
        model = Blog
        fields = '__all__'
        depth = 1


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情"""

    username = serializers.CharField(required=True)
    following = serializers.SerializerMethodField()
    blog = BlogSerializer(read_only=True, help_text='用户的博客信息')

    def get_following(self, instance):
        request = self.context.get('request', None)

        if request is None:
            return False

        follower = request.user

        if not follower.is_authenticated:
            return False

        followee = instance

        return follower.is_following(followee)

    class Meta:
        model = User
        fields = ('id', 'uid', 'blog', 'email', 'username', 'image', 'following',)
        read_only_fields = ('id', 'uid', 'email', 'image', 'following',)


class UserFollowsSerializer(serializers.ModelSerializer):
    """用户关注"""

    id = serializers.CharField(required=True)
    following = serializers.SerializerMethodField()

    def get_following(self, instance):
        request = self.context.get('request', None)

        if request is None:
            return False

        follower = request.user

        if not follower.is_authenticated:
            return False

        followee = instance

        return follower.is_following(followee)

    class Meta:
        model = User
        fields = ('id', 'following',)
        read_only_fields = ('email', 'image', 'following', 'username')
