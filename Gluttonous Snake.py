import pygame,sys,time,random,math
from pygame.locals import *

#颜色
redColor = pygame.Color(255,0,0)
brickredColor = pygame.Color(244,119,89)
lightgreenColor = pygame.Color(0,255,0)
darkgreenColor = pygame.Color(0,125,0)
blueColor = pygame.Color(0,0,255)
blackColor = pygame.Color(0,0,0)
whiteColor = pygame.Color(255,255,255)
lightgreyColor = pygame.Color(175,175,175)
darkgreyColor = pygame.Color(50,50,50)
          
#主函数
def main():
     #初始化
     pygame.init()
     fpsClock = pygame.time.Clock()

     #创建显示层
     playSurface = pygame.display.set_mode((360,640))
     pygame.display.set_caption('Gluttonous Snake')

     
     #初始化变量
     snakePosition = [130,240] #贪吃蛇：蛇头的位置
     snakeSegments = [snakePosition] #贪吃蛇：蛇的身体（初始为一个单位）
     raspberryPosition = [230,400] #树莓的初始位置
     bonusberryPosition = [180,320] #奖励莓的初始位置
     raspberrySpawned = 1 #树莓状态为已生成
     bonusberrySpawned = 1 #奖励莓状态为已生成
     bonused = False #默认设置奖励莓未被吃掉
     direction = 'right' #初始方向为右
     changeDirection = direction #改变方向
     score = 0 #得分
     num = 0 #总计吃掉树莓的个数
     block = [] #障碍
     bonusStart = 0 #奖励莓起始时间
     bunusEnd = 0 #奖励莓被吃掉的时间
     getStart = False #是否已获取起始时间
    
     #游戏底层逻辑
     while True:
         for event in pygame.event.get():
             if event.type == QUIT:
                 pygame.quit()
                 sys.exit()
                 
         #判断键盘事件
             elif event.type == KEYDOWN:
                 if event.key == K_RIGHT or event.key == ord('d'):
                     changeDirection = 'right'
                 if event.key == K_LEFT or event.key == ord('a'):
                     changeDirection = 'left'
                 if event.key == K_UP or event.key == ord('w'):
                     changeDirection = 'up'
                 if event.key == K_DOWN or event.key == ord('s'):
                    changeDirection = 'down'
                 if event.key == K_ESCAPE:
                     pygame.event.post(pygame.event.Event(QUIT))
                     
         #判断是否输入了反方向
         if changeDirection == 'right' and not direction == 'left':
            direction = changeDirection
         if changeDirection == 'left' and not direction == 'right':
             direction = changeDirection
         if changeDirection == 'up' and not direction == 'down':
             direction = changeDirection
         if changeDirection == 'down' and not direction == 'up':
             direction = changeDirection
             
         #根据方向移动蛇头的坐标
         if direction == 'right':
             snakePosition[0] += 10
         if direction == 'left':
             snakePosition[0] -= 10
         if direction == 'up':
             snakePosition[1] -= 10
         if direction == 'down':
             snakePosition[1] += 10
             
         #增加蛇的长度
         snakeSegments.insert(0,list(snakePosition))
                 
         #判断是否吃掉了树莓
         if snakePosition[0] == raspberryPosition[0] and snakePosition[1] == raspberryPosition[1]:
             raspberrySpawned = 0
         else:
             snakeSegments.pop()
             
         #如果吃掉树莓，则重新生成
         if raspberrySpawned == 0:
             bonused = False
             x = random.randrange(1,36)
             y = random.randrange(1,64)
             raspberryPosition = [int(x*10),int(y*10)]
             raspberrySpawned = 1
             score += int(speed)
             num += 1
             
         #判断是否吃掉了奖励莓
         if num > 0 and (num+1)%5 == 0:
             if ((snakePosition[0] == bonusberryPosition[0] and snakePosition[1] == bonusberryPosition[1]) or \
                (snakePosition[0] == bonusberryPosition[0]-10 and snakePosition[1] == bonusberryPosition[1]) or \
                (snakePosition[0] == bonusberryPosition[0] and snakePosition[1] == bonusberryPosition[1]-10) or \
                (snakePosition[0] == bonusberryPosition[0]-10 and snakePosition[1] == bonusberryPosition[1]-10)):
                    bonusberrySpawned = 0
         
         #如果吃掉奖励莓，则重新生成
         if bonusberrySpawned == 0 and bonused == False:
             bonusEnd = time.time()
             bonused = True
             getStart = False
             x = random.randrange(1,36)
             y = random.randrange(1,64)
             bonusberryPosition = [int(x*10),int(y*10)]   
             bonusberrySpawned = 1
             score += int(math.exp(7-(bonusEnd-bonusStart)))

             
         #绘制显示层：分数
         playSurface.fill(blackColor)
         scoreFont = pygame.font.SysFont('arial.ttf',54)
         scoreSurf = scoreFont.render('Score:'+str(score), True, darkgreyColor)
         scoreRect = scoreSurf.get_rect()
         scoreRect.midtop = (180, 320)
         playSurface.blit(scoreSurf, scoreRect)
         
         #绘制显示层：贪吃蛇与食物
         pygame.draw.rect(playSurface,lightgreenColor,(snakePosition[0],snakePosition[1],10,10))               
         for position in snakeSegments[1:]:
             pygame.draw.rect(playSurface,darkgreenColor,Rect(position[0],position[1],10,10))
         pygame.draw.circle(playSurface,redColor,(raspberryPosition[0]+5, raspberryPosition[1]+5),5)
         if(num+1)%5 == 0 and bonused == False:
             pygame.draw.circle(playSurface,blueColor,(bonusberryPosition[0],bonusberryPosition[1]),10)
             bonusFont = pygame.font.SysFont('arial.ttf',54)
             bonusSurf = bonusFont.render('bonus!', True, whiteColor)
             bonusRect = bonusSurf.get_rect()
             bonusRect.midtop = (180, 480)
             playSurface.blit(bonusSurf, bonusRect)
             if getStart == False:
                 bonusStart=time.time()
                 getStart = True
             
         #绘制显示层：障碍
         for position in block:
             pygame.draw.rect(playSurface,brickredColor,(position[0],position[1],10,10))
             
         #刷新显示层
         pygame.display.flip()
         
         #死亡判定
         if snakePosition[0] > 350 or snakePosition[0] < 0:
             gameOver(playSurface,score)
         if snakePosition[1] > 630 or snakePosition[1] < 0:
             gameOver(playSurface,score)
         for snakeBody in snakeSegments[1:]:
            if snakePosition[0] == snakeBody[0] and snakePosition[1] == snakeBody[1]:
                gameOver(playSurface,score)
         for position in block:
            if snakePosition[0] == position[0] and snakePosition[1] == position[1]:
                gameOver(playSurface,score)
                
         #控制贪吃蛇速度
         speed = 5+2*math.sqrt(num)
         fpsClock.tick(speed)


#游戏结束函数
def gameOver(playSurface,score):
     for i in range(0,5):
          gameOverFont = pygame.font.SysFont('arial.ttf',54)
          gameOverSurf = gameOverFont.render('Game Over!', True, lightgreyColor)
          gameOverRect = gameOverSurf.get_rect()
          gameOverRect.midtop = (180, 160)
          playSurface.blit(gameOverSurf, gameOverRect)

          respawnFont = pygame.font.SysFont('arial.ttf',32)
          respawnSurf = respawnFont.render('Respawning in '+str(5-i)+'...', True, lightgreyColor)
          respawnRect = respawnSurf.get_rect()
          respawnRect.midtop = (180, 200)
          playSurface.blit(respawnSurf, respawnRect)
      
          scoreFont = pygame.font.SysFont('arial.ttf',54)
          scoreSurf = scoreFont.render('Score:'+str(score), True, lightgreyColor)
          scoreRect = scoreSurf.get_rect()
          scoreRect.midtop = (180, 320)
          playSurface.blit(scoreSurf, scoreRect)

          pygame.display.flip()
          time.sleep(1)
          playSurface.fill(blackColor,respawnRect)
        
     main()   
     

if __name__ == "__main__":
    main()
