from system_ui import *
import sqlite3
import re

import pdfkit
import os
import win32api
import win32print
#import weasyprint
from datetime import datetime

GHOSTSCRIPT_PATH = os.getcwd() + "\\GHOSTSCRIPT\\bin\\gswin32.exe"
GSPRINT_PATH = os.getcwd() + "\\GSPRINT\\gsprint.exe"

class dbDriver():

    db_name = 'migration_test.db'

    def __init__(self):
        pass

    def adjust_autoincrement_id(self, table_name):
        query = "DELETE FROM sqlite_sequence WHERE name = ?"
        (_, cursor) = self.run_query(query, [table_name])
        return cursor.rowcount

    def update_bill_state_in_db(self, id, new_state, cancelation_date = None):#separar el update de la fecha de cancelacion en otra funcion
        query = "UPDATE Bills SET cancelation_date = ?, state = ? WHERE id = ?"
        (_, cursor) = self.run_query(query, [cancelation_date, new_state, id])
        return cursor.rowcount
    
    def update_articles_state_by_bill_id_in_db(self, bill_code, new_state):
        query = "UPDATE Articles SET state = ? WHERE bill_code = ?"
        (_, cursor) = self.run_query(query, [new_state, bill_code])
        return cursor.rowcount
    
    def update_article_state_by_id_in_db(self, id, new_state):
        query = "UPDATE Articles SET state = ? WHERE id = ?"
        (_, cursor) = self.run_query(query, [new_state, id])
        return cursor.rowcount
    
    def update_deposit_in_db(self, id, new_deposit):
        query = "UPDATE Bills SET deposit = ? WHERE id = ?"
        (_, cursor) = self.run_query(query, [new_deposit, id])
        return cursor.rowcount
    
    def update_deposit_for_cancelation_in_db(self, id, new_deposit_for_cancelation):
        query = "UPDATE Bills SET deposit_for_cancelation = ? WHERE id = ?"
        (_, cursor) = self.run_query(query, [new_deposit_for_cancelation, id])
        return cursor.rowcount
    
    def update_balance_in_db(self, id, new_balance):
        query = "UPDATE Bills SET balance = ? WHERE id = ?"
        (_, cursor) = self.run_query(query, [new_balance, id])
        return cursor.rowcount

    def get_client_from_db(self, phone=None):

        query = 'SELECT * FROM Clients WHERE phone = ?'
        (result, _) = self.run_query(query, [phone])
        list_result = list(result)
        return list_result[0] if len(list_result) != 0 else None

    def get_bill_from_db(self, id=None):

        query = 'SELECT * FROM Bills WHERE id = ?'
        (result, _) = self.run_query(query, [id])
        list_result = list(result)
        return list_result[0] if len(list_result) != 0 else None
    
    def delete_bill_from_db(self, id):
        query = "DELETE FROM Bills WHERE id = ?"
        (_, cursor) = self.run_query(query, [id])
        return cursor.rowcount
    
    def delete_articles_by_bill_id_from_db(self, bill_code):
        query = "DELETE FROM Articles WHERE bill_code = ?"
        (_, cursor) = self.run_query(query, [bill_code])
        return cursor.rowcount

    def get_articles_from_db(self, id=None):

        query = 'SELECT * FROM Articles WHERE bill_code = ?'
        (result, _) = self.run_query(query, [id])
        list_result = list(result)
        return list_result if len(list_result) != 0 else None

    def save_bill_to_db(self, phone, total_articles, total, deposit, deposit_for_cancelation, balance, state, generation_date, cancelation_date):
        query = 'INSERT INTO Bills (phone, total_articles, total, deposit, deposit_for_cancelation, balance, state, generation_date, cancelation_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);'
        (_, cursor) = self.run_query(query, [phone, total_articles, total, deposit, deposit_for_cancelation, balance,
                                             state, generation_date, cancelation_date])

        return cursor.lastrowid

    def save_client_to_db(self, phone, name):
        query = 'INSERT INTO Clients (phone, name) VALUES(?, ?);'
        (_, cursor) = self.run_query(query, [phone, name])

        return cursor.lastrowid

    def save_article_to_db(self, last_bill_id, number, service, description, total_value, state):
        query = 'INSERT INTO Articles (bill_code, number, service, description, total_value, state) VALUES (?, ?, ?, ?, ?, ?);'
        (_, cursor) = self.run_query(query, [last_bill_id, number,
                                             service, description, total_value, state])

        return cursor.lastrowid

    def get_last_value_from_db(self, table_name, column_name):
        query = 'SELECT {} FROM {} ORDER BY {} DESC LIMIT 1;'.format(
            column_name, table_name, column_name)
        (result, _) = list(self.run_query(query))
        list_result = list(result)
        return list_result[0][0] if len(list_result) != 0 else None

    def run_query(self, query, parameters=[]):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return (result, cursor)


class formater():

    def __init__(self):
        pass

    def add_thousand_separators_format(self, field):
        old_number = self.rem_commas(field.text())
        new_number = self.add_commas(old_number)
        field.setText(new_number)

    def rem_commas(self, number):
        without_commas_number = re.sub(",", "", number or '0')
        return int(without_commas_number)

    def add_commas(self, number):
        return f"{number:,}"


