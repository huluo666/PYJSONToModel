#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2022/3/2
# @Author  : jenkins
# @Version : V1.0
# @Features: 生成OC/Swift模型代码

from urllib import request
import datetime
import json
import getpass
import os
import pip

#MARK===============自定义配置项===================#
#前缀TX、AL、JD...
model_prefix="HK"
#后缀-Model、Item...
model_suffix=""
#Model文件名称
rootModelName="ExampleModelName"
#Taget工程名
TARGET_NAME="LNGame_Framework"
#model文件生成目录
outputDirPath = "~/Documents/JSONModel"

#测试数据
jsonDict={
	"name":"jack", 
	"address":{"city":"北京", "location":"x,x"},
	"orderList":[{"id":1, "goods":"手机"}, {"id":2, "goods":"电脑"}]
}

def getJSONDictWitUrl(url):
	if url.startswith("http"):
		req = request.Request(url=url, headers={})
		res = request.urlopen(req)
		jsonDict=json.loads(res.read().decode())
	else:
		with open(url, 'r') as json_file:
			jsonDict = json.load(json_file)
	return jsonDict
		
#使用网络或本地数据
#jsonDict=getJSONDictWitUrl("https://aider.meizu.com/app/weather/listWeather?cityIds=101280101")

#MARK===============以上为配置项===================#
outputDirPath= os.path.expanduser(outputDirPath)
os.makedirs(outputDirPath, exist_ok=True)

def importOrInstalllibs(packages):
	for package in packages:
		try:		
			globals()[package]=__import__(package)
		except ImportError as e:
			print('{} is NOT installed'.format(package))		
			result = pip.main(['install', package])
			if result != 0: # if pip could not install it reraise the error
				raise
			else:
				# if the install was sucessful, put modname in globals
				globals()[package]=__import__(package)
#第三方库引入			
importOrInstalllibs(['click', 'jinja2'])


model_OC_tmpl_h="""
@interface {{MODEL_NAME}} : NSObject 
{% set dict_item =  VAR_DICT %}
{% for key, value in dict_item.items() -%}
{% if is_list(value) and value|length > 0 -%}
@property (nonatomic, copy)   NSArray<{{PREFIX}}{{upperCase(key)}}{{SUFFIX}} *> *{{key}};
{% elif value is  number -%}
@property (nonatomic, assign)   NSInteger {{key}};
{% elif value is  mapping -%}
@property (nonatomic, strong)   {{PREFIX}}{{upperCase(key)}}{{SUFFIX}} *{{key}};
{% else -%}
@property (nonatomic, copy)   NSString *{{key}};
{% endif -%}
{% endfor %}
@end
"""

model_OC_tmpl_H_Text="""
//\n//  {{MODEL_NAME}}.h\n//  {{TARGET_NAME}}\n//\n//  Created by {{user_name}} on {{now.strftime('%Y/%m/%d')}}.\n//  Copyright © {{now.strftime('%Y')}} {{Author}}. All rights reserved.\n//\n

#import <Foundation/Foundation.h>
{% set items = MODES %}
{%- for item in items -%}
@class {{item}};
{% endfor %}
#pragma mark - Object interfaces

{{ MODEL_TEXT }}
"""

model_OC_tmpl_m="""
@implementation {{MODEL_NAME}}

@end
"""

model_OC_tmpl_M_Text="""
//\n//  {{MODEL_NAME}}.m\n//  {{TARGET_NAME}}\n//\n//  Created by {{user_name}} on  {{now.strftime(\'%Y/%m/%d\')}}.\n//  Copyright © {{now.strftime(\'%Y\')}} {{Author}}. All rights reserved.\n//\n
#import "{{MODEL_NAME}}.h"

{{ MODEL_TEXT }}
"""

model_Swift_Class_Tmpl="""
{% set dict_item =  VAR_DICT %}
// MARK: - {{MODEL_NAME}}
class {{MODEL_NAME}} : NSObject {
{%- for key, value in dict_item.items() %}
{%- if is_list(value) %}
	var	{{key}}:[{{PREFIX}}{{upperCase(key)}}{{SUFFIX}}]!
{%- elif value is  number %}
	var {{key}}: Int = 0
{%- elif value is  mapping %}
	var	{{key}}:{{PREFIX}}{{upperCase(key)}}{{SUFFIX}}
{%- else %}
	var {{key}}: String!
{%- endif %}
{%- endfor %} 
}
"""

