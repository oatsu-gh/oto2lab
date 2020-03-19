#!/usr/bin/env python3
# coding: utf-8
"""
UTAUのデータ整理用モジュール
クラスを使ってがんばる
"""
import re
# from datetime import datetime
# from pprint import pprint

# from tqdm import tqdm


class Ust:
    """UST"""

    def __init__(self):
        """インスタンス作成"""
        # ノート(クラスオブジェクト)からなるリスト
        self.notes = []

    def read_ust(self, path, mode='r'):
        """USTを読み取り"""
        # USTを文字列として取得
        try:
            with open(path, mode=mode) as f:
                s = f.read()
        except UnicodeDecodeError:
            with open(path, mode=mode, encoding='utf-8_sig') as f:
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
        if self.notes[0].tag == r'[#VERSION]':
            version_info = self.notes[0].version()
            self.notes.insert(0, 'UST Version {}'.format(version_info))

    def values(self):
        """中身を見る"""
        return self.notes

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
            first_note_tempo = self.notes[2].tempo()
            return first_note_tempo
        except KeyError:
            project_tempo = self.notes[1].tempo()
            return project_tempo

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
        print('Making "Note" instance from UST: {}'.format(tag))

        # タグ以外の行の処理
        if tag == '[#VERSION]':
            self.d['VersionInfo'] = lines[1]
        elif tag == '[#TRACKEND]':
            pass
        else:
            for v in lines[1:]:
                tmp = v.split('=', 1)
                self.d[tmp[0]] = tmp[1]

        return self
    # ここまでデータ入力系-----------------------------------------------------

    # ここからデータ参照系-----------------------------------------------------
    def values(self):
        """ノートの中身を見る"""
        return self.d

    def find_by_key(self, key):
        """ノートの特定の情報を確認"""
        return self.d[key]

    def tag(self):
        """タグを確認"""
        return self.d['Tag']

    def length(self):
        """ノート長を確認[samples]"""
        return self.d['Length']

    def lyric(self):
        """歌詞を確認"""
        return self.d['Lyric']

    def notenum(self):
        """音階番号を確認"""
        return self.d['NoteNum']

    def tempo(self):
        """BPMを確認"""
        return self.d['Tempo']

    # ここまでデータ参照系-----------------------------------------------------

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
        self.otolist = []

    def read_otoini(self, path, mode='r'):
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

    def values(self):
        """中身を確認する"""
        return self.otolist


class Oto:
    """oto.ini中の1モーラ"""

    def __init__(self):
        self.d = {}

    def from_otoini(self, l):
        """リストをもらってクラスオブジェクトにする"""
        keys = ('FileName', 'Alies', 'LBlank', 'Fixed', 'RBlank', 'Onset', 'Overlap')
        self.d = dict(zip(keys, l))
        return self

    def values(self):
        """中身を確認する"""
        return self.d

    def get_filename(self):
        """wavファイル名を確認する"""
        return self.d['FileName']

    def get_ファイル名(self):
        """wavファイル名を確認する"""
        return self.d['FileName']

    def get_alies(self):
        """エイリアスを確認する"""
        return self.d['Alies']

    def get_エイリアス(self):
        """エイリアスを確認する"""
        return self.d['Alies']

    def get_lblank(self):
        """左ブランクを確認する"""
        return self.d['LBlank']

    def get_左ブランク(self):
        """左ブランクを確認する"""
        return self.d['LBlank']

    def get_fixed(self):
        """固定範囲を確認する"""
        return self.d['Fixed']

    def get_固定範囲(self):
        """固定範囲を確認する"""
        return self.d['Fixed']

    def get_固定範囲rblank(self):
        """右ブランクを確認する"""
        return self.d['RBlank']

    def get_右ブランク(self):
        """左ブランクを確認する"""
        return self.d['RBlank']

    def get_onset(self):
        """先行発声を確認する"""
        return self.d['Onset']

    def get_先行発声(self):
        """先行発声を確認する"""
        return self.d['Onset']

    def get_overlap(self):
        """右ブランクを確認する"""
        return self.d['Overlap']

    def get_オーバーラップ(self):
        """左ブランクを確認する"""
        return self.d['Overlap']

    def set_filename(self, x):
        """wavファイル名を上書きする"""
        self.d['FileName'] = x

    def set_ファイル名(self, x):
        """wavファイル名を上書きする"""
        self.d['FileName'] = x

    def set_alies(self, x):
        """エイリアスを上書きする"""
        self.d['Alies'] = x

    def set_エイリアス(self, x):
        """エイリアスを上書きする"""
        self.d['Alies'] = x

    def set_lblank(self, x):
        """左ブランクを上書きする"""
        self.d['LBlank'] = x

    def set_左ブランク(self, x):
        """左ブランクを上書きする"""
        self.d['LBlank'] = x

    def set_fixed(self, x):
        """固定範囲を上書きする"""
        self.d['Fixed'] = x

    def set_固定範囲(self, x):
        """固定範囲を上書きする"""
        self.d['Fixed'] = x

    def set_固定範囲rblank(self, x):
        """右ブランクを上書きする"""
        self.d['RBlank'] = x

    def set_右ブランク(self, x):
        """左ブランクを上書きする"""
        self.d['RBlank'] = x

    def set_onset(self, x):
        """先行発声を上書きする"""
        self.d['Onset'] = x

    def set_先行発声(self, x):
        """先行発声を上書きする"""
        self.d['Onset'] = x

    def set_overlap(self, x):
        """右ブランクを上書きする"""
        self.d['Overlap'] = x

    def set_オーバーラップ(self, x):
        """左ブランクを上書きする"""
        self.d['Overlap'] = x

def main():
    """デバッグ用実装"""
    print('UST, otoini などを編集するためのモジュールです。')
    print('クラス Ust, Note, Otoini, Oto を実装済みです。')


if __name__ == '__main__':
    main()
    input('Press enter to exit.')

if __name__ == '__init__':
    print('UtauPy is being imported.')
