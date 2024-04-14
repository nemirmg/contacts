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

def read_data(file):
    with open(file) as f:
        data = [line.strip().split(', ') for line in f]
        headings = data[0]
        data = data[1:]
    return headings, data

def write_data(file, headings, data):
    with open(file, 'w') as f:
        f.write(', '.join(headings) + '\n')
        for elem in data:
            f.write(', '.join(elem) + '\n')
    print('Данные записаны в файл.')
        
def get_width(data, headings):
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

def find_contact(data, headings, cols_width):
    print('По какому полю будем искать?')
    for i in range(len(headings)):
        print(f'({i + 1})\t{headings[i]}')

    choice = int(input('Введите номер столбца: ')) - 1
    required_data = input('Введите данные для поиска: ').lower()
    index_search = [num for num, row in enumerate(data)
                    if required_data in row[choice].lower()]
    print()
    print_row(headings, cols_width)
    print_sep('-', cols_width)
    for val in index_search:
        print_row(data[val], cols_width)
    
def create_row(headings):
    print('\nВведите данные нового контакта:')
    new_row = [input(f'{heading}: ') for heading in headings]
    return new_row

def is_empty_row(row):
    row_len = 0
    for elem in row:
        row_len += len(elem.strip())
    if row_len:
        return False
    return True

def add_contact(data, headings):
    new_row = create_row(headings)
    while new_row in data:
        print('\nКонтакт с такими данными уже существует!',
              'Что дальше?',
              '\t(1) ввести контакт заново',
              '\t(2) отменить ввод контакта', sep='\n')
        choice = int(input('Укажите номер действия: '))
        if choice == 1:
            new_row = create_row(headings)
        elif choice == 2:
            return 'cancel'
    if is_empty_row(new_row):
        return 'empty row'
    data.append(new_row)

def main(file):
    welcome = 'Добро пожаловать в программу "Контакты"!\n'
    print(welcome)

    headings, data = read_data(file)
    cols_width = get_width(data, headings)

    main_menu = 'Что хотите сделать?\n'\
                '(1) Просмотреть контакты\n'\
                '(2) Найти контакт\n'\
                '(3) Добавить новый контакт\n'\
                '(4) Завершить работу\n'
    print(main_menu)
    choice = int(input('Ваш выбор: '))
    while choice != 4:
        if choice == 1:
            print_table(data, headings, cols_width)
        elif choice == 2:
            find_contact(data, headings, cols_width)
        elif choice == 3:
            add_contact(data, headings)
        print()
        print(main_menu)
        choice = int(input('Ваш выбор: '))
    write_data(file, headings, data)
    goodbye = 'До свиданья!'
    print(goodbye)


main('contacts.txt')
