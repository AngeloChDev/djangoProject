

def maketot_dict(in_str):
      out=dict()

      if isinstance(in_str,str):
            if "null" in in_str:
                  in_str= in_str.replace("null", '')
            if len(in_str)>2:
                  in_tolist= in_str.split(',')
                  for x in in_tolist:
                        out[x[0]] = x[1:]

      return out       

def full_dict(winers:list, out:dict):
      for winer in winers:
            if winer not in out.keys():
                  out[winer]={'w':0, 'p':0}
            if len(winers)>1:
                  out[winer]['p'] += 1
            else:
                  out[winer]['w'] += 1

      return out