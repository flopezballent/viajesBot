import psycopg2 as sql
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import emoji
from datetime import datetime, timedelta
from flask import Flask, request
import os

conn = sql.connect(
    dbname = 'd5o41d99g8sk9p',
    host = 'ec2-52-201-124-168.compute-1.amazonaws.com',
    user = 'rmktdapfsdslip',
    password = '1a07720cef03dd66d24ea3aba7182134d64bc1efc616f047aed3a353682dd0ef'
    )
print('Se conecto a la BD exitosamente')
cursor = conn.cursor()

TOKEN = "2118980188:AAG1WZfFVwxY6K469WVk3_KdVzNnOW11c8A"

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

usuario = {"id":1111,
        "nombre": "Jose",
        "apellido": "Saiz",
        "mail": "joposaiz@gmail.com",
        "telefono":2494566070}

VIAJE = {"id_conductor": 1,
        "tramo": "sda",
        "fecha": "dasd",
        "obs": "asdas"}

@bot.message_handler(commands=['start'])
#C1 V1
def start(message):
    id = message.chat.id
    msg = "Bienvenido a Match Viajes :fire:\n\n"
    msg += "Aca vas a poder encontrar la compañia para tu viaje de una manera rapida y sencilla.\n\n"
    msg += "Vas a poder cargar tu viaje a TANDIL :mountain: o CABA :cityscape: y todos los demas podran verlo para sumarse.\n\n"
    msg += "Para comenzar apretá o enviá el comando:\n /menu"
    bot.send_message(id, emoji.emojize(msg))

