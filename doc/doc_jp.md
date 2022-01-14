
# Gen ドキュメント

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

### 文字列
```
gen>> str = "Hello World "
Hello World
gen>> str * 3
Hello World Hello World Hello World
```

### Array（配列）
```
gen>> arr = ["Hello", "World", 123, 3.1415, ["me", "gen"]]
[Hello, World, 123, 3.1415, ["me", "gen"]]
gen>> arr + "bichanna"
[Hello, World, 123, 3.1415, ["me", "gen"], bichanna]
```
`@`を使ってください。
```
gen>> a = [1, 2, 3, 4]
[1, 2, 3, 4]
gen>> a@0
1
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
gen>> for i = 1 through 12 step 2 then 2^i
[2, 8, 32, 128, 512, 2048]
gen>> for i = 1 through 12 then 2^i
[2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]
```

### Whileループ
```
gen>> a = 0
0
gen>> while a <= 10 then a = a + 1
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
gen>> a 
11
```

### 関数
関数には`defunc`を使ってください（def + func)
```
gen>> defunc a(b) -> b * 4
<func a>
gen>> a(2)
8
gen>> test_func = defunc (a, b, c) -> a + b + c
<func <unnamed>>
gen>> test_func(1,2,3)
6
gen>> defunc greet(name) -> "Hello " + name
<func greet>
gen>> greet("bichanna")
Hello bichanna
```
