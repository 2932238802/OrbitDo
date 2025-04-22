from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
import logging
import json

logger = logging.getLogger(__name__)

def HomePage(request_):
    context_  = {
        "title_":"hello world!",
        'user_name': request_.user.username if request_.user.is_authenticated else "访客"
    }
    
    return render(request_,'../templates/LoginAndRegister/index.html',context_)

    """_summary_

    Returns:
        _type_: _description_ 安 
    """
@csrf_exempt
def LoginPost(request):
    if request.method == 'POST':
        try:
            # 获取信息 并解码
            data = json.loads(request.body.decode('utf-8'))
            user_name = data.get('user_name').strip()
            password = data.get('password')


            user = authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    "success": True,
                    "message": "登录成功"
                    },
                    status=200,
                    json_dumps_params={'ensure_ascii': False}
                    )
            else:
                return JsonResponse({
                    "success": False,
                    "message": "用户名或密码错误"},
                    status=401,
                    json_dumps_params={'ensure_ascii': False}
                    )
                
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, 
                 "message": "无效的 JSON 数据"}, 
                status=400,
                json_dumps_params={'ensure_ascii': False}
                )
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"服务器错误: {str(e)}"},
                status=500,
                json_dumps_params={'ensure_ascii': False}
                )
    else:
        return JsonResponse(
            {
                "success": False,
                "message": "只接受 POST 请求"
                }, 
            status=405,
            json_dumps_params={'ensure_ascii': False}
            )
        


@csrf_exempt # 注意 CSRF 风险
def RegisterPost(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "仅支持 POST 请求"},
            status=405,
            json_dumps_params={'ensure_ascii': False}
        )

    try:
        # 改进：更具体的 JSON 解析错误处理
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "无效的 JSON 数据"}, status=400)

        user_name = data.get('user_name', '').strip()
        password_ = data.get('password', '').strip()
        email = data.get('email', '').strip().lower()

        # --- 关键修复：重新加入验证逻辑并初始化 errors_ ---
        errors_ = {} # 初始化错误字典

        # 校验用户名
        if not user_name:
            errors_['user_name'] = "用户名不能为空"
        elif len(user_name) < 4:
            errors_['user_name'] = "用户名至少需要4个字符"
        elif len(user_name) > 150: # Django User model limit
             errors_['user_name'] = "用户名不能超过150个字符"

        # 校验邮箱
        if not email:
            errors_['email'] = "邮箱不能为空"
        # 可以使用更严格的邮箱格式正则表达式验证，但 '@' 是基本检查
        elif '@' not in email or '.' not in email.split('@')[-1]:
             errors_['email'] = "无效的邮箱格式"

        if errors_:
            return JsonResponse(
                {"success": False, "errors": errors_},
                status=400,
                json_dumps_params={'ensure_ascii': False}
            )

        User = get_user_model()

        if User.objects.filter(username=user_name).exists():
            errors_['user_name'] = "用户名已存在"
        if User.objects.filter(email=email).exists():
            errors_['email'] = "邮箱已被注册"

        if errors_:
            return JsonResponse(
                {"success": False, "errors": errors_},
                status=409, # 409 Conflict 更合适
                json_dumps_params={'ensure_ascii': False}
            )

        user = User.objects.create_user(
            username=user_name,
            email=email,
            password=password_
        )

        return JsonResponse({
            "success": True,
            "message": "注册成功，请登录"
        }, status=201) # 201 Created

    except Exception as error_:
        # 改进：记录详细错误，返回通用消息
        logger.error(f"注册过程中发生未知错误: {error_}", exc_info=True) # 记录堆栈跟踪
        return JsonResponse({
            "success": False,
            "message": "服务器内部错误，请稍后重试" # 不暴露具体错误信息
        }, status=500, json_dumps_params={'ensure_ascii': False})
            
        
@csrf_exempt
def Todolist(request_):
    return render(request_,'../templates/TodolistPage/index.html')
    
