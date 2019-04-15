//
// Created by rulong on 2018/11/20.
//

#include <iostream>
#include <typeinfo>
#include <cstdio>
#include "cppjieba/Jieba.hpp"
#include "deps/limonp/StringUtil.hpp"
#include <stdlib.h>

namespace cppjieba {
    using namespace limonp;

    class JiebaAPI {
    public:
        ~JiebaAPI() {
        }
        /**
         * 初始化
         * @param dictPath
         * @param modelPath
         * @param userDictPath
         * @param idfPath
         * @param stopwordsPath
         */
        JiebaAPI(const string& dictPath, const string& modelPath, const string& userDictPath,
                 const string& idfPath, const string& stopwordsPath)
            : jiebaInstance(dictPath, modelPath, userDictPath, idfPath, stopwordsPath) {
        }
        /**
         * 分词
         * @param sentence
         * @return
         */
        string Cut(const string& sentence) const {
            string result;
            vector<string> words;
            this->jiebaInstance.Cut(sentence, words, true);
            for (int i = 0; i < words.size(); i++) {
                if (Trim(words[i]).length() > 0) {
                    result += words[i] + " ";
                }
            }
            return Trim(result);
        }
        /**
         * 分词+标注
         * @param sentence
         * @return
         */
        string Tag(const string& sentence) const {
            string result;
            vector<pair<string, string>> words;
            this->jiebaInstance.Tag(sentence, words);
            for (int i = 0; i < words.size(); i++) {
                if (Trim(words[i].first).length() > 0) {
                    result += words[i].first + "/" + words[i].second + " ";
                }
            }
            return Trim(result);
        }
        /**
         * 按tfidf进行关键词提取
         * @param sentence
         * @param topN
         * @param allowedPOS
         * @return
         */
        string KeywordsTFIDF(const string& sentence,
                             const unsigned int topN,
                             const string& allowedPOS=TFIDF_DEFAULT_ALLOWED_POS) const {
            vector<pair<string, double>> keywords;
            this->jiebaInstance.extractor.Extract(sentence, keywords, topN, allowedPOS);
            return this->concatKeywords(keywords);
        }
        /**
         * 按tfidf进行关键词提取
         * @param words
         * @param topN
         * @param allowedPOS
         * @return
         */
        string KeywordsTFIDF(const vector<pair<string, string>>& words,
                             const unsigned int topN,
                             const string& allowedPOS=TFIDF_DEFAULT_ALLOWED_POS
                             ) const {
            vector<pair<string, double>> keywords;
            this->jiebaInstance.extractor.Extract(words, keywords, topN, allowedPOS);
            return this->concatKeywords(keywords);
        }
        /**
         * 按textrank进行关键词提取
         * @param sentence
         * @param topN
         * @param allowedPOS
         * @return
         */
        string KeywordsTextrank(const string& sentence,
                                const unsigned int topN,
                                const string& allowedPOS=TEXTRANK_DEFAULT_ALLOWED_POS) const {
            vector<pair<string, double>> keywords;
            this->jiebaInstance.textRankExtractor.Extract(sentence, keywords, topN, allowedPOS);
            return this->concatKeywords(keywords);
        }
        /**
         * 按textrank进行关键词提取
         * @param words
         * @param topN
         * @param allowedPOS
         * @return
         */
        string KeywordsTextrank(const vector<pair<string, string>>& words,
                                const unsigned int topN,
                                const string& allowedPOS=TEXTRANK_DEFAULT_ALLOWED_POS) const {
            vector<pair<string, double>> keywords;
            this->jiebaInstance.textRankExtractor.Extract(words, keywords, topN, allowedPOS);
            return this->concatKeywords(keywords);
        }

    private:
        string concatKeywords(vector<pair<string, double>>& keywords) const {
            string result;
            for (int i = 0; i < keywords.size(); i++) {
                if (Trim(keywords[i].first).length() > 0) {
                    result += keywords[i].first + "/" + to_string(keywords[i].second) + ",";
                }
            }
            return Trim(result, ',');
        };
        Jieba jiebaInstance;
    };
}

