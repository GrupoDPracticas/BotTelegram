import mysql.connector
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# INTERFAZ PARA USAR INVERSION DE DEPENDENCIAS CON LAS ACCIONES PERMITIDAS
class Action:
    def execute(self, bot, message):
        raise NotImplementedError("Subclasses must implement this method.")

# CLASES QUE IMPLEMENTAN LAS ACCIONES PERMITIDAS
class ConsultarExamenesAction:
    def __init__(self, db_manager):
        self.db_manager = db_manager  # Objeto DatabaseManager

    def execute(self, bot, message):
        bot.send_message(message.chat.id, "Consulta de exámenes en proceso...")

        # Conectar a la base de datos usando el método connect_db() del db_manager
        connection = self.db_manager.connect_db()
        if connection:
            cursor = connection.cursor()

            # Primera consulta: Obtener detalles de los exámenes
            query_examenes = """
            SELECT e.id_examen, e.dia_examen, e.fecha_examen, 
                   TIME_FORMAT(e.hora_examen, '%H:%i') AS hora_examen, 
                   m.Materia, e.observaciones
            FROM examenes e
            JOIN materias m ON e.id_materia = m.idMateria
            """
            cursor.execute(query_examenes)
            examenes = cursor.fetchall()

            # Crear un diccionario para almacenar los profesores de cada examen
            profesores_por_examen = {}

            # Segunda consulta: Obtener los profesores asociados a cada examen
            query_profesores = """
            SELECT ep.id_examen, p.Profesor
            FROM examen_profesor ep
            JOIN Profesores p ON ep.id_profesor = p.idProfesor
            """
            cursor.execute(query_profesores)
            profesores = cursor.fetchall()

            # Organizar los profesores por examen en un diccionario
            for id_examen, profesor in profesores:
                if id_examen not in profesores_por_examen:
                    profesores_por_examen[id_examen] = []
                profesores_por_examen[id_examen].append(profesor)

            # Crear el mensaje para enviar al bot
            if examenes:
                bot.send_message(message.chat.id, "*** MESAS FINALES DICIEMBRE 2024 ***")
                
                for id_examen, dia_examen, fecha_examen, hora_examen, materia, observaciones in examenes:
                    # Obtener la lista de profesores para el examen actual
                    profesores = profesores_por_examen.get(id_examen, ["No asignado"])
                    profesores_str = ", ".join(profesores)
                    
                    # Formatear el mensaje del examen
                    examen_message = (
                        f"Examen de {materia}:\n"
                        f"Día: {dia_examen}, Fecha: {fecha_examen.strftime('%d/%m/%Y')}\n"
                        f"Hora: {hora_examen}\n"
                        f"Profesores: {profesores_str}\n"
                        f"Observaciones: {observaciones or 'N/A'}"
                    )
                    
                    # Enviar cada examen como un mensaje individual
                    bot.send_message(message.chat.id, examen_message)
            else:
                bot.send_message(message.chat.id, "No hay exámenes disponibles.")

            # Cerrar la conexión a la base de datos
            cursor.close()
            connection.close()
        else:
            bot.send_message(message.chat.id, "Error al conectar con la base de datos.")

