# timetracked-decorator

This decorator allows to track execution time for methods and functions.

It outputs the name of decorated function and the class name in case if the function is a method.

```
$ ./timetracked.py
2018-03-21 14:31:46,402 WARNING Foo.some_class_method 0.024
2018-03-21 14:31:46,447 WARNING Foo.some_static_method 0.022
2018-03-21 14:31:46,952 WARNING Foo.other_static_method 0.505
2018-03-21 14:31:46,974 WARNING Foo.some_function 0.022
2018-03-21 14:31:47,023 WARNING Bar.some_class_method 0.024
2018-03-21 14:31:47,046 WARNING Bar.some_static_method 0.023
2018-03-21 14:31:47,070 WARNING Bar.some_function 0.023
2018-03-21 14:31:47,094 WARNING Bar.another_function 0.025
2018-03-21 14:31:47,119 WARNING some_function 0.024
```

A simple decorator function could not be used — it is not possible to get the class name if the function to be decorated is a method (in some cases the class name can be obtained from arguments, but not always). Therefore, the class-decorator `_Timetracked` was implemented, with which it is possible to get information about the object calling the method through the `__get__` descriptor.

Compatible with Python 2/3.
