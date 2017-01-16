import math
import sys
import subprocess

def int_to_bytes(integer):
    '''Converts an integer to bytes representing it

    Uses the endianness of the current machine.'''
    # size in bytes
    size = 1 if integer == 0 else math.ceil(math.log2(integer + 1) / 8)
    return integer.to_bytes(size, sys.byteorder)

def possible_bytes():
    '''Generates all possible strings in numerical byte order'''
    program_integer = 0
    while True:
        print(program_integer)
        program_bytes = int_to_bytes(program_integer)
        yield program_bytes
        program_integer += 1

def possible_programs(filename):
    '''Writes all possible programs to a file, writing the next one on next()'''
    possibilities = possible_bytes()
    for program in possibilities:
        with open(filename, 'wb') as program_file:
            program_file.write(program)
        yield program

def attempt_compile(filename, executable):
    '''Attempt compilation of the given file with g++

    Hides all output. Returns true if the compilation succeeds.
    '''
    success = subprocess.run(['g++', filename, '-o', executable],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode
    return success == 0

def main():
    program_name = 'program.cpp'
    last_length = 0
    for program in possible_programs(program_name):
        if len(program) != last_length:
            print(len(program))
            last_length = len(program)
        if attempt_compile(program_name, 'program'):
            print('Finished!')
            return

if __name__ == '__main__':
    main()
