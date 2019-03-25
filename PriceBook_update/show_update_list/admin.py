from django.contrib import admin
from show_update_list.models import *
# Register your models here.
admin.site.register([Z_Category,Assemble_Steps,Product,
                     Other_category,Monitor_type,Monitor_product,
                     AMO_step,AMO_Product,Pao_Product,
                     Custom_Made_install,Work_Service,
                     Huipu_User,PPS_CarePack_List_Price,Additional_software_value_added_services,
                     rulesName,userAssemble,Discount,RuleChoice])