class RealizarReclamoAction:
    def __init__(self, db_manager, user_data):
      self.user = user_data    
      self.db_manager = db_manager  # Objeto DatabaseManager

    def execute(self, bot, message):
        self.bot = bot  # Almacena el objeto bot
        # Solicitar el ingreso del reclamo
        bot.send_message(message.chat.id, "Por favor, ingrese su reclamo:")
        bot.register_next_step_handler(message, self.guardar_reclamo)

    def guardar_reclamo(self, message):
        # Guardar el reclamo ingresado por el usuario
        reclamo = message.text
        self.user_id_search =self.user[message.chat.id]['user_id'] 
         # Conectar a la base de datos usando el método connect_db() del db_manager
        connection = self.db_manager.connect_db()
        if connection:
            cursor = connection.cursor()

            # Consulta para obtener el idEstudiante a partir del idUsuario
            cursor.execute("SELECT idEstudiante, nombre, apellido, dni FROM Estudiantes WHERE idUsuario = %s", (self.user_id_search,))  # Comma is needed to create a tuple
            result = cursor.fetchone()

            if result:
                id_estudiante = result[0]

                # Aquí puedes continuar con la lógica para insertar el reclamo
                query = """
                INSERT INTO reclamos (id_estudiante, fecha_reclamo, motivo)
                VALUES (%s, CURRENT_DATE, %s)
                """
                cursor.execute(query, (id_estudiante, reclamo))
                connection.commit()  # Guardar cambios

                # Enviar una confirmación al usuario
                 # Mensaje de confirmación
                confirmation_message = (
                f"Reclamo guardado exitosamente.\n"
                f"Estudiante: {result[1]} {result[2]}\n"
                f"DNI: {result[3]}\n"
                f"Fecha del reclamo: {datetime.datetime.now().strftime('%d/%m/%Y')}\n"
                f"Motivo: {reclamo}"
                )

                # Enviar la confirmación al usuario
                self.bot.send_message(message.chat.id, confirmation_message)
                print(f"Reclamo guardado en la base de datos: '{reclamo}'")
               
            else:
                    self.bot.send_message(message.chat.id, "No se encontró el idEstudiante asociado a este usuario.")

            # Cerrar la conexión a la base de datos
            cursor.close()
            connection.close()
        else:
            self.bot.send_message(message.chat.id, "Error al conectar con la base de datos.")


class ConsultarReclamosAction:
    def __init__(self, db_manager):
        self.db_manager = db_manager  # Objeto DatabaseManager

    def execute(self, bot, message):
        bot.send_message(message.chat.id, "Consultando reclamos pendientes...")

        # Conectar a la base de datos usando el método connect_db() del db_manager
        connection = self.db_manager.connect_db()
        if connection:
            cursor = connection.cursor()

            # Consultar los reclamos pendientes y los detalles de los estudiantes
            query = """
            SELECT r.id_reclamo, s.nombre, s.apellido, r.fecha_reclamo, r.motivo
            FROM reclamos r
            JOIN estudiantes s ON r.id_estudiante = s.idestudiante
            WHERE r.estado = 'pendiente'
            """
            cursor.execute(query)
            reclamos = cursor.fetchall()

            bot.send_message(message.chat.id, "*** RECLAMOS PENDIENTES DICIEMBRE 2024 ***")

            # Crear el mensaje para enviar al bot
            if reclamos:
                for id_reclamo, nombre, apellido, fecha_reclamo, motivo in reclamos:
                    response_message = (
                        f"Reclamo ID: {id_reclamo}\n"
                        f"Estudiante: {nombre} {apellido}\n"
                        f"Fecha: {fecha_reclamo}\n"
                        f"Motivo: {motivo}\n"
                        "Estado: pendiente"
                    )
                    # Enviar cada reclamo como un mensaje separado
                    bot.send_message(message.chat.id, response_message)
            else:
                bot.send_message(message.chat.id, "No hay reclamos pendientes.")

            # Cerrar la conexión a la base de datos
            cursor.close()
            connection.close()
        else:
            bot.send_message(message.chat.id, "Error al conectar con la base de datos.")



