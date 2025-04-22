### 开发文档

#### Django Rest Framework
- 用于将Django全栈框架的视图层转换成基于Restful的接口，适配前后端分离架构。

#### SQLite
-  数据库：是一种嵌入式数据库, 它的数据库就是一个文件


#### 项目目录（示例）
public：项目的公共文件，一般存放 fav.icon 和 logo.icon
assets：图片目录，在页面中用到的一些图片文件
components：包含页面中可以复用的组件
less：Less 文件，负责项目的全局样式设置
router：前端页面路由信息
store：Vuex 的集中式存储管理应用的所有组件的状态。
types：TypeScript 需要的类型定义说明
utils：包含各类工具方法
views：所有页面文件，以 .vue 结尾
App.vue：项目主页面
main.ts：TypeScript 的项目入口文件
shims-vue.d.ts：TypeScript 对 Vue 的垫片文件，用于配置 TypeScript 支持识别.vue 文件
vite-env.d.ts：Vite 的环境配置文件
.gitingore：Git 版本管理中的排除文件记录，在这个文件中出现的文件，不纳入版本管理，比如 node_modules
index.html：项目如何页面，Vue 的挂在入口
package.json：项目依赖和配置文件
README.md：项目说明文件，基于 MarkDown 语法
tsconfig.json：TypeScript 的配置文件
vite.config.ts：Vite 的配置文件
yarn-error.log：Yarn 安装依赖时的错误记录文件
yarn.lock：Yarn 安装依赖后的版本号锁定文件

project：Django的配置代码和控制代码，比如 settings.py，urls.py，同时放置了一些自定义的Django中间件和公共方法
blog：博客核心逻辑所在目录，负责博客的CRUD。
common：处理用户登录，注销，修改密码，图片上传等基础公共功能，同时包含一些工具类和代码常量。
data：存放 Sqlite 数据库文件。
logs：存放项目的日志，按照天进行风分割。
upload：用于存放上传的文件，按照日期方式的文件夹进行组织。
manage.py：Django的管理和控制代码，通过执行 python manage.py XXX 方式完成对整个项目的管理
requirements.txt：记录 Python 项目的所有依赖包和版本号

#### 搭建
django-admin startproject todolist_project .
python manage.py startapp tasks

#### 项目目录
todolist_project/  <-- 你的项目根目录 (可以任意命名)
├── manage.py         <-- Django 项目管理命令行工具
├── todolist_project/ <-- Django 项目配置目录 (与项目同名)
│   ├── __init__.py     <-- 告诉 Python 这是个包
│   ├── asgi.py         <-- ASGI 服务器入口 (用于异步)
│   ├── settings.py     <-- 项目配置文件 (数据库, 应用列表, 静态文件等) ★★★
│   ├── urls.py         <-- 项目级 URL 路由配置 (通常包含指向 app 的路由) ★★★
│   └── wsgi.py         <-- WSGI 服务器入口 (用于同步)
│
├── tasks/            <-- 你的 'tasks' 应用目录 ★★★
│   ├── __init__.py     <-- 告诉 Python 这是个包
│   ├── admin.py        <-- 配置模型在 Django Admin 后台的显示 ★★★
│   ├── apps.py         <-- 应用自身的配置
│   ├── migrations/     <-- 数据库迁移文件目录 (Django 自动管理)
│   │   └── __init__.py
│   ├── models.py       <-- 定义数据库模型 (例如 Task 模型) ★★★
│   ├── tests.py        <-- 编写应用测试用例
│   ├── urls.py         <-- 'tasks' 应用内部的 URL 路由配置 ★★★ (需要手动创建)
│   ├── views.py        <-- 处理请求和响应的视图函数/类 ★★★
│   ├── forms.py        <-- 定义 Django 表单 (用于添加/编辑任务) ★★★ (需要手动创建)
│   └── templates/      <-- 存放 HTML 模板文件的目录 ★★★ (建议手动创建)
│       └── tasks/      <-- (推荐) 与应用同名的子目录, 避免模板名冲突
│           ├── base.html       <-- (可选) 基础模板, 其他模板可以继承它
│           ├── task_list.html  <-- 显示任务列表的模板
│           └── task_confirm_delete.html <-- 删除任务前的确认页面模板
│           └── (其他模板, 如 task_form.html 用于添加/编辑)
│
└── requirements.txt  <-- (推荐) 项目依赖库列表 (例如 Django==4.x)
└── .gitignore        <-- (推荐) Git 忽略文件配置
└── db.sqlite3        <-- (默认) 如果使用 SQLite, 数据库文件会在这里

#### 模板html的解释

当你的 views.py 中的 render() 函数被调用时，Django 的模板引擎会：
读取 templates/index.html 文件。
用你传入的 context 数据替换掉所有的 {{ variable }}。
执行所有的 {% tag %} 逻辑。
最终生成一个纯粹的、标准的 HTML 文档。
这个最终生成的纯 HTML 文档才是发送到用户浏览器并显示出来的网页。
所以，模板文件是源代码/蓝图，渲染后的结果才是最终产品。


#### 发送http请求
// Example POST method implementation:

```js
async function postData(url = "", data = {}) {
  // Default options are marked with *
  const response = await fetch(url, {
    method: "POST", // *GET, POST, PUT, DELETE, etc.
    mode: "cors", // no-cors, *cors, same-origin
    cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
    credentials: "same-origin", // include, *same-origin, omit
    headers: {
      "Content-Type": "application/json",
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    redirect: "follow", // manual, *follow, error
    referrerPolicy: "no-referrer", // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    body: JSON.stringify(data), // body data type must match "Content-Type" header
  });
  return response.json(); // parses JSON response into native JavaScript objects
}

postData("https://example.com/answer", { answer: 42 }).then((data) => {
  console.log(data); // JSON data parsed by `data.json()` call
});
```


#### python json 语法
- get
dict.get(key, default=None)
key：这是必须要提供的参数，代表你要在字典里查找的键。
default：属于可选参数，当字典中不存在指定的键时，就会返回这个默认值。如果不提供这个参数，默认值为 None。
   
