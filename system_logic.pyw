# TO RUN:
# cd Desktop\"GC&C"\"GC&CSystem" & designer system_ui.ui
# pyuic5 -x system_ui.ui -o system_ui.py & python system_logic.pyw

from pickle import TRUE
from modules.utils import *
import datetime
from time import sleep

DATETIME_FORMAT = "%d/%m/%Y %H:%M"
DATE_FORMAT = "%d/%m/%Y"
PYTHON_DATE_FORMAT = "dd/MM/yyyy"

class billSystem(QtWidgets.QMainWindow, Ui_MainWindow, utils):

    def __init__(self, *args, **kwargs):

        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)

        # this fields must be filled to find a client (findClientButton)

        fields_to_find_client = [self.findClientTelField]

        # this fields must be filled to add an article (addArticleButton)

        fields_to_add_article = [
            self.articleDescriptionField]

        # this fields must be filled to generate a bill (generateBillButton)

        fields_to_generate_bill = [
            self.findClientTelField, self.findClientNameField]

        # this fields must be filled to find a bill (findBillButton)

        fields_to_find_bill = [self.findBillField]

        # this fields must be filled to increase a bill deposit (increaseDepositButton)
        fields_to_increase_deposit_bill = [
            self.billCodeField, self.queryIncreaseDepositField]

        # this fields must be filled to cancel a bill (cancelBillButton)

        fields_to_cancel_bill = [self.billCodeField, self.billStateField]

        # this fields must be filled to cancel partially a bill (partialCancelationButton)

        fields_to_cancel_partially_bill = [
            self.billStateField, self.balanceAfterPartialCancelationField]

        # this fields must be filled to print a bill (printBillButton)

        fields_to_print_bill = [self.billCodeField]

        # this fields must be filled to undo a bill (undoBillButton)

        fields_to_undo_bill = [self.billCodeField, self.billStateField]


        self.tabWidget.removeTab(4)


        # findClientTelField -----------------------------------------------------------------------------------------------

        self.set_regex_validator("[0-9_]+", self.findClientTelField)

        # findClientNameField -----------------------------------------------------------------------------------------------

        # findClientButton -----------------------------------------------------------------------------------------------

        self.set_checkers(fields_to_find_client, self.findClientButton)

        self.findClientButton.clicked.connect(
            lambda: self.find_client(int(self.findClientTelField.text())))

        # articlesTable -----------------------------------------------------------------------------------------------

        self.articlesTable.setColumnWidth(0, 70)

        self.articlesTable.setColumnWidth(1, 100)

        self.articlesTable.setColumnWidth(2, 790)

        self.articlesTable.setColumnWidth(3, 180)

        self.articlesTable.itemSelectionChanged.connect(
            lambda: self.ckeck_if_can_do_action_on_table(self.articlesTable, self.removeArticleButton))

        # articlesNumberField -----------------------------------------------------------------------------------------------

        # articleServiceField -----------------------------------------------------------------------------------------------

        self.articleServiceField.addItem('Lavado')

        self.articleServiceField.addItem('Tintura')

        self.articleServiceField.addItem('Arreglo')

        # articleDescriptionField -----------------------------------------------------------------------------------------------

        # articleUnitValueField -----------------------------------------------------------------------------------------------

        self.articleUnitValueField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.articleUnitValueField))

        self.set_regex_validator("[0-9,]+", self.articleUnitValueField)

        # addArticleButton -----------------------------------------------------------------------------------------------

        self.set_checkers(fields_to_add_article, self.addArticleButton)

        self.addArticleButton.clicked.connect(self.add_article_on_creation)

        self.addArticleButton.clicked.connect(
            lambda: self.sum_column_on_field(self.articlesTable, self.totalField, 3))

        self.addArticleButton.clicked.connect(
            lambda: self.sum_column_on_field(self.articlesTable, self.totalArticlesField, 0))

        # removeArticleButton -----------------------------------------------------------------------------------------------

        self.removeArticleButton.clicked.connect(
            lambda: self.remove_article_from_table(self.articlesTable))

        self.removeArticleButton.clicked.connect(
            lambda: self.sum_column_on_field(self.articlesTable, self.totalField, 3))

        self.removeArticleButton.clicked.connect(
            lambda: self.sum_column_on_field(self.articlesTable, self.totalArticlesField, 0))

        # totalArticlesField -----------------------------------------------------------------------------------------------

        # totalField -----------------------------------------------------------------------------------------------

        self.totalField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.totalField))

        self.totalField.textChanged.connect(lambda: self.update_result_field(
            self.totalField, self.depositField, self.balanceField, self.simple_result_function))

        # depositField -----------------------------------------------------------------------------------------------

        self.depositField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.depositField))

        self.depositField.textChanged.connect(lambda: self.update_result_field(
            self.totalField, self.depositField, self.balanceField, self.simple_result_function))

        self.set_regex_validator("[0-9,]+", self.depositField)

        # balanceField -----------------------------------------------------------------------------------------------

        self.balanceField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.balanceField))

        # generateBillButton -----------------------------------------------------------------------------------------------

        self.set_checkers(fields_to_generate_bill, self.generateBillButton)
        self.generateBillButton.clicked.connect(self.process_bill_generation)

        # findBillField -----------------------------------------------------------------------------------------------

        self.set_regex_validator("[0-9_]+", self.findBillField)

        # findBillButton -----------------------------------------------------------------------------------------------

        self.set_checkers(fields_to_find_bill, self.findBillButton)
        self.findBillButton.clicked.connect(
            lambda: self.find_bill(int(self.findBillField.text())))

        # billCodeField -----------------------------------------------------------------------------------------------

        # generationDateField -----------------------------------------------------------------------------------------------

        # telField -----------------------------------------------------------------------------------------------

        # nameField -----------------------------------------------------------------------------------------------

        # consultArticlesTable -----------------------------------------------------------------------------------------------

        self.consultArticlesTable.setColumnWidth(0, 60)

        self.consultArticlesTable.setColumnWidth(1, 50)

        self.consultArticlesTable.setColumnWidth(2, 100)

        self.consultArticlesTable.setColumnWidth(3, 660)

        self.consultArticlesTable.setColumnWidth(4, 180)

        self.consultArticlesTable.setColumnWidth(5, 90)

        self.consultArticlesTable.itemSelectionChanged.connect(
            lambda: self.ckeck_if_can_do_action_on_table(self.consultArticlesTable, self.removeConsultArticleButton, 5, 'NE'))

        # removeConsultArticleButton -----------------------------------------------------------------------------------------------

        self.removeConsultArticleButton.clicked.connect(
            lambda: self.remove_article_from_table(self.consultArticlesTable, self.udpate_articicles_value_for_partial_cancelation))

        # queryTotalField -----------------------------------------------------------------------------------------------

        self.queryTotalField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.queryTotalField))

        # queryDepositField -----------------------------------------------------------------------------------------------

        self.queryDepositField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.queryDepositField))

        # increaseDepositButton -----------------------------------------------------------------------------------------------

        self.set_checkers(fields_to_increase_deposit_bill,
                          self.increaseDepositButton)
        self.increaseDepositButton.clicked.connect(
            lambda: self.increase_deposit(int(self.billCodeField.text())))

        # queryIncreaseDepositField -----------------------------------------------------------------------------------------------

        self.queryIncreaseDepositField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.queryIncreaseDepositField))

        self.set_regex_validator("[0-9,]+", self.queryIncreaseDepositField)

        # queryDepositForCancelationField -----------------------------------------------------------------------------------------------

        self.queryDepositForCancelationField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.queryDepositForCancelationField))

        # queryBalanceField -----------------------------------------------------------------------------------------------

        self.queryBalanceField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.queryBalanceField))

        # removedArticlesValueField -----------------------------------------------------------------------------------------------

        self.removedArticlesValueField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.removedArticlesValueField))

        self.removedArticlesValueField.textChanged.connect(lambda: self.update_result_field(
            self.queryDepositForCancelationField, self.removedArticlesValueField, self.depositForCancelationAfterArticleRemovalField, self.coalesce_result_function))

        self.removedArticlesValueField.textChanged.connect(lambda: self.update_result_field(
            self.removedArticlesValueField, self.queryDepositForCancelationField, self.partialBalanceField, self.coalesce_result_function))

        self.removedArticlesValueField.textChanged.connect(lambda: self.update_result_field(
            self.queryBalanceField, self.partialBalanceField, self.balanceAfterPartialCancelationField, self.coalesce_result_function))

        # depositForCancelationAfterArticleRemovalField -----------------------------------------------------------------------------------------------

        self.depositForCancelationAfterArticleRemovalField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.depositForCancelationAfterArticleRemovalField))

        # partialBalanceField -----------------------------------------------------------------------------------------------

        self.partialBalanceField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.partialBalanceField))

        # balanceAfterPartialCancelationField -----------------------------------------------------------------------------------------------

        self.balanceAfterPartialCancelationField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.balanceAfterPartialCancelationField))

        # billStateField -----------------------------------------------------------------------------------------------

        # receivedMoneyField -----------------------------------------------------------------------------------------------

        self.receivedMoneyField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.receivedMoneyField))

        self.receivedMoneyField.textChanged.connect(lambda: self.update_result_field(
            self.receivedMoneyField, self.queryBalanceField, self.changeField, self.simple_result_function))

        self.set_regex_validator("[0-9_]+", self.receivedMoneyField)

        # changeField -----------------------------------------------------------------------------------------------

        self.changeField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.changeField))

        # cancelBillButton -----------------------------------------------------------------------------------------------

        self.set_checkers(fields_to_cancel_bill, self.cancelBillButton)
        self.cancelBillButton.clicked.connect(
            lambda: self.cancel_bill(int(self.billCodeField.text())))

        # partialCancelationButton -----------------------------------------------------------------------------------------------

        self.set_checkers(fields_to_cancel_partially_bill,
                          self.partialCancelationButton)

        self.partialCancelationButton.clicked.connect(
            lambda: self.cancel_bill_partially(int(self.billCodeField.text())))

        # printBillButton -----------------------------------------------------------------------------------------------

        self.set_checkers(fields_to_print_bill, self.printBillButton)

        self.printBillButton.clicked.connect(self.print_bill_on_reprinting)

        # undoBillButton -----------------------------------------------------------------------------------------------

        self.set_checkers(fields_to_undo_bill, self.undoBillButton)

        self.undoBillButton.clicked.connect(
            lambda: self.undo_bill(int(self.billCodeField.text())))

        # filterClientsPhoneField -----------------------------------------------------------------------------------------------

        self.set_regex_validator("[0-9_]+", self.filterClientsPhoneField)

        self.filterClientsPhoneField.textChanged.connect(
            lambda: self.filter_clients_table(self.filterClientsPhoneField.text(), self.filterClientsNameField.text()))

        # filterClientsNameField -----------------------------------------------------------------------------------------------

        self.filterClientsNameField.textChanged.connect(
            lambda: self.filter_clients_table(self.filterClientsPhoneField.text(), self.filterClientsNameField.text()))

        # filterClientsTable -----------------------------------------------------------------------------------------------

        self.filterClientsTable.setColumnWidth(0, 119)
        self.filterClientsTable.setColumnWidth(1, 223)

        self.filter_clients_table()

        self.filterClientsTable.itemSelectionChanged.connect(
            lambda: self.ckeck_if_can_do_action_on_table(self.filterClientsTable, self.filterBillsButton))
        
        self.filterClientsTable.itemSelectionChanged.connect(
            lambda: self.ckeck_if_can_do_action_on_table(self.filterClientsTable, self.editClientButton))
        
        self.filterClientsTable.itemSelectionChanged.connect(
            lambda: self.set_table_column_on_field(self.filterClientsTable, 0, self.editClientPhoneField))
        
        self.filterClientsTable.itemSelectionChanged.connect(
            lambda: self.set_table_column_on_field(self.filterClientsTable, 1, self.editClientNameField))
        
        # filterBillsButton -----------------------------------------------------------------------------------------------

        self.filterBillsButton.clicked.connect(
            lambda: self.set_table_column_on_field(self.filterClientsTable, 0, self.filterBillsPhoneField))

        self.update_filter_bills_totals_handler(self.filterBillsButton, 'button')

        # editClientButton -----------------------------------------------------------------------------------------------

        self.editClientButton.clicked.connect(
            lambda: self.edit_client(self.editClientPhoneField, self.editClientNameField))

        # filterBillsPhoneField -----------------------------------------------------------------------------------------------

        self.set_regex_validator("[0-9_]+", self.filterBillsPhoneField)

        self.filterBillsPhoneField.textChanged.connect(
            lambda: self.fill_bills_table(self.filterBillsTable, self.filterBillsPhoneField.text(), self.filterBillsStateField.currentText()))
        
        self.update_filter_bills_totals_handler(self.filterBillsPhoneField, 'text_input')
        
        # filterBillsStateField -----------------------------------------------------------------------------------------------

        self.filterBillsStateField.addItem('-')

        self.filterBillsStateField.addItem('Sin entregar')

        self.filterBillsStateField.addItem('Entrega parcial')

        self.filterBillsStateField.addItem('Entregado')

        self.filterBillsStateField.currentTextChanged.connect(
            lambda: self.fill_bills_table(self.filterBillsTable, self.filterBillsPhoneField.text(), self.filterBillsStateField.currentText()))
        
        self.update_filter_bills_totals_handler(self.filterBillsStateField, 'combo_box')

        # filterBillsTable -----------------------------------------------------------------------------------------------

        self.filterBillsTable.setColumnWidth(0, 60)
        self.filterBillsTable.setColumnWidth(1, 100)
        self.filterBillsTable.setColumnWidth(2, 30)
        self.filterBillsTable.setColumnWidth(3, 90)
        self.filterBillsTable.setColumnWidth(4, 90)
        self.filterBillsTable.setColumnWidth(5, 90)
        self.filterBillsTable.setColumnWidth(6, 90)
        self.filterBillsTable.setColumnWidth(7, 100)
        self.filterBillsTable.setColumnWidth(8, 110)
        self.filterBillsTable.setColumnWidth(9, 110)

        self.fill_bills_table(self.filterBillsTable)

        # filterBillsNumberField -----------------------------------------------------------------------------------------------

        # filterBillsTotalField -----------------------------------------------------------------------------------------------
        
        self.filterBillsTotalField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.filterBillsTotalField))
        
        # filterBillsDepositField -----------------------------------------------------------------------------------------------

        self.filterBillsDepositField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.filterBillsDepositField))
        
        # filterBillsDepositForCancelationField -----------------------------------------------------------------------------------------------

        self.filterBillsDepositForCancelationField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.filterBillsDepositForCancelationField))
        
        # filterBillsBalanceField -----------------------------------------------------------------------------------------------

        self.filterBillsBalanceField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.filterBillsBalanceField))
        
        self.init_filter_totals()

        # currentDayReportButton -----------------------------------------------------------------------------------------------

        self.currentDayReportButton.clicked.connect(
            lambda: self.generate_report(self.get_date_range('current day'), 'Dia actual'))
        
        # pastDayReportButton -----------------------------------------------------------------------------------------------

        self.pastDayReportButton.clicked.connect(
            lambda: self.generate_report(self.get_date_range('past day'), 'Dia anterior'))

        # currentWeekReportButton -----------------------------------------------------------------------------------------------

        self.currentWeekReportButton.clicked.connect(
            lambda: self.generate_report(self.get_date_range('current week'), 'Semana actual'))
        
        # pastWeekReportButton -----------------------------------------------------------------------------------------------

        self.pastWeekReportButton.clicked.connect(
            lambda: self.generate_report(self.get_date_range('past week'), 'Semana anterior'))
        
        # currentMonthReportButton -----------------------------------------------------------------------------------------------

        self.currentMonthReportButton.clicked.connect(
            lambda: self.generate_report(self.get_date_range('current month'), 'Mes actual'))
        
        # pastMonthReportButton -----------------------------------------------------------------------------------------------

        self.pastMonthReportButton.clicked.connect(
            lambda: self.generate_report(self.get_date_range('past month'), 'Mes anterior'))

        # currentYearReportButton -----------------------------------------------------------------------------------------------

        self.currentYearReportButton.clicked.connect(
            lambda: self.generate_report(self.get_date_range('current year'), 'Año actual'))

        # pastYearReportButton -----------------------------------------------------------------------------------------------

        self.pastYearReportButton.clicked.connect(
            lambda: self.generate_report(self.get_date_range('past year'), 'Año anterior'))
        
        self.generateReportButton.clicked.connect(
            lambda: self.generate_report(self.get_date_range('custom'), 'Manual'))

        # reportGeneratedBillsTable -----------------------------------------------------------------------------------------------

        self.reportGeneratedBillsTable.setColumnWidth(0, 60)
        self.reportGeneratedBillsTable.setColumnWidth(1, 100)
        self.reportGeneratedBillsTable.setColumnWidth(2, 30)
        self.reportGeneratedBillsTable.setColumnWidth(3, 90)
        self.reportGeneratedBillsTable.setColumnWidth(4, 90)
        self.reportGeneratedBillsTable.setColumnWidth(5, 90)
        self.reportGeneratedBillsTable.setColumnWidth(6, 90)
        self.reportGeneratedBillsTable.setColumnWidth(7, 100)
        self.reportGeneratedBillsTable.setColumnWidth(8, 110)
        self.reportGeneratedBillsTable.setColumnWidth(9, 110)

        # reportCanceledBillsTable -----------------------------------------------------------------------------------------------

        self.reportCanceledBillsTable.setColumnWidth(0, 60)
        self.reportCanceledBillsTable.setColumnWidth(1, 100)
        self.reportCanceledBillsTable.setColumnWidth(2, 30)
        self.reportCanceledBillsTable.setColumnWidth(3, 90)
        self.reportCanceledBillsTable.setColumnWidth(4, 90)
        self.reportCanceledBillsTable.setColumnWidth(5, 90)
        self.reportCanceledBillsTable.setColumnWidth(6, 90)
        self.reportCanceledBillsTable.setColumnWidth(7, 100)
        self.reportCanceledBillsTable.setColumnWidth(8, 110)
        self.reportCanceledBillsTable.setColumnWidth(9, 110)
        
        # reportEnteredNumberField -----------------------------------------------------------------------------------------------

        # reportBilledMoneyField -----------------------------------------------------------------------------------------------

        self.reportBilledMoneyField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.reportBilledMoneyField))

        # reportEnteredDepositField -----------------------------------------------------------------------------------------------

        self.reportEnteredDepositField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.reportEnteredDepositField))
        
        # reportDeliveredNumberField -----------------------------------------------------------------------------------------------

        # reportEnteredMoneyField -----------------------------------------------------------------------------------------------

        self.reportEnteredMoneyField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.reportEnteredMoneyField))
        
        # reportTotalEnteredMoneyField -----------------------------------------------------------------------------------------------

        self.reportTotalEnteredMoneyField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.reportTotalEnteredMoneyField))
        

        # currentStateEnteredNumberField -----------------------------------------------------------------------------------------------

        # currentStateBilledMoneyField -----------------------------------------------------------------------------------------------

        self.currentStateBilledMoneyField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.currentStateBilledMoneyField))

        # currentStateNumberField -----------------------------------------------------------------------------------------------

        # currentStateDeliveredNumberField -----------------------------------------------------------------------------------------------
        
        # currentStateEnteredMoneyField -----------------------------------------------------------------------------------------------

        self.currentStateEnteredMoneyField.textChanged.connect(
            lambda: self.add_thousand_separators_format(self.currentStateEnteredMoneyField))

        self.fill_current_state_report()

    def fill_current_state_report(self):

        entered_total_articles = self.get_bills_from_db(select_content='coalesce(sum(total_articles),0)')
        billed_total = self.get_bills_from_db(select_content='coalesce(sum(total),0)')

        number = self.get_articles_from_db(state='NE', select_content='coalesce(sum(number),0)')
        delivered_total_articles = self.get_articles_from_db(state='E', select_content='coalesce(sum(number),0)')

        entered_cancelation_money = self.get_bills_from_db(state='Entregado', select_content='coalesce(sum(total),0)')
        entered_deposits = self.get_bills_from_db(select_content='coalesce(sum(deposit),0)')
        entered_total = entered_cancelation_money[0][0] + entered_deposits[0][0]

        self.currentStateEnteredNumberField.setText(str(entered_total_articles[0][0]))

        self.currentStateBilledMoneyField.setText(str(billed_total[0][0]))
        
        self.currentStateNumberField.setText(str(number[0][0]))

        self.currentStateDeliveredNumberField.setText(str(delivered_total_articles[0][0]))
        
        self.currentStateEnteredMoneyField.setText(str(entered_total))

    def generate_report(self, date_range, report_type):

        (initial_datetime, final_datetime) = date_range

        date_initial_datetime = datetime.datetime.strptime(initial_datetime, DATETIME_FORMAT)
        date_final_datetime = datetime.datetime.strptime(final_datetime, DATETIME_FORMAT)

        if date_final_datetime < date_initial_datetime:
            QtWidgets.QMessageBox.about(
                self, "ERROR", "La fecha inicial es mayor a la fecha final")
            return

        self.reportType.setText(report_type)
        self.initialDateField.setText(initial_datetime)
        self.finalDateField.setText(final_datetime)

        self.fill_bills_table(self.reportGeneratedBillsTable, initial_date=initial_datetime, final_date=final_datetime, date_field='generation_date')
        
        self.sum_column_on_field(self.reportGeneratedBillsTable, self.reportEnteredNumberField, 2)
        self.sum_column_on_field(self.reportGeneratedBillsTable, self.reportBilledMoneyField, 3)
        self.sum_column_on_field(self.reportGeneratedBillsTable, self.reportEnteredDepositField, 4)

        self.fill_bills_table(self.reportCanceledBillsTable, initial_date=initial_datetime, final_date=final_datetime, date_field='cancelation_date')

        self.sum_column_on_field(self.reportCanceledBillsTable, self.reportDeliveredNumberField, 2)
        self.sum_column_on_field(self.reportCanceledBillsTable, self.reportEnteredMoneyField, 6)

        self.update_result_field(
            self.reportEnteredDepositField, self.reportEnteredMoneyField, self.reportTotalEnteredMoneyField, self.simple_add_result_function)
    
    def get_date_range(self, report_type):
        now = datetime.datetime.now()
        initial_datetime = ''
        final_datetime = ''
        initial_time = '00:00'
        final_time = '23:59'
        
        if report_type =='current day':
            initial_datetime = now.strftime(DATE_FORMAT) + ' ' + initial_time
            final_datetime = now.strftime(DATE_FORMAT) + ' ' + final_time
        elif report_type =='past day':
            past_day = now - datetime.timedelta(days=1)
            initial_datetime = past_day.strftime(DATE_FORMAT) + ' ' + initial_time
            final_datetime = past_day.strftime(DATE_FORMAT) + ' ' + final_time
        elif report_type =='current week':
            current_week_initial_day = now - datetime.timedelta(days = now.weekday())
            current_week_final_day = now + datetime.timedelta(days = 6 - now.weekday())
            initial_datetime = current_week_initial_day.strftime(DATE_FORMAT) + ' ' + initial_time
            final_datetime = current_week_final_day.strftime(DATE_FORMAT) + ' ' + final_time
        elif report_type =='past week':
            past_week_initial_day = now - datetime.timedelta(days = 7 + now.weekday())
            past_week_final_day = now - datetime.timedelta(days = now.weekday() + 1)
            initial_datetime = past_week_initial_day.strftime(DATE_FORMAT) + ' ' + initial_time
            final_datetime = past_week_final_day.strftime(DATE_FORMAT) + ' ' + final_time
        elif report_type =='current month':
            current_month_initial_day = datetime.datetime.strptime('01' + '/' + now.strftime("%m") + '/' + now.strftime("%Y"), DATE_FORMAT)
            next_month_firts_day = datetime.datetime.strptime('01' + '/' + str(int(now.strftime("%m")) + 1) + '/' + now.strftime("%Y"), DATE_FORMAT)
            current_month_final_day = next_month_firts_day - datetime.timedelta(days = 1)
            initial_datetime = current_month_initial_day.strftime(DATE_FORMAT) + ' ' + initial_time
            final_datetime = current_month_final_day.strftime(DATE_FORMAT) + ' ' + final_time
        elif report_type =='past month':
            past_month_initial_day = datetime.datetime.strptime('01' + '/' + str(int(now.strftime("%m")) - 1) + '/' + now.strftime("%Y"), DATE_FORMAT)
            current_month_initial_day = datetime.datetime.strptime('01' + '/' + now.strftime("%m") + '/' + now.strftime("%Y"), DATE_FORMAT)
            past_month_final_day = current_month_initial_day - datetime.timedelta(days = 1)
            initial_datetime = past_month_initial_day.strftime(DATE_FORMAT) + ' ' + initial_time
            final_datetime = past_month_final_day.strftime(DATE_FORMAT) + ' ' + final_time
        if report_type =='current year':
            current_year_initial_day = datetime.datetime.strptime('01/01/' + now.strftime("%Y"), DATE_FORMAT)
            current_year_final_day = datetime.datetime.strptime('31/12/' + now.strftime("%Y"), DATE_FORMAT)
            initial_datetime = current_year_initial_day.strftime(DATE_FORMAT) + ' ' + initial_time
            final_datetime = current_year_final_day.strftime(DATE_FORMAT) + ' ' + final_time
        if report_type =='past year':
            past_year_initial_day = datetime.datetime.strptime('01' + '/01/' + str(int(now.strftime("%Y")) - 1), DATE_FORMAT)
            past_year_final_day = datetime.datetime.strptime('31' + '/12/' + str(int(now.strftime("%Y")) - 1), DATE_FORMAT)
            initial_datetime = past_year_initial_day.strftime(DATE_FORMAT) + ' ' + initial_time
            final_datetime = past_year_final_day.strftime(DATE_FORMAT) + ' ' + final_time
        if report_type =='custom':
            custom_initial_day = self.initialDateCalendar.selectedDate()
            custom_final_day = self.finalDateCalendar.selectedDate()
            initial_datetime = custom_initial_day.toString(PYTHON_DATE_FORMAT) + ' ' + initial_time
            final_datetime = custom_final_day.toString(PYTHON_DATE_FORMAT) + ' ' + final_time
        
        return(initial_datetime, final_datetime)

    def update_filter_bills_totals_handler(self, field, field_type):
    
        if field_type == 'button':
            field.clicked.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsNumberField, 2))
            field.clicked.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsTotalField, 3))
            field.clicked.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositField, 4))
            field.clicked.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositForCancelationField, 5))
            field.clicked.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsBalanceField, 6))
        elif field_type == 'text_input':
            field.textChanged.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsNumberField, 2))
            field.textChanged.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsTotalField, 3))
            field.textChanged.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositField, 4))
            field.textChanged.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositForCancelationField, 5))
            field.textChanged.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsBalanceField, 6))
        else:
            field.currentTextChanged.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsNumberField, 2))
            field.currentTextChanged.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsTotalField, 3))
            field.currentTextChanged.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositField, 4))
            field.currentTextChanged.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositForCancelationField, 5))
            field.currentTextChanged.connect(
                lambda: self.sum_column_on_field(self.filterBillsTable, self.filterBillsBalanceField, 6))
    
    def init_filter_totals(self):
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsNumberField, 2)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsTotalField, 3)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositField, 4)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositForCancelationField, 5)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsBalanceField, 6)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsNumberField, 2)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsTotalField, 3)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositField, 4)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositForCancelationField, 5)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsBalanceField, 6)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsNumberField, 2)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsTotalField, 3)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositField, 4)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsDepositForCancelationField, 5)
        self.sum_column_on_field(self.filterBillsTable, self.filterBillsBalanceField, 6)

    def find_client(self, phone):

        client = self.get_client_from_db(phone)

        if client:
            (_, name) = client
            self.findClientNameField.setText(name)
        else:
            QtWidgets.QMessageBox.about(
                self, "ERROR", "No existe un cliente con el teléfono ingresado")
    
    def edit_client(self, edit_phone_field, edit_name_field):
        current_name = self.get_table_column(self.filterClientsTable, 1)
        print(current_name)
        print(edit_phone_field.text(), edit_name_field.text())
        if current_name == edit_name_field.text():
            QtWidgets.QMessageBox.about(
                self, "ERROR", "No hay cambios en el nombre")
        else:
            affected_client = self.update_client_name(int(self.editClientPhoneField.text()), edit_name_field.text())
            if affected_client == 0:
                QtWidgets.QMessageBox.about(
                self, "ERROR", "No fue posible editar el cliente")
            else:
                self.filter_clients_table(self.filterClientsPhoneField.text(), self.filterClientsNameField.text())
                QtWidgets.QMessageBox.about(
                    self, "OK", "Cliente editado correctamente")

    def find_bill(self, id):
        bill = self.get_bill_from_db(id)
        articles = self.get_articles_from_db(id=id)

        self.reset_bill_consult_fields()

        if bill:
            (code, phone, total_articles, total,
             deposit, deposit_for_cancelation, balance, state, generation_date, cancelation_date) = bill
            (_, name) = self.get_client_from_db(phone)
            self.billCodeField.setText(str(code))
            self.generationDateField.setText(generation_date)
            self.cancelationDateField.setText(cancelation_date if cancelation_date else '-')
            self.telField.setText(str(phone))
            self.nameField.setText(name)

            if articles:
                for article in articles:
                    (article_id, _, number, service, description,
                     value, article_state) = article
                    self.add_row_to_table(
                        self.consultArticlesTable, [article_id, number, service, description, self.add_commas(value), article_state])

            self.queryTotalArticlesField.setText(str(total_articles))
            self.queryTotalField.setText(self.add_commas(total))
            self.queryDepositField.setText(self.add_commas(deposit))
            self.queryDepositForCancelationField.setText(
                self.add_commas(deposit_for_cancelation))
            self.queryBalanceField.setText(self.add_commas(balance))
            self.billStateField.setText(state)
            self.partialCancelationButton.setEnabled(False)
        else:
            QtWidgets.QMessageBox.about(
                self, "ERROR", "No existe una factura con el código ingresado")

    def increase_deposit(self, code):

        deposit_is_valid = self.check_deposit(
            self.queryBalanceField.text(), self.queryIncreaseDepositField.text())
        
        if not deposit_is_valid:

            QtWidgets.QMessageBox.about(
                self, "ERROR", "El deposito ingresado no es permitido")
            
            return

        increase = self.rem_commas(self.queryIncreaseDepositField.text())
        self.queryIncreaseDepositField.setText("0")

        old_deposit = self.rem_commas(self.queryDepositField.text())
        affected_deposit = self.update_deposit_in_db(
            code, old_deposit + increase)
        self.queryDepositField.setText(str(old_deposit + increase))

        old_deposit_for_cancelation = self.rem_commas(
            self.queryDepositForCancelationField.text())
        affected_deposit_for_cancelation = self.update_deposit_for_cancelation_in_db(
            code, old_deposit_for_cancelation + increase)
        self.queryDepositForCancelationField.setText(
            str(old_deposit_for_cancelation + increase))

        old_balance = self.rem_commas(self.queryBalanceField.text())
        affected_balance = self.update_balance_in_db(
            code, old_balance - increase)
        self.queryBalanceField.setText(str(old_balance - increase))

        if affected_deposit == 0 or affected_deposit_for_cancelation == 0 or affected_balance == 0:
            QtWidgets.QMessageBox.about(
                self, "ERROR", "No fue posible incrementar el abono")
        else:
            QtWidgets.QMessageBox.about(
                self, "OK", "Abono incrementado correctamente")

    def cancel_bill(self, code):
        now = datetime.datetime.now()
        dt_string = now.strftime(DATETIME_FORMAT)
        affected_bill = self.update_bill_state_in_db(
            code, 'Entregado', dt_string)

        self.update_articles_state_by_bill_id_in_db(code, 'E')

        if affected_bill == 0:
            QtWidgets.QMessageBox.about(
                self, "ERROR", "No fue posible cancelar la factura")
        else:
            QtWidgets.QMessageBox.about(
                self, "OK", "Factura cancelada correctamente")
            self.reset_bill_consult_fields()

    def cancel_bill_partially(self, code):

        state_updated = self.update_bill_state_in_db(code, 'Entrega parcial')
        deposit_updated = self.update_deposit_in_db(
            code, self.rem_commas(self.queryDepositField.text()) + self.rem_commas(self.partialBalanceField.text()))

        deposit_for_cancelation_updated = self.update_deposit_for_cancelation_in_db(
            code, self.rem_commas(self.depositForCancelationAfterArticleRemovalField.text()))

        balance_updated = self.update_balance_in_db(
            code, self.rem_commas(self.balanceAfterPartialCancelationField.text()))

        self.update_articles_state_by_bill_id_in_db(code, 'E')

        not_canceled_articles = self.get_items_from_table(
            self.consultArticlesTable)

        not_canceled_id_articles = list(
            map(lambda article: int(article[0]), not_canceled_articles))

        not_canceled_state_articles = list(
            map(lambda article: article[5], not_canceled_articles))

        not_canceled_id_and_state_articles = list(
            zip(not_canceled_id_articles, not_canceled_state_articles))

        not_canceled_articles_updated = list(map(lambda item: self.update_article_state_by_id_in_db(
            item[0], 'NE') if item[1] != 'E' else 1, not_canceled_id_and_state_articles))

        if state_updated == 0 or deposit_updated == 0 or deposit_for_cancelation_updated == 0 or balance_updated == 0 or not all(not_canceled_articles_updated):
            QtWidgets.QMessageBox.about(
                self, "ERROR", "Hubo un error en la cancelación parcial")
        else:
            QtWidgets.QMessageBox.about(
                self, "OK", "Factura cancelada parcialmente")
            self.reset_bill_consult_fields()

    def undo_bill(self, code):
        affected_bill = self.delete_bill_from_db(code)
        self.adjust_autoincrement_id('Bills')

        affected_articles = self.delete_articles_by_bill_id_from_db(code)
        self.adjust_autoincrement_id('Articles')

        if affected_bill == 0 and affected_articles:
            QtWidgets.QMessageBox.about(
                self, "ERROR", "No fue posible anular la factura")
        else:
            QtWidgets.QMessageBox.about(
                self, "OK", "Factura anulada correctamente")
            self.reset_bill_consult_fields()

    def filter_clients_table(self, phone = '', name = ''):
        self.filterClientsTable.setRowCount(0)

        clients = self.get_clients_from_db(phone, name)

        if clients:
            for client in clients:
                (phone, name) = client
                self.add_row_to_table(self.filterClientsTable, [phone, name])

    def fill_bills_table(self, table_field, phone = '', state = '-', initial_date = '', final_date = '', date_field = ''):
        table_field.setRowCount(0)

        bills = self.get_bills_from_db(phone=phone, state=state, initial_date=initial_date, final_date=final_date, date_field=date_field)

        if bills:
            for bill in bills:
                (code, phone, total_articles, total,
                    deposit, deposit_for_cancelation, balance, state, generation_date, cancelation_date) = bill
                self.add_row_to_table(
                    table_field,
                    [
                        str(code), str(phone), str(total_articles), self.add_commas(total), self.add_commas(deposit),
                        self.add_commas(deposit_for_cancelation), self.add_commas(balance), state, generation_date, cancelation_date if cancelation_date else '-'
                    ])

    def get_items_from_table(self, tableField):
        items = []
        rows = tableField.rowCount()
        for n in range(rows):
            row = []
            for column in range(9):
                if tableField.item(n, column):
                    row.append(tableField.item(n, column).text())

            items.append(row)

        return items

    def save_articles(self, bill_id):

        articles = self.get_items_from_table(self.articlesTable)
        for article in articles:
            (number, service, description, total_value) = article
            self.save_article_to_db(
                bill_id, number, service, description, self.rem_commas(total_value), 'NE')

    def add_article_on_creation(self):

        self.add_row_to_table(
            self.articlesTable,
            [
                int(self.articlesNumberField.text()),
                self.articleServiceField.currentText(),
                self.articleDescriptionField.text(),
                self.add_commas(int(self.articlesNumberField.text()) * self.rem_commas(self.articleUnitValueField.text()))])

        self.reset_article_addition_fields()

    def add_article_on_consult(self, article_id, number, service, description, value, article_state):

        self.add_row_to_table(
            self.consultArticlesTable, [article_id, number, service, description, self.add_commas(value), article_state])

    def add_row_to_table(self, table_field, fields):
        num_rows = table_field.rowCount()
        table_field.insertRow(num_rows)

        for (index, field) in enumerate(fields):
            table_field.setItem(
                num_rows, index, QtWidgets.QTableWidgetItem(str(field)))

    def remove_article_from_table(self, table_field, action_before_removal=None):
        index = table_field.currentRow()
        if action_before_removal:
            action_before_removal(table_field, index)
        table_field.removeRow(index)

    def sum_column_on_field(self, table_field, sum_field, column_id):
        total = 0

        total = self.sum_column(table_field, column_id)

        sum_field.setText(str(total))

    def sum_column(self, table_field, column_id):

        num_rows = int(table_field.rowCount())

        total = 0

        for i in range(num_rows):
            item = table_field.item(i, column_id)
            if item:
                total += self.rem_commas(table_field.item(i, column_id).text())

        return total
    
    def get_table_column(self, table_field, column_index):
        row_index = table_field.currentRow()
        return table_field.item(row_index, column_index).text()
    
    def set_table_column_on_field(self, table_field, column_index, field):
        row_index = table_field.currentRow()
        column_content = table_field.item(row_index, column_index).text() if table_field.item(row_index, column_index) else ''
        field.setText(column_content)

    def update_result_field(self, total_field, input_field, result_field, result_field_function):
        total_value = self.rem_commas(total_field.text())
        input_value = self.rem_commas(input_field.text())
        result_value = result_field_function(total_value, input_value)
        result_field.setText(str(result_value))

    def simple_result_function(self, first_input, second_input):
        return (first_input - second_input)

    def simple_add_result_function(self, first_input, second_input):
        return (first_input + second_input)

    def coalesce_result_function(self, first_input, second_input):
        return (first_input - second_input) if first_input >= second_input else 0

    def udpate_articicles_value_for_partial_cancelation(self, table_field, index):
        removed_article_value = self.rem_commas(
            table_field.item(index, 4).text())
        articles_value = abs(self.rem_commas(
            self.removedArticlesValueField.text()) + removed_article_value)

        self.removedArticlesValueField.setText(str(articles_value))

    def reset_bill_consult_fields(self):
        self.findBillField.setText("")
        self.billCodeField.setText("")
        self.generationDateField.setText("")
        self.cancelationDateField.setText("")
        self.telField.setText("")
        self.nameField.setText("")
        self.consultArticlesTable.setRowCount(0)
        self.queryTotalArticlesField.setText("0")
        self.queryTotalField.setText("0")
        self.queryDepositField.setText("0")
        self.queryDepositForCancelationField.setText("0")
        self.queryBalanceField.setText("0")

        self.removedArticlesValueField.setText("0")
        self.depositForCancelationAfterArticleRemovalField.setText("0")
        self.balanceAfterPartialCancelationField.setText("0")
        self.partialBalanceField.setText("0")

        self.billStateField.setText("")
        self.receivedMoneyField.setText("0")
        self.changeField.setText("0")

    def reset_bill_generation_fields(self):
        self.findClientTelField.setText("")
        self.findClientNameField.setText("")
        self.articlesTable.setRowCount(0)
        self.totalArticlesField.setText("0")
        self.articleDescriptionField.setText("")
        self.articleUnitValueField.setText("0")
        self.totalArticlesField.setText("0")
        self.totalField.setText("0")
        self.depositField.setText("0")
        self.balanceField.setText("0")

    def reset_article_addition_fields(self):
        self.articleDescriptionField.setText("")
        self.articleUnitValueField.setText("0")

    def print_bill_on_generation(self, bill_id, generation_date, subject):

        articles = self.get_items_from_table(self.articlesTable)

        articles_with_state = list(
            map(lambda article: article + ['NE'], articles))

        result = self.process_printing(
            str(bill_id),
            self.findClientNameField.text(),
            self.findClientTelField.text(),
            'Sin entregar',
            str(generation_date),
            '-',
            articles_with_state,
            self.totalArticlesField.text(),
            self.totalField.text(),
            self.depositField.text(),
            self.balanceField.text(),
            subject
        )

        return result

    def print_bill_on_reprinting(self):

        articles = self.get_items_from_table(self.consultArticlesTable)

        columns_for_printing = list(map(lambda article: article[1:], articles))

        result = self.process_printing(
            self.billCodeField.text(),
            self.nameField.text(),
            self.telField.text(),
            self.billStateField.text(),
            self.generationDateField.text(),
            self.cancelationDateField.text(),
            columns_for_printing,
            self.queryTotalArticlesField.text(),
            self.queryTotalField.text(),
            self.queryDepositField.text(),
            self.queryBalanceField.text(),
            'CONSULTA - COPIA'
        )

        QtWidgets.QMessageBox.about(
            self, "OK", "Factura impresa exitosamente")

        return result

    def process_bill_generation(self):
        client_is_valid = self.check_client(
            self.findClientTelField.text(), self.findClientNameField.text())
        deposit_is_valid = self.check_deposit(
            self.totalField.text(), self.depositField.text())

        if client_is_valid == False:
            QtWidgets.QMessageBox.about(
                self, "ERROR", "El telefono ingresado corresponde a un cliente previamente almacenado y el nombre ingresado no corresponde a dicho cliente.\n"
                "Puede:\n"
                "1. Pulsar en 'Buscar' para usar el cliente previamente almacenado.\n"
                "2. Usar otro numero de teléfono (de un cliente que no haya sido previamente almacenado).")

        if not deposit_is_valid:
            QtWidgets.QMessageBox.about(
                self, "ERROR", "El deposito ingresado no es permitido")

        if deposit_is_valid and (client_is_valid or client_is_valid is None):
            client_id = 1
            if client_is_valid is None:
                client_id = self.save_client_to_db(
                    int(self.findClientTelField.text()),
                    self.findClientNameField.text())
                if client_id == 0:
                    QtWidgets.QMessageBox.about(
                        self, "ERROR", "No fue posible almacenar el cliente")
                else:
                    QtWidgets.QMessageBox.about(
                        self, "OK", "Se ha guardado el cliente {} con el numero de teléfono {}".format(self.findClientNameField.text(), self.findClientTelField.text()))

            if client_id != 0:
                now = datetime.datetime.now()
                dt_string = now.strftime(DATETIME_FORMAT)

                bill_id = self.save_bill_to_db(
                    int(self.findClientTelField.text()),
                    int(self.totalArticlesField.text()),
                    self.rem_commas(self.totalField.text()),
                    self.rem_commas(self.depositField.text()),
                    self.rem_commas(self.depositField.text()),
                    self.rem_commas(self.balanceField.text()),
                    'Sin entregar',
                    dt_string,
                    None)

                if bill_id == 0:
                    QtWidgets.QMessageBox.about(
                        self, "ERROR", "No fue posible generar la factura")
                else:
                    self.save_articles(bill_id)
                    self.print_bill_on_generation(bill_id, dt_string, "RECIBO")
                    sleep(0.5)
                    self.print_bill_on_generation(bill_id, dt_string, "COPIA")
                    QtWidgets.QMessageBox.about(
                        self, "OK", "Factura generada exitosamente")
                    self.reset_bill_generation_fields()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = billSystem()
    window.show()
    app.exec_()
