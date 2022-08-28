from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

class Appointment:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['task']
        self.date_made = data['date_made']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.first_name = data['first_name']
    
    @staticmethod
    def valida_cita(formulario):
        es_valido = True

        if len(formulario['task']) < 3:
            flash("El nombre de la cita debe tener al menos 3 caracteres", "cita")
            es_valido = False
            
        if formulario['date_made'] == "":
            flash("Ingrese una fecha", "cita")
            es_valido = False
        
        
        return es_valido 
    
    @classmethod
    def save(cls, formulario):
        query = "INSERT INTO appointments (task, date_made, status, user_id) VALUES ( %(task)s, %(date_made)s, %(status)s, %(user_id)s )"
        nuevoId = connectToMySQL('appointments').query_db(query, formulario)
        return nuevoId

    @classmethod
    def get_all(cls):
        query = "SELECT appointments.*, first_name FROM appointments LEFT JOIN users ON users.id = appointments.user_id" 
        results = connectToMySQL('appointments').query_db(query) 
        citas = []
        for cita in results:
            citas.append(cls(cita)) 
        return citas

    
    @classmethod
    def get_by_id(cls, formulario): 
        query = "SELECT appointments.*, first_name FROM appointments LEFT JOIN users ON users.id = appointments.user_id WHERE appointments.id = %(id)s" 
        result = connectToMySQL('appointments').query_db(query, formulario) 
        appointment = cls(result[0]) 
        return appointment

    @classmethod
    def update(cls, formulario): 
        query = "UPDATE appointments SET task = %(task)s, date_made = %(date_made)s, status = %(status)s WHERE id = %(id)s"
        result = connectToMySQL('appointments').query_db(query, formulario)
        return result

    @classmethod
    def delete(cls, formulario): 
        query = "DELETE FROM appointments WHERE id = %(id)s"
        result = connectToMySQL('appointments').query_db(query, formulario)
        return result