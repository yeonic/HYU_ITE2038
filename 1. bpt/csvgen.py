import csv
from random import sample

if __name__ == '__main__':
    f1 = open('input.csv', 'w', newline='')
    f2 = open('delete.csv', 'w', newline='')

    csv_writer_input = csv.writer(f1)
    csv_writer_delete = csv.writer(f2)

    size = int(input('# of rows: '))

    rand_list = range(1, size*10)
    rands = sample(rand_list, size)

    print('Generation in progress..')
    for i in range(0, size):
        if i % (size//10) == 0:
            print('⬜️', end='')
        csv_writer_input.writerow([rands[i], rands[i] // 10 + 1])

    print('\nGeneration completed!')

    f1.close()
    f2.close()
