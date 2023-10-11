from django.shortcuts import render,redirect , HttpResponse
from staff_manage import models
from django.utils.safestring import mark_safe
# Create your views here.
def depart_list(request):
    """部门列表"""
    # 类似于列表[]
    queryset = models.Department.objects.all()  # 获取数据库中部门列表的所有信息
    return render(request, "depart_index.html",{"queryset":queryset})

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

# import random
def number_list(request):
    """靓号列表"""
    # 常用搜索操作
    # models.PrettyNum.objects.filter(id=12) # 等于12
    # models.PrettyNum.objects.filter(id__gt=12)  # 大于12
    # models.PrettyNum.objects.filter(id__gte=12)  # 大于等于
    # models.PrettyNum.objects.filter(id__lt=12)  # 小于12
    # models.PrettyNum.objects.filter(id__lte=12)  # 小于等于12
    #
    # # 字典的形式进行搜索
    # data_dict = {"id_lte":12}
    # models.PrettyNum.objects.filter(**data_dict)
    # # 字段
    # models.PrettyNum.objects.filter(mobile="999")  # 等于999
    # models.PrettyNum.objects.filter(mobile__startswith="999")  # 以999开头
    # models.PrettyNum.objects.filter(mobile__endswith="999")  # 以999结束
    # models.PrettyNum.objects.filter(id=12)  # 等于12
    # mobile_s = 17623453643
    #
    # for i in range(300):
    #     mobile_s = mobile_s + i
    #     price = 999 + i
    #     level = random.randint(1, 6)
    #     status = random.randint(0, 1)
    #     models.PrettyNum.objects.create(mobile=str(mobile_s), price = price , level=level, status=status)

    keyword = request.GET.get("q","")
    search_dic = {}
    if keyword:
        search_dic["mobile__contains"] = keyword
    # 根据用户想要访问的页码。计算起始位置和终止位置
    page = int(request.GET.get('page',1))
    page_size = 100
    start = (page-1) * page_size
    end = page * page_size

    all_num = models.PrettyNum.objects.filter(**search_dic).order_by("-level")[start:end]
    total_count = models.PrettyNum.objects.filter(**search_dic).order_by("-level").count()
    # 计算出当前页的前五页和后五页
    # 页码：
    page_count,div = divmod(total_count, page_size)
    if div:
        page_count += 1
    plus = 5
    if page_count <= 2 * plus + 1:
        # 数据库中的数据比较少，都没有达到前后各五页的时候
        start_page = 1
        end_page = page_count
    else:
        if page <= plus:
            start_page = 1
            end_page = 2*plus + 1
        else:
            # 当前页大于5
            # 判断极值  当前页+5 > 大于总页数
            if (page + plus) > page_count:
                # 数据库中的数据比较多的时候
                # 当前页小于5的时候：
                start_page = page_count - 2 * plus
                end_page = page_count + 1
            else:
                start_page = page - plus
                end_page = page + plus + 1

    page_str_list = []
    # 首页
    first_page = '<li ><a href="?page={}">首页</a></li>'.format(1)
    page_str_list.append(first_page)
    # 上一页
    if page > 1:
        prev = '<li ><a href="?page={}">上一页</a></li>'.format(page -1)
    else:
        prev = '<li ><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)
    for i in range(start_page, end_page):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i,i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    # 后一页
    if page < page_count:
        after = '<li ><a href="?page={}">下一页</a></li>'.format(page+1)
    else:
        after = '<li ><a href="?page={}">下一页</a></li>'.format(page_count)
    page_str_list.append(after)
    # 尾页
    last_page = '<li ><a href="?page={}">尾页</a></li>'.format(page_count)
    page_str_list.append(last_page)
    page_string = mark_safe("".join(page_str_list))

    return render(request , 'number_list.html',{"all_num":all_num , "page_string":page_string})



from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
class PrettyModelForm(forms.ModelForm):
    # 验证方式一：
    # mobile = forms.CharField(label="手机号",validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误，必须以1开头，且为11位数字')])
    class Meta:
        model = models.PrettyNum
        fields = ["mobile","price","level","status"]
        fields = "__all__"
        # exclude = [“price”] # 排除字段
    def __init__(self , *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name , filed in self.fields.items():
            filed.widget.attrs = {"class": "form-control","placeholder":filed.label}
    # 验证方式二：
    def clean_mobile(self):  # 钩子函数
        print(self.instance.pk)
        txt_mobile = self.cleaned_data["mobile"]
        exits_flag = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exits_flag:
            raise ValidationError("号码已存在！")
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        return txt_mobile
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
class PrettyEditModelForm(forms.ModelForm):
    mobile = forms.CharField(disabled=True, label="手机号")
    class Meta:
        model = models.PrettyNum
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, filed in self.fields.items():
            filed.widget.attrs = {"class": "form-control", "placeholder": filed.label}
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

