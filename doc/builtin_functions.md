# Gen built-in functions

I will add more built-in functions, but if you want something that's not listed here, please open an issue or contribute.

| Name | Description | Example |
|------| ----------- | ------- |
| println | Print out the given value with a new line at the end | `println("Hello World")`
| print | Similar to `println` but without a new line | `print("Hello World")`
| input | Read a line from input, convert it to string, and return it | `name = input("Enter your name: ")`
| int_input| Similar to `input` but only accepts integer | `age = int_input("Enter your age: ")`
| absolute_number_of | Return the absolute number of the given integer | `num = absolute_number_of(-8)`
| is_number | Check if the given value is a number | `println(is_number(48))`
| is_string | Check if the given value is a string | `println(is_string("some string"))`
| is_array | Check if the given value is an array | `println(is_array([1, 2, 3]))`
| size  | Return the number of elements in an array or a string | `println(size([1, 2, 3, 4, 5]))`
| is_function | Check if the given value is a function | `println(is_function(some_func))`
| exit_program | Exit the program | `exit_program()`