@bot.message_handler(commands=['menu'])
def menu(message):
    #conn = sql.connect(
    #    host = 'ec2-52-201-124-168.compute-1.amazonaws.com',
    #    user = 'rmktdapfsdslip',
    #    password = '1a07720cef03dd66d24ea3aba7182134d64bc1efc616f047aed3a353682dd0ef',
    #    database = 'd5o41d99g8sk9p'
    #    )
    #cursor = conn.cursor()
    global chat_id
    chat_id = message.chat.id
    consulta = esUsuario(chat_id)
    #C1 V1
    if consulta:
        print('Es usuario')
        bot.send_message(chat_id, "Elija una opción", reply_markup=cargar_ver_markup())
        #bot.send_message(chat_id, "<b>CrearViaje</b>\n\n"
        #                    "/VerViajes:", parse_mode=bot.ParseMode.HTML)
    else:
        print('No es usuario')
        msg = bot.send_message(chat_id, "Tenés que registrarte para continuar\n\n"
                            "Nombre (Sin apellido):")
        bot.register_next_step_handler(msg, apellido)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    sql = "SELECT id_conductor FROM viajes"
    cursor.execute(sql)
    idLista = cursor.fetchall()
    lista = []
    for elemento in idLista:
        lista.append(str(elemento[0]))

    if call.data == "Cargar":
        bot.answer_callback_query(call.id, "OK")
        bot.send_message(chat_id, "Elija el recorrido que va realizar", reply_markup=tramo_markup())
    elif call.data == "Ver":
        bot.answer_callback_query(call.id, "OK")
        bot.send_message(chat_id, "Qué viaje queres hacer?", reply_markup=tramo_markup2())
    elif call.data == "BT":
        bot.answer_callback_query(call.id, "OK")
        VIAJE["id_conductor"] = chat_id
        VIAJE["tramo"] = "BUE-TAN"
        fechaActual = datetime.today()
        conjuntoFechas = []
        for i in range(13):
            td = timedelta(i)
            fecha = fechaActual + td
            f = fecha.strftime('%d/%m/%Y')
            conjuntoFechas.append(f)
        markup = ReplyKeyboardMarkup()
        for fecha in conjuntoFechas:
            markup.add(KeyboardButton(fecha))
        msg = bot.send_message(chat_id, 'BUE - TAN\nIngrese la fecha en la que va a realizar el viaje\n', reply_markup=markup)
        bot.register_next_step_handler(msg, cargar_fecha)
    elif call.data == "TB":
        bot.answer_callback_query(call.id, "OK")
        VIAJE['id_conductor'] = chat_id
        VIAJE['tramo'] = "TAN-BUE"
        fechaActual = datetime.today()
        conjuntoFechas = []
        for i in range(13):
            td = timedelta(i)
            fecha = fechaActual + td
            f = fecha.strftime('%d/%m/%Y')
            conjuntoFechas.append(f)
        markup = ReplyKeyboardMarkup()
        for fecha in conjuntoFechas:
            markup.add(KeyboardButton(fecha))
        msg = bot.send_message(chat_id, 'TAN - BUE\nIngrese la fecha en la que va a realizar el viaje\n', reply_markup=markup)
        bot.register_next_step_handler(msg, cargar_fecha)
    elif call.data == "Confirma":
        bot.answer_callback_query(call.id, "OK")
        agregarViaje(VIAJE['id_conductor'], VIAJE['tramo'], VIAJE['fecha'], VIAJE['obs'])
        print("Se agregó un viaje")
        bot.send_message(chat_id, emoji.emojize('Su viaje se cargó correctamente :thumbs_up:\n\nLe avisaremos si hay alguien interesado en sumarse\n\n/menu'))
    elif call.data == "TAN-BUE":
        bot.answer_callback_query(call.id, "OK")
        bot.send_message(chat_id, "Estas son las opciones que tenemos para:\n"+str(call.data)+"\n\nSELECCIONE LA(S) OPCION(ES) QUE LE SIRVA")
        sql = "SELECT * FROM viajes WHERE tramo = 'TAN-BUE'" #Selecciono todos los viajes con BUE-TAN o TAN-BUE
        cursor.execute(sql)
        aux = []
        for item in cursor:
            aux.append([item[1], item[3], item[4]])
        i = 1
        conductores = []
        for viaje in aux:
            instruccion = ('SELECT * FROM usuarios WHERE id =' + str(viaje[0]))
            cursor.execute(instruccion)
            conductor = cursor.fetchall()
            conductores.append(conductor)
        for conductor, viaje in zip(conductores, aux):
            fechaViajeStr = viaje[1]
            diaViaje = fechaViajeStr.split('/')[0]
            mesViaje = fechaViajeStr.split('/')[1]
            añoViaje = fechaViajeStr.split('/')[2]
            if len(añoViaje) == 2:
                añoViaje = '20' + str(añoViaje)
            fechaViajeStr = f'{diaViaje}/{mesViaje}/{añoViaje}'
            fechaActual = datetime.today().strftime('%d/%m/%Y')
            fechaActual = datetime.strptime(fechaActual, '%d/%m/%Y')
            fechaViaje = datetime.strptime(fechaViajeStr, '%d/%m/%Y')
            if fechaViaje < fechaActual:
                continue
            else:
                markup = InlineKeyboardMarkup(row_width = 1)
                idConductor = conductores[i-1][0][0]
                markup.add(InlineKeyboardButton("OPCION "+str(i), callback_data = idConductor))
                msg = f"OPCION {i}\n"
                msg += emoji.emojize(f"   :oncoming_automobile: Conductor/a: {conductores[i-1][0][1]} {conductores[i-1][0][2]}\n")
                msg += emoji.emojize(f"   :spiral_calendar: Fecha: {viaje[1]}\n")
                msg += emoji.emojize(f"   :pencil: Aclaraciones: {viaje[2]}")
                bot.send_message(chat_id, msg, reply_markup=markup)
                i+=1
        i = 1
    elif call.data == "BUE-TAN":
        bot.answer_callback_query(call.id, "OK")
        bot.send_message(chat_id, "Estas son las opciones que tenemos para:\n"+str(call.data)+"\n\nSELECCIONE LA(S) OPCION(ES) QUE LE SIRVA")
        sql = "SELECT * FROM viajes WHERE tramo = 'BUE-TAN'" #Selecciono todos los viajes con BUE-TAN o TAN-BUE
        cursor.execute(sql)
        aux = []
        for item in cursor:
            aux.append([item[1], item[3], item[4]])
        i = 1
        conductores = []
        for viaje in aux:
            instruccion = ('SELECT * FROM usuarios WHERE ID =' + str(viaje[0]))
            cursor.execute(instruccion)
            conductor = cursor.fetchall()
            conductores.append(conductor)
        for conductor, viaje in zip(conductores, aux):
            fechaViajeStr = viaje[1]
            diaViaje = fechaViajeStr.split('/')[0]
            mesViaje = fechaViajeStr.split('/')[1]
            añoViaje = fechaViajeStr.split('/')[2]
            if len(añoViaje) == 2:
                añoViaje = '20' + str(añoViaje)
            fechaViajeStr = f'{diaViaje}/{mesViaje}/{añoViaje}'
            fechaActual = datetime.today().strftime('%d/%m/%Y')
            fechaActual = datetime.strptime(fechaActual, '%d/%m/%Y')
            fechaViaje = datetime.strptime(fechaViajeStr, '%d/%m/%Y')
            if fechaViaje < fechaActual:
                continue
            else:
                markup = InlineKeyboardMarkup(row_width = 1)
                idConductor = conductores[i-1][0][0]
                markup.add(InlineKeyboardButton("OPCION "+str(i), callback_data = idConductor))
                msg = f"OPCION {i}\n"
                msg += emoji.emojize(f"   :oncoming_automobile: Conductor/a: {conductores[i-1][0][1]} {conductores[i-1][0][2]}\n")
                msg += emoji.emojize(f"   :spiral_calendar: Fecha: {viaje[1]}\n")
                msg += emoji.emojize(f"   :pencil: Aclaraciones: {viaje[2]}")
                bot.send_message(chat_id, msg, reply_markup=markup)
                i+=1
        i = 1
    elif call.data in lista:
        print (call.data)
        sql = f"SELECT * FROM usuarios WHERE ID = {chat_id}"
        cursor.execute(sql)
        viajero = cursor.fetchall()
        msg = f":bell: {viajero[0][1]} {viajero[0][2]} quiere viajar con vos. Comunicate con el/ella para coordinar\n\n"
        msg += f"TELEFONO: {viajero[0][4]}"
        bot.send_message(chat_id, 'El conductor se comunicará con vos para confirmar')
        bot.send_message(call.data, emoji.emojize(msg))

