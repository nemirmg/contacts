'''
Задача №49

Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной


'''

import os

def read_data(file):
    with open(file) as f:
        data = [line.strip().split(', ') for line in f]
        headings = data[0]
        data = data[1:]
    return headings, data

def add_data(file, headings, row):
    text = ', '.join(row) + '\n'
    if os.path.exists(file) == False:
        text = ', '.join(headings) + '\n' + text
    with open(file, 'a') as f:
        f.write(text)
    
def write_data(file, headings, data):
    with open(file, 'w') as f:
        f.write(', '.join(headings) + '\n')
        for elem in data:
            f.write(', '.join(elem) + '\n')
        
def get_width(data, headings):
    cols_width = [len(heading) for heading in headings]
    if data:
        dt = list(zip(headings, *data))
        cols_width = [len(max(*col, key=len)) for col in dt]
    return cols_width  

def print_row(row, cols_width):
    line = [val.center(width + 2) for val, width in zip(row, cols_width)]
    print(*line, sep='|')

def print_sep(sep, cols_width):
    print(*[sep * (width + 2) for width in cols_width], sep='|')

def print_table(data, headings, cols_width):
    print_row(headings, cols_width)
    print_sep('-', cols_width)
    for row in data:
        print_row(row, cols_width)

def sort_data(data, column, required_data):
    index_search = [num for num, row in enumerate(data)
                    if required_data in row[column].lower()]
    return index_search

def find_contact(data, headings, cols_width):
    print('По какому полю будем искать?')
    for i in range(1, len(headings)):
        print(f'({i})\t{headings[i]}')

    choice = int(input('Введите номер столбца: '))
    required_data = input('Введите данные для поиска: ').lower()
    index_search = sort_data(data, choice, required_data)
    print()
    print_row(headings, cols_width)
    print_sep('-', cols_width)
    for val in index_search:
        print_row(data[val], cols_width)
    
def create_row(data, headings):
    new_row = [str(len(data) + 1)]
    print('\nВведите данные нового контакта:')
    new_row += [input(f'{heading}: ') for heading in headings[1:]]
    return new_row

def is_empty_row(row):
    row_len = 0
    for elem in row:
        row_len += len(elem.strip())
    if row_len:
        return False
    return True

def add_contact(data, headings, file):
    new_row = create_row(data, headings)
    while new_row in data:
        print('\nКонтакт с такими данными уже существует!',
              'Что дальше?',
              '\t(1) ввести контакт заново',
              '\t(2) отменить ввод контакта', sep='\n')
        choice = int(input('Укажите номер действия: '))
        if choice == 1:
            new_row = create_row(data, headings)
        elif choice == 2:
            return 'cancel'
    if is_empty_row(new_row):
        return 'empty row'
    data.append(new_row)
    add_data(file, headings, new_row)
    
def copy_contact(data, headings):
    num = int(input('Укажите номер контакта, который хотите скопировать: '))
    filename = input('Введите полное название файла для копирования: ')
    add_data(filename, headings, data[num - 1])
    print('Контакт скопирован.')

def main(file):
    welcome = 'Добро пожаловать в программу "Контакты"!\n'
    print(welcome)

    if os.path.exists(file):
        headings, data = read_data(file)
    else:
        headings = ['№', 'Фамилия', 'Имя', 'Отчество', 'Телефон']
        data = []
        write_data(file, headings, data)

    cols_width = get_width(data, headings)

    main_menu = 'Что хотите сделать?\n'\
                '(1) Просмотреть контакты\n'\
                '(2) Найти контакт\n'\
                '(3) Добавить новый контакт\n'\
                '(4) Скопировать контакт в другой файл\n'\
                '(0) Завершить работу\n'
    print(main_menu)
    choice = int(input('Ваш выбор: '))
    while choice != 0:
        if choice == 1:
            cols_width = get_width(data, headings)
            print_table(data, headings, cols_width)
        elif choice == 2:
            find_contact(data, headings, cols_width)
        elif choice == 3:
            add_contact(data, headings, file)
        elif choice == 4:
            copy_contact(data, headings)
        print()
        print(main_menu)
        choice = int(input('Ваш выбор: '))
    write_data(file, headings, data)
    goodbye = 'До свиданья!'
    print(goodbye)


main('contacts.txt')
