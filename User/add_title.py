# -*- coding: utf-8 -*-

# __author__ = lilepeng@corp.netease.com
# __date__ = 2017/10/21 10:09:42

# desc: 添加标题

import sublime_plugin
from datetime import datetime

sStr = """# -*- coding: utf-8 -*-

# __author__ = lilepeng@corp.netease.com
# __date__ = %s

# desc: """


class AddTitleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.view.run_command("insert_snippet", {
            # "contents": "%s" % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %A")
            # 可根据自己的需要进行调整（参照后面的日期时间格式）
            # "contents": sStr % datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "contents": sStr % datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        })
