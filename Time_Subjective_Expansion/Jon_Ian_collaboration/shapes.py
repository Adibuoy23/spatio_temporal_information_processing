"""
Demo of psychopy.visual.ShapeStim: lines and arbitrary fillable shapes
See shapeContains.py for dynamic interaction of ShapeStim and Mouse.
"""

from __future__ import division

from psychopy import visual, event, core, monitors
from psychopy.visual import ShapeStim

widthPix = 2880  # monitor width in pixels of Agosta
heightPix = 1800  # 800 #monitor height in pixels
monitorwidth = 52  # 28.2  # monitor width in cm
scrn = 0  # 0 to use main screen, 1 to use external screen connected to computer
fullscr = False  # True to use fullscreen, False to not. Timing probably won't be quite right if fullscreen = False
allowGUI = False
expStop = False
viewdist = 65.0  # cm

monitorname = 'testmonitor'
waitBlank = False
# relying on  monitorwidth cm (39 for Mitsubishi to do deg calculations) and gamma info in calibratn
mon = monitors.Monitor(monitorname, width=monitorwidth, distance=viewdist)
mon.setSizePix((widthPix, heightPix))
units = 'deg'  # 'cm'

win = visual.Window(monitor=mon, size=(widthPix, heightPix), allowGUI=allowGUI, units=units, fullscr=fullscr, screen=scrn, waitBlanking=waitBlank)  # Holcombe lab monitor


# some shapes:
arrowVert = [(-0.4,0.05),(-0.4,-0.05),(-.2,-0.05),(-.2,-0.1),(0,0),(-.2,0.1),(-.2,0.05)]
arrow = ShapeStim(win, vertices=arrowVert, fillColor='darkred', size=.5, lineColor='red')

star7Vert = [(0.0,0.5),(0.09,0.18),(0.39,0.31),(0.19,0.04),(0.49,-0.11),(0.16,-0.12),(0.22,-0.45),(0.0,-0.2),(-0.22,-0.45),(-0.16,-0.12),(-0.49,-0.11),(-0.19,0.04),(-0.39,0.31),(-0.09,0.18)]
star7 = ShapeStim(win, vertices=star7Vert, fillColor='green', lineWidth=2, lineColor='white')

# self-crossings are fine:
selfxVert = [(0, 0), (0, .2), (.2, 0), (.2, .2)]
selfx = ShapeStim(win, vertices=selfxVert, fillColor='darkmagenta', lineColor='yellow', opacity=.6, pos=(.2, -.3), size=2)

# `thing` has a fake hole and discontinuity (as the border will reveal):
thingVert = [(0,0),(0,.4),(.4,.4),(.4,0),(.1,0),(.1,.1),(.3,.1),(.3,.3),(.1,.3),(.1,0),(0,0),(.1,-.1),(.3,-.1),(.3,-.3),(.1,-.3),(.1,-.1)]
thing = ShapeStim(win, vertices=thingVert, fillColor='blue', lineWidth=0, opacity=.3, size=.7)

# `donut` has a true hole, using two loops of vertices:
donutVert = [[(-.2,-.2),(-.2,.2),(.2,.2),(.2,-.2)],[(-.15,-.15),(-.15,.15),(.15,.15),(.15,-.15)]]
donut = ShapeStim(win, vertices=donutVert, fillColor='orange', lineWidth=0, size=.75, pos=(-.2, -.25))

# lines are ok; use closeShape=False
lineAVert = [(0, 0), (.1, .1), (.1, .2), (.1, .1), (.1, -.1), (0, .1)]
lineA = ShapeStim(win, vertices=lineAVert, closeShape=False, lineWidth=2, pos=(-.4, .2), ori=180)

