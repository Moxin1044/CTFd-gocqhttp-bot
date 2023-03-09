# 关于
这是一个GO-CQHTTP的CTFd插件，主要功能有：题目提交提醒、题目flag正确提醒等、题目提交过快提醒等。

# 使用
您需要把`CTFd/plugins/`中的challenges替换为我的challenges，接着将gocqhttpbot也放到`CTFd/plugins/`目录中。

# 后台登陆检测
**血的教训：**
后台登陆检测需要在其他文件中定义，下面是定义方法:

修改`CTFd/admin/__init__.py`，在头部引用我们的插件：
```python
from CTFd.Plugin.gocqhttpbot.gocq from send_admin_ip
```
找到：
```python
@admin.route("/admin", methods=["GET"])
def view():
    if is_admin():
        return redirect(url_for("admin.statistics"))
    return redirect(url_for("auth.login"))
```
修改为：
```python
@admin.route("/admin", methods=["GET"])
def view():
    ip = get_ip(request)
    if is_admin():
        send_admin_ip("成功", ip)
        return redirect(url_for("admin.statistics"))
    send_admin_ip("不成功",ip)
    return redirect(url_for("auth.login"))
```

# 说明
安装插件之后首先第一件事就是要`配置！配置！配置！`\
偷了点懒，这两天的项目有点多。如果有哪里有错误还请提交问题。\
有些变量名起的随意了点，问题不大，不影响使用。

# 配置GO-CQ-HTTP
关于`Authorization`：如果你没有启用GO-CQHTTP的`access-token`，那么你填写的为空即可（这个我真的没测试，因为**安全**起见，我建议大家一定要启用Authorization！！！！安全第一！！！）

插件采用HTTP通信接口，你需要的是填写你当前服务器的IP地址加上监听端口（Go-CQHTTP的`server`-`http`-`address`那里的端口。）