def invert(staramatrica, duzina, sirina):
    novamatrica = []
    for i in range(duzina):
        novamatrica.append([])
    for i in range(duzina):
        
        for j in range(sirina): 
            try:
                novamatrica[i].append(staramatrica[j][i])
            except IndexError:
                novamatrica[i].append(None)
    return novamatrica
#l = [[14,66,47],[58,49,36]]
#print(invert(l,3,2))