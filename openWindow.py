## Ex 3-1. 창 띄우기.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QToolTip, QMainWindow, QAction, qApp
from PyQt5.QtCore import QCoreApplication           # PyQt 애플리케이션의 핵심 제어 객체를 나타냄. 이벤트 루프 관리, 기본 설정 등을 담당
from PyQt5.QtGui import QIcon,QFont


class MyApp(QMainWindow):  # MyApp 클래스는 QMainWindow 클래스를 상속받음. QMainWindow는 PyQt5에서 제공하는 기본 창 클래스

    # MyApp 클래스의 생성자. MyApp객체가 생성될 때 가장 먼저 호출되는 Method임
    def __init__(self):
        # super().__init__()는 부모 클래스의 생성자를 호출하는 코드
        super().__init__()
        self.initUI() # -> 실제 UI Interface의 설정작업이 이루어짐
    
    def initUI(self):
        # QAction : Action을 생성하는 클래스(메뉴,툴바,단축키)
        exitAction = QAction(QIcon(r'C:\Users\bichn\OneDrive\문서\github\googleCloud\exit.png'), 'Exit', self) 
        exitAction.setShortcut('Ctrl+Q')
        # exitAction버튼에 Mouse on시 상태바에 'Exit application'이라고 표시
        exitAction.setStatusTip('Exit application')  
        exitAction.triggered.connect(qApp.quit)

        # QMainWindow가 제공하는 메써드로 창 하단 StatusBar를 생성하고 반환
        # exitAction.setStatusTip('Exit application')에서 설정한 팁 메시지는 이 상태바에 표시됨
        self.statusBar()

        # MenuBar밑에 툴바를 생성. 'Exit'는 툴바의 이름으로 툴바가 여러개 있을 때 구분하거나 r-mouse클릭 시 나타나는 콘텍스트 메뉴에 표시됨
        self.toolbar = self.addToolBar('Exit')  # QMainWindow가 제공하는 메써드로 툴바를 생성하고 반환

        # 툴바에 exitAction을 추가하여 'Exit'라는 버튼을 생성
        self.toolbar.addAction(exitAction) 







        # 창 상단에 MenuBar를 생성하고 반환
        menubar = self.menuBar()
        # macOS에서처럼 화면의 MenuBar를 전체 Main상단의 MenuBar로 사용하지 않도록 설정
        menubar.setNativeMenuBar(False)
        # 생성된 MenuBar에 'File'이라는 이름의 메뉴를 추가. $기호는 단축키를 사용할 수 있또록 설정하는 기능
        filemenu = menubar.addMenu('&File')
        # filemenu에 exitAction을 추가하여 'Exit'라는 메뉴 항목을 생성
        filemenu.addAction(exitAction)
       
        self.statusBar().showMessage('Ready')  
        # QPushButton 객체를 생성. 'Quit'라는 텍스트가 있는 버튼을 생성하고, self(현재 MyApp 인스턴스)를 부모로 설정
        btn = QPushButton('Quit', self)                             # self의 부모는 MyApp 인스턴스이므로 이 버튼은 MyApp 창 안에 위치하게 됨
        btn.move(330,50)
        btn.resize(btn.sizeHint())                                  #  예를 들어 'Quit' 텍스트가 잘리지 않고 적절하게 보일 만한 너비와 높이를 계산해 줌
        btn.clicked.connect(QCoreApplication.instance().quit)       # .quit : btn버튼이 클릭되면 application을 종료하는 메서드. Qt.instance()는 현재 실행 중인 QApplication 인스턴스를 반환
        btn.setText('종료')
        btn.setToolTip('종료 버튼을 누르면 프로그램이 종료됩니다')        # btn에 툴팁 설정
        
        QToolTip.setFont(QFont('SansSerif',10))                     # font를 설정
        self.setToolTip('This is a <b>QWidget</b> widget')          # 창 전체에 툴팁을 설정

        self.setWindowTitle('My First Application')
        self.setWindowIcon(QIcon(r'C:\Users\bichn\OneDrive\문서\github\googleCloud\web.png'))
        self.setGeometry(300, 300, 500, 1000)
        # self.move(300, 300)
        # self.resize(400, 200)
        self.show()

# if __name__ == '__main__': 스크립트 파일로 직접 실행될때만 아래의 코드블록을 실행하도록 함(다른 파일에서 import될 때는 실행되지 않음)
if __name__ == '__main__':
   app = QApplication(sys.argv)     # PyQt5의 필수 객체.모든 PyQt5 애플리케이션은 반드시 QApplication 인스턴스를 생성해야 함
    # sys.argv : sys.argv는 명령행 인자. PyQt5 애플리케이션에 전달된 인자를 처리하기 위해 사용됨                                  
   ex = MyApp()                     # 
   sys.exit(app.exec_())
    # app.exec_(): PyQt5 애플리케이션의 **이벤트 루프(event loop)**를 시작합니다. 
    # 이벤트 루프는 사용자의 입력(마우스 클릭, 키보드 입력 등)이나 시스템 이벤트(창 최소화, 최대화 등)를 감지하고, 
    # 해당 이벤트에 연결된 코드를 실행하도록 대기하는 무한 루프입니다. 이 메서드가 없으면 창이 바로 떴다가 꺼집니다.

    # sys.exit(): 이벤트 루프가 종료될 때 (예: 사용자가 창을 닫을 때) 반환되는 종료 코드를 운영체제에 전달하며 프로그램을 종료합니다. 
    # 이는 프로그램이 정상적으로 종료되었음을 알리는 역할을 합니다.

