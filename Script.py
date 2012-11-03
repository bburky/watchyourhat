
print "Starting game!"
import pygame

from DefenseMain import DefenseMain
from Applejack import Applejack
from Twilight import Twilight
from Rainbowdash import Rainbowdash
from Derpy import Derpy
from Rarity import Rarity
from Pinkie import Pinkie
from Parasprite import Parasprite
from helpers import *

dp = DefenseMain()


def playGame():
	pygame.key.set_repeat(30, 30)

	dp.resetState()
	dp.setBackground('backgroundImage.png')
	dp.initializeStatic()

	#intro movie
	dp.showMovie('applejackIntro-lowRes.mpg')
	dp.playMusic('applejackTheme.mp3')

	dp.lockAll()
	dp.unlock(Applejack)
	dp.showMessage("Welcome to Equestria!\n Defend the castle against the parasprites.\n Click on Applejack's icon in the top-right,\n then place her on the screen.\n    (Click this scroll to dismiss it)\n\n-Princess Celestia")

	for i in xrange(5):
		p = Parasprite(dp)
		p.place((-0.1*dp.pWidth*i, 0.1*dp.pHeight))
		dp.addEnemy(p)
	
	prevHealth = dp.health
	while True:
		dp.updateRender()
		if 0 < dp.health <= 15 and not 0 < prevHealth <= 15:
			dp.playMusic('thisIsBad.wav', False)

		prevHealth = dp.health
		if dp.gameOver:
			return
		elif all(not e.alive() for e in dp.enemies):
			break

	dp.showMessage("Good job! Have some more money. More parasprites are coming!")
	dp.setMoney(dp.money + 100)
	
	for i in xrange(10):
		p = Parasprite(dp)
		p.place((-0.1*dp.pWidth*i, 0.1*dp.pHeight))
		dp.addEnemy(p)
	while True:
		dp.updateRender()
		if 0 < dp.health <= 15 and not 0 < prevHealth <= 15:
			dp.playMusic('thisIsBad.wav', False)

		prevHealth = dp.health
		if dp.gameOver:
			return
		elif all(not e.alive() for e in dp.enemies):
			break

	dp.showMovie('RarityIntro-lowRes.mpg')
	dp.setMoney(dp.money + 100)
	dp.unlock(Rarity)
	dp.playMusic('rarityTheme.mp3')
	dp.showMessage('I will no longer send you funds. Please have Rarity search for gems.\n-Celestia')
	
	for i in xrange(20):
		p = Parasprite(dp)
		p.place((-0.1*dp.pWidth*i, 0.1*dp.pHeight))
		dp.addEnemy(p)
	while True:
		dp.updateRender()
		if 0 < dp.health <= 15 and not 0 < prevHealth <= 15:
			dp.playMusic('thisIsBad.wav', False)

		prevHealth = dp.health
		if dp.gameOver:
			return
		elif all(not e.alive() for e in dp.enemies):
			break

	dp.showMessage('Well done. Watch out!')
	for i in xrange(20):
		p = Parasprite(dp)
		p.place((-0.1*dp.pWidth*i, 0.1*dp.pHeight))
		dp.addEnemy(p)
	while True:
		dp.updateRender()
		if 0 < dp.health <= 15 and not 0 < prevHealth <= 15:
			dp.playMusic('thisIsBad.wav', False)

		prevHealth = dp.health
		if dp.gameOver:
			return
		elif all(not e.alive() for e in dp.enemies):
			break

	dp.unlock(Derpy)
	dp.showMessage("Derpy drops anvils on enemies' heads!")
	
	for i in xrange(50):
		p = Parasprite(dp)
		p.place((-0.05*dp.pWidth*i, 0.1*dp.pHeight))
		dp.addEnemy(p)
	while True:
		dp.updateRender()
		if 0 < dp.health <= 15 and not 0 < prevHealth <= 15:
			dp.playMusic('thisIsBad.wav', False)

		prevHealth = dp.health
		if dp.gameOver:
			return
		elif all(not e.alive() for e in dp.enemies):
			break

	#dp.showMovie('PinkieIntro.mpg')
	dp.unlock(Pinkie)
	dp.playMusic('pinkieTheme.mp3')
	dp.showMessage("Pinkie Pie will be useful for groups of enemies. She has a party cannon!")
	for i in xrange(50):
		p = Parasprite(dp)
		p.place((-0.05*dp.pWidth*i, 0.1*dp.pHeight))
		dp.addEnemy(p)
	while True:
		dp.updateRender()
		if 0 < dp.health <= 15 and not 0 < prevHealth <= 15:
			dp.playMusic('thisIsBad.wav', False)

		prevHealth = dp.health
		if dp.gameOver:
			return
		elif all(not e.alive() for e in dp.enemies):
			break

	dp.showMovie("RainbowIntro-lowRes.mpg")
	dp.unlock(Rainbowdash)
	dp.playMusic('rainbowTheme.mp3')
	dp.showMessage("Good luck. :) \n   -Celestia")
	var = 100
	for rnd in xrange(5):
		for i in xrange(var/2):
			p = Parasprite(dp)
			p.place((-dp.pWidth*i*4.0/var, 0.1*dp.pHeight))
			dp.addEnemy(p)
		while True:
			dp.updateRender()
			if 0 < dp.health <= 15 and not 0 < prevHealth <= 15:
				dp.playMusic('thisIsBad.wav', False)

			prevHealth = dp.health
			if dp.gameOver:
				return
			elif all(not e.alive() for e in dp.enemies):
				break
		var *= 2
		dp.showMessage("Next level!")

while True:
	dp.playMusic(os.path.join('mainTheme.mp3'), True)
	option = dp.mainMenu()
	if option == "Play Game":
		playGame()
		if dp.gameOver:
			dp.playMusic(None)
			dp.playMusic('nooooooooooooo.wav', bg=False)
			dp.showMessage("I'm recommending you for remedial study.\nPlease return to Canterlot at once.\n   -Celestia")
		else:
			dp.playMusic(None)
			dp.playMusic('yesyesyes.mp3', bg=False)
			dp.showMessage('Well done.\n-Celestia')
			dp.showCredits()
	elif option == "Credits":
		dp.showCredits()
	elif option == "Quit":
		dp.quitGame()