model_Swift_Struct_Tmpl="""
{% set dict_item =  VAR_DICT %}
// MARK: - {{MODEL_NAME}}
struct {{MODEL_NAME}}: Codable {
{%- for key, value in dict_item.items() %}
{%- if is_list(value) %}
	let	{{key}}:[{{PREFIX}}{{upperCase(key)}}{{SUFFIX}}]!
{%- elif value is  number %}
	let {{key}}: Int = 0
{%- elif value is  mapping %}
	let {{key}}: {{PREFIX}}{{upperCase(key)}}{{SUFFIX}}
{%- else %}
	let {{key}}: String
{%- endif %}
{%- endfor %} 
}
"""

def is_list(value):
	return isinstance(value, list)

#大写首字母-其余不变	
def upperCase(str):
	if not str:
		return ''
	return str[0].upper() + str[1:]

def render(tmpl, *args, **kwds):
	'''jinja2 render'''
	vars = dict(*args, **kwds)
	#载入模板
	tmp = jinja2.Template(tmpl)	
	tmp.globals['is_list'] = is_list
	tmp.globals['upperCase'] = upperCase
	tmp.globals['now'] = datetime.datetime.now()
	tmp.globals['user_name'] = getpass.getuser()
	tmp.globals['Author'] = "Apple"
	
	# 输入变量，生成结果
	return tmp.render(vars).strip()

def generateModelCode(jsonDict,model_Tmpl,objects,modelName):
	result = render(model_Tmpl,VAR_DICT=jsonDict,MODEL_NAME=modelName,PREFIX=model_prefix,SUFFIX=model_suffix)	
	objects["content"]+=result+"\n\n"
	objects["models"].append(modelName);
	for key, value in jsonDict.items():
		model_name=model_prefix+upperCase(key)+model_suffix
		if type(value)==list and len(value)>0:
			subDict=value[0]
			generateModelCode(subDict,model_Tmpl,objects,model_name)
		elif type(value)==dict:
			generateModelCode(value,model_Tmpl,objects,model_name)
		else:
			pass

#文本方式写入文件
def WriteFile(filePath,data):
	file_obj = open(filePath,'w')    
	file_obj.write(data)
	file_obj.close()
			
@click.command()
@click.option("--choice",'-c', type=click.Choice(['1','2','3']), prompt='请输入选择项',default="1",help="1、生成OC Class 2、生成Swift Class 3、生成Swift Strut")
def appMain(choice):
	tmlSet={}
	if int(choice)==1:
		tmlSet={
			"h":[model_OC_tmpl_h,model_OC_tmpl_H_Text],
			"m":[model_OC_tmpl_m,model_OC_tmpl_M_Text]
		}
	elif int(choice)==2:		
		tmlSet={
			"swift":[model_Swift_Class_Tmpl],
		}
		
	elif int(choice)==3:		
		tmlSet={
			"swift":[model_Swift_Struct_Tmpl],
		}
	else:
		tmlSet={
			"h":[model_OC_tmpl_h,model_OC_tmpl_H_Text],
			"m":[model_OC_tmpl_m,model_OC_tmpl_M_Text]
		}
		
	for key, value in tmlSet.items():
		objects = {"content":"","models":[]}
		generateModelCode(jsonDict,value[0],objects,rootModelName)
		result=objects["content"]
		if len(value)>1:
			result = render(value[1],TARGET_NAME=TARGET_NAME,MODEL_TEXT=objects["content"],MODES=objects["models"],MODEL_NAME=rootModelName)
		WriteFile(f"{outputDirPath}/{rootModelName}.{key}",result)
	click.secho("代码生成成功："+outputDirPath,fg="green")
#	os.system("open " + outputDirPath)
	
	
	
if __name__ == '__main__':
	appMain()