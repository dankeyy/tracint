# tracint

## Premise
Given a known entry point (be it a file or a catching function), we can encode and decode a traceback as a list of integers denoting start line, end line, start column and end column, repeating for every frame in a stacktrace.
Recovery is done by working backwards to the definition of each function in the stacktrace.

## Digressions
1. Needs py 3.11.
2. Needs jedi as a dep.
3. Only works on statically derivable call sites (as that's how jedi works).
4. Can potentially make multiple reads into the same file, by both (1) jedi and (1<) linecache. In theory it might be a cause for (performance) concern, in practice it might be ok mostly if there aren't many files and/or cross references between modules so that you hit linecache or at least disk cache.
5. You lose the actual exception bottom line (though it's usually clear enough as the exception root kinda details it anyway).


## Structure
`to_list.py` - exposes a function to take an Exception object and print out a list encoding the trace. \
**important note** - this is currently 1/n-th broken, because in 3.11.3 CPython at the time of writing this, there's a bug in the function that provides the line info ([CPython tracking issue](https://github.com/python/cpython/issues/104513)). So constructing the list is half manual for now.

`from_list.py` - a script to walk the list (from a given entrypoint) and reconstruct the traceback, printing it in the process.

`tests_driver.py` - provided as an example to showcase both a capture of a traceback into a list (run `python tests_driver` to output it), and both as an entrypoint example to walk backwards to the root of the exception (give it as an argument to `from_list`).
`tests/` - package that just contains some scattered function calls to make sure everything works across modules.


## Example
Compare this
``` python

  File "/home/dankey/dev/projects/traceback_recoverer/tests_driver.py", line 4, in <module>
    tests.a.g()
  File "/home/dankey/dev/projects/traceback_recoverer/tests/a.py", line 4, in g
    f()
  File "/home/dankey/dev/projects/traceback_recoverer/tests/b.py", line 2, in f
    [][1]
    ~~^^^
IndexError: list index out of range
```

With this

``` python
python from_list.py tests_driver.py "[5, 5, 4, 15, 4, 4, 4, 7, 2, 2, 4, 9]
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
[Not quite the same but close](https://i.kym-cdn.com/entries/icons/original/000/028/021/work.jpg)

## TODO
Utilize line end and column end to provide better tracebacks then CPython's (imagine a function call that spreads across multiple lines).
