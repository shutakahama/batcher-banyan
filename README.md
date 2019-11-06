# Batcher-Banyan Networkの実装

このコードは大学の講義で実装したものです

## Batcher-Banyan network
入力と出力がいくつかあるようなネットワークにおいて，入力側のいくつかに，出力側の特定の端子に送信したい情報が指定されて入ってきたとき，
それを適切に並び替えて出力するようなネットワークである．  
Batcher networkとBanyan networkで構成されている．  
ここでは
- 入力と出力の数はそれぞれ2^n個　(nは任意の正の整数)
- 入力が指定する出力先は1〜2^nの整数で与えられる
- 同時に入力された情報について出力先は重複しない
- 全ての入力端子に入力がなくてもいい  

という状況を想定している  

<img src="https://github.com/shutakahama/batcher-banyan/blob/master/img/batcher_banyan.jpg" width="500">
(画像は http://cs.uccs.edu/~cs522/hw/hw6.htm より)

## Batcher network
Batcher network は，適当な配列に対して，存在する要素をソートし片側につめた配列を返すネットワークである.
このネットワークの基本構造は2入力をソートする 2 * 2 bitnic sorter であり，それらを組み合わせることで n * n bitnic sorter を作り，
さらに n * n bitnic sorter を組み合わせてBatcher networkができる.

一般に n * n bitnic sorter は n 個の入力に対してまず一度 2 * 2 bitnic sorter を適用し，その出力を適切に並べ替え，
その後2個の (n/2) * (n/2) bitnic sorter に入力する構造になっている. (n/2) * (n/2) bitnic sorter ができていれば 
n * n bitnic sorter を作ることができるので，その構造は再帰的に記述することが可能である.

Batcher networkは 2 * 2 bitnic sorter から始まり，一回り大きな bitnic sorter を順に直列につないでいくことで作られる.
よって適宜配列を並べ替えながら入力⻑サイズの n * n bitnic sorter までつないでいけばよい. これらはプログラム上では以下の関数で実装されている.

- sorter_base(): 2*2 bitnic sorter
- sorter(): n*n bitnic sorter
- batcher(): batcher network

## Banyan network
Banyan networkは，Batcher networkの出力を入力要素がない部分も考慮して適切なポートに配置するのようなネットワークである.
Banyan networkはビット列に対して処理を行うので，まずBatcher networkの出力を2進数表現に変換する.
このとき入力要素がない部分についてはNoneで置き換える.

Banyan networkの基本構造は，2入力でビット列の指定された要素に着目して並び替えを行うsorterである.このsorterを，
どのビットに着目して並び替えるかを変えながらつないでいったものがBanyan networkである. その繋ぎ方に関してはn * n bitnic sorterと同じなので，
それと同様の方法で再帰的に記述できる.あとは各段階で着目するビットを指定してやればよい.
これらはプログラム上では以下の関数で実装されている.

- banyan_base(): 2*2 sorter
- banyan(): banyan network

## 実行
batcher_banyan.pyとbatcher_banyan.ipynbはほぼ同様の内容が実装されています．

- 実行環境 (versionに強い指定はなし)
```
python=3.6
numpy=1.14
```

## 結果
- 入力サイズ16のとき
<img src="https://github.com/shutakahama/batcher-banyan/blob/master/img/result_16.png" width="500">

- 入力サイズ32のとき
<img src="https://github.com/shutakahama/batcher-banyan/blob/master/img/result_32.png" width="500">
