
## Gen Syntax
*Note:* **Currently Gen only supports integers and floats**

### Variables
Variable assignment is similar to Python.
```
gen>> a = 10
10
gen>> b = a
10
gen>> 1 + (c = 9)
10
```
### Logical Operators
Just like any other languages.
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

### If statement
It's simple.
```
gen>> var age = 18
18
gen>> if age >= 18 then 1 else 0
1
```

### For loop
Maybe a bit wordy.
```
gen>> a = 0
0
gen>> for b = 0 through 10 step 2 then a = a + b
gen>> a
20
```

### While loop
It's quite similar to Python.
```
gen>> a = 0
0
gen>> while a <= 10 then a = a + 1
gen>> a 
11
```

### Function
It's a bit unique with the keyword 'defunc.' (def + func)
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
