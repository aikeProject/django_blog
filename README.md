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

#### 一些知识点

```
blank
设置为True时，字段可以为空。设置为False时，字段是必须填写的。字符型字段CharField和TextField是用空字符串来存储空值的。

如果为True，字段允许为空，默认不允许。

null
设置为True时，django用Null来存储空值。日期型、时间型和数字型字段不接受空字符串。所以设置IntegerField，DateTimeField型字段可以为空时，需要将blank，null均设为True。

如果为True，空值将会被存储为NULL，默认为False。

如果想设置BooleanField为空时可以选用NullBooleanField型字段。

null 是针对数据库而言，如果 null=True, 表示数据库的该字段可以为空。
blank 是针对表单的，如果 blank=True，表示你的表单填写该字段的时候可以不填，比如 admin 界面下增加 model 一条记录的时候。直观的看到就是该字段不是粗体

```




