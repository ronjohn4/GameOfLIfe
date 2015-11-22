#todo - different environments, the environment should vary with some spots being inhabitable and some not

import random
import pprint
import sys
import time
import System.Diagnostics
import clr
from System import Console

clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
from System.Drawing import *
from System.Windows.Forms import *




class Laws(object):
    rmax = 20
    cmax = 20

    def subsist(self,a):
        a.energy -= a.energyburn

    def sun(self,a):
        a.energy += a.energyabsorbtion

    def giveenergy(self,afrom,ato,energyamount):
        if afrom.energy < energyamount:
            ato.energy += afrom.energy
            afrom.energy = 0
        else:
            ato.energy += energyamount
            afrom.energy -= energyamount


laws = Laws()



class World(object):
    __world = []
    __worldtick = []
    A1count = 0
    Iteration = 0
    Energy = 0
    Die = 0
    Born = 0

    def __init__(self):
        self.Iteration = 0
        self.Energy = 0
        self.Die = 0
        self.Born = 0
        self.A1count = 10
        self.__worldtick = [[[] for j in xrange(laws.rmax)] for i in xrange(laws.cmax)]

        for i in range(self.A1count):
            while True:
                r = random.randint(0,laws.rmax-1)
                c = random.randint(0,laws.cmax-1)
                if not self.__worldtick[r][c]:
                    break
            a = Animal1(r,c,500)
            self.__worldtick[r][c].append(a)
    
    def reset(self):
        self.__init__()


    def myneighbors(self,r,c):
        r = self.wrapr(r)
        c = self.wrapc(c)

        rowabove = r - 1
        if (rowabove < 0):
            rowabove = laws.rmax - 1
        rowbelow = r + 1
        if (rowbelow > laws.rmax - 1):
            rowbelow=0
        colleft = c - 1
        if (colleft < 0):
            colleft = laws.cmax - 1
        colright = c + 1
        if(colright > laws.cmax - 1):
            colright = 0

        return [self.__world[rowabove][colleft], 
                self.__world[rowabove][c], 
                self.__world[rowabove][colright], 
                self.__world[r][colright], 
                self.__world[rowbelow][colright], 
                self.__world[rowbelow][c], 
                self.__world[rowbelow][colleft], 
                self.__world[r][colleft] ]

    def animal(self,r,c):
        r = self.wrapr(r)
        c = self.wrapc(c)
        return self.__world[r][c]

    def wrapr(self,r):
        return r % laws.rmax

    def wrapc(self,c):
        return c % laws.cmax

    def tick(self):
        self.__worldtick = [[[] for j in xrange(laws.rmax)] for i in xrange(laws.cmax)]
        self.Born = 0
        self.Die = 0 

        for r in range(laws.rmax):
            for c in range(laws.cmax):
                a = self.__world[r][c]
                if a is not None:
                    laws.subsist(a)
 
                    if self.stayalive(a): 
                        laws.sun(a)
                        a.action()
                        self.__worldtick[r][c].append(a)
                    else:
                        self.Die += 1
                        #print 'Die(%d,%d e=%d)' % (r,c, a.energy)

    def stayalive(self,a):
        return a.energy > 0

    def tock(self):
        self.__world = [[None for j in xrange(laws.rmax)] for i in xrange(laws.cmax)]
        self.A1count = 0
        self.Energy = 0
        self.Iteration += 1

        for r in range(laws.rmax):
            for c in range(laws.cmax):
                biggestenergy = 0
                totalenergy = 0
                for a in self.__worldtick[r][c]:
                    if a.energy > biggestenergy: 
                        biggestenergy = a.energy
                        self.__world[r][c] = a
                    else:
                        self.Die += 1
                        #print 'Die(%d,%d e=%d)' % (r,c,a.energy)
                if self.__world[r][c] is not None:
                    self.Energy += biggestenergy
                    form.lblCell[r][c].Text = self.__world[r][c].show()
                    self.A1count += 1
                    print 'Alive(%d,%d e=%d count=%d)' % (r,c,self.__word[r][c].energy,self.A1count)
                else:
                    form.lblCell[r][c].Text = '-'
 
    def moveObject(self,a,r,c):
        r1 = self.wrapr(r)
        c1 = self.wrapc(c)
        #if r1 != r or c1 != c: 
            #print 'Adjust(%d %d to %d %d)' % (r,c,r1,c1)
        a.energy -= 500 #todo - distance should weigh on energy cost
        self.__worldtick[r1][c1].append(a)



class Life(object):
    def __init__(self,Row,Column,StartEnergy):
        self._r = Row
        self._c = Column
        self.energy = StartEnergy
        self.aliveiterations = 0

    def show(self):
        pass

    def action(self):
        self.aliveiterations += 1

    def neighborcount(self):
        __nc = 0
        __myworld = w.myneighbors(self._r,self._c)
        
        for n in __myworld:
            if n:
                __nc += 1
        return __nc

  
                        
class Animal1(Life):
    def __init__(self,Row,Column,StartEnergy):
        self.energyabsorbtion = 200
        self.energyburn = 100
        self.energytochild = 500
        self.energyforchild = 600
        super(Animal1, self).__init__(Row,Column,StartEnergy)

    def show(self):
        return 'X'

    def action(self):
        self.__havechild()
        self.__moveme()
