<div align="center">
    <img width="115px" src="https://user-images.githubusercontent.com/60306074/148671204-b759cf4b-dada-483b-80f5-7bc24efc49e5.png">
    <h1>Gen Programming Language</h1>
</div>

**WARNING!! THIS LANGUAGE IS IN DEVELOPMENT. ANYTHING CAN CHANGE AT ANY MOMENT.**

Gen is a procedural programming language.

See the [documentation](https://github.com/Gen-lang/Gen/tree/master/doc/doc_en.md)<br>
日本語は[こっち](https://github.com/Gen-lang/Gen/tree/master/doc/doc_jp.md)です。

Almost everything (for, if, and more) can be written in just one line. But it is pretty wordy, so it's also easy to learn.


*Note:* I created the pygen directory initially to see how this language would look and feel as soon as possible, so I will rewrite the Gen interpreter in another directory in the future using Perl (and C).


### TODO List
 - [x] Basic arithmetic
 - [x] Variables
 - [x] If statement (logical operators)
 - [x] String
 - [ ] Array
 - [x] For and while statements
 - [x] Functions
 - [ ] Reading files with extention .gen

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

### Contributing
Contributions are welcome! Especially, I need an assist on Makefile to make Gen available to Windows users.

### Credits
I learned a lot from this [series](https://ruslanspivak.com/lsbasi-part1/) and [T# programming language](https://github.com/Tsharp-lang/Tsharp).
