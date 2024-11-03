import bcrypt

# Supongamos que esto es lo que el usuario ingresó
input_password = "1234"

# Supongamos que este es el hash almacenado en la base de datos
stored_hashed_password = "$2b$12$.6.PJqXFOo19gF6aXr4Lt.jK8WAJ4rvTuSDSSsPz3CJ20ZacXo.9."  # Hash de '1234'

# Comparar la contraseña ingresada con el hash almacenado
if bcrypt.checkpw(input_password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
    print("La contraseña es correcta.")
else:
    print("Contraseña incorrecta.")