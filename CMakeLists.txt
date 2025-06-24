cmake_minimum_required(VERSION 3.31)
project(File_Manager)

set(CMAKE_CXX_STANDARD 20)

# Defina o caminho do Qt ANTES de chamar find_package
set(CMAKE_PREFIX_PATH "C:/Qt/6.9.1/mingw_64")

find_package(Qt6 COMPONENTS Core Gui Widgets Sql REQUIRED)

set(CMAKE_AUTOMOC ON)

add_executable(File_Manager File_Manager.cpp DirectoryAnalyzer.cpp DirectoryAnalyzer.h)

target_link_libraries(File_Manager Qt6::Core Qt6::Gui Qt6::Widgets Qt6::Sql)

if (WIN32)
    set_target_properties(File_Manager PROPERTIES LINK_FLAGS "-mwindows")
endif()