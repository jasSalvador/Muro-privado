from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash #flash es el encargado de mostrar mensajes/errores
import re #expresiones regulares
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

class User:

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def valida_usuario(formulario):
        #formulario = Diccionario con todos los name y valores q el usuario ingresa
        es_valido = True

        #Validamos q el nombre tenga al menos 3 caracteres
        
        if len(formulario['first_name']) < 3: 
            flash('nombre debe tener al menos 3 caracteres', 'registro') #registro: es como poner una categoria o etiqueta/se 
        #puede cambiar x otra palabra, a la hr de desplegar el msj en html, usamos esta palabra registro (index.html)
            es_valido = False

        #Validamos que el apellido tenga al menos 3 caracteres
        if len(formulario['last_name']) < 3:
            flash('Apellido debe tener al menos 3 caracteres', 'registro')
            es_valido = False
            
        #Verificar que password tenga al menos 6 caracteres
        if len(formulario['password']) < 6:
            flash('Contraseña debe tener al menos 6 caracteres', 'registro')
            es_valido = False
        
        #Verificamos que las contraseñas coincidan
        if formulario['password'] != formulario['confirm_password']:
            flash('Contraseñas NO coinciden', 'registro')
            es_valido = False
            
        #Revisamos que email tenga el formato correcto -> Expresiones Regulares
        if not EMAIL_REGEX.match(formulario['email']):
            flash('E-mail inválido', 'registro')
            es_valido = False
            
        #Consultamos si existe el correo electrónico
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('muro_privado').query_db(query, formulario)
        if len(results) >= 1:
            flash('E-mail registrado previamente', 'registro')
            es_valido = False
            
        return es_valido



    #guardar formulario registro
    @classmethod
    def save(cls, formulario): #recibimos el formulario completo
        #formulario = {first_name= "Elena", last_name= "De Troya", email="e@dojo.com", password= "123"}
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('muro_privado').query_db(query, formulario)
        return result #El ID del nuevo registro q se realizo



    #FORMULARIO INICIO SESION
    #validar si existe el correo / siempre puede ser este mismo method
    @classmethod
    def get_by_email(cls, formulario):
        #formulario = {email: elena@codingdojo.com, password: 123}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('muro_privado').query_db(query, formulario) #SELECT regresa una lista
        if len(result) < 1: #Significa que mi lista está vacía, entonces NO existe ese email
            return False
        else:
            #Me regresa una lista con UN registro, correspondiente al usuario de ese email
            #result = [
            #    {id: 1, first_name: elena, last_name:de troya.....} -> POSICION 0
            #]
            user = cls(result[0]) #User( {id: 1, first_name: elena, last_name:de troya.....})
            return user



    @classmethod
    def get_by_id(cls, formulario):
        #formulario = {id: 1}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('muro_privado').query_db(query, formulario)
        #result = [
        #    {id: 1, first_name: elena, last_name:de troya.....} -> POSICION 0
        #]
        user = cls(result[0]) #Creamos una instancia de User
        return user



    #mostrar a los usuarios para crear mensajes
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users ORDER BY first_name ASC"
        results = connectToMySQL('muro_privado').query_db(query) #regresa una lista de diccionarios
        #results = [
        #    {id: 1, first_name: elena, last_name: de troya.....}
        #    {id: 2, first_name: juana, last_name de arco.......}
        #]
        #lo transformamos de diccionario a instancia, para q el formato se vea como una lista de usuarios
        users = []
        for user in results:
        #user = {id: 1, first_name: elena, last_name: de troya........}
            users.append(cls(user)) #1.- cls(user) crea una instancia en base a el diccionario. 2.- users.append Agregando esa instancia a la lista users 

        return users
    