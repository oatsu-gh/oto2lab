#!python
# coding: utf-8
# Copyright (c) oatsu
"""
プロジェクトを変更しても処理内容を上書きされないようにする
"""

from MyProject1MyFrame1 import MyProject1MyFrame1


class MyProject1MyFrame1Child(MyProject1MyFrame1):
    """
    wxformbuilder が生成する MyProject1MyFrame1 をいじるためのクラス
    """
    def m_convertButton2OnButtonClick(self, event):
        """
        右の変換ボタンをクリックしたときの動作
        """
        self.m_convertButton2.SetLabel('pressed')
