# Chinachu2EPGS

Chinachu → EPGStation (v2) のお引越しツール

## 前提事項

Chinachu と EPGStation で同じ録画ディレクトリが見える必要があります。
ex) Chinachu で `/mnt/data1/hoge.m2ts` に録画した番組は EPGStation のコンテナからも `/mnt/data1/hoge.m2ts` が見える必要があります。

## Usage

1. EPGStation のコンテナからバックアップを取ってくる。`epgstation.json` というバックアップが生成される。  
**注意: バックアップを生成してからリストアするまでに EPGStation を操作しないでください！その間のデータはロストします！**

```shell
# cd /tmp
# docker exec EPGStation npm run backup epgstation.json
# docker cp EPGStation:/app/epgstation.json .
```

2. convert.py を実行する。`epgstation.new.json` が生成される。

```shell
# python convert.py
```

3. EPGStation のコンテナに `epgstation.new.json` をリストアする。

```shell
# docker cp epgstation.new.json EPGStation:/app/
# docker exec EPGStation npm run restore epgstation.new.json
```

なにか問題が発生した場合は以下で変更前のバックアップにリストアできます。

```shell
# docker exec EPGStation npm run restore epgstation.json
```
