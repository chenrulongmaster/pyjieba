# -*- coding: utf-8 -*-
import os
import platform
import ctypes
from ctypes import cdll as _cdll

# 系统类型
_SYS_NAME = platform.system()

# 路径
_PWD = os.path.dirname(os.path.abspath(__file__))

# 动态链接库的名字
_LIBRARY_NAME = ''
_IS_WIN = False
if _SYS_NAME == 'Linux':
    _LIBRARY_NAME = 'cppjieba_API_linux64.so'
elif _SYS_NAME == 'Darwin':
    _LIBRARY_NAME = 'cppjieba_API_osx64.so'
else:
    _LIBRARY_NAME = 'cppjieba_API_win64.dll'
    _IS_WIN = True


# 载入词典
_jiebadll = None
if _LIBRARY_NAME:
    _jiebadll = _cdll.LoadLibrary(_PWD + '/libs/' + _LIBRARY_NAME)
    # 声明返回值类型
    _jiebadll.JiebaAPI_Cut.restype = ctypes.c_void_p
    _jiebadll.JiebaAPI_Cut_Win.restype = ctypes.c_void_p
    _jiebadll.JiebaAPI_Tag.restype = ctypes.c_void_p
    _jiebadll.JiebaAPI_Tag_Win.restype = ctypes.c_void_p
    _jiebadll.JiebaAPI_Keywords_TFIDF.restype = ctypes.c_void_p
    _jiebadll.JiebaAPI_Keywords_TFIDF_Win.restype = ctypes.c_void_p
    _jiebadll.JiebaAPI_Keywords_TFIDF_WordsStr.restype = ctypes.c_void_p
    _jiebadll.JiebaAPI_Keywords_TFIDF_WordsStr_Win.restype = ctypes.c_void_p
    _jiebadll.JiebaAPI_Keywords_Textrank.restype = ctypes.c_void_p
    _jiebadll.JiebaAPI_Keywords_Textrank_Win.restype = ctypes.c_void_p
    _jiebadll.JiebaAPI_Keywords_Textrank_WordsStr.restype = ctypes.c_void_p
    _jiebadll.JiebaAPI_Keywords_Textrank_WordsStr_Win.restype = ctypes.c_void_p
    _jiebadll.FreeWCharPtr.argtypes = [ctypes.c_void_p]

# 默认词典位置
_DEFAULT_DICT = _PWD + '/dict/jieba.dict.utf8'
_DEFAULT_MODEL = _PWD + '/dict/hmm_model.utf8'
_DEFAULT_USER_DICT = _PWD + '/dict/user.dict.utf8'
_DEFAULT_IDF_DICT = _PWD + '/dict/idf.utf8'
_DEFAULT_STOP_WORDS = _PWD + '/dict/stop_words.utf8'

_api_instance = None
_DEFAULT_TFIDF_ALLOWEDPOS = 'ns,n,vn,v,x'
_DEFAULT_TEXTRANK_ALLOWEDPOS = 'ns,n,vn,v,x'


class _JiebaAPI(object):

    def __init__(self, dictPath=_DEFAULT_DICT, modelPath=_DEFAULT_MODEL, userPath=_DEFAULT_USER_DICT,
                 idfPath=_DEFAULT_IDF_DICT, stopwordsPath=_DEFAULT_STOP_WORDS):
        pass

    def cut(self, sentence):
        raise NotImplementedError('Not implemented!')

    def tag(self, sentence):
        raise NotImplementedError('Not implemented!')

    def keywordsTFIDF(self, sentence, topN=5, allowedPOS=_DEFAULT_TFIDF_ALLOWEDPOS):
        raise NotImplementedError('Not implemented!')

    def keywordsTextrank(self, sentence, topN=5, allowedPOS=_DEFAULT_TEXTRANK_ALLOWEDPOS):
        raise NotImplementedError('Not implemented!')


