from django.db import models

# Create your models here.
class Department(models.Model):
    """
        部门表
    """
    title = models.CharField(verbose_name="部门标题",max_length=32)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    # 性别
    gender_choices = (
        (1, "男"),
        (2, "女")
    )
    # 代码约束
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)
    password = models.CharField(verbose_name="密码", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    salary = models.DecimalField(verbose_name="账户余额",max_digits=10, decimal_places=2 , default=0)
    create_time = models.DateField(verbose_name="入职时间")
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)

class PrettyNum(models.Model):
    """靓号管理"""
    # 如果允许为空，则需要设置参数 null=True,blank=True
    mobile = models.CharField(verbose_name="手机号" , max_length=32)
    price = models.IntegerField(verbose_name="价格")
    level_choices = (
        (1,"1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
        (5, "5级"),
        (6, "6级"),
    )
    # 设置等级默认值
    level = models.SmallIntegerField(verbose_name="级别" , choices=level_choices ,default=1)
    status_choices = (
        (1,"已占用"),
        (0,"未使用")
    )
    # 设置状态值
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices , default=0)