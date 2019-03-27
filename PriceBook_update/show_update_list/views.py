import os
from io import BytesIO
import xlwt
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic import View
from show_update_list.models import *
from show_update_list.utils import get_hash, quick_sort
from django.urls import reverse
import re, json
from django.http import JsonResponse, HttpResponse
from .utils import Page, Page1
import uuid


class Index(View):
    """首页展示"""

    def get(self, request):
        return render(request, "PWS_PR_PriceBook/index.html")


class ISV_sales_tool(View):
    """ISV销售工具"""

    def get(self, request):
        return render(request, "PWS_PR_PriceBook/ISV_sales_tool.html")


class Z2_mini_G4(View):
    """Z2_mini_G4"""

    def get(self, request):
        id = request.GET.get("id")
        z2_mini_g4 = Z_Category.objects.get(id=int(id))
        name = z2_mini_g4.name
        step = z2_mini_g4.assemble_steps_set.all()
        qty = 0
        count = 0
        page = request.GET.get('page')
        contacts = Page(step, page)
        return render(request, "PWS_PR_PriceBook/Z2_mini_G4.html", locals())


class Monitor(View):
    """Monitor"""

    def get(self, request):
        monitor_type = Monitor_type.objects.all()
        page = request.GET.get('page')
        contacts = Page(monitor_type, page)
        return render(request, "PWS_PR_PriceBook/Monitor.html", locals())


class AMO(View):
    """AMO"""

    def get(self, request):
        amo_step = AMO_step.objects.all()
        page = request.GET.get('page')
        contacts = Page(amo_step, page)
        return render(request, "PWS_PR_PriceBook/AMO.html", locals())


class Pao_inner(View):
    """包内升级服务"""

    def get(self, request):
        pao_inner = Other_category.objects.get(id=3)
        page = request.GET.get('page')
        contacts = Page1(pao_inner.pao_product_set.all(), page)
        return render(request, "PWS_PR_PriceBook/upgrade_service.html", locals())


class Pao_out(View):
    """包内升级服务"""

    def get(self, request):
        pao_out = Other_category.objects.get(id=4)
        page = request.GET.get('page')
        contacts = Page1(pao_out.pao_product_set.all(), page)
        return render(request, "PWS_PR_PriceBook/extend_service.html", locals())


class Custom_Install(View):
    """定制及部署服务"""

    def get(self, request):
        custom_deploy = Custom_Made_install.objects.all()
        work_service = Work_Service.objects.all()
        return render(request, "PWS_PR_PriceBook/custom_deploy.html", locals())


class Added_Service(View):
    """"""

    def get(self, request):
        added_service_pps = PPS_CarePack_List_Price.objects.all()
        added_service_software = Additional_software_value_added_services.objects.all()
        return render(request, "PWS_PR_PriceBook/added_service.html", locals())


class Register(View):
    """注册用户"""

    def get(self, request):
        return render(request, "PWS_PR_PriceBook/register.html")

    def post(self, request):
        email = request.POST.get("InputEmail")
        password = request.POST.get("InputPassword")
        confirm_password = request.POST.get("ConfirmPassword")

        if not all([email, password, confirm_password]):
            return render(request, "PWS_PR_PriceBook/register.html", {"errmsg": '邮箱或密码不能为空'})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, "PWS_PR_PriceBook/register.html", {"errmsg": "邮箱格式不正确"})

        if password != confirm_password:
            return render(request, "PWS_PR_PriceBook/register.html", {"errmsg": '两次密码不一致'})

        if len(password) < 8:
            return render(request, "PWS_PR_PriceBook/register.html", {"errmsg": '密码不能少于8位'})

        try:
            user = Huipu_User.objects.get(email=email)
        except Huipu_User.DoesNotExist:
            user = None
        if user:
            return render(request, "PWS_PR_PriceBook/register.html", {"errmsg": "该邮箱已被注册"})

        security = get_hash(password)
        user = Huipu_User.objects.create(email=email, password=security)
        return redirect(reverse('show_list:login'))


class Login(View):
    """登录"""

    def get(self, request):
        return render(request, "PWS_PR_PriceBook/login.html")

    def post(self, request):
        email = request.POST.get("InputEmail")
        password = request.POST.get("InputPassword")
        if not all([email, password]):
            return render(request, "PWS_PR_PriceBook/login.html", {"errmsg": "邮箱或密码不能为空"})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, "PWS_PR_PriceBook/register.html", {"errmsg": "邮箱格式不正确"})

        try:
            user = Huipu_User.objects.get(email=email)
        except Huipu_User.DoesNotExist:
            user = None

        if user:
            if get_hash(password) == user.password:
                request.session['session_email'] = user.email  # 设置键和值
                request.session['super_user'] = user.super_user
                return render(request, "PWS_PR_PriceBook/index.html")
            else:
                return render(request, "PWS_PR_PriceBook/login.html", {"errmsg": "密码有误"})
        else:
            return render(request, "PWS_PR_PriceBook/login.html", {"errmsg": "邮箱不存在，请先注册"})


class Logout(View):
    """注销"""

    def get(self, request):
        del request.session['session_email']
        del request.session['super_user']
        return redirect(reverse("show_list:index"))


