#!python3
# coding: utf-8
# Copyright (c) oatsu
"""
USTの休符位置で音声ファイルを切断する。
もとの音声ファイル名のフォルダに、切断後の音声ファイルを格納する。
USTも休符位置で切断する。
もとのUSTファイル名のフォルダに、切断後のUSTファイルを格納する。
# NOTE: 切断・結合前後で音ズレや音質劣化がないか確認する。

- 手順 -
1. USTの休符位置を特定する。（ブレスは休符と同一視する）
2. 休符位置をもとに、切断したい時刻を決定する。
3. WAVファイルを分割する。
4. USTファイルを分割する。

5. 分割後USTをもとに、ざっくり推定したotoiniを生成する。
6. ひとつのoto.iniにまとめる。
7. moresamplerに渡す（pauとかどうすんの）

- 参考 -
【Python/pydub】mp3、wavファイルから部分抽出（切り分け、分割） | 西住工房
    https://algorithm.joho.info/programming/python/pydub-split/
【Python/pydub】mp3、wavの連結・結合 | 西住工房
    https://algorithm.joho.info/programming/python/pydub-connection/
【Python/pydub】再生時間、サンプリングレート、チャンネル数を取得 | 西住工房
    https://algorithm.joho.info/programming/python/pydub-time-sampling-rate-channel/
pydub/API.markdown at master · jiaaro/pydub
    https://github.com/jiaaro/pydub/blob/master/API.markdown
"""

import os
from copy import deepcopy
from pprint import pprint

import utaupy as up
from pydub import AudioSegment  # 音声ファイルをつぎはぎする
from tqdm import tqdm


# 実装済み
def join_br_and_pau(ust):
    """
    ustオブジェクトのブレスと休符をまとめて休符にする
    """
    new_notes = []
    notes = ust.values[2:-1]
    tpl = ('R', 'pau', 'br', '息')

    for i, note in enumerate(notes[:-1]):
        # 現在と次が休符かブレスのとき
        if notes[i].lyric in tpl and notes[i + 1].lyric in tpl:
            # 現在のノートは追加せず、次のノート長に加算する
            notes[i + 1].length += notes[i].length
        # 現在が休符でない、または次が休符ではないときは新規USTの要素に追加
        else:
            new_notes.append(note)
    new_notes.append(notes[-1])
    new_ust = up.ust.Ust()
    # NOTE: このUstクラスオブジェクトはファイル出力に適さない。ノート番号がずれている。
    new_ust.values = ust.values[:2] + new_notes + ust.values[-1:]

    return new_ust


