import pandas as pd
import itertools
import matplotlib.pyplot as plt

class Arules:
  total=[]
  transactions=[]
  freq_1={}
  def __init__(self):
    ...
  def exploratory_analysis(self,transactions,
                           min_support,
                           minconfidence=None):
      candidates = dict()
      large = dict()
      c = 0
      i = 0

      while (True):
          if i == 0:
              if c == len(df):
                  break

          if transactions.loc[c][i] != 0:
              if transactions.loc[c][i] not in candidates.keys():
                  candidates[transactions.loc[c][i]] = 1
                  i += 1
              elif transactions.loc[c][i] in candidates.keys():
                  candidates[transactions.loc[c][i]] += 1
                  if candidates[transactions.loc[c][i]] / len(df) > min_support:

                      arrr = []
                      arrr.append(transactions.loc[c][i])
                      large[tuple(arrr)] = candidates[transactions.loc[c][i]]

                  i += 1
          if i == len(transactions.loc[c]) or transactions.loc[c][i] == 0:
              i = 0
              c += 1

     # names = list(large.keys())
      values = list(large.values())
      plt.plot( values)
      plt.show()
      self.freq_1=large
      return large

  def get_frequent_item_sets(self,
                transactions,
                min_support,
                min_confidence=None):
     self.transactions = transactions

     large=dict()


     large=self.freq_1
     arr = []
     k=2
     while(True):
       self.total.append(large)
       if k==2:
         candidates = dict()

         #arr = list(large.keys())
         arr=list(large.keys())
         arr.sort()
         large = dict()

         for i in range(0, len(arr)):
             for j in range(i + 1, len(arr)):
                 candidates[tuple([arr[i][0],arr[j][0]])] = 0

         for c in range(0, len(df)):
             arr2 = []
             for i in range(0, len(transactions.loc[c])):
                 if transactions.loc[c][i]==0:
                     break
                 elif transactions.loc[c][i] != 0:
                     arr2.append(transactions.loc[c][i])
             arr2.sort()
             for x in range(0, len(arr2)):
                 for y in range(x + 1, len(arr2)):
                     if (arr2[x], arr2[y]) in candidates.keys():
                         candidates[(arr2[x], arr2[y])] += 1
                         if candidates[tuple([arr2[x], arr2[y]])] / len(df) > min_support:
                             large[(arr2[x],arr2[y])]=candidates[(arr2[x],arr2[y])]
         k+=1
       elif k>2:

           candidates=dict()
           arr = list(large.keys())
           arr.sort()
           large=dict()
           for i in range(0,len(arr)):
               for j in range(i+1,len(arr)):
                   if arr[i][0:k-2]==arr[j][0:k-2]:
                       arr_prim=[]
                       for n in arr[i]:
                            arr_prim.append(n)
                       arr_prim.append(arr[j][k-2])

                       candidates[tuple(arr_prim)]=0

           for c in range(0, len(df)):
               arr2 = []
               for i in range(0, len(transactions.loc[c])):
                   if transactions.loc[c][i] == 0:
                       break
                   elif transactions.loc[c][i] != 0:
                       arr2.append(transactions.loc[c][i])
               arr2.sort()
               it=list(itertools.combinations(arr2, k))

               for u in it:
                   if u in candidates.keys():
                       candidates[u]+=1
                       if candidates[u]/len(df)>min_support:
                           large[u]=candidates[u]

           k+=1
           if len(large.keys())==0:
               return self.total


  def get_arules(self,min_support=None,
          min_confidence=None,
          min_lift=None,
          sort_by='lift'):

    sup = dict()
    conf = dict()
    lf = dict()
    for i in range(1,len(self.total)):
        for x in self.total[i].keys():

            iter_list=[]
            iter_list=list(itertools.combinations(list(x),1))
            for it in iter_list:

                it_prim=[]
                for b in x:

                    if b != it[0]:
                        it_prim.append(b)
                        it_prim.sort()

                it_str = str(str(it_prim) + " -> " + str(it))
                if ((self.total[i][tuple(x)] / len(self.transactions))>min_support) and ((self.total[i][tuple(x)]/self.total[i-1][tuple(it_prim)]) > min_confidence) and (((len(self.transactions)*self.total[i][tuple(x)])/(self.total[i-1][tuple(it_prim)]*self.total[0][tuple(it)])) >min_lift):
                    sup[it_str]=round(self.total[i][tuple(x)]/len(self.transactions),10)

                    conf[it_str]=round(self.total[i][tuple(x)]/self.total[i-1][tuple(it_prim)],10)

                    lf[it_str]=round((len(self.transactions)*self.total[i][tuple(x)])/(self.total[i-1][tuple(it_prim)]*self.total[0][tuple(it)]),10)

    def dic_sort(d):
        dic_arr=[]
        sorted_vals=list(d.values())
        sorted_vals.sort()
        sorted_vals.reverse()
        for val in sorted_vals:
            dicc=dict()
            for k , v in d.items():
                if v==val:
                    dicc[k]=v
                    dic_arr.append(dicc)
                    break
        return dic_arr

    if sort_by=='lift':
       return dic_sort(lf)
    if sort_by=='conf':
        return dic_sort(conf)
    if sort_by=='sup':
       return dic_sort(sup)


df = pd.read_csv (r'.\shop2.csv')
df.fillna(0, inplace = True)
a=Arules()
print("------ ITEM FREQUENCY -------")
print(a.exploratory_analysis(transactions=df,min_support=0.005))

print("------- SORTED FREQUENT SETS -------")
print(a.get_frequent_item_sets(transactions=df , min_support=0.005))

print("------- SORTED RULES BY THEIR LIFT --------")

llll=a.get_arules(min_support=0.005 ,
                  min_confidence=0.2,
                  min_lift=0)
print(llll)
p_v=[]
p_k=[]
for v in range(0,len(llll)):
    s=llll[v].keys()
    p_k.append(list(s)[0])
    ss=llll[v].values()
    p_v.append(list(ss)[0])


plt.plot(p_k, p_v)
plt.show()
