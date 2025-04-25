from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.conf import settings
import logging
import json
import random

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
        


@csrf_exempt 
def RegisterPost(request):
    if request.method != "POST":
        return JsonResponse(
            {"success": False, "message": "仅支持 POST 请求"},
            status=405,
            json_dumps_params={'ensure_ascii': False}
        )

    try:
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "无效的 JSON 数据"}, status=400)

        user_name = data.get('user_name', '').strip()
        password_ = data.get('password', '').strip()
        email = data.get('email', '').strip().lower()

        errors_ = {} 

        if not user_name:
            errors_['user_name'] = "用户名不能为空"
        elif len(user_name) < 4:
            errors_['user_name'] = "用户名至少需要4个字符"
        elif len(user_name) > 150: 
             errors_['user_name'] = "用户名不能超过150个字符"

        if not email:
            errors_['email'] = "邮箱不能为空"
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
        }, status=201) 

    # 其它错误处理 
    except Exception as error_:
        logger.error(f"注册过程中发生未知错误: {error_}", exc_info=True) 
        return JsonResponse({
            "success": False,
            "message": "服务器内部错误，请稍后重试" 
        }, status=500, json_dumps_params={'ensure_ascii': False})
            
        
@csrf_exempt
def Todolist(request_):
    return render(request_,'../templates/TodolistPage/index.html')

    """
    IDIOM_DATA 存放原始数据
    IDIOM_INDEX 这个存放索引
    """
IDIOM_DATA = []  
IDIOM_INDEX = {}

def LoadIdiomData():
    """
    加载一下 json文件和数据
    # 索引：{"首字": ["成语1", "成语2", ...]}
    """
    global IDIOM_DATA, IDIOM_INDEX
    # with open('./data/idiom-database/data/idiom.json', 'r', encoding='utf-8') as f:
    with open(settings.IDIOM_FILE_PATH, 'r', encoding='utf-8') as f:
        IDIOM_DATA = json.load(f)
    
    for idiom in IDIOM_DATA:
        first_char = idiom['word'][0]
        if first_char not in IDIOM_INDEX:
            IDIOM_INDEX[first_char] = []
        IDIOM_INDEX[first_char].append(idiom['word'])
LoadIdiomData()

@csrf_exempt
def Guess(request):
    initial_idiom_word = "数据加载失败" # 默认/错误信息

    request.session.pop('last_idiom', None)

    if IDIOM_DATA:
        try:
            random_idiom_data = random.choice(IDIOM_DATA)
            initial_idiom_word = random_idiom_data.get('word', '数据格式错误')
            
            request.session['last_idiom'] = initial_idiom_word
            # 记录日志，方便调试
            logger.debug(f"为会话 {request.session.session_key} 设置的初始成语: {initial_idiom_word}")

        except IndexError: # 如果 IDIOM_DATA 为空
            logger.error("IDIOM_DATA 为空，无法选择初始成语。")
        except Exception as e:
            logger.error(f"选择初始成语时出错: {e}", exc_info=True)
    else:
         logger.warning("渲染 Guess 视图时 IDIOM_DATA 为空。")
         

    context = {
        'initial_idiom': initial_idiom_word,
    }
    # return render(request, 'GuessPage/index.html', context)
    # return render(request, 'GuessPage/index.html')
    return render(request, '../templates/GuessPage/index.html',context)


@csrf_exempt
def ReturnAnswer(request):
    """
    处理成语
    返回新成语
    返回json 格式 
    {
        error       这个就是错误信息
        valid       这个就是有效性
        message     这个就是消息
    }
    """
    if request.method !=  'POST':
        return JsonResponse({'valid': False, 'message':'支持POST请求'}, status=400)
    
    
    # 尝试加载一下请求内容
    # 前端要写 : idiom 
    # 前端统一接受 : error
    # ''给一个默认值 防止strip报错！
    try:
        data = json.loads(request.body.decode('utf-8'))
        client_idiom = data.get('idiom', '').strip()
    except Exception as e:
        logger.warning(f"解析请求失败{e}")
        return JsonResponse({'valid': False, 'message':'请求格式错误'}, status=400)
    
    # 验证提交的成语是否合法
    # 不合法返回消息 给前端弹出 非有效成语
    # 前端要接受 valid message
    if not IsValidIdiom(client_idiom):
        return JsonResponse({'valid': False, 'message': '非有效成语'})
    
    # 获取上一个成语（从session中）
    last_idiom = request.session.get('last_idiom')
    
    # 接龙规则验证（如果有上一个成语）
    if last_idiom:
        required_char = last_idiom[-1]  # 需要匹配的首字
        if client_idiom[0] != required_char:
            return JsonResponse({
                'valid': False,
                'message': f'需以【{required_char}】开头'
            })
    
    # 更新session记录
    # 这样的话 方便下次查看是不是正确的
    request.session['last_idiom'] = client_idiom
    
    return JsonResponse({
        'valid': True,
        'message': '接龙成功',
    })

def IsValidIdiom(idiom):
    """
    检查是否ok
    """
    return len(idiom) == 4 and any(
        idiom == item['word'] for item in IDIOM_DATA
    )