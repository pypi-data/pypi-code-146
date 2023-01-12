def descending_orderfunc():
  intlist = []
  intlistTot = int(input("Total Number of List Items to Sort = "))

  for i in range(1, intlistTot + 1):
          intlistvalue = int(input("Please enter the %d List Item = "  %i))
          intlist.append(intlistvalue)

  intlist.sort()
  intlist.reverse()

  print('List Items After Sorting in Descending Order')
  print(intlist)
