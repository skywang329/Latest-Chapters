from tkinter import *
from tkinter.ttk import *
from lxml import html
import requests
import webbrowser
from tkinter.font import Font

class LatestChapters(Frame):

    series = []
    times = []
    links = []
    newChapters = []
    currentSourceSelection = 0#change this to change starting source; index corresponds to item in sourcesNames
    sourcesNames = ('Mangafox', 'Mangalife');
    sourcesURL = {"Mangafox":"http://mangafox.me/", "Mangalife":"http://mangalife.us/"}
    firstInit = True
  
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.refresh()
        self.initUI()
        self.firstInit = False
        
    def initUI(self):
        #MainUI
        self.parent.title("Latest Chapters")
        self.style = Style()
        #self.style.theme_use("default")
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=BOTH)
        self.tree = Treeview(self, yscrollcommand=self.scrollbar.set)
        self.tree['columns'] = ('Link', 'newChapters', 'timeUpdated')
        self.tree.heading('#0', text='Series')
        self.tree.column("#0", minwidth=0, width=200)
        self.tree.heading('#1', text='Link')
        #column 1, links, is invis
        self.tree.heading('#2', text='newChapters')
        self.tree.column("#2", minwidth=0, width=100)
        self.tree.heading('#3', text='timeUpdated')
        self.tree.column("#3", minwidth=0, width=100)
        num = 0
        for oneSeries in range(0, len(self.series)):
            newChapterIDs = ''
            while num < len(self.newChapters) and self.series[oneSeries] in self.newChapters[num]:
                newChapterIDs += self.newChapters[num].replace(self.series[oneSeries], '')
                num += 1
            newChapterIDs = newChapterIDs.lstrip()
            self.tree.insert('', 'end', text=self.series[oneSeries], values=(self.links[oneSeries], newChapterIDs, self.times[oneSeries]))
        self.tree.bind('<Double-Button-1>' , self.moreInfo)
        self.tree["displaycolumns"]=('newChapters', 'timeUpdated')
        self.tree.pack(side=TOP, fill=BOTH, expand=True)
        self.scrollbar.config(command=self.tree.yview)
        #Ending buttons
        self.closeButton = Button(self, text="Close", command=self.master.destroy)
        self.closeButton.pack(side=RIGHT, padx=5, pady=5)
        self.refreshButton = Button(self, text="Refresh Now", command=self.refresh)
        self.refreshButton.pack(side=RIGHT, padx=5, pady=5)
        self.sourceSelection_value = StringVar()
        self.sourceSelection = Combobox(self, textvariable=self.sourceSelection_value)
        self.sourceSelection['values'] = self.sourcesNames
        self.sourceSelection.current(self.currentSourceSelection)
        self.sourceSelection.bind("<<ComboboxSelected>>", self.changeSource)
        self.sourceSelection.pack(side=RIGHT, padx=5, pady=5)
        self.pack(fill=BOTH, expand=True)

    def refresh(self):
        if self.firstInit != True:
            webscraper = Scraper(self.sourcesURL[self.sourceSelection.get()])
        else:
            webscraper = Scraper(self.sourcesURL[self.sourcesNames[self.currentSourceSelection]])
        self.series = webscraper.series
        self.times = webscraper.times
        self.links = webscraper.links
        self.newChapters = webscraper.newChapters
        if self.firstInit != True:
            if self.tree.winfo_exists() == 1:
                self.tree.destroy()
                self.scrollbar.destroy()
                self.closeButton.destroy()
                self.refreshButton.destroy()
                self.currentSourceSelection = self.sourceSelection.current()
                self.sourceSelection.destroy()
                self.initUI()

    def openLink(self, event):
        webbrowser.open(self.tree.item(self.tree.focus()).get('values')[0])

    def openLink(self):
        webbrowser.open(self.tree.item(self.tree.focus()).get('values')[0])

    def changeSource(self, event):
        #self.sourceSelection.get()
        self.refresh()

    def moreInfo(self, event):
        toplevel = Toplevel()
        #toplevel.geometry("%dx%d%+d%+d" % (350, 200, 250, 125))
        #Labels
        seriesName = Label(toplevel, text='Series Name: ' + self.tree.item(self.tree.focus()).get('text'))
        seriesName.grid(columnspan=2, sticky=NSEW)
        infoLabel = Label(toplevel, text="Info:")
        infoLabel.grid(columnspan=2, sticky=NSEW)
        #Textarea
        info = Text(toplevel, background="grey")
        mangaInfo = getInfoScraper(self.tree.item(self.tree.focus()).get('values')[0])
        info.grid(columnspan=2,sticky="nsew")
        #Populating textarea
        info.insert(INSERT, "Released: " + mangaInfo.released)
        info.insert(INSERT, "\nAuthors: " + mangaInfo.authors)
        info.insert(INSERT, "\nArtists: " + mangaInfo.artists)
        info.insert(INSERT, "\nGenres: " + mangaInfo.genres)
        info.insert(INSERT, "\n\nStatus: " + mangaInfo.status)
        info.insert(INSERT, "\nRank: " + mangaInfo.rank)
        info.insert(INSERT, "\nRating: " + mangaInfo.rating)
        info.insert(INSERT, "\n\nSynopsis:\n\n" + mangaInfo.synopsis)
        #Font changes
        bold_font = Font(weight="bold")
        info.tag_configure("BOLD", font=bold_font)
        info.tag_add("BOLD", "1.0", "1.9")
        info.tag_add("BOLD", "2.0", "2.8")
        info.tag_add("BOLD", "3.0", "3.8")
        info.tag_add("BOLD", "4.0", "4.7")
        info.tag_add("BOLD", "6.0", "6.7")
        info.tag_add("BOLD", "7.0", "7.5")
        info.tag_add("BOLD", "8.0", "8.7")
        info.tag_add("BOLD", "10.0", "10.9")
        #Ending buttons
        closeButton = Button(toplevel, text="Close", command=toplevel.destroy)
        closeButton.grid(column=1,row=3,sticky="nsew")
        webLinkButton = Button(toplevel, text="Read Manga", command=self.openLink)
        webLinkButton.grid(column=0,row=3,sticky="nsew")
        #Scaling weights
        toplevel.grid_rowconfigure(0, weight=0)#4 rows starting 0
        toplevel.grid_rowconfigure(1, weight=0)
        toplevel.grid_rowconfigure(2, weight=1)
        toplevel.grid_rowconfigure(3, weight=0)
        toplevel.grid_columnconfigure(0, weight=1)#2 columns starting 0
        toplevel.grid_columnconfigure(1, weight=1)

