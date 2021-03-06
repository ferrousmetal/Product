# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-12-29 12:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Additional_software_value_added_services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100, verbose_name='服务名称')),
                ('servie_type', models.CharField(max_length=100, verbose_name='服务类型')),
                ('HP_Description', models.CharField(max_length=100)),
                ('CarePack_Part', models.CharField(max_length=100)),
                ('GL_Price_Unit', models.CharField(max_length=100)),
                ('promotion', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': '附加的软件增值性服务',
                'verbose_name_plural': '附加的软件增值性服务',
            },
        ),
        migrations.CreateModel(
            name='AMO_Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.CharField(max_length=50, verbose_name='产品编号')),
                ('market_descrip', models.TextField(verbose_name='具体描述')),
                ('short_descrip', models.TextField(verbose_name='简短描述')),
                ('rules_descrip', models.TextField(blank=True, verbose_name='规则描述')),
                ('Phwab_Availability', models.CharField(max_length=50, verbose_name='到期时间')),
                ('End_of_Manufacturing', models.CharField(max_length=50, verbose_name='停产日期')),
                ('list_price', models.IntegerField()),
            ],
            options={
                'verbose_name': 'AMO产品',
                'verbose_name_plural': 'AMO产品',
            },
        ),
        migrations.CreateModel(
            name='AMO_step',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='AMO步骤描述')),
            ],
            options={
                'verbose_name': 'AMO步骤',
                'verbose_name_plural': 'AMO步骤',
            },
        ),
        migrations.CreateModel(
            name='Assemble_Steps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='组装步骤')),
                ('choice', models.CharField(blank=True, max_length=100, verbose_name='选项')),
                ('Rules', models.TextField(blank=True, max_length=500)),
            ],
            options={
                'verbose_name': '组装步骤',
                'verbose_name_plural': '组装步骤',
            },
        ),
        migrations.CreateModel(
            name='Custom_Made_install',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(max_length=100, verbose_name='服务类型')),
                ('protect_time', models.CharField(max_length=10, verbose_name='预计时间')),
                ('service_descripe', models.TextField(verbose_name='服务描述')),
                ('CarePack_Part', models.CharField(max_length=100)),
                ('GL_Price_Unit', models.CharField(max_length=50)),
                ('remark', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': '定制服务——CDS-安装部署和服务日服务',
                'verbose_name_plural': '定制服务——CDS-安装部署和服务日服务',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vip', models.CharField(max_length=20, verbose_name='会员等级')),
                ('discount', models.DecimalField(decimal_places=1, max_digits=1)),
            ],
            options={
                'verbose_name': '折扣',
                'verbose_name_plural': '折扣',
            },
        ),
        migrations.CreateModel(
            name='Huipu_User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('password', models.CharField(max_length=100, verbose_name='密码')),
                ('super_user', models.BooleanField(default=False, verbose_name='是否为管理员')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('vip_range', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Discount')),
            ],
            options={
                'verbose_name': '用户表',
                'verbose_name_plural': '用户表',
            },
        ),
        migrations.CreateModel(
            name='Monitor_product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='显示器名称')),
                ('part_number', models.CharField(max_length=50, verbose_name='编号')),
                ('size', models.FloatField(verbose_name='尺寸')),
                ('display_resolution', models.CharField(max_length=50, verbose_name='分辨率')),
                ('port', models.TextField(verbose_name='接口')),
                ('daisy_chain', models.CharField(max_length=10, verbose_name='菊链布线支持')),
                ('byo', models.TextField(verbose_name='自带线缆')),
                ('character', models.TextField(verbose_name='特性')),
                ('price', models.IntegerField(verbose_name='价格')),
            ],
            options={
                'verbose_name': '显示器参数',
                'verbose_name_plural': '显示器参数',
            },
        ),
        migrations.CreateModel(
            name='Monitor_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='显示器分类')),
            ],
            options={
                'verbose_name': '显示器分类',
                'verbose_name_plural': '显示器分类',
            },
        ),
        migrations.CreateModel(
            name='Other_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='其他分类')),
            ],
            options={
                'verbose_name': '其他分类',
                'verbose_name_plural': '其他分类',
            },
        ),
        migrations.CreateModel(
            name='Pao_Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PL', models.CharField(max_length=20, verbose_name='PL')),
                ('HW_Product_Model', models.TextField()),
                ('Standard_Warranty', models.CharField(max_length=20, verbose_name='Standard Warranty')),
                ('Formulation', models.CharField(max_length=100)),
                ('Upgrade_Service_Description', models.TextField()),
                ('CarePack_Part', models.CharField(max_length=50)),
                ('GL_Price', models.CharField(max_length=50)),
                ('Promotion_Price', models.CharField(blank=True, max_length=50)),
                ('Standard_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Other_category')),
            ],
            options={
                'verbose_name': '保内产品参数',
                'verbose_name_plural': '保内产品参数',
            },
        ),
        migrations.CreateModel(
            name='PPS_CarePack_List_Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Service_Style', models.CharField(max_length=50)),
                ('Hw_Pl', models.CharField(max_length=50)),
                ('HW_Product_Model', models.CharField(max_length=50)),
                ('Wty_Style', models.CharField(max_length=50)),
                ('Per_incident', models.CharField(max_length=50)),
                ('CarePack_of_Service_Option', models.CharField(max_length=50)),
                ('CarePack_Part', models.CharField(max_length=50)),
                ('GL_Price', models.CharField(max_length=50)),
                ('blone_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Other_category')),
            ],
            options={
                'verbose_name': 'FY15 PPS CarePack List Price',
                'verbose_name_plural': 'FY15 PPS CarePack List Price',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='部件订货号')),
                ('descrip', models.CharField(max_length=100, verbose_name='产品描述')),
                ('rules_descrip', models.TextField(blank=True, max_length=500, verbose_name='配置规则')),
                ('End_of_Manufacturing', models.CharField(max_length=100, verbose_name='停产时间')),
                ('CECP_EStar', models.CharField(max_length=100)),
                ('List_Price', models.IntegerField(verbose_name='价格')),
                ('Qty', models.CharField(blank=True, max_length=50)),
                ('assemble_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Assemble_Steps')),
            ],
            options={
                'verbose_name': '组装产品',
                'verbose_name_plural': '组装产品',
            },
        ),
        migrations.CreateModel(
            name='rulesName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='配置标签')),
                ('pro_number', models.IntegerField(verbose_name='部件数量')),
                ('total_count', models.IntegerField(verbose_name='总价')),
                ('blone_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Huipu_User')),
            ],
            options={
                'verbose_name': '用户配置标签',
                'verbose_name_plural': '用户配置标签',
            },
        ),
        migrations.CreateModel(
            name='userAssemble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_index_number', models.CharField(max_length=10, verbose_name='产品ID')),
                ('assemble_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.rulesName')),
            ],
            options={
                'verbose_name': '用户自定义组装',
                'verbose_name_plural': '用户自定义组装',
            },
        ),
        migrations.CreateModel(
            name='Work_Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(max_length=100, verbose_name='服务类型')),
                ('service_descripe', models.TextField(verbose_name='服务描述')),
                ('CarePack_GenericPart', models.CharField(max_length=100)),
                ('GL_Price', models.CharField(max_length=50)),
                ('remark', models.TextField(blank=True)),
                ('blone_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Other_category')),
            ],
            options={
                'verbose_name': '定制服务——CDS-工厂产线实施服务',
                'verbose_name_plural': '定制服务——CDS-工厂产线实施服务',
            },
        ),
        migrations.CreateModel(
            name='Z_Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Z系列分类')),
            ],
            options={
                'verbose_name': 'Z系列分类',
                'verbose_name_plural': 'Z系列分类',
            },
        ),
        migrations.AddField(
            model_name='monitor_type',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Other_category'),
        ),
        migrations.AddField(
            model_name='monitor_product',
            name='monitor_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Monitor_type'),
        ),
        migrations.AddField(
            model_name='custom_made_install',
            name='blone_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Other_category'),
        ),
        migrations.AddField(
            model_name='assemble_steps',
            name='assemble_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Z_Category'),
        ),
        migrations.AddField(
            model_name='amo_step',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Other_category'),
        ),
        migrations.AddField(
            model_name='amo_product',
            name='amo_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.AMO_step'),
        ),
        migrations.AddField(
            model_name='additional_software_value_added_services',
            name='blone_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='show_update_list.Other_category'),
        ),
    ]
