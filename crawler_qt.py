# -*- coding: utf-8 -*-
# @Time : 2019-08-17 12:50 
# @Author : Hubery
# @File : crawler_qt.py
# @Software: PyCharm
"""
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import sys
import os
from datetime import datetime

# from PySide2 import QtCore, QtWidgets, QtGui
from PySide2 import QtCore
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QApplication, QFormLayout, \
    QHBoxLayout, QVBoxLayout, QMessageBox

from crawler_sina import get_mid, get_response, get_context

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        formlayout = QFormLayout()
        formlayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        formlayout.setVerticalSpacing(20)

        explain = QLabel("推送小工具请粘贴微博文章详情页链接，并选择类型，提交。")
        url = QLabel('微博链接：')
        data_type = QLabel('选择类型：')

        self.url_edit = QLineEdit()
        self.data_type_edit = QComboBox()
        self.data_type_edit.addItems(['负面', '中性', '正面'])

        button = QPushButton('提交', self)
        button.setStyleSheet("background-color: rgb(255, 255, 255);")

        formlayout.addRow(explain)
        formlayout.addRow(url, self.url_edit)
        formlayout.addRow(data_type, self.data_type_edit)

        hbox = QHBoxLayout()
        hbox.addStretch(0)
        hbox.addWidget(button)
        vbox = QVBoxLayout()
        vbox.addStretch(0)
        vbox.addLayout(hbox)
        formlayout.addRow(vbox)
        self.setLayout(formlayout)
        # x y 宽 高
        self.setGeometry(500, 200, 600, 400)
        self.setWindowTitle('推送小工具')
        self.show()
        # self.data_type_edit.currentIndexChanged[str].connect(self.print_value)  # 条目发生改变，发射信号，传递条目内容
        button.clicked.connect(self.but_click)

    def but_click(self):
        url = self.url_edit.text()
        data_type_edit = self.data_type_edit.currentText()
        if not url:
            QMessageBox.critical(self, '错误', '请输入微博链接')
            return False
        mid = get_mid(url)
        if not mid:
            QMessageBox.critical(self, '错误', '请输入符合正确的微博链接')
            self.url_edit.setText('')
            return False
        status = get_response(mid)
        result = get_context(status)
        tem = '{}\n'.format(data_type_edit) + result + '{}\n'.format(url)
        write_context(tem)
        QMessageBox.information(self, '提示', '已成功写入')
        self.url_edit.setText('')
        return True


def write_context(string):
    dirname = 'result'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    result_path = os.path.join(BASE_DIR, dirname)
    file_name = '{}.txt'.format(datetime.strftime(datetime.now(), '%Y-%m-%d'))
    file_path = os.path.join(result_path, file_name)
    with open(file_path, 'a+', encoding='utf8') as f:
        f.write(string + '\n')


def run():
    """运行入口"""
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
