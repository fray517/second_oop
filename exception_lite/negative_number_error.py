class NegativeNumberError(Exception):
    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        return f"[Error {self.error_code}]: {self.message}"
    

def check_positive_number(number):
    if number < 0:
        raise NegativeNumberError("Число отрицательное", 400)
    else:
        print("Число положительное")

#check_positive_number(5)
check_positive_number(-5)