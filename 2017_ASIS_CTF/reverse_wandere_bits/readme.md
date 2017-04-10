In this challenge, we are given an ELF-64 file. After making an attempt to run it, we know that correct flag should be given as argv[1].

Then drag it into IDA. Result of static analysis was a real mess because the program was written in C++. However, the position of final comparison is clear, 