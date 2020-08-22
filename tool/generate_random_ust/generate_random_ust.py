#!python
# coding: utf-8
# Copyright (c) oatsu
"""
音程と歌詞がランダムなUSTを生成するツール
"""
import json
import random
from os import makedirs
from pprint import pprint

import utaupy as up

# from copy import deepcopy


PATH_CONFIG = 'generate_random_ust_config.json'


def generate_random_ustobj(d_config):
    """
    設定ファイルをもとに utaupy.ust.Ust オブジェクトをつくる
    """
    l_for_ust = []
    # バージョン情報用の空ノートを追加
    l_for_ust.append(up.ust.Note(tag='[#VERSION]'))
    # プロジェクト設定のノートを追加
    ust_setting = up.ust.Note(tag='[#SETTING]')
    ust_setting.set_by_key('Mode2', 'True')
    try:
        ust_setting.set_by_key('VoiceDir', d_config['voicedir'])
    except KeyError:
        ust_setting.set_by_key('VoiceDir', r'%VOICE%uta')
    try:
        ust_setting.set_by_key('Tool1', d_config['tool1'])
        ust_setting.set_by_key('Tool2', d_config['tool2'])
    except KeyError:
        ust_setting.set_by_key('Tool1', 'wavtool.exe')
        ust_setting.set_by_key('Tool2', 'resampler.exe')
    ust_setting.set_by_key('Mode2', 'True')
    l_for_ust.append(ust_setting)

    # ノートを一括で生成
    notes = [up.ust.Note(tag=f'[#{i}]') for i in range(d_config['ust_length'] - 1)]
    for note in notes:
        note.lyric = random.choice(d_config['aliases'])
        note.length = random.choice(d_config['note_length'])
        note.notenum = random.randrange(d_config['min_notenum'], d_config['max_notenum'])
    # 最初は全休符にする
    notes[0].lyric = 'R'
    notes[0].length = 1920
    # 最後は休符にする
    notes[-1].lyric = 'R'
    # リストに結合
    l_for_ust += notes

    # TRACKEND を追加
    l_for_ust.append(up.ust.Note(tag='[#TRACKEND]'))
    # Ustオブジェクトにする
    ust = up.ust.Ust()
    ust.values = l_for_ust
    # BPMをセット
    ust.tempo = d_config['bpm']

    return ust


def join_rest_note(ust):
    """
    休符を結合する
    """
    counter = 0

    for i, note in enumerate(ust.notes[1:]):
        # print(f'\n    join_rest_note: {note}')
        if (ust.notes[i].lyric == 'っ') and (note.lyric == 'っ'):
            note.lyric = 'R'
            # print("    join_rest_note: 'っ'→'っ' を検出したので後者の 'っ' を休符にしました。")
        elif (ust.notes[i].lyric == 'R') and (note.lyric == 'っ'):
            note.lyric = 'R'
            # print("    join_rest_note: 'R'→'っ' を検出したので後者の 'っ' を休符にしました。")

        if (ust.notes[i].lyric == 'R') and (note.lyric == 'R'):
            ust.notes[i].tag = '[#DELETE]'  # [#DELETE]にする
            note.length += ust.notes[i].length
            counter += 1
            # print("    join_rest_note: 'R'→'R' を検出したので休符を結合しました。")
        # print(f'    join_rest_note: {note}')
    # print(f'  休符を {counter}回 結合しました。')


def join_cl_note(ust):
    """
    促音「っ」を前の歌詞に結合する。
    """
    counter = 0
    for i, note in enumerate(ust.notes[1:]):
        if note.lyric == 'っ':
            # print(ust.notes[i])
            # print(note)
            ust.notes[i].length += note.length
            ust.notes[i].lyric += note.lyric
            note.tag = '[#DELETE]'  # [#DELETE]にする
            counter += 1
            # print(ust.notes[i])
            # print(note)
    # print(f'  促音を {counter}回 結合しました。')


def main():
    """
    ファイル入出力を担当
    """
    # 設定ファイルを読み取る
    print('PATH_CONFIG:', PATH_CONFIG)
    try:
        with open(PATH_CONFIG, mode='r', encoding='utf-8') as f_json:
            d_config = json.load(f_json)
    except UnicodeDecodeError:
        with open(PATH_CONFIG, mode='r', encoding='shift-jis') as f_json:
            d_config = json.load(f_json)
    pprint(d_config, compact=True)
    print()

    # 出力フォルダをつくる
    makedirs('out/ust_for_wav_and_lab', exist_ok=True)
    makedirs('out/ust_for_midi_and_musicxml', exist_ok=True)

    # Ustオブジェクトを生成して保存する
    for i in range(d_config['file_number']):
        path_ust_for_wav_and_lab = f'out/ust_for_wav_and_lab/random_{i}.ust'
        path_ust_for_midi_and_musicxml = f'out/ust_for_midi_and_musicxml/random_{i}.ust'
        # print('-----------------------------------------------------------')
        print(f'generating UST: path_ust_for_wav_and_lab      : {path_ust_for_wav_and_lab}')
        print(f'                path_ust_for_midi_and_musicxml: {path_ust_for_midi_and_musicxml}')
        ust = generate_random_ustobj(d_config)
        # 連続する休符を結合
        join_rest_note(ust)
        # WAV生成用のUSTを出力
        ust.write(path_ust_for_wav_and_lab)
        # 促音を前のノートに結合
        join_cl_note(ust)
        # MIDI, MusicXML, LAB 生成用のUSTを出力
        ust.write(path_ust_for_midi_and_musicxml)
    # print('-----------------------------------------------------------')


if __name__ == '__main__':
    main()
    input('Press Enter to exit.')
