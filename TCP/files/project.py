import sys


def main():
    largerst_array = ''
    len_largest_array = -1
    for line in sys.stdin:
        length = 0
        line = line[:-1]
        if line != '[]':
                length = line.count(',') + 1
        if (length > len_largest_array):
            len_largest_array = length
            largerst_array = line

    print(largerst_array)


if __name__ == '__main__':
    main()
