# フライトカメラの使い方

## 基本動作

コマンドラインツールを使ってフライトカメラを起動します．
デフォルト設定で利用する際は，

```bash
$ python -m camera
```

を実行するとアプリケーションを起動できます．

プログラムの基本的なフローは下図のとおりです．
タイムアウトなどはオプション引数を指定することで設定できます．

![flowchart](./res/flowchart.png "floawchart")

## オプション

フライトカメラを起動するコマンドにはいくつかオプションがあります．
複数のオプションを組み合わせて利用するのも可能です．

### --pin, -p

このオプションを指定すると信号線を監視するデジタル入力ピンを設定できます．
ピン番号の値は 1 ~ 26 のいずれかである必要があります．
デフォルトは 17 です．

```bash:実行例
# ピン番号を 25 にして起動
$ python -m camera -p 25
```

### --timeout, -t

このオプションでは撮影のタイムアウトを設定できます．
設定したタイムアウトの時間を超過すると，フライトカメラのプログラムは終了します．
デフォルトではタイムアウトの設定はありません．

時間を数字のみで指定した場合は，単位は秒として解析されます:

```bash:実行例
# タイムアウトを 10 分に設定して起動
$ python -m camera -t 600
```

時間をより直感的に指定するために 'h', 'm', 's' の文字列を指定することも出来ます:

```bash:実行例
# タイムアウトを 1時間半 に設定して起動
$ python -m camera -t 1h30m
```

整数だけでなく，小数で指定することも可能です:

```bash:実行例
# タイムアウトを 1時間半 に設定して起動 (小数)
$ python -m camera -t 1.5h
```

また，末尾の "s" は省略可能です:

```bash:実行例
# タイムアウトを 1分20秒 に設定して起動
$ python -m camera -t 1m20
```
時間の単位を指定するためのアルファベットには大文字・小文字の区別はありません．

### --interval, -i

このオプションはデジタル入力ピンの電圧レベルを監視する時間間隔を指定します．
デフォルトは 1秒 です．
このオプションも "--timeout" オプションで使用できる時間フォーマットを使用できます．

```bash:実行例
# 監視の時間間隔を 0.5 秒にして起動
$ python -m camera -i 0.5
```

### --fname, -f

このオプションは出力される動画のファイル名を指定するためのものです．
ファイル名は拡張子も含む必要があります．
デフォルトでは "mov_yyyy.mm.dd-HH.MM.SS.h264" というフォーマットで保存されます．

```bash:実行例
# ファイル名を指定して起動
$ python -m camera -f flight_movie.h264
```

### --resolution, -r

このオプションでは動画の解像度を設定できます．
指定する際は "width:height" のようにセミコロン ":" で区切って指定します．
デフォルトでは "640:480" です．

```bash:実行例
# 解像度を 200:200 にして起動
$ python -m camera -r 200:200
```