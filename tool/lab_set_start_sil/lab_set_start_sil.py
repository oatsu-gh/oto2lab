#!python
# coding: utf-8
# Copyright (c) oatsu
"""
LABファイルに開幕のsilを追加する
・musicname.lab (もとのLAB) を読み取る
・musicname_sinsy.lab (MusicXMLから生成したLAB)を読み取る
・musicname_sinsy のほうの1行目と2行目のpauの開始時刻を取得
・musicname.lab の 1行目に sil を追加し、最初の pau の開始時刻を上書きする。
"""
from glob import glob
import utaupy as up

def main():
    path_sinsy_lab_dir = input('2種類のLABファイルがあるフォルダを指定してください\n>>> ')
    # Sinsy で MusicXML から生成したラベルのリスト
    l_sinsy_lab = glob(f'{path_sinsy_lab_dir}/*_sinsy.lab')
    for path_sinsy_lab in l_sinsy_lab:
        path_original_lab = path_sinsy_lab.replace('_sinsy.lab', '.lab')
        print(f'processing: {path_original_lab}')
        sinsy_label = up.label.load(path_sinsy_lab)
        original_label = up.label.load(path_original_lab)
        if original_label.values[0].symbol == 'sil':
            print('すでに最初の音素が sil なのでスキップします。')
        original_label.values = [sinsy_label.values[0]] + original_label.values
        original_label.values[1].start = original_label.values[0].end
        original_label.write(path_original_lab)

if __name__ == '__main__':
    main()
    input('Press Enter to exit')
