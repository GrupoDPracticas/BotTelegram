import telebot
import mysql.connector
import bcrypt
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import time
from datetime import datetime, timedelta
# Importar las acciones
from actions import Action, ConsultarExamenesAction, RealizarReclamoAction, ConsultarReclamosAction, InscribirseEnExamenesAction, ConsultarInscripcionesAction

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.groups = {}
        self.actions = {}
        self.permissions = {}

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

    def load_initial_data(self):
        """Carga los datos de grupos, acciones y permisos en memoria al inicio de la aplicación."""
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor(dictionary=True)

            # Cargar grupos
            cursor.execute("SELECT * FROM grupos")
            self.groups = {row['idgrupos']: row for row in cursor.fetchall()}

            # Cargar acciones
            cursor.execute("SELECT * FROM acciones")
            self.actions = {row['idacciones']: row['accion'] for row in cursor.fetchall()}

            # Cargar permisos (vincula idgrupos con idacciones)
            cursor.execute("SELECT * FROM permisos")
            self.permissions = {}
            for row in cursor.fetchall():
                group_id = row['idgrupos']
                action_id = row['idacciones']
                if group_id not in self.permissions:
                    self.permissions[group_id] = []
                self.permissions[group_id].append(self.actions[action_id])

            cursor.close()
            conn.close()

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
                    password = password.lower()
                    if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                        return result
                return None
            except mysql.connector.Error as err:
                print(f"Error al consultar la base de datos: {err}")
                return None
            finally:
                cursor.close()
                conn.close()
        return None

    def get_user_permissions(self, user_id):
        """Obtiene los permisos desde la memoria sin consultar la base de datos."""
        # Obtener el grupo del usuario desde la tabla 'usuariogrupo' en la base de datos
        conn = self.db_manager.connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT idgrupos FROM usuariogrupo WHERE idusuarios = %s", (user_id,))
                result = cursor.fetchone()
                if result:
                    group_id = result[0]
                    return self.db_manager.permissions.get(group_id, [])
            except mysql.connector.Error as err:
                print(f"Error al consultar la base de datos: {err}")
                return None
            finally:
                cursor.close()
                conn.close()
        return None




