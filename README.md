# OrbitDo

#### 运行方式

- 确保本地安装了 docker && docker desktop
- 运行 : cd 到 Orbitto 目录 然后运行 
>> docker build -t orbitdo-app . 
>> docker run -d -p 8080:8080 --name my-orbitdo-container orbitdo-app
>> 打开本地 127.0.0.1:8080 端口即可访问了


#### 登录和注册界面
```python
urlpatterns = [
    # path('', HomePage, name='home'),
    # path('admin/', admin.site.urls),  
    # path('login/', LoginPost, name='login'),  
    # path('register/', RegisterPost, name='register'),
    # path('todolist/', Todolist, name='todolist'),
    # path('guess/', Guess, name='guess'),
    path('', Guess, name='guess'),
    path('returnanswer/',ReturnAnswer,name='returnanswer')
]
```
记得把
```python
path('returnanswer/',ReturnAnswer,name='returnanswer')
```
重新注释起来

#### 游戏开始界面
![alt text](png/_1.png)


#### 游戏结束界面
![alt text](png/_2.png)

#### 游戏运行界面
![alt text](png/_3.png)