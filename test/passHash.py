from flask_bcrypt import generate_password_hash, check_password_hash

def set_password(password):
        contrasena_hash = generate_password_hash(password).decode('utf-8')
        return contrasena_hash


def check_password(myEncriptedPassword, password):
    return check_password_hash(myEncriptedPassword, password)

myPasswordUserAdmin = "adminAccount0001"

mySuperPassword = "refrigeracionEnServicio2025"

passwordCoto = "pruebaCoto12345"

myEncriptedPassword = set_password(passwordCoto)

print(passwordCoto + " = " + myEncriptedPassword)

""" myPassword2 = check_password(myEncriptedPassword,myPasswordUserAdmin)
print(myPassword2) """