# MosaicArt
## 概要
モザイクアートを作成するプログラム。

## 使い方
1. `raw_data` に入力画像をアップロード
2. `python cut_data.py` を実行
> `target_data` にトリミングされた画像が出力される

3. `python data_process.py` を実行
> 直下に `cifar100object.pickle` が出力される<br>
> この実行は`cifar100` を変更しない限り再実行する必要はない
> > `cifar-100` の全画像をヒストグラム化したオブジェクトが書き込まれている<br>
4. `python main.py` を実行
> ソースコード内にある `no_duplication_flag` を変更することにより画像の重複を許す/許さないをスイッチできる<br>
> `generated_images` (重複ありの場合)<br>
> `generated_images_nodup` (重複なしの場合) に画像が出力される

## 注意点
`git push` する際に`cifar100object.pickle` もしくは `cifar100` ディレクトリにダウンロードされた画像があるとファイルサイズが100.00MB を超えてエラーになる<br>
> 上記のファイルは `data_process.py` の実行時に作成される

`git push` は上記のものを削除してから行う
> 誤ってこれらのファイルがあるまま `git commit` してしまった場合には、`commit`を取り消す必要がある<br>
> その場合の参考：[GitHubで100MB以上のファイルをコミットしてしまった場合の応急処置](https://bluebirdofoz.hatenablog.com/entry/2021/03/30/095444)
