import csv
from random import sample

f = open('input.csv', 'w', newline='')
csv_writer = csv.writer(f)

print('File opened')
size = int(input('# of row: '))

rand_list = range(1, size*10)
rands = sample(rand_list, size)

print('Generation in progress..')
for i in range(0, size):
    if i % (size//10) == 0:
        print('⬜️', end='')
    csv_writer.writerow([rands[i], rands[i] // 10 + 1])

print('\nGeneration completed!')
f.close()
