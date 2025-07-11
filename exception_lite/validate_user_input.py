def validate_user_input(data):
    if type(data) == dict:
            if not (data.get("name") and type(data.get("name")) == str):
                raise ValueError("Ключ отсутствует или его значение не является строкой")
            else:
                if not (data.get("age") and type(data['age']) == int and data['age'] > 0):
                    raise ValueError("Значение по ключу не число или его значение меньше нуля")
                else:
                    print("Все хорошо")       
    else:
        raise TypeError("Это не словарь")

#validate_user_input({"name": "Alice", "age": 30})
#validate_user_input({"имя": "Alice", "age": 30})      
#validate_user_input({"name": "Alice", "age": -5})
validate_user_input("name")