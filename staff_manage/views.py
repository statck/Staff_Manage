from django.shortcuts import render,redirect , HttpResponse
from staff_manage import models
# Create your views here.
def depart_list(request):
    """部门列表"""
    # 类似于列表[]
    queryset = models.Department.objects.all()
    return render(request, "depart_index.html",{"queryset":queryset})

def depart_add(request):
    """添加部门"""
    if request.method=="GET":

        return render(request , "depart_add.html")
    # 获取用户提交的数据
    title = request.POST.get("title")
    # 保存到数据库
    models.Department.objects.create(title = title)
    # 重定向到数据路列表
    return redirect("/depart/list/")

def depart_delete(request):
    """部门删除操作"""
    # 获取nid
    nid = request.GET.get("nid")
    # 删除操作
    models.Department.objects.filter(id=nid).delete()
    # 重定向回
    return redirect("/depart/list/")

def depart_edit(request , nid):
    """ 部门修改操作 """
    if request.method == "GET":
        # 根据nid获取它的数据
        row_obj = models.Department.objects.filter(id=nid).first()

        # print(row_obj.id , row_obj.title)
        return render(request,"depart_edit.html", {"title": row_obj})
    # 用户提交的修改信息
    title = request.POST.get("title")
    models.Department.objects.filter(id = nid).update(title=title)
    # 重定向回
    return redirect("/depart/list/")

# 用户管理
def user_list(request):
    all_info = models.UserInfo.objects.all()
    return render(request , 'user_list.html' , {"items":all_info})
def user_add(request):
    """添加用户"""
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_choices': models.Department.objects.all()
        }
        return render(request , 'user_add.html' , context)
    elif request.method == "POST":
        # 获取用户提交的数据
        user = request.POST.get("user")
        gender_id = request.POST.get("gender_id")
        age = request.POST.get("age")
        ctime = request.POST.get("create_time")
        depart = request.POST.get("depart_id")
        salary = request.POST.get("salary")
        pwd = request.POST.get("pwd")
        # 数据校验：

        models.UserInfo.objects.create(name=user,age=age,gender=gender_id,
                                       create_time=ctime,depart_id=depart,
                                       salary=salary,password=pwd)
        return redirect('/user/list/')
    else:
        return redirect('/user/list/')

    # models.UserInfo.objects.create(name=user, password=pwd, age=age, gender=gender_id, create_time=ctime, depart_id=depart, salary=salary)

    # 添加成功后，返回到用户列表
    # return redirect("/user/list/")

######################################### modelform 示例
from django import forms
class UserModelForm(forms.ModelForm):
    name = forms.CharField(min_length=3 , label="用户名")
    password = forms.CharField(label="密码" )
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "create_time","gender", "depart"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }
    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name , filed in self.fields.items():
            filed.widget.attrs = {"class": "form-control","placeholder":filed.label}
def user_model_form_add(request):
    """基于modelform添加用户"""
    if request.method == "GET":
        form = UserModelForm()
        return render(request , "user_modelform_add.html", {"form": form})
    elif request.method == "POST":
        form = UserModelForm(data=request.POST)
        if form.is_valid():
            # 如果数据合法 则记录数据
            # print(form.cleaned_data)
            form.save()
            return redirect("/user/list/")
        else:
            # 校验失败
            return render(request, "user_modelform_add.html" , {"form":form})
            # print(form.errors)

def user_edit(request , nid):
    """编辑用户"""
    # 根据id获取需要编辑的数据
    row_obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # row_obj = models.UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_obj)

        return render(request , "user_edit.html", {"form":form})
    elif request.method == "POST":

        form = UserModelForm(data=request.POST, instance=row_obj)
        if form.is_valid():
            # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一些值，可在保存前对目标字段名进行赋值操作
            # form.instance.字段名 = 值
            form.save()
            return redirect("/user/list/")
        else:
            form.errors()
        return render(request , "user_edit.html", {"form":form})
def user_delete(request, nid):
    models.UserInfo.objects.filter(id = nid).delete()
    return redirect("/user/list/")

