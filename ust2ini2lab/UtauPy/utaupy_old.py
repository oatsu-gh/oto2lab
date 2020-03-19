#!/usr/bin/python3.8
# coding: utf-8
"""
プラグイン実行したときの一時ファイルを読み取り、pythonで扱いやすいようなデータにする。
・全体のデータは辞書型で扱う。
・utaupy.py内では、辞書型変数 d を全体のデータとして用いている。
・Python3.7以上を推奨。（辞書型が要素の順番を保持できるため）
・要素の順番を保持できないとノートの順番が変わる恐れがある。
・[#DELETE]まわりの処理が不安定です。（改善中）
"""

import sys
# from collections import OrderedDict
from pprint import pprint


# -----UTAU一時ファイル入出力に使う関数群（ここから）---------------
def read_utau(path):
    """
    UTAUの一時ファイルを読み取り、辞書を要素とするリストで返す関数。
    ノート情報（辞書のキー）のうち 'Tag', 'Version' はUTAUスクリプト中には存在しないため注意。
    """
    # d = {'ノートの種類': {項目1: , 項目2: ,...}, ...}
    l = []
    d = {'Tag': 'dummy'}
    tag = ''
    info = []
    # info_key = ''
    # info_val = ''

    # 行をリストとして読む。改行コードを削除。
    try:
        with open(path, 'r+') as f:
            lines = [s.strip() for s in f.readlines()]
    # utf-8のUST用の例外処理
    except UnicodeDecodeError:
        with open(path, 'r+', encoding="utf-8_sig") as f:
            lines = [s.strip() for s in f.readlines()]

    for line in lines:
        # ノート属性を登録
        # '[#VERSION]', '[#SETTING]', ..., '[#0015]', '[#0016]', ..., '[#NEXT]'
        if line.startswith('[#'):
            l.append(d)
            tag = line
            d = {'Tag': tag}

        # ノート情報を登録
        # 例: line = 'Length=480'
        else:
            try:
                info = line.split('=', 1)
                d[info[0]] = info[1]  # 例: d['Length'] = 480

            # バージョン情報の行は '=' を含まないので例外
            except IndexError as e:
                if tag == '[#VERSION]':
                    d['Version'] = line
                else:
                    print('\nERROR in read_txt: {}'.format(e))
                    input('Press enter to exit.')
                    sys.exit()

    # 最後のノート（NEXT）をリストに追加
    l.append(d)
    # 最初の要素は空の辞書のため削除
    del l[0]

    return l


def write_utau(path, l):
    """
    辞書型の編集済みデータをもとに、UTAU一時ファイルを上書きする関数。
    改行を含む文字列にまとめてから一気に書き込む。
    """
    if not isinstance(l, list):
        print('write_utau(path, l) の l はリストで渡してください。')
    s = ''
    # 1行ずつ文字列に追加
    for d in l:
        # バージョンの行だけ '=' がないため別処理
        if d['Tag'] == '[#VERSION]':
            if d['Version'] == 'UST Version is 1.19 or older':
                pass
            else:
                s += '{}\n'.format(d['Tag'])      # 例: '[#VERSION]'
                s += '{}\n'.format(d['Version'])  # 例: 'UST Version 1.20'

        else:
            s += '{}\n'.format(d.pop('Tag'))    # 例: '[#0015]'
            for info_key, info_val in d.items():
                s += '{}={}\n'.format(str(info_key), str(info_val))  # 例: 'Length=480'

    # UTAU一時ファイルの書き込み
    with open(path, mode='w') as f:
        f.write(s)
    # 書き込んだ内容を返す
    return s
# -----UTAU一時ファイル入出力に使う関数群（ここまで）---------------


# -----ほかの関数内で呼び出しがちな関数群（ここから）-------------
def get_note(d, n):
    """
    選択範囲n番目のノート情報を取得(0-indexed)
    """
    # 辞書型は番号指定できないのでリストに変換
    # l = list(d.items())
    # VERSION, SETTINGS, PREV を無視するためにnを3ずらす
    # note = dict(l[n+3])
    # return note

    # 以上をまとめて
    return dict(list(d.items)[n + 3])


def set_noteinfo(d, n, info):
    """
    n番目のノート情報のうち、特定の情報のみを上書きする関数。
    infoは辞書 (例: {'Length': 480, 'PBW': '50,20,20'})
    """
    if not isinstance(info, dict):
        print('set_note(d, n, info) の info は辞書型で渡してください。')
        print("--- 例: {'Length': 480, 'PBW': '50,20,20'} 辞書項目は一つでも複数でもOKです。")
        input('Press enter to exit.')
    # 辞書型は番号指定できないのでリストに変換
    l = list(d.items())
    for info_key, info_val in info.items():
        # VERSION, SETTINGS, PREV を無視するためにnを3ずらす
        # n番目ノート情報を変更
        l = l[:n + 3] + {l[n + 3][info_key]: info_val} + l[n + 4:]

    # 辞書に戻して返す
    return dict(l)
