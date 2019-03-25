from django.db import models
from django.contrib.auth.models import AbstractUser


class Z_Category(models.Model):
    """Z系列分类"""
    name = models.CharField(max_length=50, verbose_name="Z系列分类")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Z系列分类"
        verbose_name_plural = verbose_name


class RuleChoice(models.Model):
    """"""
    choice = models.CharField(max_length=50, verbose_name="选项")
    less = models.IntegerField(verbose_name="最少")
    more = models.IntegerField(verbose_name="最多")
    def __str__(self):
        return self.choice

    class Meta:
        verbose_name = "配置选项"
        verbose_name_plural = verbose_name

class Assemble_Steps(models.Model):
    """组装步骤"""
    name = models.CharField(max_length=100, verbose_name="组装步骤")
    choice = models.CharField(max_length=100, verbose_name="选项", blank=True)
    Rules = models.TextField(max_length=500, blank=True)
    assemble_category = models.ForeignKey("Z_Category", on_delete=models.CASCADE)
    belone_choice = models.ForeignKey("RuleChoice")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "组装步骤"
        verbose_name_plural = verbose_name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="部件订货号")
    descrip = models.CharField(max_length=100, verbose_name="产品描述")
    rules_descrip = models.TextField(max_length=500, verbose_name="配置规则", blank=True)
    End_of_Manufacturing = models.CharField(max_length=100, verbose_name="停产时间")
    CECP_EStar = models.CharField(max_length=100)
    List_Price = models.IntegerField(verbose_name="价格")
    Qty = models.CharField(max_length=50, blank=True)
    assemble_product = models.ForeignKey("Assemble_Steps", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "组装产品"
        verbose_name_plural = verbose_name


class Other_category(models.Model):
    name = models.CharField(max_length=20, verbose_name="其他分类")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "其他分类"
        verbose_name_plural = verbose_name


class Monitor_type(models.Model):
    """显示器分类"""
    name = models.CharField(max_length=50, verbose_name="显示器分类")
    category_id = models.ForeignKey("Other_category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "显示器分类"
        verbose_name_plural = verbose_name


class Monitor_product(models.Model):
    """显示器参数"""
    name = models.CharField(max_length=50, verbose_name="显示器名称")
    part_number = models.CharField(max_length=50, verbose_name="编号")
    size = models.FloatField(verbose_name="尺寸")
    display_resolution = models.CharField(max_length=50, verbose_name="分辨率")
    port = models.TextField(verbose_name="接口")
    daisy_chain = models.CharField(max_length=10, verbose_name="菊链布线支持")
    byo = models.TextField(verbose_name="自带线缆")
    character = models.TextField(verbose_name="特性")
    price = models.IntegerField(verbose_name="价格")
    monitor_type = models.ForeignKey("Monitor_type", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "显示器参数"
        verbose_name_plural = verbose_name


class AMO_step(models.Model):
    name = models.TextField(verbose_name="AMO步骤描述")
    category_id = models.ForeignKey("Other_category", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "AMO步骤"
        verbose_name_plural = verbose_name


class AMO_Product(models.Model):
    """AMO产品"""
    pid = models.CharField(max_length=50, verbose_name="产品编号")
    market_descrip = models.TextField(verbose_name="具体描述")
    short_descrip = models.TextField(verbose_name="简短描述")
    rules_descrip = models.TextField(verbose_name="规则描述", blank=True)
    Phwab_Availability = models.CharField(max_length=50, verbose_name="到期时间")
    End_of_Manufacturing = models.CharField(max_length=50, verbose_name="停产日期")
    list_price = models.IntegerField()
    amo_id = models.ForeignKey("AMO_step", on_delete=models.CASCADE)

    def __str__(self):
        return self.pid

    class Meta:
        verbose_name = "AMO产品"
        verbose_name_plural = verbose_name


class Pao_Product(models.Model):
    """保内产品参数"""
    PL = models.CharField(max_length=20, verbose_name="PL")
    HW_Product_Model = models.TextField()
    Standard_Warranty = models.CharField(max_length=20, verbose_name="Standard Warranty")
    Formulation = models.CharField(max_length=100)
    Upgrade_Service_Description = models.TextField()
    CarePack_Part = models.CharField(max_length=50)
    GL_Price = models.CharField(max_length=50)
    Promotion_Price = models.CharField(max_length=50, blank=True)
    Standard_id = models.ForeignKey("Other_category", on_delete=models.CASCADE)

    def __str__(self):
        return self.Formulation

    class Meta:
        verbose_name = "保内产品参数"
        verbose_name_plural = verbose_name


class Custom_Made_install(models.Model):
    """定制服务——CDS-安装部署和服务日服务"""
    service_type = models.CharField(max_length=100, verbose_name="服务类型")
    protect_time = models.CharField(max_length=10, verbose_name="预计时间")
    service_descripe = models.TextField(verbose_name="服务描述")
    CarePack_Part = models.CharField(max_length=100)
    GL_Price_Unit = models.CharField(max_length=50)
    remark = models.TextField(blank=True)
    blone_category = models.ForeignKey("Other_category", on_delete=models.CASCADE)

    def __str__(self):
        return self.CarePack_Part

    class Meta:
        verbose_name = "定制服务——CDS-安装部署和服务日服务"
        verbose_name_plural = verbose_name


class Work_Service(models.Model):
    """定制服务——CDS-工厂产线实施服务"""
    service_type = models.CharField(max_length=100, verbose_name="服务类型")
    service_descripe = models.TextField(verbose_name="服务描述")
    CarePack_GenericPart = models.CharField(max_length=100)
    GL_Price = models.CharField(max_length=50)
    remark = models.TextField(blank=True)
    blone_category = models.ForeignKey("Other_category", on_delete=models.CASCADE)

    def __str__(self):
        return self.CarePack_GenericPart

    class Meta:
        verbose_name = "定制服务——CDS-工厂产线实施服务"
        verbose_name_plural = verbose_name


class PPS_CarePack_List_Price(models.Model):
    """增值服务"""
    Service_Style = models.CharField(max_length=50)
    Hw_Pl = models.CharField(max_length=50)
    HW_Product_Model = models.CharField(max_length=50)
    Wty_Style = models.CharField(max_length=50)
    Per_incident = models.CharField(max_length=50)
    CarePack_of_Service_Option = models.CharField(max_length=50)
    CarePack_Part = models.CharField(max_length=50)
    GL_Price = models.CharField(max_length=50)
    blone_category = models.ForeignKey("Other_category", on_delete=models.CASCADE)

    def __str__(self):
        return self.CarePack_Part

    class Meta:
        verbose_name = "FY15 PPS CarePack List Price"
        verbose_name_plural = verbose_name


class Additional_software_value_added_services(models.Model):
    """附加的软件增值性服务"""
    service_name = models.CharField(max_length=100, verbose_name="服务名称")
    servie_type = models.CharField(max_length=100, verbose_name="服务类型")
    HP_Description = models.CharField(max_length=100)
    CarePack_Part = models.CharField(max_length=100)
    GL_Price_Unit = models.CharField(max_length=100)
    promotion = models.CharField(max_length=100, blank=True)
    blone_category = models.ForeignKey("Other_category", on_delete=models.CASCADE)

    def __str__(self):
        return self.CarePack_Part

    class Meta:
        verbose_name = "附加的软件增值性服务"
        verbose_name_plural = verbose_name


class rulesName(models.Model):
    """用户配置标签"""
    name = models.CharField(max_length=50, verbose_name="配置标签")
    pro_number = models.IntegerField(verbose_name="部件数量")
    total_count = models.IntegerField(verbose_name="总价")
    blone_user = models.ForeignKey("Huipu_User", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户配置标签"
        verbose_name_plural = verbose_name


class userAssemble(models.Model):
    """用户自定义组装"""
    data_index_number = models.CharField(max_length=10, verbose_name="产品ID")
    assemble_name = models.ForeignKey("rulesName", on_delete=models.CASCADE)

    def __str__(self):
        return self.data_index_number

    class Meta:
        verbose_name = "用户自定义组装"
        verbose_name_plural = verbose_name


class Discount(models.Model):
    """折扣"""
    vip = models.CharField(max_length=20, verbose_name="会员等级")
    discount = models.DecimalField(max_digits=1, decimal_places=1)

    class Meta:
        verbose_name = "折扣"
        verbose_name_plural = verbose_name


class Huipu_User(models.Model):
    """用户表"""
    email = models.EmailField(verbose_name="邮箱")
    password = models.CharField(max_length=100, verbose_name="密码")
    super_user = models.BooleanField(default=False, verbose_name="是否为管理员")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    vip_range = models.ForeignKey("Discount", on_delete=models.CASCADE)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "用户表"
        verbose_name_plural = verbose_name