# a complex shape, many vertices:
coastVert = [(-23,230),(-3,223),(32,233),(43,230),(46,236),(34,240),(31,248),(31,267),(45,260),(52,266),(43,274),(47,279),(53,268),(65,282),(65,273),(56,266),(59,265),(53,261),(47,237),(43,230),(39,225),(43,219),(39,209),(29,206),(12,189),(9,183),(-2,183),(18,179),(-2,165),(10,169),(2,162),(29,177),(40,169),(74,170),(80,169),(86,153),(77,145),(76,132),(61,107),(61,100),(33,86),(51,91),(57,84),(27,63),(36,63),(51,70),(71,60),(87,42),(100,4),(97,-9),(125,-28),(139,-46),(138,-56),(148,-73),(118,-66),(149,-82),(157,-98),(157,-106),(151,-109),(148,-114),(154,-120),(158,-120),(159,-111),(168,-110),(188,-114),(205,-131),(203,-144),(200,-160),(188,-170),(164,-180),(179,-180),(179,-188),(157,-193),(172,-196),(165,-197),(176,-202),(193,-200),(193,-211),(181,-217),(180,-229),(172,-220),(155,-234),(139,-227),(118,-233),(99,-227),(94,-232),(91,-237),(101,-243),(106,-242),(107,-237),(103,-232),(94,-238),(90,-233),(81,-233),(81,-240),(61,-243),(50,-234),(27,-240),(21,-262),(15,-262),(15,-260),(-2,-253),(-13,-256),(-26,-264),(-26,-272),(-31,-275),(-31,-269),(-38,-267),(-41,-268),(-46,-271),(-46,-267),(-41,-262),(-28,-257),(-8,-226),(-8,-219),(1,-219),(3,-210),(25,-205),(30,-210),(35,-210),(35,-204),(29,-205),(29,-200),(15,-185),(0,-191),(0,-187),(3,-183),(-4,-180),(-24,-187),(-32,-178),(-29,-178),(-29,-174),(-35,-174),(-26,-164),(4,-149),(8,-139),(6,-118),(3,-117),(-4,-118),(-5,-122),(-16,-122),(-11,-115),(-2,-107),(-2,-100),(-11,-93),(-11,-85),(0,-84),(7,-93),(14,-88),(32,-89),(40,-96),(39,-85),(47,-90),(41,-79),(42,-55),(48,-53),(44,-41),(35,-48),(22,-21),(23,-3),(15,0),(4,-6),(-5,0),(-3,-14),(-20,-2),(-20,-16),(-31,2),(-13,36),(-18,48),(-18,65),(-21,50),(-35,65),(-25,76),(-39,64),(-37,56),(-37,44),(-28,30),(-26,37),(-32,49),(-39,45),(-39,29),(-52,25),(-47,32),(-45,50),(-45,65),(-54,57),(-61,43),(-69,43),(-73,50),(-73,57),(-72,57),(-71,57),(-68,57),(-66,57),(-64,57),(-62,57),(-62,58),(-60,58),(-59,59),(-58,59),(-58,66),(-47,76),(-46,71),(-44,80),(-44,89),(-29,120),(-48,99),(-48,91),(-59,87),(-71,87),(-63,92),(-66,99),(-89,93),(-76,108),(-64,105),(-52,96),(-64,116),(-53,120),(-53,130),(-83,158),(-95,163),(-102,130),(-116,113),(-105,133),(-105,166),(-96,172),(-95,169),(-93,175),(-94,181),(-94,206),(-66,227),(-66,215),(-66,202),(-67,188),(-89,173),(-94,164),(-81,158),(-67,171),(-55,141),(-50,143),(-52,161),(-50,181),(-43,186),(-30,186),(-38,197),(-26,230)]
coast = ShapeStim(win, vertices=coastVert, fillColor='darkgray', lineColor=None, size=.007, pos=(.4, .2))

while not event.getKeys():
    donut.draw()
    coast.draw()
    star7.setOri(1, '-')  # rotate
    star7.setSize(star7.ori % 360 / 360)  # shrink
    star7.draw()
    thing.setOri(-star7.ori / 7)  # rotate slowly
    thing.draw()
    arrow.draw()
    lineA.draw()
    # dynamic vertices:
    selfxVert[0] = star7.size / 5
    selfxVert[3] = star7.size / 5 * (0, .9)
    selfx.vertices = selfxVert  # can be slow with many vertices
    selfx.draw()

    win.flip()

win.close()
core.quit()
