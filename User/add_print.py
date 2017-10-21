# -*- coding: utf-8 -*-

# __author__ = lilepeng@corp.netease.com
# __date__ = 2017/10/21 10:10:30

# desc: 添加测试打印

import re
import os
import sublime_plugin

clean_name = re.compile('^\s*(public\s+|private\s+|protected\s+|static\s+|function\s+|def\s+)+', re.I)


class AddPrintCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sPrint = """print("llp Test==========%s%s:$1",$2)"""
        sFileName = self.get_current_file_name()
        sName = self.get_current_class_and_function()
        sName = ".%s" % sName if sName else ""
        self.view.run_command("insert_snippet", {
            "contents": sPrint % (sFileName, sName),
        })

    def get_current_file_name(self):
        """获取当前文件名"""
        file_name = os.path.basename(self.view.file_name())
        return file_name.split('.')[0]

    def get_current_class_and_function(self):
        """获取当前区域的类名和函数名"""
        for region in self.view.sel():
            region_row, region_col = self.view.rowcol(region.begin())
            print("CurrentPos", region_row, region_col)

            name_class = ""
            name_fuction = ""
            found = False
            top_function = False
            classline = 0

            class_regions = self.view.find_by_selector("entity.name.class")
            for r in reversed(class_regions):
                row, col = self.view.rowcol(r.begin())
                print("ClassPos", row, col, region_row, self.view.substr(r))
                if row <= region_row:
                    name_class = self.view.substr(r)
                    found = True
                    classline = row
                    break

            function_regions = self.view.find_by_selector('meta.function - meta.function.inline')
            if function_regions:
                for r in reversed(function_regions):
                    row, col = self.view.rowcol(r.begin())
                    if row < classline:
                        continue
                    print("FunctionPos", row, col, region_row)
                    if row <= region_row:
                        lines = self.view.substr(r).splitlines()
                        line = lines[0]
                        print(line)
                        if line.startswith(" ") or line.startswith("\t"):
                            top_function = False
                        else:
                            top_function = True
                        name = clean_name.sub('', line)
                        if 'C++' in self.view.settings().get('syntax'):
                            if len(name.split('(')[0].split('::')) < 2:
                                name_fuction = name.split('(')[0].strip()
                            else:
                                name_fuction = name.split('(')[0].split('::')[1].strip()
                        else:
                            name_fuction = name.split('(')[0].split(':')[0].strip()
                        found = True
                        break

            s = ""
            if found:
                print(name_class, name_fuction, top_function)
                # 一级函数
                if top_function:
                    return name_fuction

                # 类的函数
                if name_class:
                    s += name_class
                if name_fuction:
                    if s:
                        s += "."
                    s += name_fuction
                return s
        return ""
