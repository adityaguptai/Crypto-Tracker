import sys,json
from PyQt4 import QtGui,QtCore
from coinmarketcap import Market
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtCore import QUrl
import requests
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import datetime
import time

coinmarketcap = Market()

coins = coinmarketcap.ticker(limit=500)
limit=30
label=[]
Rank=[]
Name=[]
Market=[]
Price=[]
Volume=[]
Supply=[]
Change=[]
marketValue=[]
def clearLayout(self):
    while self.count():
        child = self.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
class crypto(QtGui.QWidget):
    def __init__(self):
        super(crypto, self).__init__()
        self.initUI()
        
    #Market Value Function
    def fetchMarketValue(self,symbol):
        return requests.get('https://api.cryptonator.com/api/full/'+symbol+'-usd')
    #To Display Graph    
    def nextPage(self,homeWindow,grid,grid1):
        print(self.sender().objectName())
        symbol=coins[int(self.sender().objectName())]["symbol"]
        print(symbol)
        if(symbol=='MIOTA'):
            symbol='IOTA'
        marketValue = self.fetchMarketValue(symbol)
        historicalData = requests.get('https://min-api.cryptocompare.com/data/histoday?fsym='+symbol+'&tsym=USD&limit=10000&aggregate=3&e=CCCAGG')

        print(marketValue.text)
        try:
            marketValue=json.loads(marketValue.text)["ticker"]
            historicalData=json.loads(historicalData.text)["Data"]
        except:
            print("DATA Not Available")
            error=QtGui.QLabel("Something went wrong!")
            error.setStyleSheet('color:Red;')
            grid1.addWidget(error,1,2,1,2,QtCore.Qt.AlignCenter)
        print("==================")
        #print(historicalData)
        #print(historicalData["time"])
        hist_time = []
        hist_time_readable = []
        hist_price_high = []
        for data in historicalData:
            x = data["time"]
            y = datetime.datetime.fromtimestamp(x).strftime('%x')
            hist_time.append(x)
            hist_time_readable.append(y)
            hist_price_high.append(data["high"])

        #print(hist_time,hist_price_high,hist_time_readable)

        
        central_widget = QtGui.QWidget()
        central_layout = QtGui.QGridLayout()
        figure = Figure(figsize=(70, 70), dpi=72, facecolor=(1, 1, 1), edgecolor=(1, 1, 1), tight_layout=True)
        axes = figure.add_subplot(111)
        axes.grid(b=True, which='both')
        axes.set_title('Historical Prices of '+symbol)
        axes.set_xlabel('Date')
        axes.set_ylabel('Price')
        axes.set_xticks(hist_time[::50])
        axes.set_xticklabels(hist_time_readable[::50])
        axes.plot(hist_time,hist_price_high)
        canvas = FigureCanvas(figure)
        toolbar = NavigationToolbar(canvas, central_widget)

        central_layout.addWidget(canvas,0,0)
        central_layout.addWidget(toolbar,1,0)
        central_layout.addWidget(central_widget,2,0,QtCore.Qt.AlignCenter)
        homeWindow.addLayout(central_layout,2,3,2,7,QtCore.Qt.AlignCenter)
        
        market=QtGui.QGridLayout()
        back=QtGui.QPushButton()
        back.setText("Home")
        clearLayout(grid1)
        clearLayout(grid)
        grid1.addWidget(back,0,0,QtCore.Qt.AlignLeft)
        back.clicked.connect(lambda:self.home(homeWindow))
        homeWindow.addLayout(market,4,2,10,8)
        Market=[]
        Price=[]
        Volume=[]
        Sr=[]
        label=[]
        myFont=QtGui.QFont()
        myFont.setBold(True)
        header=["Rank","Exchnage Name","Current Price(USD)","Trade Volume"]
        for i in range(4):
            label+=[QtGui.QPushButton(header[i])]
            label[i].setStyleSheet('color:black;border:1px solid black;font-family:roboto')
            label[i].setFont(myFont) 
            market.addWidget(label[i],0,i)
        i=1
            
        for markets in marketValue["markets"]:

            #print(str(markets["market"]),str(markets["price"]),str(markets["volume"]))
            Market+=[QtGui.QLabel(str(markets["market"]),self)]
            Price+=[QtGui.QLabel(str(markets["price"]),self)]
            Volume+=[QtGui.QLabel(str(markets["volume"]),self)]
            Sr+=[QtGui.QLabel(str(i),self)]
            
            Market[i-1].setStyleSheet('color:red;border:1px solid black;')
            Price[i-1].setStyleSheet('color:red;border:1px solid black;')
            Volume[i-1].setStyleSheet('color:red;border:1px solid black;')
            Sr[i-1].setStyleSheet('color:red;border:1px solid black;')

            Market[i-1].setAlignment(QtCore.Qt.AlignCenter)
            Price[i-1].setAlignment(QtCore.Qt.AlignCenter)
            Volume[i-1].setAlignment(QtCore.Qt.AlignCenter)
            Sr[i-1].setAlignment(QtCore.Qt.AlignCenter)

            market.addWidget(Sr[i-1],i,0)
            market.addWidget(Market[i-1],i,1)
            market.addWidget(Price[i-1],i,2)
            market.addWidget(Volume[i-1],i,3)
            
            i+=1
        if(len(marketValue["markets"])==0):
            Market=QtGui.QLabel("No Supplier Of this Currency",self)
            Market.setStyleSheet('color:red;border:1px solid black;')
            market.addWidget(Market,0,2)
        self.update()

    #Search Page    
    def search(self,homeWindow,grid,grid1,name):
        for i in range(len(coins)):
            if(coins[i]["name"].lower()==name.lower()):
                self.sender().setObjectName(str(i))
                return self.nextPage(homeWindow,grid,grid1)
            else:
                continue
        error=QtGui.QLabel("Not A Cryptocurrency Name Please Try Another Name")
        error.setStyleSheet('color:Red;')
        grid1.addWidget(error,1,3,1,2,QtCore.Qt.AlignCenter)

    #Home Function
    def home(self,homeWindow):
        clearLayout(homeWindow)
        self.ShowAll(homeWindow)

    #Applying Filter
    def setFilter(self,homeWindow):
        global limit
        limit=int(self.sender().currentText())
        self.home(homeWindow)
    #To open url in The Browser
    def openUrl(self,url):
        print(url)
        QDesktopServices.openUrl(QUrl(url))
    #To Display News  
    def news(self,newsLayout):
        clearLayout(newsLayout)
        news=requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
        print(news)
        news=json.loads(news.text)["Data"]
        newsLayout.setSpacing(0)
        i=0
        j=0
        title=[]
        content=[]
        source=[]
        url=[]
        news = news[:10]
        myFont=QtGui.QFont()
        myFont.setBold(True)
        for News in news:
            body_list = News["body"].split()[:25]
            title+=[QtGui.QLabel("Title : "+News["title"],self)]
            content+=[QtGui.QLabel("Content : "+" ".join(body_list)+"...[Read More click url below]",self)]
            source+=[QtGui.QLabel("Source : "+News["source"],self)]
            url+=[QtGui.QLabel(self)]
            Url='<a href='+"\""+str(News["url"])+"\""+'>'+"Link -> "+str(News["source"])+'</a>'
            print(Url)
            url[j].setText(Url)
            url[j].linkActivated.connect(self.openUrl)
            #content[j].setWordWrap(True)
            #content[j].
            url[j].setStyleSheet("margin-bottom:10px;text-decoration:None")

            title[j].setStyleSheet('color:black;border:1px solid black;margin:0;')
            title[j].setFont(myFont)
            content[j].setStyleSheet('color:green;margin:0;')
            source[j].setStyleSheet('color:blue;')
            
            newsLayout.addWidget(title[j],i,0,QtCore.Qt.AlignLeft)
            newsLayout.addWidget(content[j],i+2,0,QtCore.Qt.AlignLeft)
            newsLayout.addWidget(source[j],i+4,0,QtCore.Qt.AlignLeft)
            newsLayout.addWidget(url[j],i+6,0,QtCore.Qt.AlignLeft)
            i+=8
            j+=1
    #To Show Details between 2 Crypto Currencies
    def Compare(self,grid,name1,name2):
        print(name1,name2)
        clearLayout(grid)
        left=QtGui.QVBoxLayout()
        right=QtGui.QVBoxLayout()
        symbol1=""
        symbol2=""
        index1=0
        index2=0
        for i in range(len(coins)):
            if(coins[i]["name"].lower()==name1.lower()):
                symbol1=coins[i]["symbol"]
                index1=i
            if(coins[i]["name"].lower()==name2.lower()):
                symbol2=coins[i]["symbol"]
                index2=i
            else:
                continue
        
        title1=QtGui.QLabel(symbol1,self)
        title2=QtGui.QLabel(symbol2,self)
        name1=QtGui.QLabel(coins[index1]["name"],self)
        rank1=QtGui.QLabel("Current Ranking : "+coins[index1]["rank"],self)
        price1=QtGui.QLabel("Current Price : "+coins[index1]["price_usd"]+"$",self)
        change1=QtGui.QLabel("Change in 24hrs : "+coins[index1]["percent_change_24h"]+" %",self)
        marketCap1=QtGui.QLabel("Current MarketCap : "+coins[index1]["market_cap_usd"]+"$",self)
        name2=QtGui.QLabel(coins[index2]["name"],self)
        rank2=QtGui.QLabel("Current Ranking : "+coins[index2]["rank"],self)
        change2=QtGui.QLabel("Change in 24hrs : "+coins[index2]["percent_change_24h"]+" %",self)
        price2=QtGui.QLabel("Current Price : "+coins[index2]["price_usd"]+"$",self)
        marketCap2=QtGui.QLabel("Current MarketCap : "+coins[index2]["market_cap_usd"]+"$",self)
        
        #left.setSpacing(0)
        #right.setSpacing(0)
        #left.setStretch(0,0)
        #right.setStretch(0,0)

        #left.setStyleSheet('border:2px solid black')
        #right.setStyleSheet('border:2px solid black')
        
        left.addWidget(title1)
        left.addWidget(name1)
        left.addWidget(rank1)
        left.addWidget(price1)
        left.addWidget(change1)
        left.addWidget(marketCap1)
        right.addWidget(title2)
        right.addWidget(name2)
        right.addWidget(rank2)
        right.addWidget(price2)
        right.addWidget(change2)
        right.addWidget(marketCap2)
        left.insertSpacing(6,500)
        right.insertSpacing(6,500)

        grid.addLayout(left,0,0,QtCore.Qt.AlignCenter)
        grid.addLayout(right,0,1,QtCore.Qt.AlignCenter)
    
    #Display Compare Page    
    def compare(self,grid):
        clearLayout(grid)
        form=QtGui.QFormLayout()
        x=[]
        for i in range(40):
            x+=[coins[i]['name']]
        x.sort()
        left_search = QtGui.QComboBox()
        right_search= QtGui.QComboBox()
        left_search.addItems(x[1:])
        right_search.addItems(x[1:])
        left_search.setCurrentIndex(0)
        right_search.setCurrentIndex(0)
        com_button = QtGui.QPushButton("Click To Compare")

        left_search.setStyleSheet('max-width:250px;')
        right_search.setStyleSheet('max-width:250px;')
        com_button.setStyleSheet('max-width:250px;')
        com_button.clicked.connect(lambda:self.Compare(grid,left_search.currentText(),right_search.currentText()))

        form.setFormAlignment(QtCore.Qt.AlignCenter)
        form.addRow(left_search)
        form.addRow(right_search)
        form.addRow(com_button)
        
        grid.addLayout(form,0,0)

    #open mainpage0    
    def ShowAll(self,homeWindow):
        global label,Rank,Name,Market,Price,Volume,Supply,Change,limit
        label=[]
        Rank=[]
        Name=[]
        Market=[]
        Price=[]
        Volume=[]
        Supply=[]
        Change=[]
        grid1 = QtGui.QGridLayout()
        grid1.setSpacing(0)
        Filter=QtGui.QComboBox()
        Filter.addItems(['10','20','30','40'])
        Filter.setCurrentIndex(int(limit)/10-1)
        Filter.currentIndexChanged.connect(lambda:self.setFilter(homeWindow))
        grid1.addWidget(Filter,1,2,QtCore.Qt.AlignLeft)
        grid = QtGui.QGridLayout()
        grid.setSpacing(0)
        header=["Rank","Name","Market Cap","Price(USD)","Volume","Supply","Change"];
        myFont=QtGui.QFont()
        myFont.setBold(True)
        homeWindowText=QtGui.QLabel("Crypto Tracker",self)
        homeWindowText.setStyleSheet('font-size:100px;font-family:roboto;')

        #Search Bar
        x=[]
        for i in range(100):
            x+=[coins[i]['name']]
        x.sort()
        input_line = QtGui.QComboBox()
        input_line.addItems(x[1:])
        search_button=QtGui.QPushButton("Search")
        search_button.clicked.connect(lambda:self.search(homeWindow,grid,grid1,input_line.currentText()))

        #refresh

        refresh_button=QtGui.QPushButton("Home")
        refresh_button.clicked.connect(lambda:self.home(homeWindow))
        
        #news

        news_button=QtGui.QPushButton("News")
        news_button.clicked.connect(lambda:self.news(grid))

        #compare
        
        compare_button=QtGui.QPushButton("Compare")
        compare_button.clicked.connect(lambda:self.compare(grid))
    
        #Layouts

        grid1.addWidget(refresh_button,1,7)
        grid1.addWidget(input_line,1,4,1,2)
        grid1.addWidget(search_button,1,6)
        grid1.addWidget(news_button,1,8)
        grid1.addWidget(compare_button,1,9)
        
        grid1.addWidget(homeWindowText,0,2,QtCore.Qt.AlignCenter)
        homeWindow.addLayout(grid1,0,1,2,7,QtCore.Qt.AlignCenter)
        
        
    # self.label.setFont(myFont)
        for i in range(7):
            label+=[QtGui.QPushButton(header[i])]
            label[i].setStyleSheet('color:black;border:1px solid black;font-family:roboto;margin:0;')
            label[i].setFont(myFont) 
            grid.addWidget(label[i], 3,i)

        for i in range(1,limit+1):
            Rank+=[QtGui.QPushButton(coins[i-1]['rank'])]
            Name+=[QtGui.QPushButton(coins[i-1]['name'])]
            Market+=[QtGui.QPushButton(coins[i-1]['market_cap_usd'])]
            Price+=[QtGui.QPushButton(coins[i-1]['price_usd'])]
            Volume+=[QtGui.QPushButton(coins[i-1]['24h_volume_usd'])]
            Supply+=[QtGui.QPushButton(coins[i-1]['total_supply'])]
            Change+=[QtGui.QPushButton(coins[i-1]['percent_change_24h'])]

            Rank[i-1].setStyleSheet('color:#353b48;border:1px solid black;margin:0;')
            Name[i-1].setStyleSheet('color:#3867d6;border:1px solid black;margin:0;')
            Market[i-1].setStyleSheet('color:#353b48;border:1px solid black;margin:0;')
            Price[i-1].setStyleSheet('color:#353b48;border:1px solid black;margin:0;')
            Volume[i-1].setStyleSheet('color:#353b48;border:1px solid black;margin:0;')
            Supply[i-1].setStyleSheet('color:#353b48;border:1px solid black;margin:0;')
            Change[i-1].setStyleSheet('color:#e84118;border:1px solid black;margin:0;')
            if(coins[i-1]["percent_change_24h"][0]!='-'):
                Change[i-1].setStyleSheet('color:green;border:1px solid black;margin:0;')
            Name[i-1].setObjectName(str(i-1))
            Market[i-1].setObjectName(str(i-1))
            Price[i-1].setObjectName(str(i-1))
            Volume[i-1].setObjectName(str(i-1))
            Supply[i-1].setObjectName(str(i-1))
            Change[i-1].setObjectName(str(i-1))
            Rank[i-1].setObjectName(str(i-1))
            
            Rank[i-1].clicked.connect(lambda:self.nextPage(homeWindow,grid,grid1))
            Name[i-1].clicked.connect(lambda:self.nextPage(homeWindow,grid,grid1))
            Market[i-1].clicked.connect(lambda:self.nextPage(homeWindow,grid,grid1))
            Price[i-1].clicked.connect(lambda:self.nextPage(homeWindow,grid,grid1))
            Volume[i-1].clicked.connect(lambda:self.nextPage(homeWindow,grid,grid1))
            Supply[i-1].clicked.connect(lambda:self.nextPage(homeWindow,grid,grid1))
            Change[i-1].clicked.connect(lambda:self.nextPage(homeWindow,grid,grid1))

            grid.addWidget(Rank[i-1], i+3,0)
            grid.addWidget(Name[i-1], i+3,1)
            grid.addWidget(Market[i-1], i+3,2)
            grid.addWidget(Price[i-1], i+3,3)
            grid.addWidget(Volume[i-1], i+3,4)
            grid.addWidget(Supply[i-1], i+3,5)
            grid.addWidget(Change[i-1], i+3,6)
            
        homeWindow.addLayout(grid,2,0,1000,8)    
        
    def initUI(self):
        self.setGeometry(100, 100, 700, 500)
        self.setWindowTitle('Crypto Tracker')
        self.w = QtGui.QWidget(self)
        palette = self.w.palette()
        role = self.w.backgroundRole()
        #42b0f4
        #d1d8e0
        palette.setColor(role, QtGui.QColor('#d1d8e0'))
        self.setPalette(palette)
        img=QtGui.QPixmap('img.png')
        homeWindow=QtGui.QGridLayout()  
        homeWindow.setSpacing(0)
        self.setLayout(homeWindow)
        self.ShowAll(homeWindow)       
        self.show()
        
def main():
    
        app = QtGui.QApplication(sys.argv)
        window = crypto()
        app.exec_()
    
try:
    if __name__ == '__main__':
        main()
except:
        print("Something went wrong")