class BotHandler:
    def __init__(self, bot, authenticator, db_manager):
        self.bot = bot
        self.authenticator = authenticator
        self.user_data = {}
        self.setup_handlers()
        self.db_manager = db_manager
    
    # Mapeo de acciones
        buttonactions = {
        "Consultar Fechas.": ConsultarExamenesAction(db_manager),
        "Realizar Reclamo.": RealizarReclamoAction(db_manager, self.user_data ),
        "Consultar Reclamos.":ConsultarReclamosAction(db_manager),
        "Inscribirse en los exámenes.":InscribirseEnExamenesAction(db_manager, self.user_data),
        "Consultar Inscripciones.":ConsultarInscripcionesAction(db_manager)
        } 


         # Asigna el mapeo de acciones desde el archivo actions.py
        self.buttonactions = buttonactions
    
       


    def setup_handlers(self):
        self.bot.message_handler(commands=['start'])(self.send_welcome)
        self.bot.message_handler(func=lambda message: message.text == "Login")(self.start_form)
        self.bot.message_handler(func=lambda message: message.text == "Logout")(self.logout)
        self.bot.message_handler(func=lambda message: message.chat.id in self.user_data and message.text in self.user_data[message.chat.id].get('actions', []))(self.handle_button_click)
        self.bot.message_handler(content_types=['photo', 'audio', 'document', 'video', 'sticker', 'animation', 'voice', 'text'])(self.handle_unrecognized_input)
        
    # Manejador para los botones en línea (callback_query)
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("idMateria_"))(self.handle_materia_selection)

    def handle_materia_selection(self, call):
        # Extraer el ID de la materia desde el callback_data
        id_materia = call.data.split("_")[1]
        
        # Responder a la interacción del usuario
        self.bot.answer_callback_query(call.id, f"Has seleccionado la materia con ID: {id_materia}")
        
        # Obtener `id_estudiante` desde `user_data`
        chat_id = call.message.chat.id
        id_estudiante = self.user_data.get(chat_id, {}).get('user_id')
        
        # Validar que el usuario esté autenticado y se obtuvo su id
        if not id_estudiante:
            self.bot.send_message(chat_id, "Error: Usuario no autenticado.")
            return
        
        # Datos de inscripción
        id_examen = id_materia  # Asumimos que `id_examen` es igual a `id_materia`
        fecha_inscripcion = datetime.now().strftime('%Y-%m-%d')  # Fecha actual en formato YYYY-MM-DD
        estado = 'pendiente'
        
        # Conectar a la base de datos y realizar la inserción
        connection = self.db_manager.connect_db()
        if connection:
            cursor = connection.cursor()
            
            # Insertar un nuevo registro en la tabla `inscripciones_examenes`
            insert_query = """
            INSERT INTO inscripciones_examenes (id_estudiante, id_examen, fecha_inscripcion, estado)
            VALUES (%s, %s, %s, %s)
            """
            
            try:
                cursor.execute(insert_query, (id_estudiante, id_examen, fecha_inscripcion, estado))
                connection.commit()  # Confirmar la inserción en la base de datos
                
                # Confirmación de inscripción exitosa al usuario
                self.bot.send_message(chat_id, f"Inscripción realizada con éxito para la materia con ID: {id_materia}. Estado: {estado}")
            
            except Exception as e:
                # En caso de error, enviar mensaje de error al usuario
                self.bot.send_message(chat_id, f"Error al realizar la inscripción: {str(e)}")
                connection.rollback()  # Revertir cambios en caso de fallo
            
            finally:
                # Cerrar cursor y conexión
                cursor.close()
                connection.close()
        else:
            self.bot.send_message(chat_id, "Error al conectar con la base de datos.")

    def handle_button_click(self, message):
        action_name = message.text
        action = self.buttonactions.get(action_name)
        print(f"Boton : '{action_name}'") 
        print(f"Diccionario : '{action}'") 


        if action:
            action.execute(self.bot, message)           
        else:
            self.bot.send_message(message.chat.id, f"Acción '{action_name}' no está implementada.")

    def ignore_unrecognized_text(self, message):
        self.bot.send_message(message.chat.id, "Por favor, utiliza los botones para interactuar con el bot.")

          
    def handle_unrecognized_input(self, message):
        # Verificar si el mensaje contiene emojis o si es de un tipo no permitido
        #if message.content_type != 'text' or not message.text.isalnum():
            self.send_warning(message)

    def ignore_unrecognized_text(self, message):
        # Aquí puedes enviar un mensaje de advertencia si quieres
        self.bot.send_message(message.chat.id, "Por favor, utiliza los botones para interactuar con el bot.")



    def send_warning(self, message):
      keyboard = self.main_keyboard(message.chat.id)  # Pass chat_id here
      self.bot.send_message(
        message.chat.id,
        "Acción no permitida. Por favor, utiliza los botones proporcionados para interactuar con el bot.",
        reply_markup=keyboard
    )

    def only_alfanum_warning(self, message):
        keyboard = self.main_keyboard()
        self.bot.send_message(
            message.chat.id,
            "Solo caracteres alfanumericos son validos.",
            reply_markup=keyboard
        )

    def send_welcome(self, message):
        keyboard = self.main_keyboard(message.chat.id)
        # Enviar un logo junto con el mensaje
        with open('img/logo.jpg', 'rb') as logo:
            self.bot.send_photo(
                message.chat.id, 
                logo, 
                caption="Bienvenido al Bot Asistente del ISFT 151.\n"
                        "Este Bot te permite:\n* Inscribirte en las mesas de exámenes\n* Realizar consultas y reclamos.",
                reply_markup=keyboard
            )

   
    def main_keyboard(self, chat_id):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
       
        # Condicional para el botón de Login: solo si el usuario no está en sesión activa
        if chat_id not in self.user_data:
            login_button = KeyboardButton("Login")
            keyboard.add(login_button)
        else:
            logout_button = KeyboardButton("Logout")
            keyboard.add(logout_button)



        # Agregar acciones si el usuario está logueado
        if chat_id and chat_id in self.user_data and 'actions' in self.user_data[chat_id]:
            actions = self.user_data[chat_id]['actions']
            for action in actions:
                keyboard.add(KeyboardButton(action))

        
        return keyboard

    def start_form(self, message):
        self.user_data[message.chat.id] = {}
        self.bot.send_message(message.chat.id, "*** Login ***\nIngrese Usuario:")
        self.bot.register_next_step_handler(message, self.ask_user)

    def ask_user(self, message):
        self.user_data[message.chat.id]['user'] = message.text

        if message.content_type != 'text':# Verifica si el texto solo contiene caracteres alfanuméricos
            self.only_alfanum_warning(message)          
        else:
            self.bot.send_message(message.chat.id, "Ingrese Contraseña:")
            self.bot.register_next_step_handler(message, self.ask_password)

    def ask_password(self, message):
        password = message.text
        if message.content_type != 'text': # Verifica si la contraseña solo contiene caracteres alfanuméricos
            self.only_alfanum_warning(message)
            
        else:
            user = self.user_data[message.chat.id]['user']
            self.bot.send_message(message.chat.id, "Autenticando Usuario ...........")

            user_data = self.authenticator.authenticate_user(user, password)
            if user_data:
                user_id = user_data[0]  # Asume que el ID del usuario es el primer elemento de `user_data`
                self.user_data[message.chat.id]['user_id'] = user_id  # Almacena el ID en `user_data`
                self.bot.send_message(message.chat.id, "Login exitoso.")
                self.bot.send_message(message.chat.id, f"ID de usuario: {user_id}")              
                self.bot.send_message(message.chat.id, f"Usuario: {user_data[1]}")
                actions = self.authenticator.get_user_permissions(user_data[0])

                if actions:
                    self.user_data[message.chat.id]['actions'] = actions
                    keyboard = self.main_keyboard(message.chat.id)
                    self.bot.send_message(message.chat.id, "Utilice los botones para las Acciones permitidas:", reply_markup=keyboard)
                else:
                    self.bot.send_message(message.chat.id, "No hay permisos para este usuario.")
            else:
                self.bot.send_message(message.chat.id, "Usuario o contraseña incorrectos.")



    def logout(self, message):
        if message.chat.id in self.user_data:
            del self.user_data[message.chat.id]
            keyboard = self.main_keyboard(message.chat.id)
            self.bot.send_message(message.chat.id, "Te has deslogueado correctamente.", reply_markup=keyboard)
           
        else:
            self.bot.send_message(message.chat.id, "No has iniciado sesión.")
  



class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        db_manager = DatabaseManager('localhost', 'root', '', 'botdb')
        db_manager.load_initial_data()  # Carga datos en memoria al iniciar
        authenticator = Authenticator(db_manager)
        self.bot_handler = BotHandler(self.bot, authenticator, db_manager)

    




    def run(self):
        self.bot.polling()

# Inicializa y ejecuta el bot
if __name__ == "__main__":
    TELEGRAM_TOKEN = '6519376337:AAH2AOqkaLASQw8Ei177H5oMtvHFKii2pXE'
    bot = TelegramBot(TELEGRAM_TOKEN)
    bot.run()

# version 20 
# BASE DE DATOS COMPLETA : IMPLEMENTACION DE LOS METODOS
#  

