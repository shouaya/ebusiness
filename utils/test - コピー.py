# coding: UTF-8

MEISAI = [['10A', '02', '03', 100],
          ['10A', '02', '04', 100],
          ['10A', '02', '04', 100],
          ['10A', '02', '04', 100],
          ['10A', '02', '04', 100],
          ['10A', '02', '04', 100],
          ['10A', '02', '04', 100],
          ['10A', '02', '04', 100],
          ['10A', '02', '04', 100],
          ['10A', '02', '04', 100],
          ['10A', '02', '04', 100],
          ['10A', '02', '04', 100],
          ['15A', '02', '03', 100],
          ['15A', '02', '03', 100],
          ['15A', '02', '03', 100],
          ['15A', '02', '03', 100],
          ['15A', '03', '01', 100],
          ['15A', '03', '01', 100],
          ['15A', '03', '01', 100],
          ['15A', '03', '01', 100],
          ['15A', '03', '02', 100],
          ['15A', '03', '02', 100],
          ['15A', '03', '02', 100],
          ['15A', '03', '03', 100],
          ['15A', '03', '03', 100]]

class PrintData:

    def __init__(self):
        self.lineCount = 0
        self.pageCount = 1

    def printData(self):
        allJig = allBu = allKa = 0
        wJig = wBu = wKa = None
        self.printHeader()
        for lst in MEISAI:
            if wJig is None and wBu is None and wKa is None:
                wJig = lst[0]
                wBu = lst[1]
                wKa = lst[2]
            cJig, cBu, cKa, cT = lst
            if cJig != wJig:
                allJig += cT
                allBu += cT
                allKa += cT
                self.printKa(allKa)
                self.printBu(allBu)
                self.printJig(allKa)
                self.printMeisai(lst)
            elif cBu != wBu:
                allJig += cT
                allBu += cT
                allKa += cT
                self.printKa(allKa)
                self.printBu(allBu)
                self.printMeisai(lst)
            elif cKa != wKa:
                allJig += cT
                allBu += cT
                allKa += cT
                self.printKa(allKa)
                self.printMeisai(lst)
            else:
                self.printMeisai(lst)
            wJig = cJig
            wBu = cBu
            wKa = cKa

    def printMeisai(self, lst):
        self.printLine(lst[0].rjust(10) + lst[1].rjust(10) + lst[2].rjust(10) + str(lst[3]).rjust(20))

    def printJig(self, total):
        self.printLine("total Jig".rjust(30) + str(total).rjust(20))
        self.printLine(" ")

    def printBu(self, total):
        self.printLine("total Bu".rjust(30) + str(total).rjust(20))
        self.printLine(" ")

    def printKa(self, total):
        self.printLine(" ")
        self.printLine("total Ka".rjust(30) + str(total).rjust(20))
        self.printLine(" ")

    def printHeader(self):
        self.lineCount = 0
        print " "
        print "ページ %s ".rjust(50) % (self.pageCount)
        print " "
        print "                  ☆☆☆ 一 覧 ☆☆☆                     "
        print " "
        print "Jig".rjust(10) + "Bu".rjust(10) + "Ka".rjust(10) + "Total".rjust(20)
        print " "

    def printLine(self, text):
        if self.lineCount >= 15:
            self.pageCount += 1
            self.printHeader()
        self.lineCount += 1
        print text
    
pd = PrintData()
pd.printData()
