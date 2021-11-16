# sine.utils

the set of common tools

## tools

### Class EventManager

provide event sending and listening.
use a hashable key to identify an event.

```python
def f(key, data):
    print data

manager = EventManager()
manager.start() # start listen

manager.addListener(key='evnet_key', listener=f)

manager.sendEvent(key='evnet_key', 'print hello')


# other methods
manager.removeListener(key='evnet_key', f)
manager.stop() # stop listen
manager.clear() # clear event
```

### Class Path

convenient to join file path in a chain manner:

```python
s = Path('.')
s = s.join('a', 'b').join('..')
# s == 'a'
```

it uses `os.path.join` and always normalizes the path with `os.path.normpath`  
because `os.path.join` join the `'a', '..'` to `'a/..'`

### Module properties

read/write .properties file in line-oriented format  
`key=value` per line *through function*.

*the code refers to `java.util.Properties` in Java 1.6.*

#### Common Usage

* file I/O:

    ```python
    # input
    properties = load(file)
    # or update existing dictionary
    load(file, properties)

    # output
    store(file, properties)
    ```

* custom input:  
    `class LineReader` read in one key-value data. It skips all comment lines,  
    blank lines, leading whitespace, and processes multi-line data.  
    `loadSingle(string)` read each piece of data given above to key-value.  

    ```python
    for line in LineReader(file): # each key-value line has no line seperator
        key, value = loadSingle(line)
        # do something
    ```

* custom output:  
    `storeComments(writable, comments, linesep=os.linesep))`  
    write comment (accept multi-line), can specify the line terminator.  
    `storeSingle(writable, key, value, sep='=', linesep=os.linesep)`  
    write one key-value, can specify the seperator and the line terminator.  

    ```python
    storeComments(file, 'this is a comment')
    storeSingle(file, 'key', 'value')
    ```

#### File Format

normally each line is comment line or a key-value pair.

main features:

* seperate key and value by one of `=`, `:`, ` `, `\t`
* ignore whitespaces leading in a line or around `=` or `:`
* comment line begin with `#` or `!`
* escape unicode by `\uxxxx`
* escape special characters by adding `\`

others:

* data line ends with `\` discard the line break

differences with Java:

* store method will not write datetime comment

### Thread classes

```python
def func(a, b, stop_event):
    while 1:
        if stop_event.is_set():
            break
        # do your work

thread = StoppableThread(target=func, args=('a', 'b'))
thread.start()
# ...
thread.stop(-1) # stop and join forever
# thread.stopped() == True


thread = ReStartableThread(target=func, args=('a', 'b'), event_name='stop_event') # can specify the parameter's name
thread.start()
# ...
thread.stop(1) # stop and join for 1 second
# ...
thread.start()
# ...
thread.stop()
thread.join()
# ...
```

### sine.storage

#### Brief

provide simple reliable persistence for string data base on a string key.

data changes will append to the file like logging while update.
data are store in **csv** format.
you can compress the data anytime reliably.

#### Examples

```python
# common use
storage = getStorage('./data.csv')
author = storage.setdefault('author', 'sine')
storage['author'] = 'Sine'
del storage['author']

for k in storage.keys():
    print(k, storage[k])

# compress data
storage.compress()
```

## Change Log

### v0.2.0, 2021-11-15

* [new] class PredictableProcessBar
* [new] class ConfigFileAlone
* [new] functional: byte2readable, mkdir

### v0.1.1, 2019-12-14

* EventManager's process thread defaults to be daemon, can be set.

### v0.1.0, 2019-7-21

collect from exist package:

* sine.path-v0.1.3
* sine.threads-v0.1.7
* sine.event-v0.0.2
* sine.properties-v0.1.1

and the new 'storage'.

news:

* EventManager: change arguments passing, include the key (just like calling the sendEvent)
* threads: fix about args appending