class printerDriver():
    def __init__(self):
        pass

    def process_printing(self, bill_id, name, phone, generation_date, articles, total_articles, total, deposit, balance, subject):
        
        first_part = """
            <head>
                <meta charset="UTF-8">
            </head>
            <h1 style="text-align: center;"><span style="text-decoration: underline; background-color: #999999;">GAMUZAS, CUERO &
                    COLOR</span></h1>
            <h4 style="text-align: center;"><span style="color: #808080;">LAVANDERÍA Y TINTORERÍA</span></h4>
            <p style="text-align: center;"><strong>""" + subject + """</strong></p>
            <p style="text-align: center;"><strong>Código:</strong> """ + bill_id + """</p>
            <p style="text-align: center;"><strong>Nombre:</strong> """ + name + """</p>
            <p style="text-align: center;"><strong>Teléfono:</strong> """ + phone + """</p>
            <p style="text-align: center;"><strong>Fecha:</strong> """ + generation_date + """</p>
            <p style="text-align: center;"><strong>ARTÍCULOS</strong></p>
            <table style="border-collapse: collapse; width: 100%; height: 72px;" border="1">
                <tbody>
                    <tr style="height: 18px;">
                        <td style="width: 3.97727%; height: 18px; text-align: center;"><strong>#</strong></td>
                        <td style="width: 16.0511%; height: 18px; text-align: center;"><strong>SERV</strong></td>
                        <td style="width: 57.9546%; height: 18px; text-align: center;"><strong>DESCRIPCIÓN</strong></td>
                        <td style="width: 11.0085%; height: 18px; text-align: center;"><strong>VALOR</strong></td>
                        <td style="width: 11.0085%; text-align: center;"><strong>EST</strong></td>
                    </tr>"""
        
        articles_part = ""
                     
        if articles:
            for article in articles:
                (number, service, description, value, article_state) = article
                articles_part = articles_part + """
                    <tr style="height: 54px;">
                        <td style="width: 3.97727%; height: 54px; text-align: center;">""" + number + """</td>
                        <td style="width: 16.0511%; height: 54px; text-align: center;">""" + service + """</td>
                        <td style="width: 57.9546%; height: 54px; text-align: center;">""" + description + """</td>
                        <td style="width: 11.0085%; height: 54px; text-align: center;">""" + value + """</td>
                        <td style="width: 11.0085%; text-align: center;">""" + article_state + """</td>
                    </tr>"""
        
        last_part = """
                    </tbody>
            </table>
            <p style="text-align: center;"><strong>TOTAL PRENDAS:</strong> """ + total_articles + """</p>
            <p style="text-align: center;"><strong>TOTAL:</strong> """ + total + """</p>
            <p style="text-align: center;"><strong>ABONO:</strong> """ + deposit + """</p>
            <p style="text-align: center;"><strong>SALDO:</strong> """ + balance + """</p>"""
        
        bill_html = first_part + articles_part + last_part

        config = pdfkit.configuration(wkhtmltopdf= os.getcwd() + "\\wkhtmltopdf\\bin\\wkhtmltopdf.exe") # set wkhtmltopdf .exe path  os.getcwd() + "\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
        pdfkit.from_string(bill_html, 'pdf_generated.pdf', configuration=config, css='style.css',
            options =
                {
                    'page-height': '297mm', #Depends on POS Printer dimensions
                    'page-width': '72.1mm', #Depends on POS Printer dimensions
                    'margin-top': '0.0mm',
                    'margin-right': '0.0mm',
                    'margin-bottom': '0.0mm',
                    'margin-left': '0.0mm',
                    'dpi': '203',#Depends on POS Printer dimensions
                })


        currentprinter = win32print.GetDefaultPrinter()

        win32api.ShellExecute(0, 'open', GSPRINT_PATH, '-ghostscript "'+GHOSTSCRIPT_PATH+'" -printer "'+currentprinter+'" "pdf_generated.pdf"', '.', 0)



class utils(dbDriver, formater, printerDriver):
    def __init__(self):
        pass

    def check_deposit(self, total_text, deposit_text):
        total = self.rem_commas(total_text)
        deposit = self.rem_commas(deposit_text)
        if deposit > total:
            return False
        else:
            return True

    def check_client(self, find_client_tel_field_text, find_client_name_field_text):
        client = self.get_client_from_db(int(find_client_tel_field_text))

        if client:
            (_, name) = client
            name_field = find_client_name_field_text
            if name == name_field:
                return True
            else:
                return False
        else:
            return None

    def set_checkers(self, components, action_component):
        for component in components:
            component.textChanged.connect(
                lambda: self.check_if_can_do_action(components, action_component))

    def check_if_can_do_action(self, fields_to_be_ckeck, action_component):
        ckeck_results = map(lambda field:
                            field.text() != ''
                            and field.text() != '0'
                            and field.text() != 'Entregado'
                            and field.text() != 'Anulado',
                            fields_to_be_ckeck)

        if all(ckeck_results):
            action_component.setEnabled(True)
        else:
            action_component.setEnabled(False)

    def set_regex_validator(self, reg_exp, field):
        regex = QtCore.QRegExp(reg_exp)
        validator = QtGui.QRegExpValidator(regex)
        field.setValidator(validator)

    def ckeck_if_can_remove_article(self, table_field, remove_button, column_id = None, required_value = None):
        if len(table_field.selectionModel().selectedRows()) > 0:
            if column_id or required_value:
                selected_row = table_field.currentRow()
                if table_field.item(selected_row, column_id).text() == required_value:
                    remove_button.setEnabled(True)
                else:
                    remove_button.setEnabled(False)
            else:
                remove_button.setEnabled(True)
        else:
            remove_button.setEnabled(False)