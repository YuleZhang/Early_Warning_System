'''
@Author: YuleZhang
@Description: Apriori算法包
@Date: 2020-04-07 17:40:46
'''

class Apriori():
    def __init__(self):
        pass

    # 根据数据集构建最初候选集
    def createC1(self,dataSet):
        C1 = []
        for student in dataSet:
            for subject in student:
                if [subject] not in C1:
                    C1.append([subject])
        return list(map(frozenset,C1))

    # 由候选集生成频繁集
    def generateLk(self,D,Ck,minSupport):
        ssCnt = {} #记录集合的支持数
        for tid in D:
            for can in Ck:
                if can.issubset(tid):
                    ssCnt[can] = ssCnt.get(can,0)+1
        stuNums = float(len(D))
        retList = []
        supportData = {}
        for key in ssCnt.keys():
            support = ssCnt[key] / stuNums
            if support >= minSupport:
                retList.insert(0,key)
            supportData[key] = support
        return retList,supportData
    
    # 根据频繁集重新生成候选集
    def generateCk(self,Lk,k):
        lenLk = len(Lk)
        candidate = []
        for i in range(lenLk):
            for j in range(i+1,lenLk):
                L1 = Lk[:k-2]
                L2 = Lk[:k-2]
                L1.sort()
                L2.sort()
                # 若L1和L2之前的其他项都一致，就合并
                if L1 == L2:
                    newSubset = Lk[i] | Lk[j]
                    candidate.append(newSubset)
        return candidate

    # apriori的核心，即不断生成频繁集候选集
    def apriori(self,dataSet,minSupport):
        D = list(map(set,dataSet))
        C1 = self.createC1(dataSet)
        L1,supportData = self.generateLk(D,C1,minSupport)
        k = 2
        L = [L1]
        while len(L[k-2])> 0: # 直到没有新的频繁集为止  
            Ck = self.generateCk(L[k-2],k)
            Lk,subk = self.generateLk(D,Ck,minSupport)
            supportData.update(subk)
            L.append(Lk)
            k+=1
        return L,supportData

        # 从频繁项集挖掘关联规则
        # def generateRules(self,L,supportData,minConf=0.7):
    
    def generateRules(self,L,supportData,minConf=0.7):
        bigRuleList = []
        for i in range(1,len(L)):
            for freqSet in L[i]:
                H1 = [frozenset([item]) for item in freqSet]
                if i > 1:
                    self.rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf)
                else:
                    self.calConf(freqSet,H1,supportData,bigRuleList,minConf)
        return bigRuleList
                    
    def calConf(self,freqSet,H,supportData,brl,minConf=0.7):
        prunedH = []
        for conseq in H:
            if len(freqSet)>2 or len(freqSet-conseq)<1 or supportData.get(freqSet-conseq,0)==0: continue
            conf = supportData[freqSet] / supportData[freqSet-conseq]
            if conf>=minConf:
                # print(freqSet-conseq,'-->',conseq,'conf:',conf)
                flag = True
                for item in brl:
                    if item[0] == conseq and item[1] == freqSet-conseq:
                        flag = False
                if flag:
                    brl.append([freqSet-conseq,conseq,conf])
                    prunedH.append(conseq)
        return prunedH

    # 关联规则合并
    def rulesFromConseq(self,freqSet,H,supportData,brl,minConf=0.7):
        m = len(H[0])
        if len(freqSet) > (m+1): #查看频繁集freqSet是否可以大到溢出大小为m的子集
            Hmpl = self.generateCk(H,m+1) # 从Hm合并Hm+1
            Hmpl = self.calConf(freqSet,Hmpl,supportData,brl,minConf)
            if len(Hmpl) > 1: #若合并后的Hm+1的元素大于1个，则继续合并
                self.rulesFromConseq(freqSet,Hmpl,supportData,brl,minConf)


if __name__ == "__main__":
    dataset  = [['高等数学','英语','大物'],['高等数学','线性代数','大物']]
    apr = Apriori()
    C1=apr.createC1(dataset)
    D=list(map(set,dataset))
    L1,supportData0=apr.generateLk(D,C1,0.5)
    L,supportData=apr.apriori(dataset,minSupport=0.5)
    rules=apr.generateRules(L,supportData,minConf=0.8)
    print(rules)
    # print(L)
    # print(supportData)


