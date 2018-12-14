import zipfile
import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QGridLayout, QWidget, QComboBox, QSpinBox, QSizePolicy,
                             QLabel, QHBoxLayout, QVBoxLayout, QDoubleSpinBox, QCalendarWidget, QDialog)
from urllib.request import urlretrieve
from datetime import date, timedelta
import pyqtgraph as pg


class Assignment_1(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        '''
            Create a list of currencies directly from the URL
        :return: String representation of the CSV file
        '''
        self.csvFile = Unzip().download_unzip()

        '''
            Convert CSV file into an Array
        '''
        self.csvFile = self.csvFile.split("\n")

        '''
            Select the first element of the CSV file. Split the currency for combobox
        '''
        self.currencies = self.csvFile[0][5:-1].split(",")

        '''
            Remove the first Element of the CSV file.
            i.e. All the currencies header. We no longer need those
        '''
        self.csvFile.pop(0)

        # print(self.csvFile[0].split(","))

        '''
            Set default date to current date.
        '''
        self.defaultDate = self.csvFile[0].split(",")[0]

        # print("Default Date: " + self.defaultDate)

        self.lineChart = []

        '''
            Create the empty dictionary for all the content in CSV file except currencies.
        '''
        self.dict = {}

        '''
            Populate the dictionary.
            Key: Date
            Value: List of all the exchange rate to that date 
        '''
        for arrays in self.csvFile:
            '''
                Get array of the whole CSV file and Split in chunks of array
                Each Element contains different: (date and exchange rate to that date) 
            '''
            arrays = arrays.split(",")
            '''
                Removes the empty last element.
            '''
            arrays.pop()
            '''
                Removes and return the date and store it as the key in the dictionary
                Rest of the list is store as the value to that key
            '''
            self.dict[arrays.pop(0)] = arrays

        # Add it to the Combo Box

        # Create Calender Widgets

        # Set the grid layout properly

        # -----------------------------------------------#

        ''' Grid Layout for the Application '''
        layout = QGridLayout()

        # Horizontal layout for Label and comboboxes
        hBox1 = QHBoxLayout()  # From Currency layout
        hBox2 = QHBoxLayout()  # To Currency layout
        hBox3 = QHBoxLayout()  # Amount to Convert (SpinBox) layout
        hBox4 = QHBoxLayout()  # Result layout

        # Add Calender to the Horizontal Layouts
        hBox5 = QHBoxLayout()  # Calender 1 layout
        hBox6 = QHBoxLayout()  # Calender 2 layout

        # Label for the ComboBox 1
        self.fromCurrencyLabel = QLabel("From Currency")
        self.fromCurrency = QComboBox()  # First ComboBox
        self.fromCurrency.setFixedWidth(150)  # Set the width to 150

        self.toCurrencyLabel = QLabel("To Currency")
        self.toCurrency = QComboBox()
        self.toCurrency.setFixedWidth(150)

        '''
            Add the stretch to the Horizontal layout, So that the Label and the ComboBox doesn't separate
            from each other
        '''
        hBox1.addStretch()
        hBox1.addWidget(self.fromCurrencyLabel)
        hBox1.addWidget(self.fromCurrency)

        hBox2.addStretch()
        hBox2.addWidget(self.toCurrencyLabel)
        hBox2.addWidget(self.toCurrency)

        '''
            Add the list of currency to the combobox
        '''
        self.fromCurrency.addItems(self.currencies)
        self.toCurrency.addItems(self.currencies)

        '''
            Set default currency to AUD
        '''
        self.fromCurrency.setCurrentText("AUD")
        self.toCurrency.setCurrentText("AUD")

        self.amtToConvertLabel = QLabel("Amount to Convert: ")
        self.amtToConvert = QDoubleSpinBox()
        self.amtToConvert.setFixedWidth(180)
        self.amtToConvert.setValue(1)
        self.amtToConvert.setMaximum(10000)

        hBox3.addStretch()
        hBox3.addWidget(self.amtToConvertLabel)
        hBox3.addWidget(self.amtToConvert)

        self.resultLabel = QLabel("Result of conversion based on most recent rates: ")
        self.result = QLabel("")

        hBox4.addWidget(self.resultLabel)
        hBox4.addWidget(self.result)

        '''
            Create the instance of the Calender
        '''
        self.from_date = QCalendarWidget()
        '''
            Set Default date of the first calender to 3 weeks behind
        '''
        self.from_date.setSelectedDate(self.from_date.selectedDate().toPyDate() + timedelta(-21))
        '''
            Set Maximum Date to current date
        '''
        self.from_date.setMaximumDate(date.today())
        hBox5.addWidget(self.from_date)

        self.to_date = QCalendarWidget()
        self.to_date.setMaximumDate(date.today())
        hBox6.addWidget(self.to_date)

        self.plots = pg.PlotWidget()
        self.plots.plotItem.setLabel("left", "Rates")
        self.plots.plotItem.setLabel("bottom", "Days")
        self.plots.plotItem.showGrid(True, True)

        self.p1 = None
        self.p2 = None

        self.legend = self.plots.plotItem.addLegend()

        '''
            Add all the widgets to the layouts
        '''
        layout.addLayout(hBox1, 0, 0)
        layout.addLayout(hBox2, 0, 1)
        layout.addLayout(hBox3, 1, 0)
        layout.addLayout(hBox4, 1, 1)
        layout.addLayout(hBox5, 2, 0)
        layout.addLayout(hBox6, 2, 1)
        layout.addWidget(self.plots, 3, 0, 3, 0)

        '''
            Add the eventHandler to the Calender, ComboBox and SpinBox
        '''
        self.from_date.clicked.connect(self.dateChanged)
        self.to_date.clicked.connect(self.dateChanged)
        self.fromCurrency.currentTextChanged.connect(self.comboBoxChange)
        self.toCurrency.currentTextChanged.connect(self.comboBoxChange)
        self.amtToConvert.valueChanged.connect(self.comboBoxChange)

        '''
            Add the layout to the window
        '''
        self.setLayout(layout)

        '''
            Set the Window Title
        '''
        self.setWindowTitle("Currency Converter - Assignment 1 - Manik Shakya - 2869290")
        self.show()

    '''
       This function is called when the Calender value is changed
       i.e. When date is changed 
    '''

    def dateChanged(self):
        # print(self.from_date.selectedDate().toPyDate().isoformat())
        # print(self.to_date.selectedDate().toPyDate().isoformat())

        '''
            Store the value of calender date in 'YYYY-MM-DD'
        '''
        cal1 = self.from_date.selectedDate().toPyDate()
        cal2 = self.to_date.selectedDate().toPyDate()

        '''
            Create the empty list to store the exchange rate of different days for the 
            duration from_date - to_date
        '''
        chart1 = []
        chart2 = []

        '''
            Loop through from_date till it reaches to_date
        '''

        # Overflow error needs to be fixed
        # if(cal1 < cal2)
        while (cal1.isoformat() != cal2.isoformat()):
            latestRate = self.dict.get(cal1.isoformat())

            ''' Check if the date is available in the CSV file '''
            if (latestRate != None):
                ''' Store the float values in the list. So that we don't have to convert them later. '''
                chart1.append(float(latestRate[self.fromCurrency.currentIndex()]))
                chart2.append(float(latestRate[self.toCurrency.currentIndex()]))

            ''' Increment the date by 1 '''
            cal1 += timedelta(1)

        print(chart1)
        print(chart2)

        '''
            Remove and Update the legend
        '''
        self.plots.plotItem.scene().removeItem(self.legend)
        # self.plots.removeItem(self.p1)
        # self.plots.removeItem(self.p2)
        #self.plots.plotItem.clear()

        '''
            Plot the graph When the Calender value is changed
        '''
        self.p1 = self.plots.plotItem.plot(y=chart1, pen="r", symbol="x",
                                           name=self.fromCurrency.currentText())
        self.p2 = self.plots.plotItem.plot(y=chart2, pen="g", symbol="o",
                                           name=self.toCurrency.currentText())
        self.legend = self.plots.plotItem.addLegend()

        self.plots.addItem(self.p1)
        self.plots.addItem(self.p2)

        #print(self.plots.getPlotItem())

    def comboBoxChange(self):
        sender = self.sender()

        ''' Get the Currency index to retrieve the exchange rates from the dictionary list '''
        fromCurrencyIndex = self.fromCurrency.currentIndex()
        toCurrencyIndex = self.toCurrency.currentIndex()

        ''' Get the value to convert '''
        amountToConvert = self.amtToConvert.value()

        # print(self.dict.get(self.defaultDate)[self.fromCurrency.currentIndex()])
        # print(self.amtToConvert.value())

        ''' Get the list Exchange rate for the latest date possible via the key. '''
        latestRate = self.dict.get(self.defaultDate)

        ''' Check if the date is available '''
        if (latestRate != None):
            ''' Retrieve the value with the index key. '''
            fromRate = latestRate[fromCurrencyIndex]
            toRate = latestRate[toCurrencyIndex]

            ''' 
                Check if the exchange rate value is not 'N/A'.

                isinstance(fromRate, float) and isinstance(toRate, float) can also be used as the condition
            '''
            if (fromRate != "N/A" and toRate != "N/A"):
                ''' Perform the require calculation necessary '''
                exRate = (float(amountToConvert) / float(fromRate)) * float(toRate)

                ''' Round up the result to 2 decimal place and display the result. '''
                self.result.setText(str(round(exRate, 2)))
            else:
                self.result.setText("N/A")
        self.currencies[self.fromCurrency.currentIndex()]
        self.toCurrency.currentIndex()


'''
    Class to Unzip the zip file from the URL.
'''


class Unzip(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.download_unzip()  # call method to test it

    def download_unzip(self):  # method is stand alone put 'self' in brackets when you are including in a class.
        self.data = {}  # empty data dictionary
        url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip'  # new data source
        self.file, _ = urlretrieve(url)
        zip_file_object = zipfile.ZipFile(self.file, 'r')
        first_file = zip_file_object.namelist()[0]
        self.file = zip_file_object.open(first_file)
        content = self.file.read()
        # print(content.decode("utf-8"))
        return content.decode("utf-8")


app = QApplication(sys.argv)
assignment = Assignment_1()

sys.exit(app.exec_())
