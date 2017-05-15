#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2011 Riverbank Computing Limited.
## Copyright (C) 2011 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import random


class Ball(QGraphicsEllipseItem):
#initalising a ball and setting MRO (Method Resolution Order) with super
    def __init__(self,parent=None):
        super(Ball,self).__init__(parent)
        self.vel=[0,0]
        self.radius=16

# reflectX for reflection from paddles
    def reflectX(self):
        self.vel[0]=-self.vel[0]
        if self.vel[0]<0:
            self.vel[0]-=0.5
        else:
            self.vel[0]+=0.5
        self.setX(self.x()+self.vel[0])

# reflectY for reflection from boundaries
    def reflectY(self):
        self.vel[1]=-self.vel[1]
        self.setY(self.y()+self.vel[1])
        #print self.vel[1]

# move for normal movement of ball
    def move(self):
        self.setX(self.x()+self.vel[0])
        self.setY(self.y()+self.vel[1])

#Then I write the Paddle class.
class Paddle(QGraphicsRectItem):
#initialization and setting up MRO with super
    def __init__(self,maxHeight,parent=None):
        super(Paddle,self).__init__(parent)
        self.maxHeight=maxHeight-105
        #maxHeight comes from the boundary of QGraphicsView class. I define to stop the paddle from #moving out of view

# for moving the paddle up
    def moveUp(self):
        if self.y()>0:
            self.setY(self.y()-10)

# for moving the paddle down
    def moveDown(self):
        if self.y()<self.maxHeight:
            self.setY(self.y()+10)

class View(QGraphicsView,QObject):
#initialize and set up MRO
    def __init__(self,parent=None):
        super(View,self).__init__(parent)
#fix the size of display window so that it cannot be resized. The items outside size this will not be seen.
        self.setFixedSize(700,400)
#set the alignment of displaywindow so that (0,0) lies on top left corner
        self.setAlignment(Qt.AlignTop|Qt.AlignLeft)
#shut down the scroll bar. Scrollbar causes problems. To see what problems scrollbar might cause, #comment out following lines.
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#setting window title
        self.setWindowTitle('Pong')
#making antialiased display
        self.setRenderHint(QPainter.Antialiasing)
# setting the part of the scene to be displayed on the view window
        self.setSceneRect(self.x()-2,self.y()+self.height()/2-2,self.width(),self.height())

#defining the signals that will be passed onto the game class instance
    Wpress=pyqtSignal()
    Spress=pyqtSignal()
    UPpress=pyqtSignal()
    DownPress=pyqtSignal()

#defining key press events so that the signals are emitted. These signals are caught by game class instance.
def keyPressEvent(self,event):
        if event.key() == Qt.Key_W:
            self.Wpress.emit()
        elif event.key() == Qt.Key_S:
            self.Spress.emit()
        elif event.key() == Qt.Key_Up:
            self.UPpress.emit()
        elif event.key() == Qt.Key_Down:
            self.DownPress.emit()

class SceneAndView:
#initializing
    def __init__(self):
        #instantizing QGraphicsScene class
        self.scene=QGraphicsScene()
#instantizing the View class created above
        self.view=View()
#setting the scene for view
        self.view.setScene(self.scene)

class PongGame:
#initializing
    def __init__(self,parent=None):
#instantizing sceneAndView class for ponggame
        self.sceneView=SceneAndView()
#instantizing the ball class for game
        self.ball=Ball()
#defining the bounding rectangle for the ball class. This is very useful for collision detection.
#the setRect method for uses needs (X-coordinate,Y-coordinate,height and width). Here, the ball is placed at the center of view window and height and width are equal to radius.
        self.ball.setRect((self.sceneView.view.size().width()-15)/2,self.sceneView.view.height(),self.ball.radius,self.ball.radius)

#Here, boundary is defined as the maximum width and height within the view window. It will be used to #define the boundary that is to be crossed to declare the ball as missed by the player.
        self.boundary=[self.sceneView.view.width(),self.sceneView.view.height()]

