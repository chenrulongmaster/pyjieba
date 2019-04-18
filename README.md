# pyjieba

[![996.icu](https://img.shields.io/badge/link-996.icu-red.svg)](https://996.icu)
[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)
![python](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)

Python wrapper for cppjieba without any dependency, no need to compile by using gcc/c++

1. Python 封装C++版本的jieba分词器，性能好，并且已经预编译，无需安装时编译，即拿即用。
2. 已在Centos7、MaxOS10.13.6上测试 【Windows可能在某些情况下运行异常】。
3. C++ 代码源自"结巴"中文分词的C++版本，[CPPJieba](https://github.com/yanyiwu/cppjieba)

## 使用说明

pip安装

```shell
pip install pyjieba
```

手动安装
```shell
cd pyjieba
python setup.py install
```

接口使用
```Python
# 导入包
import pyjieba
# 初始化[可选]
pyjieba.initialize()
# 初始化时，可以指定自己的词典
pyjieba.initialize(dictPath='yourpath',  # 默认词典路径， 默认在包下路径/dict/jieba.dict.utf8
    userPath='yourpath',  # 用户词典，默认在包下路径/dict/user.dict.utf8，多个词典使用英文分号;分隔开
    idfPath='yourpath',  # IDF词典，默认在包下路径/dict/idf.utf8，提取关键词时使用
    stopwordsPath='yourpath'  # 停用词词典，默认在包下路径/dict/stop_words.utf8
)

# 分词
sentence = '视觉中国再次致歉'
pyjieba.cut(sentence)
# 输出结果 ['视觉', '中国', '再次', '致歉']

# 词性标注
pyjieba.tag(sentence)
# 输出结果 ['视觉/n', '中国/ns', '再次/d', '致歉/v']

# 使用TFIDF提取关键词
pyjieba.keywordsTFIDF(sentence,  # 句子，可以是文本，也可以传入分词的结果例如 ['视觉', '中国', '再次', '致歉']
    topN=5, # 最多返回几个关键词， 可选
    allowedPOS='ns,n,vn,v,x'  # 关键词属性限制, 可选
)
# 输出结果 [('致歉', 3.618718), ('视觉', 2.680915), ('中国', 1.009107)]

# 使用Textrank算法提取关键词
pyjieba.keywordsTextrank(sentence, # 句子，可以是文本，也可以传入分词的结果例如 ['视觉', '中国', '再次', '致歉']
    topN=5, # 最多返回几个关键词， 可选
    allowedPOS='ns,n,vn,v,x'  # 关键词属性限制, 可选
)
# 输出结果 [('视觉', 1.0), ('致歉', 0.996685), ('中国', 0.992994)]
```


## 源码修改与编译命令

如果需要进行cppjieba源码修改，需要在三个平台上分别进行编译，生成新的so和dll文件

```shell
> cd cppjieba_src

# windows
> g++ jiebaapi.cpp -fPIC -I deps -I include -std=c++11 -shared -o ../pyjieba/libs/cppjieba_API_win64.dll

# MaxOS
> g++ jiebaapi.cpp -fPIC -I deps -I include -std=c++11 -shared -o ../pyjieba/libs/cppjieba_API_osx64.dll

# Linux
> g++ jiebaapi.cpp -fPIC -I deps -I include -std=c++11 -shared -o ../pyjieba/libs/cppjieba_API_linux64.so

```

## Benchmark
1. 平台 Centos7, 8核16G，Python3.6
2. 小说文本长度：83791
3. 循环分词次数：10

| 次数 | pyjieba | jieba |
| --- | --- | --- |
| 1 | 3147.3ms | 11137.5ms |
| 2 | 4692.9ms | 12792.7ms |
| 3 | 3257.1ms | 10830.7ms |

总体来看，pyjieba平均耗时为jieba的1/3。



## 鸣谢
1. [CPPJieba](https://github.com/yanyiwu/cppjieba)  "结巴"中文分词的C++版本
2. [jieba](https://github.com/fxsjy/jieba)  结巴中文分词