class Edit(View):
    """编辑Z系列"""

    def post(self, request):
        print("aaaa")
        id_number = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            product = Product.objects.get(id=int(id_number))
            return JsonResponse({"res": 1,
                                 "id": product.id,
                                 "name": product.name,
                                 "descrip": product.descrip,
                                 "rules_descrip": product.rules_descrip,
                                 "End_of_Manufacturing": product.End_of_Manufacturing,
                                 "CECP_EStar": product.CECP_EStar,
                                 "List_Price": product.List_Price,
                                 "Qty": product.Qty
                                 })
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class Z_Save(View):
    """Z系列修改存储"""

    def post(self, request):
        id = request.POST.get("id")
        pro = Product.objects.get(id=int(id))
        pro.name = request.POST.get("name")
        pro.descrip = request.POST.get("descrip")
        pro.rules_descrip = request.POST.get("rules_descrip")
        pro.End_of_Manufacturing = request.POST.get("End_of_Manufacturing")
        pro.CECP_EStar = request.POST.get("CECP_EStar")
        pro.List_Price = request.POST.get("List_Price")
        pro.Qty = request.POST.get("Qty")
        pro.save()
        return JsonResponse({"res": 1})


class Admin(View):
    """后台管理首页"""

    def get(self, request):
        if request.session['session_email']:
            email = request.session['session_email']
            user = Huipu_User.objects.get(email=email)
            if user.super_user:
                pro_categorys = Z_Category.objects.all()
                other_categorys = Other_category.objects.all()
                rulechoice = RuleChoice.objects.all()
                return render(request, "admin/admin.html", locals())
            else:
                return HttpResponse('<div>没有权限</div>')
        else:
            return HttpResponseRedirect("/user/login")


class Add_Z_category(View):
    """"""

    def get(self, request):
        return render(request, "admin/add_z_category.html")

    def post(self, request):
        category = request.POST.get("add_z")
        add = Z_Category.objects.create(name=category)
        return redirect(reverse("show_list:admin_auth"))


class Add_Other_category(View):
    """"""

    def get(self, request):
        return render(request, "admin/add_other_category.html")

    def post(self, request):
        category = request.POST.get("add_z")
        add = Other_category.objects.create(name=category)
        return redirect(reverse("show_list:admin_auth"))


