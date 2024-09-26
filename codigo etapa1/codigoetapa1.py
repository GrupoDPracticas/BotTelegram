# Clase DatabaseManager: Conexión y consultas a la base de datos.
# Clase Authenticator:   Autenticación del usuario, verificando la contraseña y obteniendo los permisos.
# Clase BotHandler:      Manejo de los comandos del bot y las interacciones con los usuarios.
# Clase TelegramBot:     Inicializar y ejecutar el bot, delegando las responsabilidades a las clases anteriores.

import telebot
import mysql.connector
import bcrypt
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


# Clase que maneja la conexión y consultas a la base de datos
class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect_db(self):
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Error de conexión a la base de datos: {err}")
            return None


# Clase que maneja la autenticación de usuarios
class Authenticator:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def authenticate_user(self, username, password):
        conn = self.db_manager.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM usuarios WHERE Usuario = %s", (username,))
                result = cursor.fetchone()

                if result:
                    hashed_password = result[2]
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                        return result  # Devolver todos los datos del usuario
                return None  # Usuario o contraseña incorrectos
            except mysql.connector.Error as err:
                print(f"Error al consultar la base de datos: {err}")
                return None
            finally:
                cursor.close()
                conn.close()
        return None

    def get_user_permissions(self, user_id):
        conn = self.db_manager.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT idgrupos FROM usuariogrupo WHERE idusuarios = %s", (user_id,))
                grupo_result_id = cursor.fetchone()
                if not grupo_result_id:
                    return None

                cursor.execute("SELECT grupo FROM grupos WHERE idgrupos = %s", (grupo_result_id[0],))
                grupo_result_name = cursor.fetchone()

                cursor.execute("SELECT idacciones FROM permisos WHERE idgrupos = %s", (grupo_result_id[0],))
                acciones_result_id = cursor.fetchall()

                cursor.execute("SELECT accion FROM acciones WHERE idacciones IN "
                               "(SELECT idacciones FROM permisos WHERE idgrupos = %s)", (grupo_result_id[0],))
                acciones_result = cursor.fetchall()

                return {
                    "grupo_id": grupo_result_id[0],
                    "grupo_name": grupo_result_name[0] if grupo_result_name else None,
                    "acciones_id": acciones_result_id,
                    "acciones": acciones_result
                }
            except mysql.connector.Error as err:
                print(f"Error al consultar la base de datos: {err}")
                return None
            finally:
                cursor.close()
                conn.close()
        return None


# Clase que maneja los comandos e interacciones del bot
class BotHandler:
    def __init__(self, bot, authenticator):
        self.bot = bot
        self.authenticator = authenticator
        self.user_data = {}
        self.setup_handlers()

    def setup_handlers(self):
        self.bot.message_handler(commands=['start'])(self.send_welcome)
        self.bot.message_handler(commands=['login'])(self.start_form)

    def send_welcome(self, message):
        self.bot.reply_to(message, "Bienvenido al Bot Asistente del ISFT 151.\n"
                                   "Este Bot te permite:\n* Inscribirte en las mesas de examenes\n* Realizar consultas y reclamos.")

    def start_form(self, message):
        self.user_data[message.chat.id] = {}  # Inicializamos un diccionario para este usuario
        self.bot.send_message(message.chat.id, "*** Login ***\n")
        self.bot.send_message(message.chat.id, "Ingrese Usuario:")
        self.bot.register_next_step_handler(message, self.ask_user)

    def ask_user(self, message):
        self.user_data[message.chat.id]['user'] = message.text
        self.bot.send_message(message.chat.id, "Ingrese Contraseña:")
        self.bot.register_next_step_handler(message, self.ask_password)

    def ask_password(self, message):
        user = self.user_data[message.chat.id]['user']
        password = message.text
        self.bot.send_message(message.chat.id, "Autenticando Usuario ...........")

        # Verifica si el usuario y la contraseña existen en la base de datos
        user_data = self.authenticator.authenticate_user(user, password)
        if user_data:
            self.bot.send_message(message.chat.id, "Login exitoso.")
            self.bot.send_message(message.chat.id, f"Usuario: {user_data[1]}")

            # Obtener y mostrar permisos del usuario
            permissions = self.authenticator.get_user_permissions(user_data[0])
            if permissions:
                self.bot.send_message(message.chat.id, f"ID Grupo del usuario: {permissions['grupo_id']}")
                self.bot.send_message(message.chat.id, f"Grupo del usuario: {permissions['grupo_name']}")

                acciones_texto = '\n'.join(action[0] for action in permissions['acciones'])
                self.bot.send_message(message.chat.id, f"Acciones permitidas:\n{acciones_texto}")

                # Crear un teclado con botones
                keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
                fila1 = [KeyboardButton(action[0]) for action in permissions['acciones'][:len(permissions['acciones']) // 2]]
                fila2 = [KeyboardButton(action[0]) for action in permissions['acciones'][len(permissions['acciones']) // 2:]]
                keyboard.add(*fila1)
                keyboard.add(*fila2)

                self.bot.send_message(message.chat.id, "Selecciona una acción:", reply_markup=keyboard)
            else:
                self.bot.send_message(message.chat.id, "No hay permisos para este usuario.")
        else:
            self.bot.send_message(message.chat.id, "Usuario o contraseña incorrectos.")

        # Limpiar los datos del usuario después de la verificación
        if message.chat.id in self.user_data:
            del self.user_data[message.chat.id]


# Clase principal que inicializa y corre el bot
class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        db_manager = DatabaseManager('localhost', 'root', '', 'botaccess')
        authenticator = Authenticator(db_manager)
        self.bot_handler = BotHandler(self.bot, authenticator)

    def run(self):
        self.bot.polling()


# Inicializa y ejecuta el bot
if __name__ == "__main__":
    TELEGRAM_TOKEN = '6519376337:AAH2AOqkaLASQw8Ei177H5oMtvHFKii2pXE'
    bot = TelegramBot(TELEGRAM_TOKEN)
    bot.run()
