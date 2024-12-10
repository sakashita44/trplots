# Change Log

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and versioning is based on [Semantic Versioning](http://semver.org/).

## [Unreleased]

* 箱ひげ図へのハッチング機能

## [3.0.0] 2024-12-04 (sakashita44)

### Added in 3.0.0

* 箱ひげ図作成関数にjitterを表示する機能を追加
* 箱ひげ図作成関数で平均値マーカ等の設定を追加

### Fixed in 3.0.0

### Changed in 3.0.0

* グラフ生成モジュールを周辺ツールと分離し，モジュールのみをこのリポジトリとして管理するように変更
* 箱ひげ図のブラケットの高さをグラフサイズに対する割合で指定するように変更

## [2.2.0] 2024-11-17 (sakashita44)

### Added in 2.2.0

* instructions.csvで指定したlegendの順番でグラフを出力する機能を追加

## [2.1.2] 2024-11-17 (sakashita44)

### Fixed in 2.1.2

* legendの指定がない場合にlegendが空欄になる問題を修正

## [2.1.1] 2024-11-15 (sakashita44)

### Fixed in 2.1.1

* legendが変更されない問題を修正
* singleデータの箱ひげ図でx軸が正しく設定されない問題を修正
* graph.pyに存在した使用されていない箱ひげ図作成関数を削除
* そのた細かな修正

## [2.1.0] 2024-11-15 (sakashita44)

### Added in 2.1.0

* init.ps1に入出力ディレクトリを自動生成するスクリプトを追加
* init.ps1にinstructions.csvを生成するスクリプトを追加
* run.ps1を追加

## [2.0.1] 2024-11-15 (sakashita44)

### Fixed in 2.0.1

* ディレクトリ構造を変更
* ディレクトリ構造変更に伴うパスの修正

## [2.0.0] 2024-10-08 (sakashita44)

### Added in 2.0.0

* 単発データの箱ひげ図出力にグループ化機能を追加
* 連続データの折れ線グラフ出力に±SDではなく個別のデータを出力する機能を追加
* 環境生成スクリプトの追加

### Removed in 2.0.0

* v1.0.0の入力形式でのグラフ出力

## [1.0.0] 2024-09-19 (sakashita44)

### Added in 1.0.0

* 単発データの箱ひげ図出力(ブラケットつき)
* 連続データの折れ線グラフ出力(±SDの網掛けつき)
* グラフ出力形式の指定

<!--
以下テンプレート

## [x.y.z] yyyy-mm-dd (sakashita)

### Added in x.y.z

### Fixed in x.y.z

### Changed in x.y.z

### Removed in x.y.z

-->