# 実装済み
# DEBUG: ノート内は16分音符区切りだが、グローバルなグリッドには沿わないのを直す
def get_split_time_list(ust, threshold=240):
    """
    ust: utaupy.ust.Ust クラスオブジェクト
    threshold: 切断対象ノート最低長さ
    (threshold=480 ... 4分音符以上の休符で分割)

    Ustオブジェクトの休符位置を特定し、切断していい時刻のリストを返す。
    [切断時刻1, 切断時刻2, ... ]
    出来るだけ小節か拍の区切りで切断する。
    時刻の単位はms

    1. Ustオブジェクトの休符の開始時刻・終了時刻・長さを（UTAUのサンプル数で）取得する。
    2. 休符の長さが4分音符以上だったら切断位置の候補にする。
    3. ノートではなく楽譜上で8分音符の位置で切断するように（サンプル数で）計算する。
    4. 切断時刻をリストに追加する。
    5. 切断時刻をミリ秒に変換する
    5. リストを返す。
    """
    l = []
    t_start = 0  # ノート開始時刻（UTAUのサンプル数）
    notes = ust.values[2:-1]  # 歌詞のあるノート

    for note in notes:
        # print('get_split_time_list: processing: t_start={} lyric={},'.format(t_start, note.lyric))  # デバッグ用
        # 分割したいノートでの処理
        if (note.lyric in ['R', 'pau', 'br', '息']) and (note.length >= threshold):
            # 基準値の半ノート長
            half_threshold = threshold // 2
            # 半ノート長がいくつとれるか
            q = note.length // half_threshold
            # 分割位置のサンプル時刻(中央付近のグリッドで休符を分割する)
            t_split = t_start + (q // 2) * half_threshold
            print(f'  lyric: {note.lyric}, t_split: {t_split} Ticks')  # デバッグ用
            # 分割サンプル時刻のリストに追加
            l.append(t_split)

        # 次のノート開始時刻を更新
        t_start += note.length

    # 切断時刻をミリ秒に変換する
    l = [(125 * v / ust.tempo) for v in l]
    # 切断時刻(ms) のリストを返す
    return l


# 実装済み
def split_otoini(otoini, split_time_list):
    """
    iniファイルの音素時刻を切断後のwavファイルに合わせる。
    iniファイル内のwavファイル名を連番にする。
    USTをやるよりずっと簡単だと思う。
    """
    i = 0
    l = [0] + split_time_list
    for oto in otoini.values:
        # print(f'{oto.alias}\t{oto.offset}')  # デバッグ用
        # 切断位置を超えたらファイル名を変え、左ブランクの時間をずらす
        if oto.offset >= l[i + 1]:
            i += 1
        oto.filename = oto.filename.replace('.wav', f'__{str(i).zfill(6)}') + '.wav'
        oto.offset -= l[i]


# 未実装
def join_inifile():
    """
    oto.iniをもとにもどす。
    """
    pass


# 実装済み
def split_wavfile(path_wav, path_outdir, split_time_list):
    """
    path_wav: 分割したい音声ファイルのパス
    path_outdir: 分割音声を出力するフォルダのパス
    split_times: get_split_time_list で取得した、切断時刻のリスト

    切断時刻のリストをもとに、音声ファイルを切断する。
    出力ファイル名は basename__temp_000001.wav
    """
    # wavファイルの読み込み
    sound = AudioSegment.from_file(path_wav, format='wav')

    l = [0] + split_time_list + [len(sound)]
    # ミリ秒で区間指定して分割
    for n, _ in enumerate(l[:-1]):
        p = path_outdir + '/' + os.path.splitext(os.path.basename(path_wav))[0] + '__' + str(n).zfill(6) + '.wav'
        # 始端と終端時刻
        t_start = l[n]
        t_end = l[n + 1]
        print(f'  {p}  t_start: {t_start}  t_end: {t_end}')  # デバッグ用
        cut_sound = sound[t_start:t_end]
        cut_sound.export(p, format='wav')


def main():
    # 処理対象ファイルを指定
    path_ust = input('path_ust: ')
    path_table = input('path_table: ')
    path_wav = path_ust.replace('.ust', '.wav')
    # 出力フォルダを作成
    os.makedirs('out', exist_ok=True)
    path_outdir = 'out'
    # ustを読み取り
    ust_original = up.ust.load(path_ust)
    # ustオブジェクトの休符とブレスを連結
    ust_processed = join_br_and_pau(ust_original)
    ust_processed.make_finalnote_R()
    ust_processed.write('out/test.ust')
    # ustから分割時刻を取得(ms)
    split_time_list = get_split_time_list(ust_processed)
    print(f'split_time_list: {split_time_list}')  # デバッグ用
    # wavファイルを分割
    split_wavfile(path_wav, path_outdir, split_time_list)

    name_wav = os.path.basename(path_wav)
    # 休符結合済みustオブジェクトからmoresampler用のotoiniオブジェクトを生成する
    # NOTE: ひらがな連続音エイリアスになるようにする
    otoini_processed = up.convert.ust2otoini(ust_processed, name_wav, path_table)
    # 左ブランクの時刻をもとに、切断が含まれるエイリアスでfilenameの通し番号を変える
    split_otoini(otoini_processed, split_time_list)
    otoini_processed.write('out/oto.ini')
    # moresamplerを起動して、update機能を実行する
    # TODO: update
    # もとのustから生成したotoiniに、moresamplerで設定したパラメータを適用する。
    # またはもとのustから生成したotoiniと比較して、ブレスと休符のエイリアスを追加する。
    # otoiniをファイル出力する


if __name__ == '__main__':
    main()
    input('Press Enter to exit.')
