# visualize

## 概要

* 規程形式の入力データをグラフ化する
* (option) データの概要を出力する

## 環境 (動作確認済み)

* Python 3.12.2
    * ライブラリはrequirements.txtを参照

## How to use

### 準備

1. このリポジトリをクローンする
1. 以下のコマンドを実行し，必要なライブラリをインストールする

```bash
pip install -r requirements.txt
```

### 実行

1. visualize/Input/に指示ファイル，データファイルを配置する(詳細は以下)
1. visualize/config.ymlを編集する
1. 以下のコマンドを実行する

```bash
python src/gen_graph.py
```

## ファイル構成

```plaintext
visualize/
```

## 入力

* 以下の通り1つの指示ファイルと1つ以上のデータファイル，config.ymlを用意する

### 指示ファイル

Input/にinstructions.csvを配置し，以下の通り記述する．
なお2列目以降は例であり，実際には必要な列数だけ記述する．
**指示ファイルの形式が間違っている場合のエラー処理等は実装していないので注意**

```csv

output_name, filename, is_time_series, xlim_min, xlim_max, ylim_min, ylim_max, xlabel, ylabel, legend, brackets, bracket_base_y
output1, data1.csv, TRUE, 0, 100, -10, 200, frame, parameter1,True:continue.False:stop, 1:2:*.1:3:**, 70
output2, data2.csv, FALSE,,,20, 50, condition, parameter2,True:continue.False:stop.:PGT,,

```

このとき各列の指定方法は以下の通り

1. output_name: 出力ファイル名(**必須**，拡張子なし，png形式で出力)
1. filename: データファイル名(**必須**，拡張子あり，csv形式，visualize/Input/をルートとした相対パスで指定)
1. is_time_series: 時系列データかどうか(TRUE/FALSE，"TRUE"以外の文字列が入力された場合はFALSEとして扱われる)
1. xlim_min: x軸の最小値
    * minとmaxが同時に指定されていない場合は適用されない(以下min, max系は同様)
1. xlim_max: x軸の最大値
1. ylim_min: y軸の最小値
1. ylim_max: y軸の最大値
    * bracket_base_yよりも大きい値を指定することを推奨
1. xlabel: x軸のラベル，$$で囲むことでLaTex数式記法使用可能 (**必須**)
1. ylabel: y軸のラベル，$$で囲むことでLaTex数式記法使用可能 (**必須**)
1. legend: 入力csvの列名と凡例の対応表(コロンで対応，ピリオドで区切り)
    * 例: Trueをcontinue，Falseをstop，空文字をPGTというラベルにしたい場合: True:continue.False:stop.:PGT
1. brackets: 有意差の対応表(コロンで対応，ピリオドで区切り)
    * 指定した順に下から追加される
    * 数字は左から順に1, 2, 3...と対応
    * ※例中のバックスラッシュは実際には不要(mdのエスケープ文字)
    * 例: 1と2の間に\*の有意差を示す場合: 1:2:\*
    * 例: 1と2の間に\*，2と3の間に\*\*の有意差を示す場合: 1:2:\*.2:3:\*\*
1. bracket_base_y: 箱ひげ図の有意差を示す線の最低y座標
    * データの最大値より大きい値を指定することを推奨

exampleファイル，brackets系は[参考画像](docs/brackets.png)も参照のこと

### データファイル

#### 試行ごとに単発のパラメータとして出力されるもの

例: 歩行終了距離

* 形式: csv
    * 1列目: 自由
    * 2列目: 値
    * 3列目: 条件
        * 3列の条件別に箱ひげ図として出力される
        * 条件名は指示ファイルのlegendで指定したものに対応させる
    * 4列目: グループ
        * 箱ひげ図の横軸のグループ分けに使用
            * グループが1つしかない場合は指定不要

```csv
id, value, condition, group
1, 10, TRUE, 1
2, 20, TRUE, 1
3, 30, TRUE, 2
4, 40, TRUE, 2
5, 50, FALSE, 1
6, 60, FALSE, 1
7, 70, FALSE, 2
8, 80, FALSE, 2
9, 90, TRUE, 3
10, 100, TRUE, 3

```

#### 試行ごとに時系列データとして出力されるもの

例: 歩行時の関節角度

