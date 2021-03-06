#!/usr/bin/env python3
# Copyright (c) 2020 oatsu
"""モノラベルだけからフルラベルを生成する。

NNSVSで話し声を学習してみたい。
"""

import utaupy as up
from utaupy.hts import Syllable, Note, Song
from tqdm import tqdm
from typing import List


def monolabel_to_full_phonemes(mono_label:up.label.Label, hts_conf: dict) -> List[up.hts.Phoneme]:
    """音素をCVで区切って音節のリストにする

    mono_label: モノラベル
    hts_conf: 母音などの判定をするやつ
    """
    # 音素の分類
    vowels = hts_conf['VOWELS']
    pauses = hts_conf['PAUSES']
    silences = hts_conf['SILENCES']
    breaks = hts_conf['BREAKS']
    # フルラベル用の音素に変換する。
    full_phonemes = []
    for mono_phoneme in mono_label:
        full_phoneme = up.hts.Phoneme()
        full_phoneme.start = mono_phoneme.start
        full_phoneme.end = mono_phoneme.end
        full_phoneme.identity = mono_phoneme.symbol
        full_phonemes.append(full_phoneme)
    # p1を埋める
    for phoneme in full_phonemes:
        phoneme_identity = phoneme.identity
        if phoneme_identity == 'xx':
            phoneme.language_independent_identity = 'xx'
        elif phoneme_identity in vowels:
            phoneme.language_independent_identity = 'v'
        elif phoneme_identity in pauses:
            phoneme.language_independent_identity = 'p'
        elif phoneme_identity in silences:
            phoneme.language_independent_identity = 's'
        elif phoneme_identity in breaks:
            phoneme.language_independent_identity = 'b'
        else:
            phoneme.language_independent_identity = 'c'
    return full_phonemes

def full_phonemes_to_syllables(full_phonemes: List[up.hts.Phoneme]) -> List[up.hts.Syllable]:
    """フルラベル用のPhonemeを音節ごとに区切る。

    後ろから作っていくと多分うまくいく。
    """
    syllable = Syllable()
    syllable.append(full_phonemes[-1])
    # 音節のリストを作る
    l_syllables = [syllable]

    full_phonemes_reversed = list(reversed(full_phonemes))
    for i, phoneme in enumerate(full_phonemes_reversed[1:], 1):
        # 休符と息継ぎと促音
        if phoneme.is_rest() or phoneme.is_break():
            syllable = Syllable()
            l_syllables.append(syllable)
            syllable.append(phoneme)
        # 母音
        elif phoneme.is_vowel():
            # 母音の次が息継ぎか促音のときは、同じ音節にする。
            if full_phonemes[i-1].is_break():
                syllable.append(phoneme)
            # 母音の次が息継ぎか促音でないときは、音節を切り替える。
            else:
                syllable = Syllable()
                l_syllables.append(syllable)
                syllable.append(phoneme)
        # 子音
        else:
            syllable.append(phoneme)

    # 音節と音素の順序を逆転させて、発声順に直す
    for syllable in l_syllables:
        syllable.data.reverse()
    l_syllables.reverse()
    return l_syllables

def syllables_to_notes(syllables: List[Syllable]) -> List[Note]:
    """
    音節のリストをノートのリストにする。
    日本語しか想定してないので1ノート1音節。
    """
    l_notes = []
    for syllable in syllables:
        note = Note()
        note.append(syllable)
        l_notes.append(note)
    return l_notes

def notes_to_song(notes:List[Note]) -> Song:
    """ノート(Note)のリストをSongオブジェクトにする。
    """
    song = Song()
    song.data = notes
    return song

def monolabel_to_song(mono_label: up.label.Label, hts_conf) -> Song:
    """
    モノラベル用のオブジェクトをフルラベル用のSongオブジェクトにする。
    """
    full_phonemes = monolabel_to_full_phonemes(mono_label, hts_conf)
    syllables = full_phonemes_to_syllables(full_phonemes)
    notes = syllables_to_notes(syllables)
    song = notes_to_song(notes)
    song._fill_phoneme_contexts(hts_conf)
    song._fill_syllable_contexts()
    # 休符からの距離(フレーズ内で何番目か)
    song._fill_e18_e19()
    # e6 を埋める。
    for note in song:
        note.number_of_syllables = len(note)
    # フレーズ数
    song._fill_j3()
    return song

def monolabel_file_to_fulllabel_file(path_mono_lab_in, path_full_lab_out, path_hts_conf):
    # TODO: ここtableじゃないようにする
    hts_conf = up.table.load(path_hts_conf)
    mono_label = up.label.load(path_mono_lab_in)
    song = monolabel_to_song(mono_label, hts_conf)
    song.write(path_full_lab_out)

def main():
    """
    ファイルを指定して変換
    """
    path_mono = input('path_mono: ')
    assert path_mono.strip('"').endswith('.lab')
    path_full = path_mono.replace('.lab', '_fakefull.lab')
    path_conf = input('path_conf: ')
    monolabel_file_to_fulllabel_file(path_mono, path_full, path_conf)
    up.utils.hts2json(path_full, path_full.replace('.lab', '.json'))

if __name__ == '__main__':
    main()
