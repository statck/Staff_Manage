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