&nbsp;&nbsp;From hints of this challenge (Cobra, python) and some strings in the given file ("MEIPASS"), we can easily guess that this file is packed with pyinstaller.
&nbsp;&nbsp;There is a file Archive_view.py inside pyinstaller github repo, which can extract pyc bytecode from packed elfs, so just run it.

![Alt archiveviewer01](./images/archiveviewer01.png?raw=true)

&nbsp;&nbsp;Besides usual so libraries, there are files like "reverse_1.1", "pyimod00_crypto_key" and "flag.enc" that worth noticing. So I used "X" command to extract them, and add .pyc header to extracted "reverse_1.1" (because uncompyle need a correct pyc header, which we will mention later). The header consists of 8 bytes, mine was "03 F3 0D 0A A3 EF E1 58". First four bytes are magic number of python 2.7, and latter four are timestamp so can be any four bytes. 

&nbsp;&nbsp;Then I ran uncompyle6 to decompile extracted pyc, and got python code as follows

![Alt uncompyle01](./images/uncompyle01.jpeg?raw=true)

&nbsp;&nbsp;So easy. Again I wrote a simple script to decrypt flag.enc, and got a picture which contains the flag.

![Alt decoded](./images/decoded.png?raw=true)