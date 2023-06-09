# tracint

## Premise
Given a known entry point (be it a file or a catching function), we can encode and decode a traceback as a list of integers denoting start line, end line, start column and end column, repeating for every frame in a stacktrace.
Recovery is done by working backwards to the definition of each function in the stacktrace.

## Caveats
1. Needs py 3.11.
2. Needs jedi as a dep.
3. Only works on statically derivable call sites (as that's how jedi works).
4. Can potentially make multiple reads into the same file, by both (1) jedi and (1<) linecache. In theory it might be a cause for (performance) concern, in practice it might be ok mostly if there aren't many files and/or cross references between modules so that you hit linecache or at least disk cache enough times.
5. You lose the actual exception bottom line (though it's usually clear enough as the exception root kinda details it anyway).


## Example
Compare this
```py
Traceback (most recent call last):
  File "/home/dankey/dev/projects/traceback_recoverer/tests_driver.py", line 5, in <module>
    tests.a.g()
  File "/home/dankey/dev/projects/traceback_recoverer/tests/a.py", line 4, in g
    f()
  File "/home/dankey/dev/projects/traceback_recoverer/tests/b.py", line 2, in f
    [][1]
    ~~^^^
IndexError: list index out of range
```

With this

```console
$ python from_list.py \
         "tests_driver.py" \
         "[5, 5, 4, 15, 4, 4, 4, 7, 2, 2, 4, 9]"  # get from to_list.print_list
```
```py
Traceback (most recent call last):
File "/home/dankey/dev/projects/traceback_recoverer/tests_driver.py", line 5, in <module> 
    tests.a.g()
    ^^^^^^^^^^^
File "/home/dankey/dev/projects/traceback_recoverer/tests/a.py", line 4, in g 
    f()
    ^^^
File "/home/dankey/dev/projects/traceback_recoverer/tests/b.py", line 2, in f 
    [][1]
    ^^^^^
```
[close enough](https://i.kym-cdn.com/entries/icons/original/000/028/021/work.jpg)\
Note for testing how `tests_driver.py` can be used to showcase both a capture of a traceback into a list (run directly), and as an entrypoint to walk backwards to the root of the exception (as an argument to `from_list`).

## TODO
Utilize line end and column end to provide better tracebacks than CPython's (imagine a function call that spreads across multiple lines).
