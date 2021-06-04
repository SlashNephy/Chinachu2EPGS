# Chinachu2EPGS

Chinachu → EPGStation (v2) のお引越しツール

すでに稼働している EPGStation のバックアップデータと Chinachu の録画番組データをマージすることで引っ越しを可能にします。

## 前提事項

Chinachu と EPGStation で同じ録画ディレクトリが見える必要があります。  
ex) Chinachu で `/mnt/data1/hoge.m2ts` に録画した番組は EPGStation のコンテナからも `/mnt/data1/hoge.m2ts` が見える必要があります。

## Usage

1. すでに稼働している EPGStation のコンテナからバックアップを取得します。`epgstation.json` というバックアップが生成されます。  
**注意: バックアップを生成してからリストアするまでに EPGStation を操作しないでください！その間のデータはロストします！**

```console
$ cd /tmp
# docker exec EPGStation npm run backup epgstation.json
# docker cp EPGStation:/app/epgstation.json .
```

2. 同じディレクトリに Chinachu の録画番組データ `recorded.json` を配置しておきます。その後, convert.py を実行します。`epgstation.new.json` が生成されるはずです。

```console
$ cp /path/to/chinachu/data/recorded.json .
$ python convert.py
```

3. EPGStation のコンテナに `epgstation.new.json` をリストアします。

```console
# docker cp epgstation.new.json EPGStation:/app/
# docker exec EPGStation npm run restore epgstation.new.json
```

なにか問題が発生した場合は以下で変更前のバックアップにリストアできます。

```console
# docker exec EPGStation npm run restore epgstation.json
```