#       todo - self.__otheraction()
 
    def __moveme(self):
        pass    #this is a plant and can't move

    def __havechild(self):
        if self.energy > self.energyforchild:
            a2 = Animal1(self._r,self._c,self.energyforchild)
            laws.giveenergy(self,a2,self.energytochild)
            #todo - where to move child?
            #Console.WriteLine('test')
            while True:
                rd = random.randint(-1,1)
                cd = random.randint(-1,1)
                if rd != 0 or cd !=0:
                    break
            #print 'Born From(%d %d) To(%d %d)' % (self._r,self._c,self._r+rd,self._c+cd)
            w.moveObject(a2, self._r + rd,self._c + cd)
            w.Born += 1

w = World()


class MyForm(Form):
    lblIteration = None
    lblCount = None
    lblEnergy = None
    lblCell = [[None for j in xrange(laws.rmax)] for i in xrange(laws.cmax)]

    def __init__(self):
        wHeight = 450
        wWidth = 550
        wMargin = 10

        self.FormBorderStyle = FormBorderStyle.FixedSingle

        # Configure btnOK
        btnTicToc = Button()
        btnTicToc.Text = "&Tic Toc"
        btnTicToc.Location = Point(wWidth - btnTicToc.Width - wMargin, wMargin)
 
        # Configure btnCancel
        btnReset = Button()
        btnReset.Text = "&Reset"
        btnReset.Location = Point(btnTicToc.Left, btnTicToc.Top + btnTicToc.Height + wMargin)
 
        # Configure btnReset
        btnCancel = Button()
        btnCancel.Text = "&Cancel"
        btnCancel.Location = Point(btnReset.Left, btnReset.Top + btnReset.Height + wMargin)
 
        # Configure lblMessage
        lblMessage = Label()
        lblMessage.Text = 'Message:'
        lblMessage.Location = Point(wMargin, wMargin)
        lblMessage.AutoSize = True

        # Configure lblCount
        self.lblCount = Label()
        self.lblCount.Text = 'A1 Count: %i' % 0
        self.lblCount.Location = Point(wMargin, lblMessage.Top + lblMessage.Height)
        self.lblCount.AutoSize = True

        # Configure lblEnergy
        self.lblEnergy = Label()
        self.lblEnergy.Text = 'Energy: %i' % 0
        self.lblEnergy.Location = Point(wMargin, self.lblCount.Top + self.lblCount.Height)
        self.lblEnergy.AutoSize = True

        # Configure lblDie
        self.lblDie = Label()
        self.lblDie.Text = 'Die: %i' % 0
        self.lblDie.Location = Point(wMargin, self.lblEnergy.Top + self.lblEnergy.Height)
        self.lblDie.AutoSize = True

        # Configure lblBorn
        self.lblBorn = Label()
        self.lblBorn.Text = 'Born: %i' % 0
        self.lblBorn.Location = Point(wMargin, self.lblDie.Top + self.lblDie.Height)
        self.lblBorn.AutoSize = True

        # Configure lblIteration
        self.lblIteration = Label()
        self.lblIteration.Text = 'Iteration: %i' % 0
        self.lblIteration.Location = Point(wMargin, self.lblBorn.Top + self.lblBorn.Height)
        self.lblIteration.AutoSize = True
 
        # Configure the form.
        self.ClientSize = Size(wWidth, wHeight)
        self.Text = 'Game of Life - Modified'
        self.AcceptButton = btnTicToc
        self.CancelButton = btnCancel
 
        # Add the controls to the form.
        self.Controls.Add(btnTicToc)
        self.Controls.Add(btnReset)
        self.Controls.Add(btnCancel)
        self.Controls.Add(lblMessage)
        self.Controls.Add(self.lblCount)
        self.Controls.Add(self.lblIteration)
        self.Controls.Add(self.lblEnergy)
        self.Controls.Add(self.lblDie)
        self.Controls.Add(self.lblBorn)

        btnTicToc.Click += self.btnTicToc_Click
        btnReset.Click += self.btnReset_Click
        btnCancel.Click += self.btnCancel_Click
       
        wTopOfGrid = self.lblIteration.Top + self.lblIteration.Height + wMargin

        for r in range(laws.rmax):
            for c in range(laws.cmax):
                self.lblCell[r][c] = Label()
                self.lblCell[r][c].Text = 'X'
                self.lblCell[r][c].Location = Point(r*13 + wMargin, c*13 + wTopOfGrid)
                self.lblCell[r][c].Size = Size(13, 13)
                self.lblCell[r][c].Click += self.lblCell_Click
                self.Controls.Add(self.lblCell[r][c])

    def showstatus(self):
        self.lblIteration.Text = 'Iteration: %i' % w.Iteration
        self.lblCount.Text = 'A1 Count: %i' % w.A1count
        self.lblEnergy.Text = 'Energy: %i' % w.Energy
        self.lblDie.Text = 'Die: %i' % w.Die
        self.lblBorn.Text = 'Born: %i' % w.Born

    def lblCell_Click(*args):
        args[0].Text= 'T'                        
        #MessageBox.Show(args[0].ToString())
        #MessageBox.Show('Cell Click')

    def btnTicToc_Click(*args):
        args[0].Enabled = False
        w.tick()
        w.tock()
        form.showstatus()
        args[0].Enabled = True
 
    def btnReset_Click(*args):
        w.reset()
        w.tock()
        form.showstatus()

    def btnCancel_Click(*args):
        form.Close()


Application.EnableVisualStyles()
Application.SetCompatibleTextRenderingDefault(False)

form = MyForm()
w.tock()

form.showstatus()
Application.Run(form)
