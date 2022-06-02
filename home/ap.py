def toBinary(a):
  m=[]
  for i in a:
    c = bin(ord(i))[2:]
    n = 8-len(c)
    c = ('0'*n)+c
    m.append(c)
  return m
def split(b,n=2):
   ret = [] 
   for a in b:
     for i in range(0,8,n):
       part = a[i:i+n]
       ret.append(part)
   return ret
def merge(a):
  ret = []
  while(a):
    n,txt = 4,''
    while(a and n):
      txt = txt + a.pop(0)
      n=n-1
    ret.append(txt)
  return ret
def text(a):
  ret =''
  for b in a:
    intt = int(b,2)
    schr = chr(intt)
    ret += schr
  return ret