class _CPPJiebaAPI(_JiebaAPI):

    def __init__(self, dictPath=_DEFAULT_DICT, modelPath=_DEFAULT_MODEL, userPath=_DEFAULT_USER_DICT,
                 idfPath=_DEFAULT_IDF_DICT, stopwordsPath=_DEFAULT_STOP_WORDS):
        """
        初始化
        :param dictPath:
        :param modelPath:
        :param userPath: 多个词典用;分隔
        :param idfPath:
        :param stopwordsPath:
        """
        _JiebaAPI.__init__(self)
        if _api_instance is None:
            print('Initialize CPPJieba ... ')
            _jiebadll.JiebaAPI_init(ctypes.c_char_p(dictPath.encode('utf-8')),
                                    ctypes.c_char_p(modelPath.encode('utf-8')),
                                    ctypes.c_char_p(userPath.encode('utf-8')),
                                    ctypes.c_char_p(idfPath.encode('utf-8')),
                                    ctypes.c_char_p(stopwordsPath.encode('utf-8')))
            print('Initialized CPPJieba!')

    def cut(self, sentence):
        res = None
        try:
            if _IS_WIN:
                res = _jiebadll.JiebaAPI_Cut_Win(ctypes.c_char_p(sentence.encode('utf-8')))
                value = ctypes.cast(res, ctypes.c_char_p).value.decode('utf-8')
            else:
                res = _jiebadll.JiebaAPI_Cut(ctypes.c_char_p(sentence.encode('utf-8')))
                value = ctypes.cast(res, ctypes.c_wchar_p).value
            return value.split(' ')
        except Exception as e:
            raise e
        finally:
            if res is not None and not _IS_WIN:
                try:
                    _jiebadll.FreeWCharPtr(ctypes.cast(res, ctypes.c_wchar_p))
                except:
                    pass

    def tag(self, sentence):
        res = None
        try:
            if _IS_WIN:
                res = _jiebadll.JiebaAPI_Tag_Win(ctypes.c_char_p(sentence.encode('utf-8')))
                value = ctypes.cast(res, ctypes.c_char_p).value.decode('utf-8')
            else:
                res = _jiebadll.JiebaAPI_Tag(ctypes.c_char_p(sentence.encode('utf-8')))
                value = ctypes.cast(res, ctypes.c_wchar_p).value
            return value.split(' ')
        except Exception as e:
            raise e
        finally:
            if res is not None and not _IS_WIN:
                try:
                    _jiebadll.FreeWCharPtr(ctypes.cast(res, ctypes.c_wchar_p))
                except:
                    pass

    def keywordsTFIDF(self, sentence, topN=5, allowedPOS=_DEFAULT_TFIDF_ALLOWEDPOS):
        """
        tfidf提取关键词
        :param sentence: 句子-字符串-将会分词； 词组-字符串数组["大会/n", "大师/n"]-将不会分词
        :param allowedPOS:
        :return:
        """
        res = None
        result = list()
        if isinstance(sentence, str):
            if _IS_WIN:
                res = _jiebadll.JiebaAPI_Keywords_TFIDF_Win(ctypes.c_char_p(sentence.encode('utf-8')), ctypes.c_int(topN),
                                                            ctypes.c_char_p(allowedPOS.encode('utf-8')))
            else:
                res = _jiebadll.JiebaAPI_Keywords_TFIDF(ctypes.c_char_p(sentence.encode('utf-8')), ctypes.c_int(topN),
                                                        ctypes.c_char_p(allowedPOS.encode('utf-8')))
        elif isinstance(sentence, list):
            sentence = ' '.join(sentence)
            if _IS_WIN:
                res = _jiebadll.JiebaAPI_Keywords_TFIDF_WordsStr_Win(ctypes.c_char_p(sentence.encode('utf-8')),
                                                                     ctypes.c_int(topN),
                                                                     ctypes.c_char_p(allowedPOS.encode('utf-8')))            
            else:
                res = _jiebadll.JiebaAPI_Keywords_TFIDF_WordsStr(ctypes.c_char_p(sentence.encode('utf-8')),
                                                                 ctypes.c_int(topN),
                                                                 ctypes.c_char_p(allowedPOS.encode('utf-8')))
        if res is not None:
            try:
                if _IS_WIN:
                    value = ctypes.cast(res, ctypes.c_char_p).value.decode('utf-8')
                else:
                    value = ctypes.cast(res, ctypes.c_wchar_p).value
                for i in value.split(','):
                    if i:
                        item = i.split('/')
                        if len(item) == 2:
                            result.append((item[0], float(item[1])))
            except Exception as e:
                raise e
            finally:
                if res is not None and not _IS_WIN:
                    try:
                        _jiebadll.FreeWCharPtr(ctypes.cast(res, ctypes.c_wchar_p))
                    except:
                        pass
        return result

    def keywordsTextrank(self, sentence, topN=5, allowedPOS=_DEFAULT_TEXTRANK_ALLOWEDPOS):
        """
        textrank 关键词提取
        :param sentence:
        :param allowedPOS:
        :return:
        """
        res = None
        result = list()
        if isinstance(sentence, str):
            if _IS_WIN:
                res = _jiebadll.JiebaAPI_Keywords_Textrank_Win(ctypes.c_char_p(sentence.encode('utf-8')), ctypes.c_int(topN),
                                                               ctypes.c_char_p(allowedPOS.encode('utf-8')))
            else:
                res = _jiebadll.JiebaAPI_Keywords_Textrank(ctypes.c_char_p(sentence.encode('utf-8')), ctypes.c_int(topN),
                                                           ctypes.c_char_p(allowedPOS.encode('utf-8')))
        elif isinstance(sentence, list):
            sentence = ' '.join(sentence)
            if _IS_WIN:
                res = _jiebadll.JiebaAPI_Keywords_Textrank_WordsStr_Win(ctypes.c_char_p(sentence.encode('utf-8')),
                                                                        ctypes.c_int(topN),
                                                                        ctypes.c_char_p(allowedPOS.encode('utf-8')))
            else:
                res = _jiebadll.JiebaAPI_Keywords_Textrank_WordsStr(ctypes.c_char_p(sentence.encode('utf-8')),
                                                                    ctypes.c_int(topN),
                                                                    ctypes.c_char_p(allowedPOS.encode('utf-8')))
        if res is not None:
            try:
                if _IS_WIN:
                    value = ctypes.cast(res, ctypes.c_char_p).value.decode('utf-8')
                else:
                    value = ctypes.cast(res, ctypes.c_wchar_p).value
                for i in value.split(','):
                    if i:
                        item = i.split('/')
                        if len(item) == 2:
                            result.append((item[0], float(item[1])))
            except Exception as e:
                raise e
            finally:
                if res is not None and not _IS_WIN:
                    try:
                        _jiebadll.FreeWCharPtr(ctypes.cast(res, ctypes.c_wchar_p))
                    except:
                        pass
        return result


