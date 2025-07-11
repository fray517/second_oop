import ast
def convert_to_int(value):
    try: 
        value = ast.literal_eval(value)
        value = int(value)
    except ValueError:
        print(f"Ошибка: {value} вы ввели не число.")
    except BaseException as e:
        print(f"Ошибка: {e} неизвестная ошибка и неожиданная ошибка")
    finally:
        print("попытка преобразования завершена")
        
value = input("Введите число: ")
convert_to_int(value)