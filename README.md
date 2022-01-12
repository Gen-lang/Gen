<div align="center">
    <img width="115px" src="https://user-images.githubusercontent.com/60306074/148671204-b759cf4b-dada-483b-80f5-7bc24efc49e5.png">
    <h1>Gen Programming Language</h1>
</div>

**WARNING!! THIS LANGUAGE IS IN DEVELOPMENT. ANYTHING CAN CHANGE AT ANY MOMENT.**

Gen is supposed to be a general-purpose programming language.

### TODO List
 - [x] Basic arithmetic
 - [x] Variables
 - [x] If statement (logical operators)
 - [ ] String
 - [x] For and while statements
 - [ ] Functions

### Installation
```
git clone https://github.com/Gen-lang/PyGen.git
cd PyGen
```
Then you can run Makefile:
```
make install
```
Then you can use pygen:
```
pygen
```

### Syntax
*Note:* **Currently Gen only supports integers and floats**

#### Variables
Variable assignment is very simple.
```
gen>> var a = 10
10
gen>> var b = a
10
```
#### Logical Operators
Just like any other language.
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
gen>> if age >= 18: 1 else 0
1
```

### For loop
Maybe a bit wordy.
```
gen>> var a = 0
0
gen>> for b = 0 through 10 step 2: var a = a + b
gen>> a
20
```

### While loop
It's quite similar to Python.
```
gen>> var a = 0
0
gen>> while a <= 10: var a = a + 1
gen>> a 
11
```

### Contributing
Contributions are welcome!

### Credits
I learned a lot from this [series](https://ruslanspivak.com/lsbasi-part1/)

