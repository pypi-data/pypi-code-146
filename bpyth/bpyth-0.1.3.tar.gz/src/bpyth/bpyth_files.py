
import os, pickle, warnings

#, sys, time, random, string, re, datetime

 
    
#############################################################################################################
###
### Permanence
###
#############################################################################################################    


def dump_pickle( anything, filename ):
    '''
    open, dump, close
    '''
    f = open(filename,'wb')
    try:
        pickle.dump( anything, f )
    finally:
        f.close()
        
        
    
def load_pickle( filename ):  
    '''
    open, load, close
    '''    
    f = open(filename,'rb')
    result = None
    #try:
    result = pickle.load(f)
    #finally:
    f.close()
    return result






            

class StreamFiles(object):
    '''Iterable, returns all filenames of a parent directory.
       Instantiation with 
       * a path which is traversed recursively
       * a file extension. All other files will be igorated.    
    '''

    # Instanziierung mit 
    # * einem Pfad, der rekursiv durchlaufen wird
    # * einer Dateiendung. Alle anderen Dateien werden igoriert.
    #
    def __init__(self, _path, _extension ):
        self.path = _path
        self.extension = _extension            

        
    # Streamt einen Dateinamen   
    #
    def __iter__(self):
        for verzeichnis, egal_subdirs, dateien in os.walk(self.path):  
            dateien.sort()
            for fname in dateien:
                if not fname.endswith(self.extension) :
                    continue          
                fname_full = os.path.join(verzeichnis, fname)            # Dateiname der Quell-Datei  
                yield fname_full


StreamDateien = StreamFiles

                
                

class StreamLines(object):
    '''Iterable, returns all lines of a text file'''

    # Instanziierung mit einem vollständigen Dateipfad
    #
    def __init__(self, _filename ):
        self.filename = _filename
         

    # Streamt die Datei Zeile für Zeile    
    #
    def __iter__(self):
        # Einzelne Sätze liefern
        for zeile in open(self.filename):
            yield zeile

            
StreamZeilen = StreamLines            
            
    
    

def path_join(basepath, supplement, test='ignore'):
    '''
    Joins two parts of a path and optionally tests if the path exists.
    basepath:   a path
    supplement: path to join in forward slash notation.
    test:       should it be checked if the path exists? If yes, set it to 'warn' or 'raise'.   
    '''
    if supplement.endswith('/'):
        supplement = supplement[:-1]
    parts = tuple(supplement.split('/'))
    result = os.path.join( basepath, *parts)
    
    if test == 'warn':
        if not os.path.exists( os.path.dirname(result) ): 
            warnings.warn('Directory does not exist: ' + result) 
        if not os.path.exists( result ): 
            warnings.warn('Path does not exist: ' + result) 
            
    elif test == 'raise':
        if not os.path.exists( os.path.dirname(result) ): 
            raise Exception('Directory does not exist: ' + result) 
        if not os.path.exists( result ): 
            raise Exception('Path does not exist: ' + result)             
    
    return result