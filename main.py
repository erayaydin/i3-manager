import sys
import os
from shutil import copyfile
import json

from PyQt4 import QtGui
from PyQt4 import QtCore

from UI.main import Ui_MainWindow

homePath = os.path.expanduser('~')
try:
    appPath = os.path.dirname(os.path.abspath(__file__))
except NameError:
    appPath = os.path.dirname(os.path.abspath(sys.argv[0]))

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(os.path.join(appPath, 'assets', 'images', 'icon.jpg')))

        self.apps = []
        self.workspaces = []
        self.keyboards = []
        self.modes = {}

        self.initConfig()
        self.prepareUi()
        self.listenButtons()

        self.show()

    def initConfig(self):
        self.configFolder = os.path.join(homePath, '.config', 'i3-manager')
        if not os.path.exists(self.configFolder):
            os.makedirs(self.configFolder)

        if not os.path.exists(os.path.join(self.configFolder, 'config.json')):
            copyfile(os.path.join(appPath, 'stubs', 'config.json'), os.path.join(self.configFolder, 'config.json'))

        self.readConfig()

    def readConfig(self):
        with open(os.path.join(self.configFolder, 'config.json')) as data:
            self.config = json.load(data)
        for workspace in self.config['workspaces']:
            self.workspaces.append(workspace)
        for app in self.config['app']:
            self.apps.append({
                "command": app['command'],
                "class": app['class'],
                "hotkey": app['hotkey'],
                "workspace": app['workspace'],
                "floating": app['floating'],
                "move": app['move']
            })
        for hotkey in self.config['hotkey']:
            self.keyboards.append({
                "key": hotkey['key'],
                "action": hotkey['action']
            })
        for modeKey in self.config['mode']:
            self.modes[modeKey] = {}

    def listenButtons(self):
        self.ui.btnInsertWorkspace.clicked.connect(self.insertWorkspace)
        self.ui.pushButton_5.clicked.connect(self.insertApp)
        self.ui.btnKeyboardInsert.clicked.connect(self.insertKeyboard)

    def insertWorkspace(self):
        name = self.ui.workspaceName.text()
        self.workspaces.append(name)
        self.refreshWorkspaces()
        self.refreshAppWorkspace()

    def insertApp(self):
        command = self.ui.appName.text()
        appClass = self.ui.appClass.text()
        hotkey = self.ui.appHotkey.text()
        if self.ui.appWorkspace.currentIndex() == 0:
            workspace = None
        else:
            workspace = self.ui.appWorkspace.currentIndex()
        if self.ui.appFloating.currentIndex() == 0:
            floating = None
        elif self.ui.appFloating.currentIndex() == 1:
            floating = "enable"
        else:
            floating = "disable"
        if self.ui.appMove.currentIndex() == 0:
            move = None
        else:
            move = "center"
        self.apps.append({
            "command": command,
            "class": appClass,
            "hotkey": hotkey,
            "workspace": workspace,
            "floating": floating,
            "move": move
        })
        self.refreshApps()

    def insertKeyboard(self):
        hotkey = self.ui.keyboardHotkey.text()
        action = self.ui.keyboardAction.text()
        self.keyboards.append({
            "key": hotkey,
            "action": action
        })
        self.refreshKeyboards()

    def prepareUi(self):
        self.readModifierKey()
        self.readFloatingKey()
        self.readOrientation()
        self.readWorkspaceLayout()
        self.readBorders()
        self.readWindowDecoration()
        self.readBar()
        self.refreshWorkspaces()
        self.refreshAppWorkspace()
        self.refreshApps()
        self.refreshKeyboards()
        self.refreshModes()
        self.readStartup()

    def readModifierKey(self):
        if self.config['modKey'] == 'Mod1':
            self.ui.modKey.setCurrentIndex(0)
        elif self.config['modKey'] == 'Mod4':
            self.ui.modKey.setCurrentIndex(1)
        elif self.config['modKey'] == 'CTRL':
            self.ui.modKey.setCurrentIndex(2)
        elif self.config['modKey'] == 'Shift':
            self.ui.modKey.setCurrentIndex(3)

    def readFloatingKey(self):
        if self.config['floatingKey'] == 'Mod1':
            self.ui.floatingKey.setCurrentIndex(0)
        elif self.config['floatingKey'] == 'Mod4':
            self.ui.floatingKey.setCurrentIndex(1)
        elif self.config['floatingKey'] == 'CTRL':
            self.ui.floatingKey.setCurrentIndex(2)
        elif self.config['floatingKey'] == 'Shift':
            self.ui.floatingKey.setCurrentIndex(3)

    def readOrientation(self):
        if self.config['orientation'] == 'auto':
            self.ui.orientation.setCurrentIndex(2)
        elif self.config['orientation'] == 'horizontal':
            self.ui.orientation.setCurrentIndex(0)
        elif self.config['orientation'] == 'vertical':
            self.ui.orientation.setCurrentIndex(1)

    def readWorkspaceLayout(self):
        if self.config['workspaceLayout'] == 'default':
            self.ui.workspaceLayout.setCurrentIndex(0)
        elif self.config['workspaceLayout'] == 'stacking':
            self.ui.workspaceLayout.setCurrentIndex(2)
        elif self.config['workspaceLayout'] == 'tabbed':
            self.ui.workspaceLayout.setCurrentIndex(1)

    def readBorders(self):
        if self.config['borders'] == 'none':
            self.ui.borders.setCurrentIndex(0)
        elif self.config['borders'] == 'vertical':
            self.ui.borders.setCurrentIndex(1)
        elif self.config['borders'] == 'horizontal':
            self.ui.borders.setCurrentIndex(2)
        elif self.config['borders'] == 'both':
            self.ui.borders.setCurrentIndex(3)
        elif self.config['borders'] == 'smart':
            self.ui.borders.setCurrentIndex(4)

    def readWindowDecoration(self):
        window = self.config['theme']['window']

        focused = window['focused']
        self.ui.windowFocusBorder.setText(focused['border'])
        self.ui.windowFocusBackground.setText(focused['background'])
        self.ui.windowFocusText.setText(focused['text'])
        self.ui.windowFocusIndicator.setText(focused['indicator'])

        unfocused = window['unfocused']
        self.ui.windowUnfocusBorder.setText(unfocused['border'])
        self.ui.windowUnfocusBackground.setText(unfocused['background'])
        self.ui.windowUnfocusText.setText(unfocused['text'])
        self.ui.windowUnfocusIndicator.setText(unfocused['indicator'])

        inactive = window['inactive']
        self.ui.windowInactiveBorder.setText(inactive['border'])
        self.ui.windowInactiveBackground.setText(inactive['background'])
        self.ui.windowInactiveText.setText(inactive['text'])
        self.ui.windowInactiveIndicator.setText(inactive['indicator'])

        urgent = window['urgent']
        self.ui.windowUrgentBorder.setText(urgent['border'])
        self.ui.windowUrgentBackground.setText(urgent['background'])
        self.ui.windowUrgentText.setText(urgent['text'])
        self.ui.windowUrgentIndicator.setText(urgent['indicator'])

    def readBar(self):
        bar = self.config['theme']['bar']
        self.ui.barBackground.setText(bar['background'])
        self.ui.barSeparator.setText(bar['separator'])
        self.ui.barStatus.setText(bar['status'])

        focused = bar['focused']
        self.ui.barFocusBorder.setText(focused['border'])
        self.ui.barFocusBackground.setText(focused['background'])
        self.ui.barFocusText.setText(focused['text'])

        active = bar['active']
        self.ui.barActiveBorder.setText(active['border'])
        self.ui.barActiveBackground.setText(active['background'])
        self.ui.barActiveText.setText(active['text'])

        inactive = bar['inactive']
        self.ui.barInactiveBorder.setText(inactive['border'])
        self.ui.barInactiveBackground.setText(inactive['background'])
        self.ui.barInactiveText.setText(inactive['text'])

        urgent = bar['urgent']
        self.ui.barUrgentBorder.setText(urgent['border'])
        self.ui.barUrgentBackground.setText(urgent['background'])
        self.ui.barUrgentText.setText(urgent['text'])

        mode = bar['mode']
        self.ui.barModeBorder.setText(mode['border'])
        self.ui.barModeBackground.setText(mode['background'])
        self.ui.barModeText.setText(mode['text'])

    def refreshWorkspaces(self):
        table = self.ui.workspacesTable
        table.setRowCount(0)
        row = 0
        for workspace in self.workspaces:
            table.insertRow(row)
            table.setItem(row, 0, QtGui.QTableWidgetItem(workspace))
            removeBtn = QtGui.QPushButton(table)
            removeBtn.setText('Remove')
            table.setCellWidget(row, 1, removeBtn)
            row+=1

    def refreshAppWorkspace(self):
        workspacesCombo = self.ui.appWorkspace
        workspacesCombo.clear()
        workspacesCombo.addItem("None Workspace")
        for workspace in self.workspaces:
            workspacesCombo.addItem(workspace)

    def refreshApps(self):
        table = self.ui.appsTable
        table.setRowCount(0)
        row = 0
        for app in self.apps:
            table.insertRow(row)
            table.setItem(row, 0, QtGui.QTableWidgetItem(app['command']))
            table.setItem(row, 1, QtGui.QTableWidgetItem(app['class']))
            table.setItem(row, 2, QtGui.QTableWidgetItem(app['hotkey']))

            # Workspaces Cell
            workspacesCombo = QtGui.QComboBox()
            workspacesTableModel = self.ui.workspacesTable.model()
            workspacesCombo.addItem("None Workspace")
            for workspaceRow in range(workspacesTableModel.rowCount()):
                workspacesCombo.addItem(self.ui.workspacesTable.model().index(workspaceRow, 0).data())
            if app['workspace']:
                workspacesCombo.setCurrentIndex(app['workspace'])
            else:
                workspacesCombo.setCurrentIndex(0)
            table.setCellWidget(row, 3, workspacesCombo)

            # Floating Cell
            floatingCombo = QtGui.QComboBox()
            floatingCombo.addItem("No Force")
            floatingCombo.addItem("Force Enable")
            floatingCombo.addItem("Force Disable")
            if(app['floating'] == 'enable'):
                floatingCombo.setCurrentIndex(1)
            elif(app['floating'] == 'disable'):
                floatingCombo.setCurrentIndex(2)
            else:
                floatingCombo.setCurrentIndex(0)
            table.setCellWidget(row, 4, floatingCombo)

            # Move Cell
            moveCombo = QtGui.QComboBox()
            moveCombo.addItem("No Force")
            moveCombo.addItem("Move Center")
            if (app['move'] == 'center'):
                moveCombo.setCurrentIndex(1)
            else:
                moveCombo.setCurrentIndex(0)
            table.setCellWidget(row, 5, moveCombo)

            # Remove Cell
            removeBtn = QtGui.QPushButton(table)
            removeBtn.setText('Remove')
            table.setCellWidget(row, 6, removeBtn)
            row+=1

    def refreshKeyboards(self):
        table = self.ui.keyboardTable
        table.setRowCount(0)
        row = 0
        for hotkey in self.keyboards:
            table.insertRow(row)
            table.setItem(row, 0, QtGui.QTableWidgetItem(hotkey['key']))
            table.setItem(row, 1, QtGui.QTableWidgetItem(hotkey['action']))
            removeBtn = QtGui.QPushButton(table)
            removeBtn.setText('Remove')
            table.setCellWidget(row, 2, removeBtn)
            row += 1

    def readStartup(self):
        table = self.ui.startupTable
        row = 0
        for startup in self.config['startup']:
            table.insertRow(row)
            table.setItem(row, 0, QtGui.QTableWidgetItem(startup))
            removeBtn = QtGui.QPushButton(table)
            removeBtn.setText('Remove')
            table.setCellWidget(row, 1, removeBtn)
            row += 1

    def refreshModes(self):
        tabs = self.ui.modesTab
        tabs.clear()
        for modeKey in self.modes:
            tabContent = QtGui.QWidget()
            modeKeyboardTable = QtGui.QTableWidget(tabContent)
            modeKeyboardTable.setGeometry(QtCore.QRect(10, 10, 700, 350))
            modeKeyboardTable.setObjectName("mode"+modeKey+"KeyboardTable")
            modeKeyboardTable.setColumnCount(3)
            modeKeyboardTable.setRowCount(0)
            item = QtGui.QTableWidgetItem("Hotkey")
            modeKeyboardTable.setHorizontalHeaderItem(0, item)
            item = QtGui.QTableWidgetItem("Action")
            modeKeyboardTable.setHorizontalHeaderItem(1, item)
            item = QtGui.QTableWidgetItem("Remove")
            modeKeyboardTable.setHorizontalHeaderItem(2, item)

            table = modeKeyboardTable
            row = 0
            for modeHotkey in self.config['mode'][modeKey]:
                table.insertRow(row)
                table.setItem(row, 0, QtGui.QTableWidgetItem(modeHotkey['key']))
                table.setItem(row, 1, QtGui.QTableWidgetItem(modeHotkey['action']))
                removeBtn = QtGui.QPushButton(table)
                removeBtn.setText('Remove')
                table.setCellWidget(row, 2, removeBtn)
                row += 1

            modeFormLayoutWidget1 = QtGui.QWidget(tabContent)
            modeFormLayoutWidget1.setGeometry(QtCore.QRect(10, 370, 211, 22))
            modeFormLayoutWidget1.setObjectName("mode"+modeKey+"FormLayoutWidget1")
            modeFormLayout1 = QtGui.QFormLayout(modeFormLayoutWidget1)
            modeFormLayout1.setMargin(0)
            modeFormLayout1.setObjectName("mode"+modeKey+"FormLayout1")
            modeFormLabel = QtGui.QLabel(modeFormLayoutWidget1)
            modeFormLabel.setText("Hotkey")
            modeFormLayout1.setWidget(0, QtGui.QFormLayout.LabelRole, modeFormLabel)
            keyboardHotkey = QtGui.QLineEdit(modeFormLayoutWidget1)
            keyboardHotkey.setObjectName("mode"+modeKey+"keyboardHotkey")
            modeFormLayout1.setWidget(0, QtGui.QFormLayout.FieldRole, keyboardHotkey)
            modeFormLayoutWidget2 = QtGui.QWidget(tabContent)
            modeFormLayoutWidget2.setGeometry(QtCore.QRect(230, 370, 421, 22))
            modeFormLayout2 = QtGui.QFormLayout(modeFormLayoutWidget2)
            modeFormLayout2.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
            modeFormLayout2.setMargin(0)
            keyboardAction = QtGui.QLineEdit(modeFormLayoutWidget2)
            keyboardAction.setObjectName("mode"+modeKey+"keyboardAction")
            modeFormLayout2.setWidget(0, QtGui.QFormLayout.FieldRole, keyboardAction)
            modeFormLabel2 = QtGui.QLabel(modeFormLayoutWidget2)
            modeFormLabel2.setText("Action")
            modeFormLayout2.setWidget(0, QtGui.QFormLayout.LabelRole, modeFormLabel2)
            btnKeyboardInsert = QtGui.QPushButton(tabContent)
            btnKeyboardInsert.setGeometry(QtCore.QRect(660, 370, 55, 21))
            btnKeyboardInsert.setText("Insert")
            tabs.addTab(tabContent, modeKey)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    i3manager = MainWindow()
    i3manager.show()
    sys.exit(app.exec_())