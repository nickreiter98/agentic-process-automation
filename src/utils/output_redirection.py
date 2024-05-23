import sys

def _print(text:str) -> None:
    print(text)
    with open('build/print_output.txt', 'a') as f:
        f.write(f'{text}\n')