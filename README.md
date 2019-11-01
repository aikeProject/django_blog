#### django restAPI jwt

##### 01 安装开发相关包

```
pip install Django django-cors-middleware django-extensions djangorestframework django-filter django-formtools djangorestframework-jwt python-slugify
```

```
Django==2.2.6
django-cors-middleware==1.4.0       解决跨域问题
django-extensions==2.2.3            用来扩展django命令行工具
djangorestframework==3.10.3         REST API
django-filter==2.2.0                django 过滤插件
django-formtools==2.1               Web api 表单预览插件      
django-crispy-forms==1.8.0          Web api 表单美化
djangorestframework-jwt==1.11.0     jwt 认证插件
python-slugify==4.0.0               slugify('月尽天明 like you') -> 'yue-jin-tian-ming-like-you'
```

##### 02 authentication

- 自定义用户类 `settings.py` [authentication](/Blog/apps/authentication/models.py)

```
AUTH_USER_MODEL = 'authentication.User'

User 类需要继承 AbstractUser
```

##### 03 jwt

```
.......
```