class Scraper:

    url = ''
    series = []
    times = []
    links = []
    newChapters = []
    
    def __init__(self, url):
        self.url = url
        page = requests.get(url)
        tree = html.fromstring(page.content)
        self.getSeries(tree)
        self.getTimes(tree)
        self.getLinks(tree)
        self.getNewChapters(tree)
        
    def getSeries(self, tree):#Format is in "<Series Name>"
        if self.url == 'http://mangafox.me/':
            self.series = tree.xpath('//ul[@id="updates"]/li/div/h3/a/text()')
        elif self.url == 'http://mangalife.us/':
            self.series = tree.xpath('//div/div/div/div/a/div/div/p/text()')
            for count in range(0, len(self.series)):
                self.series[count] = self.series[count].rstrip('1234567890').lstrip()

    def getTimes(self, tree):#Format follows website's chosen format
        if self.url == 'http://mangafox.me/':
            self.times = tree.xpath('//ul[@id="updates"]/li/div/h3/em/text()')
        elif self.url == 'http://mangalife.us/':
            self.times = tree.xpath('//div/div/div/div/a/div/div/time/text()')
        
    def getLinks(self, tree):#Format is the http:// link
        self.links = []
        if self.url == 'http://mangafox.me/':
            for count in range(0, len(self.series)):
                self.links.append(self.series[count].getparent().get('href'))
        elif self.url == 'http://mangalife.us/':
            for count in range(0, len(self.series)):
                if tree.xpath('//div/div/div/div/a/div/div/p/text()')[count].getparent().getparent().getparent().getparent().get('href') is not None:
                    self.links.append('http://mangalife.us' + tree.xpath('//div/div/div/div/a/div/div/p/text()')[count].getparent().getparent().getparent().getparent().get('href'))
                elif tree.xpath('//div/div/div/div/a/div/div/p/text()')[count].getparent().getparent().getparent().getparent().getparent().get('href') is not None:
                    self.links.append('http://mangalife.us' + tree.xpath('//div/div/div/div/a/div/div/p/text()')[count].getparent().getparent().getparent().getparent().getparent().get('href'))
            
    def getNewChapters(self, tree):#Format is "<Series Name> <Chapter>"
        if self.url == 'http://mangafox.me/':
            self.newChapters = tree.xpath('//ul[@id="updates"]/li/div/dl/dt/span/a/text()')
        elif self.url == 'http://mangalife.us/':
            self.newChapters = tree.xpath('//div/div/div/div/a/div/div/p/text()')

