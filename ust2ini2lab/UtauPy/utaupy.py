#!/usr/bin/env python3
# coding: utf-8
"""
UTAUのデータ整理用モジュール
クラスを使ってがんばる
"""
import os
import re

# from datetime import datetime
# from pprint import pprint

# from tqdm import tqdm


def new_otoiniobj_from_ustobj(ust, name_wav, dt=200, overlap=100):
    """
    UstクラスオブジェクトからOtoIniクラスオブジェクトを生成
    dt     : 左ブランクと先行発声の時間距離
    overlap: オーバーラップと先行発声の距離
    【パラメータ設定図】
    # t-dt           t-overlap      t            length+dt  length+dt    length+dt
    # |  左ブランク  |オーバーラップ|  先行発声  | 固定範囲 | 右ブランク |
    # |(dt-overlap)ms| (overlap)ms  | (length)ms |   0ms    |    0ms     |
    """
    notes = ust.get_values()
    tempo = ust.get_tempo()
    otoini = OtoIni()
    otolist = []
    t = 0
    for note in notes[2:-1]:
        length = note.get_length_ms(tempo)
        oto = Oto()
        oto.set_filename(name_wav)
        oto.set_alies(note.get_lyric())
        oto.set_lblank(max(t - dt, 0))
        oto.set_overlap(min(length - 20, dt - overlap))
        oto.set_onset(min(length - 10, dt))
        oto.set_fixed(length + dt)
        oto.set_rblank(-(length + dt))  # 負で左ブランク相対時刻, 正で絶対時刻
        otolist.append(oto)
        t += length  # 今のノート終了位置が次のノート開始位置
    otoini.set_values(otolist)
    return otoini


def write_inifile(otoini, outpath):
    """OtoIniクラスオブジェクトをiniファイルとして出力"""
    s = ''
    for oto in otoini.get_values():
        l = []
        l.append(oto.get_filename())
        l.append(oto.get_alies())
        l.append(oto.get_lblank())
        l.append(oto.get_fixed())
        l.append(oto.get_rblank())
        l.append(oto.get_onset())
        l.append(oto.get_overlap())
        s += '{}={},{},{},{},{},{}\n'.format(*l)  # 'l[0]=l[1],l[2],...'
    with open(outpath, 'w', encoding='shift-jis') as f:
        f.write(s)
    return s


def ust2ini_solo(path_ust, outdir):
    """USTファイルをINIファイルに変換する"""
    basename = os.path.basename(path_ust)
    ust = Ust()
    ust.new_from_ustfile(path_ust)
    otoini = new_otoiniobj_from_ustobj(ust, basename)
    outpath = outdir + basename.replace('.wav', '.ini')
    write_inifile(otoini, outpath)
    return outpath

class Ust:
    """UST"""

    def __init__(self):
        """インスタンス作成"""
        # ノート(クラスオブジェクト)からなるリスト
        self.notes = []

    def new_from_ustfile(self, path_ust, mode='r'):
        """USTを読み取り"""
        # USTを文字列として取得
        try:
            with open(path_ust, mode=mode) as f:
                s = f.read()
        except UnicodeDecodeError:
            with open(path_ust, mode=mode, encoding='utf-8_sig') as f:
                s = f.read()
        # USTをノート単位に分割
        l = [r'[#' + v.strip() for v in s.split(r'[#')]
        # 最初の行は空なので消す
        del l[0]
        # さらに行ごとに分割
        l = [v.split('\n') for v in l]
        # print('\n-----l in Ust.read_file----------')
        # pprint(l)
        # print('-----l in Ust.read_file----------\n')
        # ノートのリストを作る
        for lines in l:
            note = Note()
            note.from_ust(lines)
            self.notes.append(note)
        # 旧形式の場合にタグの数を合わせる
        if self.notes[0].get_tag() != r'[#VERSION]':
            ust_version = self.notes[0].get_by_key('UstVersion')
            note = Note()
            note.set_tag(r'[#VERSION]')
            note.set_by_key('UstVersion', ust_version)
            self.notes.insert(0, note)
        print('USTを読み取りました。: {}'.format(os.path.basename(path_ust)))

    def get_values(self):
        """中身を見る"""
        return self.notes

    def set_values(self, l):
        """中身を上書きする"""
        self.notes = l

    # def write_file(self, path, mode='w'):
    def write_ust(self, path, mode='w'):
        """USTを保存"""
        lines = []
        for note in self.notes:
            # ノートを解体して行のリストに
            tmp = note.as_lines()
            lines += tmp
        # 出力用の文字列
        s = '\n'.join(lines) + '\n'
        # ファイル出力
        with open(path, mode=mode) as f:
            f.write(s)
        return s

    def get_tempo(self):
        """全体のBPMを見る"""
        try:
            project_tempo = self.notes[1].get_tempo()
            return project_tempo
        except KeyError:
            first_note_tempo = self.notes[2].get_tempo()
            return first_note_tempo

        print('\n[ERROR]--------------------------------------------------')
        print('USTのテンポが設定されていません。とりあえず120にします。')
        print('---------------------------------------------------------\n')
        return '120'


