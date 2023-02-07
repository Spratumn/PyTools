#coding:utf-8

import os
"""
    从指定根目录获取指定类型的文件路径列表和文件名列表
"""
def get_path(root, file_types):
    file_paths = []
    file_names = []
    for file_name in os.listdir(root):
        if file_name.endswith(file_types):
            file_paths.append('/'.join([root, file_name]))
            file_names.append(file_name.split('.')[0])
    return file_paths, file_names