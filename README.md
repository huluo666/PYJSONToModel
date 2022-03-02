JSON转Model工具python版

根据JSON自动生成Model文件，支持*JSON*和URL请求。支持 `Objective-C` 和 `Swift` 代码生成

脚本基于`jinja2`模板引擎，代码量少可扩展性高。若你对此脚本进行二次开发，可了解[jinja2](http://docs.jinkan.org/docs/jinja2/)模板使用

### 一、使用帮助

```shell
$ python3 JSONToModel.py --help
Usage: JSONToModel.py [OPTIONS]

Options:
  -c, --choice [1|2|3]  1、生成OC Class 2、生成Swift Class 3、生成Swift Strut
  --help                Show this message and exit.
```



#### 二、修改配置项数据

```python
#MARK===============自定义配置项===================#
#Model前缀TX、AL、JD...
model_prefix="HK"
#Model后缀-Model、Item...
model_suffix=""
#Model文件名称
rootModelName="ExampleModelName"
#Taget工程名
TARGET_NAME="LNGame_Framework"
#Model文件输出目录
outputDirPath = "~/Documents/JSONModel"
```



#### 三、终端执行

1、`cd 'JSONToModel.py文件所在路径'`

2、`python3 JSONToModel.py`



**生成结果:**

ExampleModelName.h

```objective-c
//
//  ExampleModelName.h
//  LNGame_Framework
//
//  Created by jenkins on 2022/03/02.
//  Copyright © 2022 Apple. All rights reserved.
//


#import <Foundation/Foundation.h>
@class ExampleModelName;
@class HKAddress;
@class HKOrderList;

#pragma mark - Object interfaces

@interface ExampleModelName : NSObject 

@property (nonatomic, copy)   NSString *name;
@property (nonatomic, strong)   HKAddress *address;
@property (nonatomic, copy)   NSArray<HKOrderList *> *orderList;

@end

@interface HKAddress : NSObject 

@property (nonatomic, copy)   NSString *city;
@property (nonatomic, copy)   NSString *location;

@end

@interface HKOrderList : NSObject 

@property (nonatomic, assign)   NSInteger id;
@property (nonatomic, copy)   NSString *goods;

@end
```



ExampleModelName.m

```objective-c
//
//  ExampleModelName.m
//  LNGame_Framework
//
//  Created by jenkins on  2022/03/02.
//  Copyright © 2022 Apple. All rights reserved.
//

#import "ExampleModelName.h"

@implementation ExampleModelName

@end

@implementation HKAddress

@end

@implementation HKOrderList

@end
```



## 其他：

- **Jinja2官方文档**：http://docs.jinkan.org/docs/jinja2/

- **在线JSON转Model工具**

  https://app.quicktype.io/

  https://modelend.com/

  https://json2kt.com/

  https://jsonformatter.org/json-to-swift

  https://json.im/json2model/json2ObjectC.html

  

- **字符串转义（压缩字符串）**

  https://onlinestringtools.com/escape-string

  https://jsonformatter.org/json-escape

- 如在使用过程中遇到问题，请你Issues me。