class Note:
    """UST内のノート"""

    def __init__(self):
        self.d = {'Tag': None}

    # ここからデータ入力系-----------------------------------------------------
    def from_ust(self, lines):
        """USTの一部からノートを生成"""
        # ノートの種類
        tag = lines[0]
        self.d['Tag'] = tag
        # print('Making "Note" instance from UST: {}'.format(tag))
        # タグ以外の行の処理
        if tag == '[#VERSION]':
            self.d['UstVersion'] = lines[1]
        elif tag == '[#TRACKEND]':
            pass
        else:
            for v in lines[1:]:
                tmp = v.split('=', 1)
                self.d[tmp[0]] = tmp[1]
        return self
    # ここまでデータ入力系-----------------------------------------------------

    # ここからデータ参照系-----------------------------------------------------
    def get_values(self):
        """ノートの中身を見る"""
        return self.d

    def get_by_key(self, key):
        """ノートの特定の情報を確認"""
        return self.d[key]

    def get_tag(self):
        """タグを確認"""
        return self.d['Tag']

    def get_length(self):
        """ノート長を確認[samples]"""
        return self.d['Length']

    def get_length_ms(self, tempo):
        """ノート長を確認[ms]"""
        return 125 * float(self.d['Length']) / float(tempo)

    def get_lyric(self):
        """歌詞を確認"""
        return self.d['Lyric']

    def get_notenum(self):
        """音階番号を確認"""
        return self.d['NoteNum']

    def get_tempo(self):
        """BPMを確認"""
        return self.d['Tempo']
    # ここまでデータ参照系-----------------------------------------------------

    # ここからデータ上書き系-----------------------------------------------------
    def set_values(self, d):
        """ノートの中身を見る"""
        self.d = d

    def set_by_key(self, key, x):
        """ノートの特定の情報を確認"""
        self.d[key] = x

    def set_tag(self, x):
        """タグを確認"""
        self.d['Tag'] = x

    def set_length(self, x):
        """ノート長を確認[samples]"""
        self.d['Length'] = x

    def set_length_ms(self, x, tempo):
        """ノート長を確認[ms]"""
        self.d['Length'] = x * tempo // 125

    def set_lyric(self, x):
        """歌詞を確認"""
        self.d['Lyric'] = x

    def set_notenum(self, x):
        """音階番号を確認"""
        self.d['NoteNum'] = x

    def set_tempo(self, x):
        """BPMを確認"""
        self.d['Tempo'] = x
    # ここまでデータ上書き系-----------------------------------------------------

    # ここからデータ操作系-----------------------------------------------------
    def add_property(self, key, value):
        """
        ノート情報を追加
        既存情報の上書きに注意
        """
        self.d[key] = value

    def del_property(self, key):
        """ノート情報を削除"""
        if key != 'Tag':
            del self.d[key]
        else:
            print('\n[ERROR]-----------------------------')
            print('タグ（ノート番号）は削除できません。')
            print('[ERROR]-----------------------------\n')
    # ここまでデータ操作系-----------------------------------------------------

    # ここからノート操作系-----------------------------------------------------
    def delete(self):
        """選択ノートを削除"""
        self.d['Tag'] = '[#DELETE]'

    def insert(self):
        """ノートを挿入(したい)"""
        self.d['Tag'] = '[#INSERT]'
    # ここまでノート操作系-----------------------------------------------------

    # ここからデータ出力系-----------------------------------------------------
    def as_lines(self):
        """出力用のリストを返す"""
        d = self.d
        lines = []
        lines.append(d.pop('Tag'))
        for k, v in d.items():
            line = '{}={}'.format(str(k), str(v))
            lines.append(line)
        return lines
    # ここまでデータ出力系-----------------------------------------------------


