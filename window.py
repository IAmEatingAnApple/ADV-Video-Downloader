# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ADV(object):
    def setupUi(self, ADV):
        ADV.setObjectName("ADV")
        ADV.resize(379, 274)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ADV.sizePolicy().hasHeightForWidth())
        ADV.setSizePolicy(sizePolicy)
        ADV.setMinimumSize(QtCore.QSize(379, 274))
        ADV.setMaximumSize(QtCore.QSize(379, 274))
        self.pasteLinkButton = QtWidgets.QPushButton(ADV)
        self.pasteLinkButton.setGeometry(QtCore.QRect(10, 10, 61, 21))
        self.pasteLinkButton.setDefault(False)
        self.pasteLinkButton.setFlat(False)
        self.pasteLinkButton.setObjectName("pasteLinkButton")
        self.linkText = QtWidgets.QLabel(ADV)
        self.linkText.setGeometry(QtCore.QRect(80, 10, 291, 21))
        self.linkText.setText("")
        self.linkText.setObjectName("linkText")
        self.debugField = QtWidgets.QTextEdit(ADV)
        self.debugField.setGeometry(QtCore.QRect(10, 70, 361, 191))
        self.debugField.setReadOnly(True)
        self.debugField.setObjectName("debugField")
        self.progressBar = QtWidgets.QProgressBar(ADV)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(10, 40, 361, 16))
        self.progressBar.setMaximum(1)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")

        self.retranslateUi(ADV)
        QtCore.QMetaObject.connectSlotsByName(ADV)

    def retranslateUi(self, ADV):
        _translate = QtCore.QCoreApplication.translate
        ADV.setWindowTitle(_translate("ADV", "ADV Video Downloader"))
        self.pasteLinkButton.setText(_translate("ADV", "Paste link"))