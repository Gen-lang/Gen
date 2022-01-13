
# Gen ドキュメント
*Note:* **現在、Genは整数と浮動小数点数のみをサポートしています。**

### バリアブル（変数）
Pythonそっくり。
```
gen>> a = 10
10
gen>> b = a
10
gen>> 1 + (c = 9)
10
```
### 論理演算子
```
gen>> 1 > 10
0
gen>> 1 < 10 
1
gen>> 2 <= 3
1
gen>> 2 >= 3
0
gen>> 2 == 3
0
gen>> 2 == 2
1
gen>> 2 != 4
1
```

### If文
```
gen>> var age = 18
18
gen>> if age >= 18 then 1 else 0
1
```

### Forループ
```
gen>> a = 0
0
gen>> for b = 0 through 10 step 2 then a = a + b
gen>> a
20
```

### Whileループ
```
gen>> a = 0
0
gen>> while a <= 10 then a = a + 1
gen>> a 
11
```

### 関数
関数には、defuncを使ってください（def + func)

```
gen>> defunc a(b) -> b * 4
<func a>
gen>> a(2)
8
gen>> test_func = defunc (a, b, c) -> a + b + c
<func <unnamed>>
gen>> test_func(1,2,3)
6
```
