# -*- coding=utf-8 -*-
# 
# GK
"""
    自定义分页组件
"""
from django.utils.safestring import mark_safe
class PageNation():
    def __init__(self, request, qureyset, page_param="page",page_size= 50 , plus = 5):
        """

        :param request:  请求的对象
        :param qureyset:  # 复合条件的数据
        :param page_param:  # 在url中传递获取分页的参数
        :param page_size:  # 每页显示多少条数据
        :param plus:  # 页码展示的数量
        """
        import copy
        qurey_dict = copy.deepcopy(request.GET)
        qurey_dict._mutable = True
        self.query_dict = qurey_dict
        self.page_param = page_param


        # 获取当前页
        page = request.GET.get(page_param,"1") # 默认值设置成字符串格式
        if page.isdecimal():  # 判断page是否是十进制的数
            page = int(page)
        else:
            page = 1
        self.page = page
        self.page_size = page_size # 每页数据的条数
        self.start = (page-1) * page_size  # 数据开始
        self.end = page * page_size # 数据结束

        self.page_qureyset = qureyset[self.start:self.end]
        # 总页码数量
        total_count = qureyset.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        # 计算出当前页的前五页和后五页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中的数据比较少，都没有达到前后各五页的时候
            start_page = 1
            end_page = self.total_page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                # 当前页大于5
                # 判断极值  当前页+5 > 大于总页数
                if (self.page + self.plus) > self.total_page_count:
                    # 数据库中的数据比较多的时候
                    # 当前页小于5的时候：
                    start_page = self.total_page_count - 2 * self.plus
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus + 1
        page_str_list = []
        self.query_dict.setlist(self.page_param , [1])
        self.query_dict.urlencode()
        # 首页
        first_page = '<li ><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(first_page)
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li ><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li ><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        # 后一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            after = '<li ><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            after = '<li ><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(after)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        last_page = '<li ><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(last_page)
        search_string = """
        <li>
            <form style="float: left;margin-left: -1px" method="get" action="">
                <input name="page" style="position:relative;float: left;display: inline-block;width: 80px;
                border-radius: 0" type="text" class="form-control" placeholder="页码">
                <button style="border-radius: 0" class="btn btn-default" type="submit">跳转</button>
            </form>
        </li>
        """
        page_str_list.append(search_string)
        page_string = mark_safe("".join(page_str_list))
        return page_string
