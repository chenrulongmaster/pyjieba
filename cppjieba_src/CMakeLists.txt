cmake_minimum_required(VERSION 3.10)
project(testcplusplus)

set(CMAKE_CXX_STANDARD 11)

INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/deps)
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/deps/limonp)
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/include)
INCLUDE_DIRECTORIES(${PROJECT_SOURCE_DIR}/include/cppjieba)

ADD_SUBDIRECTORY(deps)
ADD_SUBDIRECTORY(${PROJECT_SOURCE_DIR}/include/cppjieba)
add_library(jiebaapi SHARED
        jiebaapi.cpp include/cppjieba/Utils.hpp
        include/cppjieba/DictTrie.hpp
        include/cppjieba/FullSegment.hpp
        include/cppjieba/HMMModel.hpp
        include/cppjieba/HMMSegment.hpp
        include/cppjieba/Jieba.hpp
        include/cppjieba/KeywordExtractor.hpp
        include/cppjieba/MixSegment.hpp
        include/cppjieba/MPSegment.hpp
        include/cppjieba/PosTagger.hpp
        include/cppjieba/PreFilter.hpp
        include/cppjieba/QuerySegment.hpp
        include/cppjieba/SegmentBase.hpp
        include/cppjieba/SegmentTagged.hpp
        include/cppjieba/TextRankExtractor.hpp
        include/cppjieba/Trie.hpp
        include/cppjieba/Unicode.hpp)
add_executable(testcplusplus main.cpp jiebaapi.cpp)