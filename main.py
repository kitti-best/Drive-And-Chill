from Game import *
from Stack import Stack
from Menu import *
from Score import *
from Summary import *

# create a stack for running each state
state = Stack()
state.add(Menu())

delta = 1
if __name__ == '__main__':
    RUNNING = 1
    while RUNNING:
        SCREEN.fill(JADE)
        pygame.display.set_caption("Drive And Chill")

        if state.seek().id == "menu":
            if state.seek().nextState == 1:
                game = Game()
                state.add(game)
            elif state.seek().nextState == 2:
                state.add(Score())
            elif state.seek().nextState == 3:
                pygame.quit()

        elif state.seek().id == "score":
            if state.seek().nextState == 1:
                state.pop()

        elif state.seek().id == "game":
            if state.seek().nextState == 1:
                state.pop()
            if state.seek().nextState == 2:
                finishTravel = [state.seek().travel,state.seek().travelString]
                finishTime = state.seek().timeString
                state.pop()
                state.add(Summary(finishTravel,finishTime))

        elif state.seek().id == "summary":
            if state.seek().nextState == 1:
                state.pop()
                state.add(Score())

        # run top most state
        state.seek().run(delta)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                RUNNING = 0
                exit()
                pygame.quit()

        pygame.display.update()
        delta = CLOCK.tick(FPS)/1000