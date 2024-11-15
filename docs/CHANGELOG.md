# Change Log

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and versioning is based on [Semantic Versioning](http://semver.org/).

## [Unreleased]

* 箱ひげ図のブラケットの高さの指定機能を追加
* 単発データのviolin plot出力機能を追加
* 箱ひげ図へのハッチング機能を追加
* 箱ひげ図のgroup名を変更する機能を追加

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