* 形式: csv
    * 1列目: frame(フレーム番号)
    * 2列目以降: 値
        * 2列目以降のヘッダ毎に平均を実線，標準偏差を網掛けでプロットしたグラフが出力される
        * ヘッダ名は指示ファイルのlegendで指定したものに対応させることで凡例を変更可能

```csv
frame, condition1, condition1, condition2, condition2
1, 10, 20, 30, 40
2, 20, 30, 40, 50
3, 30, 40, 50, 60
4, 40, 50, 60, 70
5, 50, 60, 70, 80
```

### config.yml

* グラフ出力等に関する設定を記述する
* visualize/に配置する
* 詳細はconfig.yml-template参考画像を参照
    * [フォント](docs/fonts.png)
    * [位置](docs/locs.png)

## 出力

* Output/にグラフが出力される
* config.ymlでグラフ出力に関する設定を変更可能

## 処理内容

### src/graph.py

#### single_graph関数

seaborn.boxplotのラッパー風関数

1. 引数
    1. pandas.DataFrame
        * 1列目: trial_id(試行番号)
        * 2列目: parameter※(パラメータ) ※ファイルにより異なる
        * 3列目: is_assist_continue(実験のアシスト条件(TRUE/FALSE) またはPGT(null))
    1. ax: matplotlib.pyplot.Axes
    1. plotのその他引数(x, y, axを除く)
1. 返り値
    1. seaborn.boxplotの返り値
    1. 使用したデータの概要(pandas.DataFrame)
1. 処理
    1. 3列目の値で分類して箱ひげ図をax.boxplot内に作成
    1. また，箱ひげ図内に外れ値を除いた平均値をxでプロット
    1. この関数外部でx軸の範囲等を設定する

#### add_brackets関数

箱ひげ図に有意差を示す線を追加する関数

1. 引数
    1. ax: matplotlib.pyplot.Axes
    1. brackets: 有意差を示すタプルのリスト (例: [(1, 2, '*'), (2, 3, '**')])
    1. bracket_base_y: 有意差を示す線の最低y座標 (デフォルトはNone)
    1. dh: 有意差線の高さの増分 (デフォルトは1)
    1. fs: フォントサイズ (デフォルトは10)
1. 返り値
    1. なし
1. 処理
    1. bracketsの各タプルについて、指定された位置に有意差を示す線とアスタリスクを追加
    1. bracket_base_yがNoneの場合、y軸の最大値に基づいて自動的に設定
        * この場合y軸の最大値は自動的に変更されてしまうため注意
    1. dhに基づいて各有意差線の高さを調整
    1. fsに基づいてアスタリスクのフォントサイズを設定

#### time_series_graph関数

seaborn.lineplotとseaborn.betweenplotを組み合わせた関数

1. 引数
    1. pandas.DataFrame
        * 1列目: frame
        * 2列目以降: parameter※(パラメータ) ※ファイルにより異なる
    1. plotのその他引数(x, yを除く)
1. 返り値
    1. ax.plotの返り値
1. 処理
    1. 2列目以降の値について，ヘッダ毎に平均値を実数，標準偏差を網掛けでプロット
    1. この関数外部でx軸の範囲等を設定する

#### **_describe関数

グラフ出力時に渡したデータと同じデータを入力することで，そのデータの概要をcsv形式で出力する関数

#### set_ax関数

axの設定を行う関数

1. 引数
    1. ax: matplotlib.pyplot.Axes
    1. xlabel: x軸のラベル名
    1. ylabel: y軸のラベル名
    1. xlim: x軸の範囲 (デフォルトはNone)
    1. ylim: y軸の範囲 (デフォルトはNone)
    1. is_time_series: 時系列データかどうか (デフォルトはFalse)
1. 返り値
    1. ax: matplotlib.pyplot.Axes
1. 処理
    1. config.ymlからフォントサイズを読み込み、axに設定
    1. x軸、y軸のラベル名を設定
    1. x軸、y軸の範囲を設定
    1. ラベルの配置を設定
    1. グリッドを点線で表示
    1. is_time_seriesがTrueの場合、x軸のメモリを整数にし、凡例のフォントサイズを設定
    1. is_time_seriesがFalseの場合、凡例を非表示に設定

### src/gen_graph.py

* このファイルを実行することで指示ファイルに従ってグラフを生成する
* このファイルをpythonで実行するとgen_graph関数が実行される
* gen_graph関数は以下の処理を行う
    1. 指示ファイルを読み込む
    1. 指示ファイル内の各列ごとにグラフを生成する