class InscribirseEnExamenesAction:
 
    def __init__(self, db_manager, user_data):
        self.db_manager = db_manager  # Objeto DatabaseManager
        self.user = user_data
        self.materias_aptas =[] 

    
    def execute(self, bot, message):
        bot.send_message(message.chat.id, "Consultando examenes...")
        bot.send_message(message.chat.id, "*** MATERIAS QUE PUEDEN SER RENDIDAS  ***")
        self.user_id_search = self.user[message.chat.id]['user_id'] 

        # Conectar a la base de datos usando el método connect_db() del db_manager
        connection = self.db_manager.connect_db()
        if connection:
            cursor = connection.cursor()

           
            # Consultar las materias cursadas con statusMateria 4 y con idEstudiante coincidente
            query = """
            SELECT mc.idMateriaCursada, m.Materia, mc.fecha, mc.idStatusMateria
            FROM MateriasCursadas mc
            JOIN materias m ON mc.idMateria = m.idMateria
            WHERE mc.idEstudiante = %s AND mc.idStatusMateria = 4 
            """
            cursor.execute(query, (self.user_id_search,))
            cursada_no_aprobada = cursor.fetchall()
            print("Cursada no aprobada:", cursada_no_aprobada)

            # Verificar si hay resultados en cursada_no_aprobada
            if cursada_no_aprobada:
                
                for id_materia_cursada, nombre_materia, fecha_cursada, status in cursada_no_aprobada:
                       # Copiar la materia en el diccionario materias_aptas
                        materia_info = {
                            'idMateriaCursada': id_materia_cursada,
                            'Materia': nombre_materia,
                            'idStatusMateria': 'Cursada no aprobada.',
                            'modalidad': 'Libre'  # Agregar el campo modalidad
                        }
                        self.materias_aptas.append(materia_info)

            # Ahora materias_aptas contendrá las materias con 2 o menos años de antigüedad
            print("Materias aptas:", self.materias_aptas)


            # Consultar las materias cursadas con statusMateria 1 y con idEstudiante coincidente
            query = """
            SELECT mc.idMateriaCursada, m.Materia, mc.fecha, mc.idStatusMateria
            FROM MateriasCursadas mc
            JOIN materias m ON mc.idMateria = m.idMateria
            WHERE mc.idEstudiante = %s AND mc.idStatusMateria = 1 
            """
            cursor.execute(query, (self.user_id_search,))
            materias_status_1 = cursor.fetchall()
            print("Materias con status 1:", materias_status_1)

            if materias_status_1:
              for id_materia_cursada, nombre_materia, fecha_cursada, status in materias_status_1:
                # Verificar correlativas
                cursor_correlativas = connection.cursor()
                query_correlativas = """
                SELECT C.idCorrelativa
                FROM Correlativas AS C
                LEFT JOIN MateriasCursadas AS MC ON C.idCorrelativa = MC.idMateria
                WHERE C.idMateria = %s AND (MC.idStatusMateria IS NULL OR MC.idStatusMateria = 5);
                """
                cursor_correlativas.execute(query_correlativas, (id_materia_cursada,))
                correlativas_pendientes = cursor_correlativas.fetchall()

            # Si no hay correlativas o todas están aprobadas, agregar al diccionario
            if not correlativas_pendientes:  # Si no hay correlativas pendientes
                materia_info = {
                    'idMateriaCursada': id_materia_cursada,
                    'Materia': nombre_materia,
                    'idStatusMateria': 'No Cursada',
                    'modalidad': 'Libre'  # Agregar el campo modalidad
                }
                self.materias_aptas.append(materia_info)

                cursor_correlativas.close()

                # Ahora materias_aptas contendrá las materias con status 1 sin correlativas pendientes
                print("Materias aptas:", self.materias_aptas)

               
               # Consultar las materias cursadas con statusMateria 3 y con idEstudiante coincidente
                query = """
                SELECT mc.idMateriaCursada, m.Materia, mc.fecha, mc.idStatusMateria
                FROM MateriasCursadas mc
                JOIN materias m ON mc.idMateria = m.idMateria
                WHERE mc.idEstudiante = %s AND mc.idStatusMateria = 3 
                """
                cursor.execute(query, (self.user_id_search,))
                materias_status_3 = cursor.fetchall()
                print("Materias con status 3:", materias_status_3)
                if materias_status_3:
                    for id_materia_cursada, nombre_materia, fecha_cursada, status in materias_status_3:
                        materia_info = {
                        'idMateriaCursada': id_materia_cursada,
                        'Materia': nombre_materia,
                        'idStatusMateria': 'Cursada aprobada.',
                        'modalidad': 'Regular'  # Agregar el campo modalidad
                        }
                    self.materias_aptas.append(materia_info)


                    # Ahora materias_aptas contendrá las materias con status 3
                    print("Materias aptas:", self.materias_aptas)


                     # Ahora enviar los datos de materias_aptas al bot
                    if self.materias_aptas:
                        for materia in self.materias_aptas:
                            message_content = (
                                f"Materia: {materia['Materia']}\n"
                                f"Id Materia: {materia['idMateriaCursada']}\n"
                                f"Estado: {materia['idStatusMateria']}\n"
                                f"Modalidad: {materia['modalidad']}\n"
                                "------------------------------"
                            )
                           
                   
                       # Crear un teclado en línea con un botón para el ID de la materia
                            keyboard = InlineKeyboardMarkup()
                            button = InlineKeyboardButton(
                            text=f"Inscribirse",
                            callback_data=f"idMateria_{materia['idMateriaCursada']}"
                                        )
                            keyboard.add(button)

                            # Enviar el mensaje con el teclado adjunto
                            bot.send_message(message.chat.id, message_content, reply_markup=keyboard)
                    else:
                        bot.send_message(message.chat.id, "No se encontraron materias aptas.")

                

            # Cerrar la conexión a la base de datos
            cursor.close()
            connection.close()

        else:
                bot.send_message(message.chat.id, "Error al conectar con la base de datos.")