class getInfoScraper:

    #info
    url = ''
    released = ''
    authors = ''
    artists = ''
    genres = ''
    synopsis = ''

    #statusinfo
    status = ''
    rating = ''
    rank = ''
    
    def __init__(self, url):
        self.url = url
        if 'http://mangalife.us/' in self.url:
            self.url = self.url.split("-chapter",1 )[0].replace('read-online', 'manga')
        page = requests.get(self.url)
        tree = html.fromstring(page.content)
        if 'http://mangafox.me/' in self.url:
            self.info = tree.xpath('//div/div/div/table/tr/td/a/text()')
            self.statusInfo = tree.xpath('//div/div/div/div/span/text()')
        elif 'http://mangalife.us/' in self.url:
            self.info = tree.xpath('//div/div/div/div/span/div/div/a/text()')
            #No statusInfo like ranking for this source
        self.getReleased(tree)
        self.getAuthors(tree)
        self.getArtists(tree)
        self.getGenres(tree)
        self.getSynopsis(tree)
        self.getStatus(tree)
        self.getRating(tree)
        self.getRank(tree)

    def getReleased(self, tree):
        if 'http://mangafox.me/' in self.url:
            for count in range(0, len(self.info)):
                if 'released' in self.info[count].getparent().get('href'):
                    self.released = self.info[count]
        if 'http://mangalife.us/' in self.url:
            for count in range(0, len(self.info)):
                if 'year' in self.info[count].getparent().get('href'):
                    self.released = self.info[count]
                    
    def getAuthors(self, tree):
        if 'http://mangafox.me/' in self.url:
            for count in range(0, len(self.info)):
                if 'author' in self.info[count].getparent().get('href'):
                    if self.authors == '':
                        self.authors += self.info[count]
                    else:
                        self.authors += ', ' + self.info[count]
        if 'http://mangalife.us/' in self.url:
            for count in range(0, len(self.info)):
                if 'author' in self.info[count].getparent().get('href'):
                    if self.authors == '':
                        self.authors += self.info[count]
                    else:
                        self.authors += ', ' + self.info[count]

    def getArtists(self, tree):
        if 'http://mangafox.me/' in self.url:
            for count in range(0, len(self.info)):
                if 'artist' in self.info[count].getparent().get('href'):
                    if self.artists == '':
                        self.artists += self.info[count]
                    else:
                        self.artists += ', ' + self.info[count]
            if self.artists == '':
                self.artists += 'Unknown'
        if 'http://mangalife.us/' in self.url:
            self.artists = "NIL for this source."

    def getGenres(self, tree):
        if 'http://mangafox.me/' in self.url:
            for count in range(0, len(self.info)):
                if 'genres' in self.info[count].getparent().get('href'):
                    if self.genres == '':
                        self.genres += self.info[count]
                    else:
                        self.genres += ', ' + self.info[count]
        if 'http://mangalife.us/' in self.url:
            for count in range(0, len(self.info)):
                if 'genre' in self.info[count].getparent().get('href'):
                    if self.genres == '':
                        self.genres += self.info[count]
                    else:
                        self.genres += ', ' + self.info[count]

    def getSynopsis(self, tree):
        if 'http://mangafox.me/' in self.url:
            for count in range(0, len(tree.xpath('//div/div/div[@id="title"]/p/text()'))):
                self.synopsis += tree.xpath('//div/div/div[@id="title"]/p/text()')[count]
        if 'http://mangalife.us/' in self.url:
            for count in range(0, len(tree.xpath('//div[@class="description"]/text()'))):
                self.synopsis += tree.xpath('//div[@class="description"]/text()')[count]

    def getStatus(self, tree):
        if 'http://mangafox.me/' in self.url:
            self.status = self.statusInfo[0].rstrip().lstrip().replace(',','')
        if 'http://mangalife.us/' in self.url:
            self.status = "NIL for this source."

    def getRating(self, tree):
        if 'http://mangafox.me/' in self.url:
            if len(self.statusInfo) == 3:#basically if status=completed, different format of xpath output
                self.rating = self.statusInfo[2].rstrip().lstrip()
            else:
                self.rating = self.statusInfo[4].rstrip().lstrip()
        if 'http://mangalife.us/' in self.url:
            self.rating = "NIL for this source."

    def getRank(self, tree):
        if 'http://mangafox.me/' in self.url:
            if len(self.statusInfo) == 3:#basically if status=completed, different format of xpath output
                self.rank = self.statusInfo[1].rstrip().lstrip()
            else:
                self.rank = self.statusInfo[3].rstrip().lstrip()
        if 'http://mangalife.us/' in self.url:
            self.rank = "NIL for this source."
                
def main():
    root = Tk()
    root.geometry("450x255+300+300")
    app = LatestChapters(root)
    root.mainloop()

if __name__ == '__main__':
    main()
