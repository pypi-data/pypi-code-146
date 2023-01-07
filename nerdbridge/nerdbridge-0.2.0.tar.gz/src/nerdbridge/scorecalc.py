
BASIS_PUNTEN =  {'k': 20, 'r': 20, 'h': 30, 's': 30, 'a': 40}
SLAG_PUNTEN =   {'k': 20, 'r': 20, 'h': 30, 's': 30, 'a': 30}
MANCHE_PUNTEN = [ 300, 500 ]
SLEM_PUNTEN =   [ 500, 750 ]
DOWN_PUNTEN = [ [ 100, 200, 200, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300 ],   # niet kwetsbaar
                [ 200, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300 ] ]  # kwetsbaar

# let op! De bonus voor het maken van een ge-redoubleerd contract is 100 punten.
# Dit is anders ten opzichtte van "Bridge, het leerplan voor de complete bridger"
# van Ceest Sint, 1984, waar maar 50 punten worden toegekend.

def bridgecalc(contract, overslagen=0, kwetsbaar=0, doublet=0):
    '''
    contract is een string (bv. '1sa')
    overslagen is 0 voor contract precies gemaakt en negatief voor downslagen, 
    kwetsbaar = 0,1
    doublet = 0,1,2
    '''

    ck = contract[-1].lower()   # contractkleur
    cs = int(contract[0])       # contractslagen
    os = overslagen
    kw = kwetsbaar
    db = doublet

    # contract gehaald
    if os >= 0:

        # basis punten
        pt = (BASIS_PUNTEN[ck] + (cs-1) * SLAG_PUNTEN[ck]) * 2**db

        # manche bonus
        if pt >= 100:
            pt = pt + MANCHE_PUNTEN[kw]
        else:
            pt = pt + 50

        # db bonus
        pt = pt + 50 * db

        # slem bonus
        if cs >= 6:
            pt = pt + SLEM_PUNTEN[kw] * 2**(cs-6)

        # overslagen
        if db == 0:
            pt = pt + os * SLAG_PUNTEN[ck]
        else:
            pt = pt + os * 100 * 2**kw * 2**(db-1)

    # contract niet gehaald
    else:

        if db == 0:
            pt = os * 50 * 2**kw
        else:
            pt = -1 * sum(DOWN_PUNTEN[kw][0:abs(os)]) * 2**(db-1)

    return pt


def table(overslagen=0):

    os = overslagen
    table = []

    Kl = ['k', 'h', 'sa']
    Ks = ['K/R', 'H/S', 'SA ']
    
    print('      |    niet-kwetsbaar     |       kwetsbaar       |')
    print('      |       | Doub. |  Red. |       | Doub. |  Red. |')
    print('-------------------------------------------------------')

    for N in range(1,8):
        for K in range(3):
            row = []
            for W in range(2):
                for D in range(3):
                    if (6 + N + os) > 13 or (6 + N + os) < 0:
                        row.append(0)
                    else:
                        row.append(bridgecalc('%d%s' % (N,Kl[K]), os, W ,D))
            print(' %1d%3s ' % (N,Ks[K]) + '| %5d | %5d | %5d | %5d | %5d | %5d |' % tuple(row))
            table.append(row)

