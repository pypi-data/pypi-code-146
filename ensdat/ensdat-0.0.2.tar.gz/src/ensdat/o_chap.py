def o_chap( str : str, sleept : float = 0.1 ) -> str :
    '''
    o_chap(str, sleept) ---> only str
    if str is 'abc', sleept is 0.1, 
        #-0.1 sec later-
            printed `'a'`
        #-0.2 sec later-
            printed `'ab'`
        #-0.3 sec later-
            printed `'abc'` and return 0

    '''
    try :
        from time import sleep
        for i in str :
            print(i, end = '')
            sleep(sleept)
        return 0
    except TypeError : 
        TypeError("only str")
        return 1
    except : 
        TypeError("unexpected error")
        return -1
    finally :
        print(end='\n')

