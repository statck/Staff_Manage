from django.db import models

# Create your models here.
class Department(models.Model):
    """
        部门表
    """
    title = models.CharField(verbose_name="部门标题",max_length=32)

class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    # 性别
    gender_choices = (
        (1,"男"),
        (2,"女")
    )
    # 代码约束
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)
    password = models.CharField(verbose_name="密码", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    salary = models.DecimalField(verbose_name="账户余额",max_digits=10, decimal_places=2 , default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")
    # 无约束
    # depart_id = models.BigIntegerField(verbose_name="部门id")
    # 1. 有约束
    #  - to  : 与那张表关联
    #  - to_field : 与表中的那一列关联
    # 2.django自动设置
    #   - 写的depart
    #   - 生辰给的数据列 depart_id
    # 级联删除:部门删除，关联的用户也会删除
    # depart = models.ForeignKey(to="Department" , to_fields="id", on_delete=models.CASCADE())
    # 置空 ： 部门删除，关联的用户对应字段会成为空
    depart = models.ForeignKey(to="Department", to_field="id", null=True, blank=True, on_delete=models.SET_NULL)