#Here, left and right paddles are instantized. maxHeight is passed as the height of the window. Bounding #rectangle are also defined for the paddles. This is simililar to defining bounding rectangle of Ball above.
        self.paddleLeft=Paddle(self.sceneView.view.height())
        self.paddleLeft.setRect(0,self.sceneView.view.size().height()/2,10,100)
        self.paddleRight=Paddle(self.sceneView.view.height())
        self.paddleRight.setRect(self.sceneView.view.size().width()-15,self.sceneView.view.size().height()/2,10,100)
        self.sceneView.scene.addLine(self.boundary[0]/2,self.boundary[1]/2,self.boundary[0]/2,self.boundary[1]*2)

#ball and paddles are added to the scene
        self.sceneView.scene.addItem(self.ball)
        self.sceneView.scene.addItem(self.paddleLeft)
        self.sceneView.scene.addItem(self.paddleRight)
        self.sceneView.view.Wpress.connect(self.paddleLeft.moveUp)
        self.sceneView.view.Spress.connect(self.paddleLeft.moveDown)
        self.sceneView.view.UPpress.connect(self.paddleRight.moveUp)
        self.sceneView.view.DownPress.connect(self.paddleRight.moveDown)


# timer mechanism is used to move the ball. The ball moving function is to be called every 30  milliseconds. #This keeps CPU usage low.

#Timer is defined for Viewer class.   When timeout occurs, ballMove function is called.
#Reset function is used in case if we add reset frature to the game.
        self.timer=QTimer(self.sceneView.view)
        self.timer.timeout.connect(self.ballMove)
        self.reset()

#Reset method resets the game

    def reset(self):
        self.serve(random.choice([0,1]))

#serve method serves the ball once a ball is missed by the paddles(player). If leftSide is true, ball is served to #the left, else it is served to right. Timer is started to fire every 30 seconds.

    def serve(self,leftSide):
        self.ball.setPos(0,0)
        if leftSide:
            self.ball.vel=[-10,random.choice([-3,-2,-1,1,2,3])]
        else:
            self.ball.vel=[10,random.choice([-3,-2,-1,3,2,1])]
        self.timer.start(30)

# ballHitsPaddle method returns True if ball hits the paddle. It uses QGraphicsEllipseItem collidesWith #method to check whether the ball collides with any of the paddles.

    def ballHitsPaddle(self):
        z= self.sceneView.scene.collidingItems(self.ball)
        if self.ball.collidesWithItem(self.paddleLeft) or self.ball.collidesWithItem(self.paddleRight):
            return True
        pass

#ballHitsBoundary checks if the ball hits top or bottom boundary.

    def ballHitsBoundary(self):
        if self.ball.y()<-self.boundary[1]/2+15 or self.ball.y()>self.boundary[1]/2-15:
            return True
        pass

#ballMissed method checks if the ball is beyond the paddles or view window. It returns (True, 'right') if right #paddle misses , (True,'left') if left paddle misses and (False,None) if ball is not missed

    def ballMissed(self):
        #print self.boundary[0]/2,self.ball.x()
        if self.ball.x()<-self.boundary[0]/2:
            #print 'missed left'
            return True,'left'
        elif self.ball.x()>self.boundary[0]/2:
            #print 'missed right'
            return True,'right'
        else:
            return False,'none'

#ballMove method defines how the ball moves. If ball hits the paddle, it is reflected horizontally. If ball hits #upper or lower boundary, ball is reflected vertically. If the ball is missed, it adds score to the opposite side #and calls to serve the ball to the side which missed the ball. If none of this happens, the ball moves normally.

    def ballMove(self):
        if self.ballHitsBoundary():
            self.ball.reflectY()
        elif self.ballHitsPaddle():
            self.ball.reflectX()
            #self.ball.reflectY()
        elif self.ballMissed()[0]:
            if self.ballMissed()[1]=='left':
                self.serve(True)
            elif self.ballMissed()[1]=='right':
                self.serve(False)
        else:
            self.ball.move()

if __name__=='__main__':
    app=QApplication(sys.argv)
    w=PongGame()
    w.sceneView.view.show()
    sys.exit(app.exec_())
