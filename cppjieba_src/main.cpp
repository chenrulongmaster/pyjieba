#include <iostream>
#include <cppjieba/Jieba.hpp>



namespace example {

    void start() {
        using namespace std;
        using namespace cppjieba;
        const string rootpath = "/Users/rulong/Desktop/Workspaces/sourcecode/myproject/testcplusplus/dict";
        const string dictPath = rootpath + "/jieba.dict.utf8";
        const string modelPath = rootpath + "/hmm_model.utf8";
        const string userdictPath = rootpath + "/user.dict.utf8";
        const string idfPath = rootpath + "/idf.utf8";
        const string stopwordsPath = rootpath + "/stop_words.utf8";

        cppjieba::Jieba jieba = Jieba(dictPath, modelPath, userdictPath, idfPath, stopwordsPath);

        const string sent = "天目药业揭露行业内幕";
        vector<pair<string, string>> mywords;
        jieba.Tag(sent, mywords);
        for (int i = 0; i < mywords.size(); i++) {
            cout<< mywords[i].first << "/" << mywords[i].second.length() << endl;
        }
            const string sent2 = "天目药业揭露行业内幕";
            vector<pair<string, string>> mywords2;
            jieba.Tag(sent2, mywords2);
            for (int i = 0; i < mywords2.size(); i++) {
                    cout<< mywords2[i].first << "/" << mywords2[i].second << endl;
            }
    }

}

int main() {
    example::start();
    // g++ jiebaapi.cpp -fPIC -I deps -I include -std=c++11 -shared -o cppjieba_API_osx64.so
}