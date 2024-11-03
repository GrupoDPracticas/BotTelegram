import bcrypt

# Contraseña en texto plano ingresada por el usuario
password = "a*12"

# Generar un hash bcrypt de la contraseña
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# El hash es lo que se almacena en la base de datos
print(hashed_password.decode('utf-8'))

# Carlos , 1234
# Jose , abcd
# Luis , a*12
# Sergio , b*13
