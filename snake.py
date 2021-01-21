import pygame as pg
import sys
import random

#вывод текста
pg.font.init()
def draw_text(surf, text, size, x, y):
    font = pg.font.SysFont('arial', size)
    text = font.render(text, True, [200,200,200])
    surf.blit(text, [x,y])

#проверка на смерть
def IsDead(head, body, poisonFruit):	
	for i in body:
		if((head[0] == i[0] and head[1] == i[1]) or (head[0] >= 600 or head[0] <= 0 or head[1] >= 600 or head[1] <= 0)):
			return True
		if(head[0] == poisonFruit[0] and head[1] == poisonFruit[1]):
			return True
	return False

#перемещение змеи
def move(body, head):
	new_x = body[-2][0]
	new_y = body[-2][1]
	new_part = [new_x, new_y]
	i = len(body)-1
	while i >= 1:			
		body[i][0] = new_x
		body[i][1] = new_y
		new_x = body[i-2][0]
		new_y = body[i-2][1]
		i -= 1
	body[0][0] = head[0]
	body[0][1] = head[1]
	return body, new_part
#начало новой игры
def new_game():
	head = [180,180]
	body = [[160,180],[140,180],[120,180]]
	new_part = []
	score = 0
	death = False
	fruits()
	return head, body, new_part, score, death
#генерация новых фруктов
def fruits():
	fruit = [random.randint(1,29)*box, random.randint(1,29)*box]
	poisonFruit = fruit
	while fruit == poisonFruit:
		poisonFruit = [random.randint(1,29)*box, random.randint(1,29)*box]
	return fruit, poisonFruit


#инициализация окна
size = [600,600]
window = pg.display.set_mode(size)
pg.display.set_caption('snek!')
screen = pg.Surface(size)
box = 20

#инициализация змеи
snek = pg.Surface([box,box])
snek.fill([255,255,255]) 
head, body, new_part, score, death = new_game()

#инициализация фрукта и ядовитого фрукта
fruitIMG = pg.Surface([box,box])
fruitIMG.fill([255,255,0])

poisonFruitIMG = pg.Surface([box,box])
poisonFruitIMG.fill([0,255,0])

fruit, poisonFruit = fruits()

#направление движения
direction = "RIGHT"
to = "RIGHT"


running = True
while running:
	for e in pg.event.get():
		if e.type  == pg.QUIT:
			running = False
		elif e.type == pg.KEYDOWN:
			#управление
			if e.key == ord('w'):
				to = "UP"
			if e.key == ord('s'):
				to = "DOWN"
			if e.key == ord('a'):
				to = "LEFT"
			if e.key == ord('d'):
				to = "RIGHT"
			if e.key == ord('n') and death == True:
				head, body, new_part, score, death = new_game()
				snek.fill([255,255,255])
				fruit, poisonFruit = fruits()
				direction = "RIGHT"
				to = "RIGHT"
		#проверка направления движения
		if(to == "UP" and direction != "DOWN"):
			direction = "UP"
		if(to == "DOWN" and direction != "UP"):
			direction = "DOWN"
		if(to == "RIGHT" and direction != "LEFT"):
			direction = "RIGHT"
		if(to == "LEFT" and direction != "RIGHT"):
			direction = "LEFT"



	#перемещение
	if direction == "UP" and death == False:		
		body, new_part = move(body, head)
		head[1] -= box
	if direction == "RIGHT" and death == False:		
		body, new_part = move(body, head)
		head[0] += box
	if direction == "LEFT" and death == False:
		body, new_part = move(body, head)
		head[0] -= box
	if direction == "DOWN" and death == False:		
		body, new_part = move(body, head)
		head[1] += box
	#сьеден фрукт
	if(head[0] == fruit[0] and head[1] == fruit[1]):
		score+=1
		fruit, poisonFruit = fruits()
		body.append(new_part)

	#смерть
	death = IsDead(head, body, poisonFruit)
	if death:
		snek.fill([255,0,0])
		

	
	#отрисовка
	screen.fill([0, 0, 0])
	screen.blit(poisonFruitIMG, poisonFruit)
	screen.blit(snek, head)
	for i in range(len(body)):
		screen.blit(snek, body[i])
	screen.blit(fruitIMG,fruit)
	if(death):
		draw_text(screen, "You lose!", 40, 200, 200)
		draw_text(screen, "you score: " + str(score) +"!", 40, 180, 250)
		draw_text(screen, "press N for new game!", 40, 130, 300)
	else:
		draw_text(screen, str(score), 20, 300, 10)		
	window.blit(screen, [0,0])
	pg.display.flip()
	pg.time.delay(150)

pg.quit()