class OtoIni:
    """oto.iniを想定したクラス"""

    def __init__(self):
        # 'Oto'クラスからなるリスト
        self.otolist = []

    def new_from_inifile(self, path, mode='r'):
        """otoiniを読み取ってオブジェクト生成"""
        with open(path, mode=mode) as f:
            l = [re.split('[=,]', s.strip()) for s in f.readlines()]
        # 入力ファイル末尾の空白行を除去
        while l[-1] == ['']:
            del l[-1]

        for v in l:
            oto = Oto()
            oto.from_otoini(v)
            self.otolist.append(oto)
        return self

    def new_from_ustobj(self, ust):
        """クラスUstのオブジェクトからクラスOtoIniオブジェクトを作る"""

    def get_values(self):
        """中身を確認する"""
        return self.otolist

    def set_values(self, l):
        """中身を上書きする"""
        self.otolist = l


class Oto:
    """oto.ini中の1モーラ"""

    def __init__(self):
        keys = ('FileName', 'Alies', 'LBlank', 'Fixed', 'RBlank', 'Onset', 'Overlap')
        l = [None] * 7
        self.d = dict(zip(keys, l))

    def from_otoini(self, l):
        """リストをもらってクラスオブジェクトにする"""
        keys = ('FileName', 'Alies', 'LBlank', 'Fixed', 'RBlank', 'Onset', 'Overlap')
        self.d = dict(zip(keys, l))
        return self

    # ここからノートの全値の処理----------------------
    def get_values(self):
        """中身を確認する"""
        return self.d

    def set_values(self, d):
        """中身を上書きする"""
        self.d = d
    # ここまでノートの全値の処理----------------------

    # ここからノートの各値の参照----------------------
    def get_filename(self):
        """wavファイル名を確認する"""
        return self.d['FileName']

    def get_alies(self):
        """エイリアスを確認する"""
        return self.d['Alies']

    def get_lblank(self):
        """左ブランクを確認する"""
        return self.d['LBlank']

    def get_fixed(self):
        """固定範囲を確認する"""
        return self.d['Fixed']

    def get_rblank(self):
        """右ブランクを確認する"""
        return self.d['RBlank']

    def get_onset(self):
        """先行発声を確認する"""
        return self.d['Onset']

    def get_overlap(self):
        """右ブランクを確認する"""
        return self.d['Overlap']
    # ここまでノートの各値の参照----------------------

    # ここからの各値の上書き----------------------
    def set_filename(self, x):
        """wavファイル名を上書きする"""
        self.d['FileName'] = x

    def set_alies(self, x):
        """エイリアスを上書きする"""
        self.d['Alies'] = x

    def set_lblank(self, x):
        """左ブランクを上書きする"""
        self.d['LBlank'] = x

    def set_fixed(self, x):
        """固定範囲を上書きする"""
        self.d['Fixed'] = x

    def set_rblank(self, x):
        """右ブランクを上書きする"""
        self.d['RBlank'] = x

    def set_onset(self, x):
        """先行発声を上書きする"""
        self.d['Onset'] = x

    def set_overlap(self, x):
        """右ブランクを上書きする"""
        self.d['Overlap'] = x
    # ここまでノートの各値の上書き----------------------


def main():
    """デバッグ用実装"""
    print('UST, otoini などを編集するためのモジュールです。')
    print('クラス Ust, Note, Otoini, Oto を実装済みです。')


if __name__ == '__main__':
    main()
    input('Press enter to exit.')

if __name__ == '__init__':
    print('ξ・ヮ・) < UtauPy imported.')
