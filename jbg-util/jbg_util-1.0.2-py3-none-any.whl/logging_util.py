from pathlib import Path
class AnsiEscapes:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

class Logger:
    SECTION_DIVIDER_WIDTH=50
    
    def __init__(self,file_path=None,should_print_to_screen=False):
        self.file_path=None
        if file_path is not None:
            self.file_path = file_path
            Path(file_path).parent.mkdir(parents=True, exist_ok=True) #ensure the directory exists
                
        self.should_print_to_screen = should_print_to_screen
        
    def empty_log(self):
        if self.file_path is None:
            return
        with open(self.file_path,'wt',encoding='utf-8') as f:
            f.write('')

    def log_colored(self,color,*strs):
        colored_strs=[]
        for s in strs:
            s = f"{color}{s}{AnsiEscapes.ENDC}"
            colored_strs.append(s)
        
        if self.should_print_to_screen:
            print(*colored_strs)
            
        if self.file_path is not None:
            with open(self.file_path,'at',encoding='utf-8') as f:
                f.write(' '.join(strs)+'\n')

    def success(self,*s):
        self.log_colored(AnsiEscapes.GREEN,*s)

    def error(self,*s):
        self.log_colored(AnsiEscapes.RED,*s)

    def warning(self,*s):
        self.log_colored(AnsiEscapes.YELLOW,*s)

    def info(self,*s):
        self.log_colored(AnsiEscapes.CYAN,*s)

    def primary(self,*s):
        self.log_colored(AnsiEscapes.BLUE,*s)

    def secondary(self,*s):
        self.log_colored(AnsiEscapes.PURPLE,*s)
        
    def bold(self,*s):
        self.log_colored(AnsiEscapes.BOLD,*s)
        
    def underline(self,*s):
        self.log_colored(AnsiEscapes.UNDERLINE,*s)
        
    def log(self,*s):
        self.log_colored(AnsiEscapes.WHITE,*s)
        
    def section_header(self,title,text_color : AnsiEscapes = AnsiEscapes.WHITE, divider_color : AnsiEscapes = AnsiEscapes.WHITE):
        divider = ''.join(['*' for _ in range(0,Logger.SECTION_DIVIDER_WIDTH)])
        double_divider = divider+'\n'+divider
        self.log_colored(divider_color,'\n'+double_divider)
        self.log_colored(text_color,title)
        self.log_colored(divider_color,double_divider)
        
    def subsection_header(self,title,text_color : AnsiEscapes = AnsiEscapes.WHITE, divider_color : AnsiEscapes = AnsiEscapes.WHITE):
        divider = ''.join(['-' for _ in range(0,Logger.SECTION_DIVIDER_WIDTH)])
        self.log_colored(divider_color,'\n'+divider)
        self.log_colored(text_color,title)
        self.log_colored(divider_color,divider)