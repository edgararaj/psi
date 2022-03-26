# PSI (Python Shell Intermediate)

PSI is a language that combines the easy interaction with the os from shell scripts (*.sh, *.bat) and the flexibility of python scripts.
Allowing you to interpolate between both flavours in a cross-platform manner.

## Quick start

Runtime dependencies:
* python3

#### 1st step: Download build.py & build.psi

Place build.py and build.psi on the same directory.
build.psi is just and example from a project of mine!

#### 2nd step: Write your own .psi

PSI scripts should have this first line:
```
#!./build.py
```

Here is a quick demonstration:
```python
#!./build.py

if you_are_ready:
    delete_this_snippet()

def delete_this_snippet():
    print("This is just like python!")
    print("But you can write like this aswell:")

    sh {
        echo This line will only run on linux's sh
        gcc main.cpp
    }

    if error_code:
        print("Cross platform way to check last shell command's error code")

    bat {
        @echo OFF
        FOR %%x IN (1 2 3) DO ECHO Goodbye batch madness! (%%x)
        PAUSE
    }
```

#### 3rd step: Have fun! 🎉
To run the script just type:
```console
foo@bar:~/pavucontrol-qt$ chmod +x ./build.psi
foo@bar:~/pavucontrol-qt$ ./build.psi
```