class ConsultarInscripcionesAction:
    def __init__(self, db_manager):
        self.db_manager = db_manager  # Objeto DatabaseManager

    def execute(self, bot, message):
        bot.send_message(message.chat.id, "Consultando Inscrpciones pendientes...")        

          # Conectar a la base de datos usando el método connect_db() del db_manager
        connection = self.db_manager.connect_db()
        if connection:
            cursor = connection.cursor()

                # Consulta para recuperar todos los campos de inscripciones_examenes
            # y los campos nombre y apellido de estudiantes
            query = """
            SELECT r.*, s.nombre, s.apellido
            FROM inscripciones_examenes r
            JOIN estudiantes s ON r.id_estudiante = s.idestudiante
            """
            cursor.execute(query)
            inscripciones = cursor.fetchall()

            # Verificar si hay inscripciones y enviar el mensaje correspondiente
            if inscripciones:
                bot.send_message(message.chat.id, "*** LISTADO DE INSCRIPCIONES ***")

                # Crear el mensaje para cada inscripción y enviarlo al bot
                for inscripcion in inscripciones:
                    (id_inscripcion, id_estudiante, id_examen, fecha_inscripcion, estado, 
                     nombre, apellido) = inscripcion

                    # Formatear fecha_inscripcion a dd/mm/yyyy
                    fecha_inscripcion = fecha_inscripcion.strftime("%d/%m/%Y") if fecha_inscripcion else "Desconocida"

                    # Segunda consulta: obtener detalles del examen
                    cursor.execute("SELECT dia_examen, fecha_examen, hora_examen, id_materia FROM examenes WHERE id_materia = %s", (id_examen,))
                    examen_result = cursor.fetchone()

                    # Verificar y asignar los detalles del examen, incluyendo id_materia
                    if examen_result:
                        dia_examen, fecha_examen, hora_examen, id_materia = examen_result
                        # Formatear fecha_examen a dd/mm/yyyy
                        fecha_examen = fecha_examen.strftime("%d/%m/%Y") if fecha_examen else "Desconocida"
                    else:
                        dia_examen = fecha_examen = hora_examen = id_materia = "Desconocido"

                    # Tercera consulta: obtener el nombre de la materia a partir de id_materia
                    if id_materia != "Desconocido":
                        cursor.execute("SELECT materia FROM materias WHERE idMateria = %s", (id_materia,))
                        materia_result = cursor.fetchone()
                        nombre_materia = materia_result[0] if materia_result else "Desconocido"
                    else:
                        nombre_materia = "Desconocido"

                    # Formatear el mensaje con los detalles de inscripción, examen y materia
                    response_message = (
                        f"Inscripción ID: {id_inscripcion}\n"
                        f"Estudiante: {nombre} {apellido}\n"
                        f"ID Examen: {id_examen}\n"
                        f"Fecha Inscripción: {fecha_inscripcion}\n"
                        f"Estado: {estado}\n"
                        f"Día Examen: {dia_examen}\n"
                        f"Fecha Examen: {fecha_examen}\n"
                        f"Hora Examen: {hora_examen}\n"
                        f"Materia: {nombre_materia}"
                    )
                    # Enviar cada mensaje al bot
                    bot.send_message(message.chat.id, response_message)
            else:
                bot.send_message(message.chat.id, "No hay inscripciones registradas.")

            # Cerrar la conexión a la base de datos
            cursor.close()
            connection.close()
        else:
            bot.send_message(message.chat.id, "Error al conectar con la base de datos.")