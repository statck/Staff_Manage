from django.shortcuts import render,redirect
from staff_manage.utils.pagenation import *
from staff_manage import models
from staff_manage.utils.form import UserModelForm,PrettyModelForm,PrettyEditModelForm

def depart_list(request):
    """部门列表"""
    # 类似于列表[]
    queryset = models.Department.objects.all()  # 获取数据库中部门列表的所有信息

    # 添加分页功能    2023.10.12
    page_obj = PageNation(request,queryset)
    context = {
        "queryset": page_obj.page_qureyset,
        "page_string": page_obj.html()
    }

    return render(request, "depart_index.html",context)
def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request , "depart_add.html")
    # 获取用户提交的数据
    title = request.POST.get("title")
    # 保存到数据库  在部门数据表中创建新的数据
    models.Department.objects.create(title = title)
    # 重定向到数据路列表
    return redirect("/depart/list/")
def depart_delete(request):
    """部门删除操作"""
    # 获取nid
    nid = request.GET.get("nid") # 使用GET方法获取nid
    # 删除操作 根据id编号删除数据表中的数据
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
    title = request.POST.get("title") # 获取修改后的信息
    # 更新数据表中的信息
    models.Department.objects.filter(id = nid).update(title=title)
    # 重定向回
    return redirect("/depart/list/")
# 用户管理
def user_list(request):
    # 获取所有的信息列表
    qureyset = models.UserInfo.objects.all()
    # 添加分页  2023.10.12
    page_obj = PageNation(request , qureyset)
    context = {
        "items": page_obj.page_qureyset,
        "page_string":page_obj.html()
    }

    return render(request , 'user_list.html' , context)
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
def number_list(request):
    """靓号列表"""



    search_data = request.GET.get("q","")
    data_dic = {}
    if search_data:
        data_dic["mobile__contains"] = search_data
    qureyset = models.PrettyNum.objects.filter(**data_dic)
    page_object = PageNation(request, qureyset)
    print(page_object.page_qureyset)
    print(page_object.html())
    context = {
        "search_data" : search_data,
        "all_num": page_object.page_qureyset, # 分完页的数据
        "page_string": page_object.html(), # 页码
    }
    return render(request , 'number_list.html',context)
def number_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, "number_add.html" , {"form" : form})
    elif request.method == "POST":
        form = PrettyModelForm(data=request.POST)
        if form.is_valid():
            # 如果数据合法 则记录数据
            form.save()
            return redirect("/number/list/")
        else:
            # 校验失败
            return render(request, "number_add.html", {"form": form})
    else:
        form = PrettyModelForm()
        return render(request, "number_add.html", {"form": form})
def number_edit(request , nid):
    """编辑用户"""
    # 根据id获取需要编辑的数据
    row_obj = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_obj)
        return render(request, "number_edit.html", {"form":form})
    elif request.method == "POST":
        form = PrettyEditModelForm(data=request.POST, instance=row_obj)
        if form.is_valid():
            # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一些值，可在保存前对目标字段名进行赋值操作
            # form.instance.字段名 = 值
            form.save()
            return redirect("/number/list/")
    else:
        form = PrettyEditModelForm(instance=row_obj)
        return render(request, "number_edit.html", {"form":form})

def number_delete(request , nid):
    models.PrettyNum.objects.filter(id = nid).delete()
    return redirect("/number/list/")