class Del_Z_category(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        # Z_Category.objects.get(id=id).delete()
        return JsonResponse({"res": 1})


class Del_other_category(View):
    """"""

    def get(self, request):
        id = request.GET.get("id")
        # Other_category.objects.get(id=id).delete()
        return redirect(reverse("show_list:admin_auth"))


class Monitor_Edit(View):
    """编辑产品"""

    def post(self, request):
        id_number = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            product = Monitor_product.objects.get(id=int(id_number))
            return JsonResponse({"res": 1,
                                 "id": product.id,
                                 "name": product.name,
                                 "part_number": product.part_number,
                                 "size": product.size,
                                 "display_resolution": product.display_resolution,
                                 "port": product.port,
                                 "daisy_chain": product.daisy_chain,
                                 "byo": product.byo,
                                 "character": product.character,
                                 "price": product.price,
                                 })
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class Monitor_Save(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        pro = Monitor_product.objects.get(id=int(id))
        pro.name = request.POST.get("name")
        pro.part_number = request.POST.get("part_number")
        pro.size = request.POST.get("size")
        pro.display_resolution = request.POST.get("display_resolution")
        pro.port = request.POST.get("port")
        pro.daisy_chain = request.POST.get("daisy_chain")
        pro.byo = request.POST.get("byo")
        pro.character = request.POST.get("character")
        pro.price = request.POST.get("price")
        pro.save()
        return JsonResponse({"res": 1})


class Monitor_Del(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            # Monitor_product.objects.get(id=int(id)).delete()
            return JsonResponse({"res": 1})
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class Amo_Edit(View):
    """编辑产品"""

    def post(self, request):
        id_number = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            product = AMO_Product.objects.get(id=int(id_number))
            return JsonResponse({"res": 1,
                                 "id": product.id,
                                 "pid": product.pid,
                                 "market_descrip": product.market_descrip,
                                 "short_descrip": product.short_descrip,
                                 "rules_descrip": product.rules_descrip,
                                 "Phwab_Availability": product.Phwab_Availability,
                                 "End_of_Manufacturing": product.End_of_Manufacturing,
                                 "list_price": product.list_price,
                                 })
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class Amo_Save(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        pro = AMO_Product.objects.get(id=int(id))
        pro.pid = request.POST.get("pid")
        pro.market_descrip = request.POST.get("market_descrip")
        pro.short_descrip = request.POST.get("short_descrip")
        pro.rules_descrip = request.POST.get("rules_descrip")
        pro.Phwab_Availability = request.POST.get("Phwab_Availability")
        pro.End_of_Manufacturing = request.POST.get("End_of_Manufacturing")
        pro.list_price = request.POST.get("list_price")
        pro.save()
        return JsonResponse({"res": 1})


class AMO_Del(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            # AMO_Product.objects.get(id=int(id)).delete()
            return JsonResponse({"res": 1})
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class Pao_inner_Edit(View):
    """编辑产品"""

    def post(self, request):
        id_number = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            product = Pao_Product.objects.get(id=int(id_number))
            return JsonResponse({"res": 1,
                                 "id": product.id,
                                 "PL": product.PL,
                                 "HW_Product_Model": product.HW_Product_Model,
                                 "Standard_Warranty": product.Standard_Warranty,
                                 "Formulation": product.Formulation,
                                 "Upgrade_Service_Description": product.Upgrade_Service_Description,
                                 "CarePack_Part": product.CarePack_Part,
                                 "GL_Price": product.GL_Price,
                                 "Promotion_Price": product.Promotion_Price,
                                 })
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class Pao_inner_Save(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        pro = Pao_Product.objects.get(id=int(id))
        pro.PL = request.POST.get("PL")
        pro.HW_Product_Model = request.POST.get("HW_Product_Model")
        pro.Standard_Warranty = request.POST.get("Standard_Warranty")
        pro.Formulation = request.POST.get("Formulation")
        pro.Upgrade_Service_Description = request.POST.get("Upgrade_Service_Description")
        pro.CarePack_Part = request.POST.get("CarePack_Part")
        pro.GL_Price = request.POST.get("GL_Price")
        pro.Promotion_Price = request.POST.get("Promotion_Price")
        pro.save()
        return JsonResponse({"res": 1})


class Pao_Inner_Del(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            # Pao_Produc.objects.get(id=int(id)).delete()
            return JsonResponse({"res": 1})
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class CDS_Work_Edit(View):
    """编辑产品"""

    def post(self, request):
        id_number = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            product = Work_Service.objects.get(id=int(id_number))
            return JsonResponse({"res": 1,
                                 "id": product.id,
                                 "service_type": product.service_type,
                                 "service_descripe": product.service_descripe,
                                 "CarePack_GenericPart": product.CarePack_GenericPart,
                                 "GL_Price": product.GL_Price,
                                 "remark": product.remark,
                                 })
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class CDS_Work_Save(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        pro = Work_Service.objects.get(id=int(id))
        pro.service_type = request.POST.get("service_type")
        pro.service_descripe = request.POST.get("service_descripe")
        pro.CarePack_GenericPart = request.POST.get("CarePack_GenericPart")
        pro.GL_Price = request.POST.get("GL_Price")
        pro.remark = request.POST.get("remark")
        pro.save()
        return JsonResponse({"res": 1})


class CDS_Work_Del(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            # Work_Service.objects.get(id=int(id)).delete()
            return JsonResponse({"res": 1})
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class CDS_Install_Edit(View):
    """编辑产品"""

    def post(self, request):
        id_number = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            product = Custom_Made_install.objects.get(id=int(id_number))
            return JsonResponse({"res": 1,
                                 "id": product.id,
                                 "service_type": product.service_type,
                                 "protect_time": product.protect_time,
                                 "service_descripe": product.service_descripe,
                                 "CarePack_Part": product.CarePack_Part,
                                 "GL_Price_Unit": product.GL_Price_Unit,
                                 "remark": product.remark,
                                 })
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class CDS_Install_Save(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        pro = Custom_Made_install.objects.get(id=int(id))
        pro.service_type = request.POST.get("service_type")
        pro.protect_time = request.POST.get("protect_time")
        pro.service_descripe = request.POST.get("service_descripe")
        pro.CarePack_Part = request.POST.get("CarePack_Part")
        pro.GL_Price_Unit = request.POST.get("GL_Price_Unit")
        pro.remark = request.POST.get("remark")
        pro.save()
        return JsonResponse({"res": 1})


class CDS_Install_Del(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            # Custom_Made_install.objects.get(id=int(id)).delete()
            return JsonResponse({"res": 1})
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class PPS_Edit(View):
    """编辑产品"""

    def post(self, request):
        id_number = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            product = PPS_CarePack_List_Price.objects.get(id=int(id_number))
            return JsonResponse({"res": 1,
                                 "id": product.id,
                                 "Service_Style": product.Service_Style,
                                 "Hw_Pl": product.Hw_Pl,
                                 "HW_Product_Model": product.HW_Product_Model,
                                 "Wty_Style": product.Wty_Style,
                                 "Per_incident": product.Per_incident,
                                 "CarePack_of_Service_Option": product.CarePack_of_Service_Option,
                                 "CarePack_Part": product.CarePack_Part,
                                 "GL_Price": product.GL_Price,
                                 })
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class PPS_Save(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        pro = PPS_CarePack_List_Price.objects.get(id=int(id))
        pro.Service_Style = request.POST.get("Service_Style")
        pro.Hw_Pl = request.POST.get("Hw_Pl")
        pro.HW_Product_Model = request.POST.get("HW_Product_Model")
        pro.Wty_Style = request.POST.get("Wty_Style")
        pro.Per_incident = request.POST.get("Per_incident")
        pro.CarePack_of_Service_Option = request.POST.get("CarePack_of_Service_Option")
        pro.CarePack_Part = request.POST.get("CarePack_Part")
        pro.GL_Price = request.POST.get("GL_Price")
        pro.save()
        return JsonResponse({"res": 1})


class PPS_Del(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            # PPS_CarePack_List_Price.objects.get(id=int(id)).delete()
            return JsonResponse({"res": 1})
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class Additional_software_Edit(View):
    """编辑产品"""

    def post(self, request):
        id_number = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            product = Additional_software_value_added_services.objects.get(id=int(id_number))
            return JsonResponse({"res": 1,
                                 "id": product.id,
                                 "service_name": product.service_name,
                                 "servie_type": product.servie_type,
                                 "HP_Description": product.HP_Description,
                                 "CarePack_Part": product.CarePack_Part,
                                 "GL_Price_Unit": product.GL_Price_Unit,
                                 "promotion": product.promotion,
                                 })
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class Additional_software_Save(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        pro = Additional_software_value_added_services.objects.get(id=int(id))
        pro.service_name = request.POST.get("service_name")
        pro.servie_type = request.POST.get("servie_type")
        pro.HP_Description = request.POST.get("HP_Description")
        pro.CarePack_Part = request.POST.get("CarePack_Part")
        pro.GL_Price_Unit = request.POST.get("GL_Price_Unit")
        pro.promotion = request.POST.get("promotion")
        pro.save()
        return JsonResponse({"res": 1})


class Additional_software_Del(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            # Additional_software_value_added_services.objects.get(id=int(id)).delete()
            return JsonResponse({"res": 1})
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class Admin_Z_Product_del(View):
    """"""

    def post(self, request):
        id = request.POST.get("id")
        session_number = request.session.get('session_email')
        super = Huipu_User.objects.get(email=session_number)
        if super.super_user == 1:
            # Product.objects.get(id=id).delete()
            return JsonResponse({"res": 1})
        else:
            return JsonResponse({"res": 0, "errmsg": "您不是管理员，没权限"})


class Admin_Other_Category(View):
    """Monitor"""

    def get(self, request):
        id = request.GET.get("id")
        other_category = Other_category.objects.get(id=int(id))
        if id == "1":
            monitors = Monitor_type.objects.all()
            return render(request, "admin/monitor_type.html", locals())
        if id == "2":
            amo_steps = AMO_step.objects.all()
            return render(request, "admin/amo_step.html", locals())
        if id == "3":
            monitor_type = Other_category.objects.all()
            return render(request, "admin/edit_保内升级服务.html", locals())
        if id == "4":
            monitor_type = Other_category.objects.all()
            return render(request, "admin/edit_保内升级服务.html", locals())
        if id == "5":
            monitor_type = Other_category.objects.all()
            return render(request, "admin/edit_定制及部署服务.html", locals())
        if id == "6":
            monitor_type = Other_category.objects.all()
            return render(request, "admin/edit_增值服务.html", locals())


class Admin_Z_Product(View):
    """"""

    def get(self, request):
        id = request.GET.get("id")
        category = Assemble_Steps.objects.get(id=int(id))
        return render(request, "admin/admin_edit_z.html", locals())

    def post(self, request):
        step_id = request.POST.get("step_id")
        name = request.POST.get("name")
        descrip = request.POST.get("descrip")
        rules_descrip = request.POST.get("rules_descrip")
        End_of_Manufacturing = request.POST.get("End_of_Manufacturing")
        CECP_EStar = request.POST.get("CECP_EStar")
        List_Price = request.POST.get("List_Price")
        print(step_id, descrip, rules_descrip, End_of_Manufacturing, CECP_EStar, List_Price)
        Product.objects.create(name=name,
                               descrip=descrip,
                               rules_descrip=rules_descrip,
                               End_of_Manufacturing=End_of_Manufacturing,
                               CECP_EStar=CECP_EStar,
                               List_Price=List_Price,
                               assemble_product_id=int(step_id))
        return render(request, "admin/admin_edit_z.html", locals())


class Admin_Monitor(View):
    """显示器产品添加"""

    def get(self, request):
        monitor_type = Monitor_type.objects.all()
        return render(request, "admin/edit_Monitor.html", locals())

    def post(self, request):
        name = request.POST.get("monitor_category")
        part_number = request.POST.get("part_number")
        size = request.POST.get("size")
        display_resolution = request.POST.get("fps")
        port = request.POST.get("port")
        daisy_chain = request.POST.get("julian_string")
        byo = request.POST.get("own_string")
        character = request.POST.get("special")
        price = request.POST.get("price")
        select = request.POST.get("select")
        monitor = Monitor_type.objects.get(name=select).id
        Monitor_product.objects.create(name=name,
                                       part_number=part_number,
                                       size=size,
                                       display_resolution=display_resolution,
                                       port=port,
                                       daisy_chain=daisy_chain,
                                       byo=byo,
                                       character=character,
                                       price=price,
                                       monitor_type_id=int(monitor))
        return render(request, "admin/edit_Monitor.html")


class Admin_AMO(View):
    """AMO产品添加"""

    def get(self, request):
        monitor_type = AMO_step.objects.all()
        return render(request, "admin/edit_AMO.html", locals())

    def post(self, request):
        pid = request.POST.get("pid")
        market_descrip = request.POST.get("market_descrip")
        short_descrip = request.POST.get("short_descrip")
        rules_descrip = request.POST.get("rules_descrip")
        Phwab_Availability = request.POST.get("Phwab_Availability")
        End_of_Manufacturing = request.POST.get("End_of_Manufacturing")
        list_price = request.POST.get("list_price")
        select = request.POST.get("category")
        print(select)
        amo_id = AMO_step.objects.get(name=select).id
        print(amo_id)
        AMO_Product.objects.create(pid=pid,
                                   market_descrip=market_descrip,
                                   short_descrip=short_descrip,
                                   rules_descrip=rules_descrip,
                                   Phwab_Availability=Phwab_Availability,
                                   End_of_Manufacturing=End_of_Manufacturing,
                                   list_price=list_price,
                                   amo_id_id=amo_id
                                   )
        return render(request, "admin/edit_AMO.html")


class Admin_Pao(View):
    """包内保外产品添加"""

    def post(self, request):
        pao_name = request.POST.get("pao_inner")
        PL = request.POST.get("PL")
        HW_Product_Model = request.POST.get("HW_Product_Model")
        Standard_Warranty = request.POST.get("Standard_Warranty")
        Formulation = request.POST.get("Formulation")
        Upgrade_Service_Description = request.POST.get("Upgrade_Service_Description")
        CarePack_Part = request.POST.get("CarePack_Part")
        GL_Price = request.POST.get("GL_Price")
        Promotion_Price = request.POST.get("Promotion_Price")
        pao_inner = Other_category.objects.get(name=pao_name).id
        Pao_Product.objects.create(PL=PL,
                                   HW_Product_Model=HW_Product_Model,
                                   Standard_Warranty=Standard_Warranty,
                                   Formulation=Formulation,
                                   Upgrade_Service_Description=Upgrade_Service_Description,
                                   CarePack_Part=CarePack_Part,
                                   GL_Price=GL_Price,
                                   Promotion_Price=Promotion_Price,
                                   Standard_id_id=int(pao_inner))
        return render(request, "admin/edit_保内升级服务.html")


class Admin_custom_Made_install(View):
    """CDS-安装部署和服务日服务"""

    def post(self, request):
        service_type = request.POST.get("service_type")
        protect_time = request.POST.get("protect_time")
        service_descripe = request.POST.get("service_descripe")
        CarePack_Part = request.POST.get("CarePack_Part")
        GL_Price_Unit = request.POST.get("GL_Price_Unit")
        remark = request.POST.get("remark")
        Custom_Made_install.objects.create(service_type=service_type,
                                           protect_time=protect_time,
                                           service_descripe=service_descripe,
                                           CarePack_Part=CarePack_Part,
                                           GL_Price_Unit=GL_Price_Unit,
                                           remark=remark,
                                           blone_category_id=5)
        return render(request, "admin/edit_定制及部署服务.html")


class Admin_Work_Service(View):
    """CDS-工厂产线实施服务"""

    def post(self, request):
        service_type = request.POST.get("service_type")
        service_descripe = request.POST.get("service_descripe")
        CarePack_GenericPart = request.POST.get("CarePack_GenericPart")
        GL_Price = request.POST.get("GL_Price")
        remark = request.POST.get("remark")
        Work_Service.objects.create(service_type=service_type,
                                    service_descripe=service_descripe,
                                    CarePack_GenericPart=CarePack_GenericPart,
                                    GL_Price=GL_Price,
                                    remark=remark,
                                    blone_category_id=5)
        return render(request, "admin/edit_定制及部署服务.html")


class Admin_Additional_software(View):
    """附加的软件增值性服务"""

    def get(self, request):
        return render(request, "admin/edit_增值服务.html")

    def post(self, request):
        service_name = request.POST.get("service_name")
        servie_type = request.POST.get("servie_type")
        HP_Description = request.POST.get("HP_Description")
        CarePack_Part = request.POST.get("CarePack_Part")
        GL_Price_Unit = request.POST.get("GL_Price_Unit")
        promotion = request.POST.get("promotion")
        Additional_software_value_added_services.objects.create(service_name=service_name,
                                                                servie_type=servie_type,
                                                                HP_Description=HP_Description,
                                                                CarePack_Part=CarePack_Part,
                                                                GL_Price_Unit=GL_Price_Unit,
                                                                promotion=promotion,
                                                                blone_category_id=6)
        return render(request, "admin/edit_增值服务.html")


class Admin_PPS_CarePack_List_Price(View):
    """增值服务"""

    def post(self, request):
        Service_Style = request.POST.get("Service_Style")
        Hw_Pl = request.POST.get("Hw_Pl")
        HW_Product_Model = request.POST.get("HW_Product_Model")
        Wty_Style = request.POST.get("Wty_Style")
        Per_incident = request.POST.get("Per_incident")
        CarePack_of_Service_Option = request.POST.get("CarePack_of_Service_Option")
        CarePack_Part = request.POST.get("CarePack_Part")
        GL_Price = request.POST.get("GL_Price")
        PPS_CarePack_List_Price.objects.create(Service_Style=Service_Style,
                                               Hw_Pl=Hw_Pl,
                                               HW_Product_Model=HW_Product_Model,
                                               Wty_Style=Wty_Style,
                                               Per_incident=Per_incident,
                                               CarePack_of_Service_Option=CarePack_of_Service_Option,
                                               CarePack_Part=CarePack_Part,
                                               GL_Price=GL_Price,
                                               blone_category_id=6)
        return render(request, "admin/edit_增值服务.html")


class saveUserRules(View):
    """编辑保存用户配置规则"""

    def post(self, request):
        session_number = request.session.get('session_email')
        rules_id = request.POST.get('rules_id')
        radios = json.loads(request.POST.get('radios'))
        checkeds = json.loads(request.POST.get('checkeds'))
        new_arrays = radios + checkeds
        new_array = []
        for i in new_arrays:
            new_array.append(int(i))
        new_array1 = quick_sort(new_array)
        pro_number = len(new_array1)
        print(rules_id)
        rule = rulesName.objects.get(id=int(rules_id))
        rule.userassemble_set.all().delete()
        total_count = 0
        for array in new_array1:
            total_count += Product.objects.get(id=int(array)).List_Price
            userAssemble.objects.create(data_index_number=array, assemble_name_id=int(rules_id))
        vip_id = Huipu_User.objects.get(email=session_number).vip_range_id
        if vip_id:
            total_count = float(total_count) * float((Discount.objects.get(id=int(vip_id)).discount))
        print("aaa")
        rul = rulesName.objects.get(id=int(rules_id))
        rul.pro_number = pro_number
        rul.total_count = total_count
        rul.save()
        return JsonResponse({"msg": 1})


class saveUserRules2(View):
    """新建配置规则"""

    def post(self, request):
        session_number = request.session.get('session_email')
        rules_name = request.POST.get("rules_id")
        print(rules_name)
        radios = json.loads(request.POST.get('radios'))
        checkeds = json.loads(request.POST.get('checkeds'))
        pro_number = request.POST.get('count')
        total_count = request.POST.get('qty')
        print(pro_number, total_count)
        vip_id = Huipu_User.objects.get(email=session_number).vip_range_id
        if vip_id:
            total_count = float(total_count) * float((Discount.objects.get(id=int(vip_id)).discount))
        new_arrays = radios + checkeds
        new_array = []
        for i in new_arrays:
            new_array.append(int(i))
        new_array1 = quick_sort(new_array)
        print("bbb")
        rules_name1 = rules_name + '---' + str(uuid.uuid4())[:7]
        user_id = Huipu_User.objects.get(email=session_number).id
        rulesName.objects.create(name=rules_name1, pro_number=pro_number, total_count=total_count,
                                 blone_user_id=user_id)
        assemble_id = rulesName.objects.get(name=rules_name1).id
        cateID = rulesName.objects.get(name=rules_name1).id
        for array in sorted(new_array1):
            userAssemble.objects.create(data_index_number=array,
                                        assemble_name_id=assemble_id)
        return JsonResponse({"msg": 1, "cateID": cateID})


class showUserLabel(View):
    """展示用户配置标签"""

    def get(self, request):
        session_number = request.session.get('session_email')
        user_id = Huipu_User.objects.get(email=session_number).id
        labels = rulesName.objects.filter(blone_user=user_id)
        return render(request, "PWS_PR_PriceBook/user_rules_label.html", locals())


class DelUserLabel(View):
    """删除用户配置标签"""

    def get(self, request):
        id = request.GET.get("id")
        rulesName.objects.get(id=int(id)).delete()
        return redirect(reverse("show_list:user_label_show"))


class showUserRules(View):
    """展示用户详细配置规则"""

    # dict={"组装步骤1":['产品1','产品2']，"组装步骤2":['产品1','产品2']}
    def get(self, request):
        id = request.GET.get("id")
        label = rulesName.objects.get(id=int(id))
        rules = label.userassemble_set.all()
        qty = label.pro_number
        count = label.total_count
        pro = []
        for i in rules:
            pro.append(Product.objects.get(id=int(i.data_index_number)).name)
        pro_array = json.dumps(pro)
        for i in rules:
            z_category = Z_Category.objects.get(id=Assemble_Steps.objects.get(
                id=Product.objects.get(id=int(i.data_index_number)).assemble_product_id).assemble_category_id).id
            break
        pro_list = [{Assemble_Steps.objects.get(id=Product.objects.get(id=int(
            rule.data_index_number)).assemble_product_id).name: Product.objects.get(
            id=int(rule.data_index_number))} for rule in rules]
        return render(request, "PWS_PR_PriceBook/user_rules.html", locals(), {"pro_array": pro_array})


class Users(View):
    def get(self, request):
        users = Huipu_User.objects.all()

        return render(request, "admin/USER.html", locals())


class ShowDiscount(View):
    """管理折扣"""

    def get(self, request):
        discounts = Discount.objects.all()
        return render(request, "admin/discount.html", locals())


class AddDiscount(View):
    """增加折扣"""

    def get(self, request):
        return render(request, "admin/add_discount.html")

    def post(self, request):
        discount_price = request.POST.get("discount_price")
        discount = request.POST.get("discount")
        Discount.objects.create(vip=discount_price, discount=float(discount))
        return redirect(reverse("show_list:users"))


class User_disccount(View):
    """用户折扣"""

    def post(self, request):
        count = int(request.POST.get("totalPrice"))
        session_number = request.session.get('session_email')
        if session_number:
            range = Huipu_User.objects.get(email=session_number)
            if range.vip_range_id:
                discount = Discount.objects.get(id=range.vip_range_id).discount
                count = count * discount
                return JsonResponse({"res": 1, "totalPrice": count})
            else:
                return JsonResponse({"res": 1, "totalPrice": count})
        else:
            return JsonResponse({"res": 1, "totalPrice": count})


class Test(View):
    """"""

    def post(self, request):
        rules_id = request.POST.get("label")
        select_pros = rulesName.objects.get(id=int(rules_id)).userassemble_set.all()
        qty = len(select_pros)
        count = 0
        for i in select_pros:
            count = count + (Product.objects.get(id=int(i.data_index_number)).List_Price)
        id = request.POST.get("id")
        z2_mini_g4 = Z_Category.objects.get(id=int(id))
        contacts = z2_mini_g4.assemble_steps_set.all()
        step_list = []
        for i in contacts:
            step_list.append(i.name)
        step_list1 = json.dumps(step_list)
        html = render_to_string('PWS_PR_PriceBook/配置规则.html', locals())
        return JsonResponse(
            {"res": 1, "html": html, "cateName": z2_mini_g4.name, "step_list1": step_list1, "rules_id": rules_id})


class Test2(View):
    """"""

    def post(self, request):
        id = request.POST.get("cate_id")
        z2_mini_g4 = Z_Category.objects.get(id=int(id))
        label_name = z2_mini_g4.name
        contacts = z2_mini_g4.assemble_steps_set.all()
        step_list = []
        for i in contacts:
            step_list.append(i.name)
        step_list1 = json.dumps(step_list)
        html = render_to_string('PWS_PR_PriceBook/配置规则.html', locals())
        return JsonResponse({"res": 1, "html": html, "step_list1": step_list1, "label_name": label_name})


class Vip_edit(View):
    """"""

    def get(self, request):
        id = request.GET.get("id")
        email = Huipu_User.objects.get(id=int(id))
        vips = Discount.objects.all()
        return render(request, "admin/user_edit.html", locals())

    def post(self, request):
        vip = request.POST.get("select")
        user = request.POST.get("email")
        print(user, vip)
        a = Huipu_User.objects.get(email=user)
        a.vip_range_id = Discount.objects.get(vip=vip).id
        a.save()
        return redirect(reverse("show_list:users"))


class ShowCategory(View):
    """"""

    def get(self, request):
        category = Z_Category.objects.all()
        return render(request, "PWS_PR_PriceBook/show_category.html", locals())


class ShowAssembleStep(View):
    """"""

    def get(self, request):
        id = request.GET.get("id")
        category = Z_Category.objects.get(id=int(id))
        return render(request, "PWS_PR_PriceBook/assemble_step.html", locals())


class AddAssembleStep(View):
    """"""

    def get(self, request):
        id = request.GET.get('id')
        return render(request, "PWS_PR_PriceBook/add_assemble_step.html", locals())

    def post(self, request):
        id = request.POST.get("category")
        name = request.POST.get("name")
        choice = request.POST.get("choice")
        rules = request.POST.get("rules")
        print(id, name)
        Assemble_Steps.objects.create(name=name, choice=choice, Rules=rules, assemble_category_id=int(id))
        return redirect(reverse("show_list:admin_auth"))


class DelAssembleStep(View):
    """"""

    def get(self, request):
        id = request.GET.get("id")
        Assemble_Steps.objects.get(id=int(id)).delete()
        return redirect(reverse("show_list:admin_auth"))


class ShowAssemblePdoduct(View):
    ''''''

    def get(self, request):
        id = request.GET.get("id")
        step = Assemble_Steps.objects.get(id=int(id))
        return render(request, "PWS_PR_PriceBook/show_peoduct.html", locals())


class AddLimit(View):
    """"""

    def get(self, request):
        return render(request, "admin/limit.html")

    def post(self, request):
        limit = request.POST.get("limit")
        less = request.POST.get("less")
        more = request.POST.get("more")
        RuleChoice.objects.create(choice=limit, less=int(less), more=int(more))
        return render(request, "admin/limit.html")


class DelLimit(View):
    """"""

    def get(self, request):
        id = request.GET.get("id")
        RuleChoice.objects.get(id=int(id)).delete()
        return redirect(reverse('show_list:admin_auth'))


class ShowMonitorPro(View):
    """"""

    def get(self, request):
        id = request.GET.get("id")
        monitor_pros = Monitor_type.objects.get(id=int(id)).monitor_product_set.all()
        return render(request, "admin/show_monitor.html", locals())


class AddMonitorType(View):
    """"""

    def get(self, request):
        return render(request, "admin/add_monitor_type.html")

    def post(self, request):
        monitor_type = request.POST.get("monitor_category")
        Monitor_type.objects.create(name=monitor_type, category_id_id=1)
        return render(request, "admin/add_monitor_type.html", {"msg": "添加成功"})


class DelMonitorType(View):
    """"""

    def get(self, request):
        id = request.GET.get("id")
        Monitor_type.objects.get(id=int(id)).delete()
        return redirect(reverse("show_list:admin_auth"))


class ShowAmoPro(View):
    """"""

    def get(self, request):
        id = request.GET.get("id")
        print(id)
        amo_pros = AMO_step.objects.get(id=int(id)).amo_product_set.all()
        return render(request, "admin/amo_pro.html", locals())


class AddAmoStep(View):
    """"""

    def get(self, request):
        return render(request, "admin/add_amo_step.html", locals())

    def post(self, request):
        amo_step = request.POST.get("amo_step")
        print(amo_step)
        AMO_step.objects.create(name=amo_step, category_id_id=2)
        return render(request, "admin/add_amo_step.html", locals())


class DelAmoStep(View):
    """"""

    def get(self, request):
        id = request.GET.get("id")
        AMO_step.objects.get(id=int(id)).delete()
        return redirect(reverse("show_list:admin_auth"))


class PDF(View):
    """
        导出excel表格
        """

    def get(self, request):
        id = request.GET.get("id")
        label = rulesName.objects.get(id=int(id))
        rules = label.userassemble_set.all()
        qty = label.pro_number
        count = label.total_count
        pro = []
        for i in rules:
            pro.append(Product.objects.get(id=int(i.data_index_number)).name)
        pro_array = json.dumps(pro)
        for i in rules:
            z_category = Z_Category.objects.get(id=Assemble_Steps.objects.get(
                id=Product.objects.get(id=int(i.data_index_number)).assemble_product_id).assemble_category_id).id
            break
        pro_list = [{Assemble_Steps.objects.get(id=Product.objects.get(id=int(
            rule.data_index_number)).assemble_product_id).name: Product.objects.get(
            id=int(rule.data_index_number))} for rule in rules]
        if pro_list:
            ws = xlwt.Workbook(encoding='utf8')
            w = ws.add_sheet(u"%s" % (label.name))
            w.write(0, 0, u"部件订货号")
            w.write(0, 1, u"产品描述")
            w.write(0, 2, u"End of Manufacturing")
            w.write(0, 3, u"List Price")
            excel_row = 1
            for pro in pro_list:
                for j, k in pro.items():
                    print(j, k)
                    w.write(excel_row, 0, k.name)
                    w.write(excel_row, 1, k.descrip)
                    w.write(excel_row, 2, k.End_of_Manufacturing)
                    w.write(excel_row, 3, k.List_Price)
                    excel_row += 1
            exist_file = os.path.exists("%s.xls" % (label.name))
            if exist_file:
                os.remove(r"%s.xls" % (label.name))
            ws.save("%s.xls" % (label.name))
            sio = BytesIO()
            ws.save(sio)
            sio.seek(0)
            response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s.xls' % (label.name)
            response.write(sio.getvalue())
            return response


class IndexSaveRules(View):
    """首页保存配置规则"""

    def post(self, request):
        localData = request.POST.get('localData')
        localPrice = request.POST.get('localPrice')
        name = request.POST.get('z-name')
        session_number = request.session.get('session_email')
        localData = json.loads(localData)
        localPrice = json.loads(localPrice)
        pro_number = len(localData)
        total_count = 0
        for price in localPrice:
            total_count = total_count + int(price)
        vip_id = Huipu_User.objects.get(email=session_number).vip_range_id
        if vip_id:
            total_count = float(total_count) * float((Discount.objects.get(id=int(vip_id)).discount))
        rules_name = name + '---' + str(uuid.uuid4())[:7]
        user_id = Huipu_User.objects.get(email=session_number).id
        rulesName.objects.create(name=rules_name, pro_number=pro_number, total_count=total_count,
                                 blone_user_id=user_id)
        assemble_id = rulesName.objects.get(name=rules_name).id
        for array in sorted(localData):
            userAssemble.objects.create(data_index_number=array,
                                        assemble_name_id=assemble_id)
        return JsonResponse({"res": 1})


class IndexExportExcel(View):
    """
        导出excel表格
        """

    def post(self, request):
        localData = request.POST.get('localData')
        localPrice = request.POST.get('localPrice')
        name = request.POST.get('z-name')
        localData = json.loads(localData)
        localPrice = json.loads(localPrice)
        pro_number = len(localData)
        total_count = 0
        for price in localPrice:
            total_count = total_count + int(price)
        excel_name = name + '---' + str(uuid.uuid4())[:7]
        if localData:
            ws = xlwt.Workbook(encoding='utf8')
            w = ws.add_sheet(u"%s" % (excel_name))
            w.write(0, 0, u"部件订货号")
            w.write(0, 1, u"产品描述")
            w.write(0, 2, u"End of Manufacturing")
            w.write(0, 3, u"List Price")
            excel_row = 1
            for pro in localData:
                k = Product.objects.get(id=int(pro))
                w.write(excel_row, 0, k.name)
                w.write(excel_row, 1, k.descrip)
                w.write(excel_row, 2, k.End_of_Manufacturing)
                w.write(excel_row, 3, k.List_Price)
                excel_row += 1
            exist_file = os.path.exists("%s.xls" % (excel_name))
            if exist_file:
                os.remove(r"%s.xls" % (excel_name))
            ws.save("%s.xls" % (excel_name))
            sio = BytesIO()
            ws.save(sio)
            sio.seek(0)
            response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=%s.xls' % (excel_name)
            response.write(sio.getvalue())
            return response