# -----ほかの関数内で呼び出しがちな関数群（ここまで）-------------


def get_notes(d):
    """
    選択範囲のノート情報のみ取得
    """
    # 辞書型は番号指定できないのでリストに変換して抽出
    # l = list(d.items())
    # notes = dict(l[3:-1])
    # return notes

    # 以上をまとめて
    return dict(list(d.items)[3: -1])

    # あるいはノート情報以外を削除
    # del(d['[#VERSION]'], d['[#SETTINGS]'], d['[#PREV]'], d['[#NEXT]'])
    # return d


def delete_note(l, n):
    """
    n番目のノートを削除する関数(0-indexed)
    ノートが消えてもリストには残ることに注意
    """
    l[n + 3]['Tag'] = '[#DELETE]'
    return l


def set_note(d, n, note):
    """
    n番目のノートをまるごと上書きする関数。(0-indexed)
    """
    # 辞書型は番号指定できないのでリストに変換
    l = list(d.items())

    # VERSION, SETTINGS, PREV を無視するためにnを3ずらす
    # n番目ノートを上書き
    l = l[:n + 3] + list(note.items()) + l[n + 4:]

    # 辞書に戻して返す
    return dict(l)


def get_version(d):
    """
    USTのバージョンを取得する関数
    """
    return d['[#VERSION]']


def get_setting(d):
    """
    UTAU設定を取得する関数
    """
    return d['[#SETTING]']


def get_prevnote(d):
    """
    選択範囲直前のノート情報を取得する関数
    """
    return d['[#PREV]']


def get_nextnote(d):
    """
    選択範囲直後のノート情報を取得する関数
    """
    return d['[#NEXT]']


def get_envelope(d, n):
    """
    n番目のノートのEnvelopeをリストで返す
    """
    envelope = get_note(d, n)['Envelope']
    envelope = list(map(int, envelope.split(',')))
    return envelope


def get_pbw(d, n):
    """
    n番目のノートのPBWをリストで取得
    """
    pbw = get_note(d, n)['PBW']
    pbw = list(map(int, pbw.split(',')))
    return pbw


def set_envelope(d, n, envelope):
    """
    n番目のノートのPBWを上書きする関数
    変更前データは辞書型で、PBWはリストで受け取る
    変更後データを辞書型で返す
    """
    # リストとして受け取ったEnvelopeを文字列にしてから、辞書を生成
    info = {'PBW': ','.join(envelope)}
    # PBW情報をもとの辞書に上書き
    d = set_note(d, n, info)

    return d


def set_pbw(d, n, pbw):
    """
    n番目のノートのPBWを上書きする関数
    変更前データは辞書型で、PBWはリストで受け取る
    変更後データを辞書型で返す
    """
    if isinstance(pbw, list):
        print('set_pbw(d, n, pbw) の pbw は配列型で渡してください。')
        input('Press enter to exit.')
        sys.exit()
    # リストとして受け取ったPBWを文字列にしてから辞書を生成
    info = {'PBW': ','.join(pbw)}
    # PBW情報をもとの辞書に上書き
    d = set_note(d, n, info)

    return d


def length_to_msec(tempo, length):
    """
    Tempo[beat/min] 480[Ticks/beat] を用いて、
    Length[Ticks] → Length[msec] の変換をする。
    """
    # sec_per_beat = 60 / tempo
    # ticks_per_beat = 480
    # sec_per_ticks = sec_per_beat / tick_per_beat
    # msec_per_ticks = sec_per_ticks * 1000
    # 以上をまとめると msec_per = int(1000 * 60 / 480 / tempo)
    # msec = length * msec_per_ticks
    # return int(msec)
    return 125 * length // tempo  # 単位が[msec]な値を返す


def msec_to_length(tempo, msec):
    """
    msec → Length[Tics] の換算をする。
    """
    return msec * tempo // 125


def main():
    '''
    全体の処理実行
    '''
    debug = True

    # UTAU一時ファイルをコマンドライン引数で指定
    # コマンドライン引数で指定されていない場合は標準入力を要求
    try:
        path = sys.argv[1]
    except IndexError:
        path = input('UTAU一時ファイルのパス\n>>> ')

    # 入力ファイルを読み取り
    utau_in = read_utau(path)
    if debug:
        print('path =', path)
        print('----↓read_utauの結果↓-------------------')
        pprint(utau_in)
        print('----↑read_utauの結果↑-------------------\n')

    # このへんで編集
    d = utau_in

    # 編集結果をファイル出力
    utau_out = write_utau(path + '_debug.cs', d)
    if debug:
        print('----↓write_utauの内容↓------------------')
        print(utau_out)
        print('----↑write_utauの内容↑------------------\n')


if __name__ == '__main__':
    main()


if __name__ == '__init__':
    print('using UtauPy...')