def __init(dictPath=_DEFAULT_DICT, modelPath=_DEFAULT_MODEL, userPath=_DEFAULT_USER_DICT,
                 idfPath=_DEFAULT_IDF_DICT, stopwordsPath=_DEFAULT_STOP_WORDS):
    global _api_instance
    _api_instance = _CPPJiebaAPI(dictPath, modelPath, userPath, idfPath, stopwordsPath)


def __cut(sentence):
    if not _api_instance:
        __init()
    return _api_instance.cut(sentence)


def __tag(sentence):
    if not _api_instance:
        __init()
    return _api_instance.tag(sentence)


def __keywordsTFIDF(sentence, topN=5, allowedPOS=_DEFAULT_TFIDF_ALLOWEDPOS):
    if not _api_instance:
        __init()
    return _api_instance.keywordsTFIDF(sentence, topN, allowedPOS)


def __keywordsTextrank(sentence, topN=5, allowedPOS=_DEFAULT_TFIDF_ALLOWEDPOS):
    if not _api_instance:
        __init()
    return _api_instance.keywordsTextrank(sentence, topN, allowedPOS)


initialize = __init
cut = __cut
tag = __tag
keywordsTFIDF = __keywordsTFIDF
keywordsTextrank = __keywordsTextrank


if __name__ == '__main__':
    sentence = '俞敏洪，你不需要道歉！'
    # sentence = codecs.open('./test.txt', mode='r', encoding='utf-8').read()
    sentence = sentence
    import time
    initialize()
    start = time.time() * 1000
    for i in range(1):
        res = cut(sentence)
        print(res)
        res = tag(sentence)
        print(res)
        res = keywordsTFIDF(sentence)
        print(res)
        res = keywordsTextrank(sentence)
        print(res)
    print('total - %s' % str(time.time() * 1000 - start))
        # res = keywordsTFIDF(sentence)
        # print(res)
        # print('========TFIDF')
        # res = keywordsTFIDF(tag(sentence))
        # print(res)
        # print('========TFIDF words')
        # res = keywordsTextrank(sentence)
        # print(res)
        # print('========Textrank')
        # res = keywordsTextrank(tag(sentence))
        # print(res)
        # print('========Textrank words')


