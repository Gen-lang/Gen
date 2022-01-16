<div align="center">
    <img width="115px" src="https://user-images.githubusercontent.com/60306074/148671204-b759cf4b-dada-483b-80f5-7bc24efc49e5.png">
    <h1>Gen Programming Language</h1>
</div>

**WARNING!! THIS LANGUAGE IS IN DEVELOPMENT. ANYTHING CAN CHANGE AT ANY MOMENT.**

Gen is a dynamic, interpreted, procedural programming language.

See the [documentation](https://github.com/Gen-lang/Gen/tree/master/doc/doc_en.md)<br>
日本語は[こっち](https://github.com/Gen-lang/Gen/tree/master/doc/doc_jp.md)です。

Almost everything (for, if, and more) can be written in just one line. But it is pretty wordy, so it's also easy to learn.


*Note:* I will convert my current Python source code to many languages I know, because Python is quite slow.


### TODO List
 - [x] Built-in functions
 - [ ] Map (dictionary in Python)
 - [ ] Import other files
 - [x] Reading files with extention .gen (meaning allowing multi-line statements)

### Installation
```
git clone https://github.com/Gen-lang/Gen.git
cd PyGen/pygen
```
Then you can run Makefile:
```
make install
```
Then you can use pygen:
```
pygen
```

### Hello World
```
println("Hello World in Gen")
```

### Example
For examples, see [examples directory](https://github.com/Gen-lang/Gen/tree/master/examples).
```
# Fizzbuzz

for fizzbuzz = 0 through 51 then
	if fizzbuzz % 3 == 0 and fizzbuzz % 5 == 0 then
		println("fizzbuzz")
		continue
	elseif fizzbuzz % 3 == 0 then
		println("fizz")
		continue
	elseif fizzbuzz % 5 == 0 then
		println("buzz")
		continue
	end
end
```

### Contributing
Contributions are welcome! Especially, I need an assist on Makefile to make Gen available to Windows users.

### Reports
If you found a bug, please open a new issue and paste the error message and your code that caused the bug.

### Credits
I learned a lot from this [series](https://ruslanspivak.com/lsbasi-part1/) and [T# programming language](https://github.com/Tsharp-lang/Tsharp).
