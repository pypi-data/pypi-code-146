from meshgrid.visualizers.notebook import NotebookVisualizer

class NotebookPlayer:
    '''The top-level class to run Meshgrid games within Jupyter Notebooks
    
    :GameClass: A Meshgrid-friendly game class
    '''

    def __init__(self,GameClass,**kwargs):
        
        self.game = GameClass(**kwargs)
        self.viz = NotebookVisualizer(**kwargs)
        self.viz.bind_game(self.game)
        
    def play(self):
        '''Run one full session of the game, with a visualization.'''
        
        self.viz.display()
        
    def headless(self):
        '''Run one full session of the game, without any visualization.'''
        
        while True:
            done = self.game.step()
            if done:
                break 