#__________________________FUNCIONES SQL________________________________________
def esUsuario(id):
    idSelection = cursor.execute('SELECT id FROM usuarios')
    lista = cursor.fetchall()
    IDs = []
    for item in lista:
        IDs.append(item[0])
    if id in IDs:
        return True
    else:
        return False

def agregarUsuario(id, nombre, apellido, mail, telefono):
    sql = f"INSERT INTO usuarios VALUES({id}, '{nombre}', '{apellido}', '{mail}', {telefono})"
    cursor.execute(sql)
    conn.commit()

def agregarViaje(id, tramo, fecha, obs):
    sql = f"INSERT INTO viajes (id_conductor, tramo, fecha, obs) VALUES({id}, '{tramo}', '{fecha}', '{obs}')"
    cursor.execute(sql)
    conn.commit()

def commit(que, enDonde):
    sql = "INSERT INTO viajes" + enDonde +"VALUES(" + que +")"
    cursor.execute(sql)
    conn.commit()

#__________________________FUNCIONES BOT________________________________________

def apellido(message):
    chat_id = message.chat.id
    usuario['id'] = chat_id
    usuario['nombre'] = message.text
    msg = bot.send_message(chat_id, "Apellido:")
    bot.register_next_step_handler(msg, mail)

def mail(message):
    chat_id = message.chat.id
    usuario['apellido'] = message.text
    msg = bot.send_message(chat_id, "Mail:")
    bot.register_next_step_handler(msg, telefono)

def telefono(message):
    chat_id = message.chat.id
    usuario['mail'] = message.text
    msg = bot.send_message(chat_id, "Telefono:")
    bot.register_next_step_handler(msg, confirmacion)

def confirmacion(message):
    chat_id = message.chat.id
    usuario['telefono'] = message.text
    agregarUsuario(usuario['id'], usuario['nombre'], usuario['apellido'], usuario['mail'], usuario['telefono'])
    print("Se registró un nuevo usuario")
    bot.send_message(chat_id, emoji.emojize("Usuario registrado correctamente :thumbs_up:"))
    bot.send_message(chat_id, "Elija una opcion", reply_markup=cargar_ver_markup())

def cargar_ver_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Cargar viaje", callback_data="Cargar"),
                               InlineKeyboardButton("Ver viajes", callback_data="Ver"))
    return markup

def tramo_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("BUE - TAN", callback_data="BT"),
                               InlineKeyboardButton("TAN - BUE", callback_data="TB"))
    return markup

def tramo_markup2():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("BUE - TAN", callback_data="BUE-TAN"),
                               InlineKeyboardButton("TAN - BUE", callback_data="TAN-BUE"))
    return markup

def confirmacion_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Confirmar", callback_data="Confirma"),
                               InlineKeyboardButton("Editar", callback_data="Cargar"))
    return markup
#C4
def cargar_fecha(message):
    #global fecha
    chat_id = message.chat.id
    markup = types.ReplyKeyboardRemove(selective=False)
    VIAJE['fecha'] = message.text
    msg = bot.send_message(chat_id, "Ingrese alguna aclaracion sobre el viaje\n"
                                    "(Hora de salida, lugar de salida, etc.)", reply_markup=markup)
    bot.register_next_step_handler(msg, cargar_obs)
#C5
def cargar_obs(message):
    #global obs
    chat_id = message.chat.id
    VIAJE['obs'] = message.text
    msg = f"Revise los datos cargados y confirma\n\n"
    msg += f"RECORRIDO: {VIAJE['tramo']}\n"
    msg += f"FECHA: {VIAJE['fecha']}\n"
    msg += f"OBSERVACIONES: {VIAJE['obs']}"
    bot.send_message(chat_id, msg, reply_markup=confirmacion_markup())

def confirmacion_carga(message):
    chat_id = message.chat.id
    agregarViaje(VIAJE['ID_conductor'], VIAJE['tramo'], VIAJE['fecha'], VIAJE['obs'])
    bot.send_message(chat_id, "Usuario registrado correctamente")
    bot.send_message(chat_id, "Elija una opcion", reply_markup=cargar_ver_markup())

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
print("el bot se esta ejecutando")

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url = 'https://match-viajes.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

