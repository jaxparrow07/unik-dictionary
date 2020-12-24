#!/usr/bin/env python3

import sys
import requests
import json
import vlc
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QIcon



class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.TextInputlbl = QLabel('Search Query', self)
        self.TextInputlbl.move(300,40)

        self.Outputlbl = QLabel('Result:', self) 
        self.Outputlbl.move(10,110)

        self.Definition = QLabel('Definition - ', self) 
        self.Definition.setGeometry(10,140, 280, 30)

        self.Phonetics = QLabel('Phonetics -', self) 
        self.Phonetics.move(10,190)

        self.Example = QLabel('Example -', self) 
        self.Example.move(10,220)

        self.Synonmyms = QLabel('Synonmym - ', self)
        self.Synonmyms.move(10,270)

        self.about_lbl = QLabel('Made by Jaxparrow', self)
        self.about_lbl.setGeometry(460,350, 160, 30)

        btn1 = QPushButton("Search", self)
        btn1.move(410, 70)
        btn1.clicked.connect(self.buttonClicked)

        self.phonetics_speak = QPushButton('Speak', self)
        self.phonetics_speak.move(190,183)
        self.phonetics_speak.clicked.connect(self.start_speaking)


        self.searchtext = QLineEdit(self)
        self.searchtext.setGeometry(200, 70, 210, 32)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&App')
        fileMenu.addAction(exitAct)

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Unik Dictionary')
        self.show()

    def start_speaking(self):

        p = vlc.MediaPlayer(self.audio_link)
        p.play()



    def buttonClicked(self):

        self.audio_link = 'N_A'

        input = self.searchtext.text()
        print('Searching word : '+input)
        input = input.lower()
        response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/"+input)

        data = json.loads(response.text)

        finder = str(data)

        if finder.find('No Definitions Found') == -1:
            print('Found word : '+input)
            print('Showing Results!')
            print('')

            if finder.find('definition') != -1:
                def_val = data[0]["meanings"][0]["definitions"][0]["definition"]
            else:
                def_val = 'N/A'

            if finder.find('example') != -1:
                example_val = data[0]["meanings"][0]["definitions"][0]["example"]
            else:
                example_val = 'N/A'

            if finder.find('text') != -1:
                phonetics_val = data[0]["phonetics"][0]["text"]
                self.audio_link = data[0]["phonetics"][0]["audio"]
                self.phonetics_speak.setVisible(True)
            else:
                phonetics_val = 'N/A'
                self.audio_link = 'N_A'
                self.phonetics_speak.setVisible(False)

            if finder.find('synonyms') != -1:
                synonyms_val = data[0]["meanings"][0]["definitions"][0]["synonyms"][0]
            else:
                synonyms_val = 'N/A'
        else:
            print('Not Found  : '+input)
            print('')
            phonetics_val = 'N/A'
            def_val = 'N/A'
            example_val = 'N/A'
            synonyms_val = 'N/A'
            self.phonetics_speak.setVisible(False)


        self.Phonetics.setText('Phonetics - '+phonetics_val)
        self.Phonetics.adjustSize() 

        if len(def_val) > 80:
            N = 80
            def_val = def_val[ : N] + '\n' + def_val[N : ]
            self.Definition.setText('Definition - '+def_val)
        else:
            self.Definition.setText('Definition - '+def_val)

        self.Definition.adjustSize() 

        if len(example_val) > 80:
            N = 80
            example_val = example_val[ : N] + '\n' + example_val[N : ]
            self.Example.setText('Example - '+example_val)
        else:
            self.Example.setText('Example - '+example_val)

        self.Example.adjustSize()
        self.Synonmyms.setText('Synonmym - '+synonyms_val)


        self.Synonmyms.adjustSize()
        self.about_lbl.adjustSize()



def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()