#!/bin/bash
# coding: utf-8
# Copyright (c) 2020 oatsu

# wsl run.sh で実行するとPATHが皆無なので登録する
PATH="$HOME/.local/:$PATH"
# pysinsyがSinsyにアクセスできるようにする
LD_LIBRARY_PATH=/usr/local/lib/
# pathに日本語が含まれるとSinsyがエラーを出すので、一時フォルダを使って回避する。
path_temp_dir=$HOME/temp_nnsvs
# このファイルがあるディレクトリ
script_dir=$(cd $(dirname $0); pwd)

# 入出力するフォルダ
path_dir_xml="./musicxml"
path_dir_lab="./lab_input_sinsy"
path_dir_uttlist="./xml2lab_mono/02_uttlist"
path_uttlist="./xml2lab_mono/02_uttlist/utt_list.txt"
path_dir_table="./xml2lab_mono/dic/sinsy"

# 出力フォルダを作成する
mkdir -p $path_dir_lab
mkdir -p $path_dir_uttlist

# 古いファイルを掃除する
rm -rf $path_temp_dir
rm -f $path_dir_lab/*
rm -f $path_dir_uttlist/*

# 一時フォルダを作る
mkdir $path_temp_dir

# musicxml ファイルをWSLのHOMEに移動させる
python $script_dir/xml2lab.py \
    $path_dir_xml \
    $path_temp_dir \
    $path_dir_lab \
    $path_dir_table \
    $path_uttlist

# 不要になった一時フォルダを削除
rm -rf $path_temp_dir