extern "C" {
    using namespace cppjieba;

    const static JiebaAPI* api;

    /**
     * 实例化
     * @param dictPath
     * @param modelPath
     * @param userDictPath
     * @param idfPath
     * @param stopwordsPath
     */
    void JiebaAPI_init(const char* dictPath, const char* modelPath, const char* userDictPath,
                           const char* idfPath, const char* stopwordsPath){
        if (api == nullptr) {
            api = new JiebaAPI(dictPath, modelPath, userDictPath, idfPath, stopwordsPath);
        }
    }

    /**
    * 将string 指针转换成 wchar_t 指针
    * @param charPtr
    * @return
    */
    const wchar_t* _ConvertString2WCharPtr(string& StringData) {
        const char* CChar = StringData.c_str();
        size_t len = strlen(CChar) + 1;
        wchar_t* WStr;
        WStr = new wchar_t[len];
        mbstowcs(WStr, CChar, len);
        return WStr;
    }

    /**
     * 分词
     * @param sentence
     * @return 中文问题，需要返回wchar_t
     */
    const wchar_t* JiebaAPI_Cut(const char* sentence){
        string result = api->Cut(sentence);
        const wchar_t* res = _ConvertString2WCharPtr(result);
        return res;
    }

    /**
     * 分词 windows 平台
     * @param sentence
     * @return
     */
    const char* JiebaAPI_Cut_Win(const char* sentence){
        string result = api->Cut(sentence);
        return result.c_str();
    }

    /**
     * 分词+词性标注
     * @param sentence
     * @return 中文问题，需要返回wchar_t
     */
    const wchar_t* JiebaAPI_Tag(const char* sentence){
        string result = api->Tag(sentence);
        return _ConvertString2WCharPtr(result);
    }

    /**
     * 分词+词性标注 windows 平台
     * @param sentence
     * @return
     */
    const char* JiebaAPI_Tag_Win(const char* sentence){
        string result = api->Tag(sentence);
        return result.c_str();
    }

    /**
     * 按TDIDF进行关键词提取
     * @param sentence
     * @param topN
     * @param allowedPOS
     * @return 中文问题，需要返回wchar_t
     */
    const wchar_t* JiebaAPI_Keywords_TFIDF(const char* sentence, const unsigned int topN, const char* allowedPOS) {
        string result = api->KeywordsTFIDF(sentence, topN, allowedPOS);
        return _ConvertString2WCharPtr(result);
    }

    /**
     * 按TDIDF进行关键词提取 windows 平台
     * @param sentence
     * @param topN
     * @param allowedPOS
     * @return
     */
    const char* JiebaAPI_Keywords_TFIDF_Win(const char* sentence, const unsigned int topN, const char* allowedPOS) {
        string result = api->KeywordsTFIDF(sentence, topN, allowedPOS);
        return result.c_str();
    }

    /**
     * 按TDIDF进行关键词提取
     * @param wordsStr
     * @param topN
     * @param allowedPOS
     * @return 中文问题，需要返回wchar_t
     */
    const wchar_t* JiebaAPI_Keywords_TFIDF_WordsStr(const char* wordsStr, const unsigned int topN, const char* allowedPOS) {
        vector<string> wordsItems = Split(wordsStr, " ");
        vector<pair<string, string>> words;
        vector<string> item;
        for (int i = 0; i < wordsItems.size(); i++) {
            item = Split(wordsItems[i], "/");
            if (item.size() == 2 && Trim(item[0]).length() > 0) {
                words.emplace_back(item[0], item[1]);
            }
        }
        string result = api->KeywordsTFIDF(words, topN, allowedPOS);
        return _ConvertString2WCharPtr(result);
    }

    /**
     * 按TDIDF进行关键词提取 windows 平台
     * @param wordsStr
     * @param topN
     * @param allowedPOS
     * @return
     */
    const char* JiebaAPI_Keywords_TFIDF_WordsStr_Win(const char* wordsStr, const unsigned int topN, const char* allowedPOS) {
        vector<string> wordsItems = Split(wordsStr, " ");
        vector<pair<string, string>> words;
        vector<string> item;
        for (int i = 0; i < wordsItems.size(); i++) {
            item = Split(wordsItems[i], "/");
            if (item.size() == 2 && Trim(item[0]).length() > 0) {
                words.emplace_back(item[0], item[1]);
            }
        }
        string result = api->KeywordsTFIDF(words, topN, allowedPOS);
        return result.c_str();
    }

    /**
     * 按Textrank进行关键词提取
     * @param sentence
     * @param topN
     * @param allowedPOS
     * @return 中文问题，需要返回wchar_t
     */
    const wchar_t* JiebaAPI_Keywords_Textrank(const char* sentence, const unsigned int topN, const char* allowedPOS) {
        string result = api->KeywordsTextrank(sentence, topN, allowedPOS);
        return _ConvertString2WCharPtr(result);
    }

    /**
     * 按Textrank进行关键词提取 windows 平台
     * @param sentence
     * @param topN
     * @param allowedPOS
     * @return
     */
    const char* JiebaAPI_Keywords_Textrank_Win(const char* sentence, const unsigned int topN, const char* allowedPOS) {
        string result = api->KeywordsTextrank(sentence, topN, allowedPOS);
        return result.c_str();
    }

    /**
    * 按Textrank进行关键词提取
    * @param wordsStr
    * @param topN
    * @param allowedPOS
    * @return 中文问题，需要返回wchar_t
    */
    const wchar_t* JiebaAPI_Keywords_Textrank_WordsStr(const char* wordsStr, const unsigned int topN, const char* allowedPOS) {
        vector<string> wordsItems = Split(wordsStr, " ");
        vector<pair<string, string>> words;
        vector<string> item;
        for (int i = 0; i < wordsItems.size(); i++) {
            item = Split(wordsItems[i], "/");
            if (item.size() == 2 && Trim(item[0]).length() > 0) {
                words.emplace_back(item[0], item[1]);
            }
        }
        string result = api->KeywordsTextrank(words, topN, allowedPOS);
        return _ConvertString2WCharPtr(result);
    }

    /**
    * 按Textrank进行关键词提取 windows 平台
    * @param wordsStr
    * @param topN
    * @param allowedPOS
    * @return
    */
    const char* JiebaAPI_Keywords_Textrank_WordsStr_Win(const char* wordsStr, const unsigned int topN, const char* allowedPOS) {
        vector<string> wordsItems = Split(wordsStr, " ");
        vector<pair<string, string>> words;
        vector<string> item;
        for (int i = 0; i < wordsItems.size(); i++) {
            item = Split(wordsItems[i], "/");
            if (item.size() == 2 && Trim(item[0]).length() > 0) {
                words.emplace_back(item[0], item[1]);
            }
        }
        string result = api->KeywordsTextrank(words, topN, allowedPOS);
        return result.c_str();
    }

    /**
     * 释放
     * @param ptr
     */
    const void FreeWCharPtr(void* ptr) {
//        cout << "free address:" << &ptr << endl;
//        printf("freeing address: %p\n", ptr);
//        delete[] ptr;
        if (ptr != nullptr) {
            free(ptr);
        }
    }


}



