# NSE2020 Raspberry Pi

東北大学 From The Earth が製作している NSE2020 で打ち上げ予定の機体に搭載する Raspberry Pi Camera を使ったフライトカメラ用のアプリケーションです．

## Installation

pip または pipenv でインストール出来ます．

```bash:pip の場合
$ python -m pip install git+https://github.com/jjj999/nse2020.git
```

```bash:pipenv の場合
$ pipenv install git+https://github.com/jjj999/nse2020.git#egg=camera
```

pipenv を利用する場合は，アプリケーション実行前に仮想環境に入ってください．


## Usage

以下のコマンドで撮影を開始できます．

```bash:実行例
$ python -m camera
```

詳細な使い方は[こちら](./docs/usage.md)を参照してください．

## Development

開発方法については[こちら](./docs/develop.md)を参照してください．
問い合わせは [Issues](https://github.com/jjj999/nse2020/issues) からお願いします．
