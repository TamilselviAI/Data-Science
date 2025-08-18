class Univariate():
    
    def quanqual(dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            #print(columnName)
            if(dataset[columnName].dtype=='O'):
                #print("qual")
                qual.append(columnName)
            else:
                #print("quan")
                quan.append(columnName)
        return quan,qual

    def univariate(dataset,quan):
        descriptive= pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q1:50%","Q1:75%","Q1:100%","IQR","1.5 Rule","Lesser","Greater","Min","Max"],columns=quan)
        for ColumnName in quan:
            descriptive.loc["Mean",ColumnName]=dataset[ColumnName].mean()
            descriptive.loc["Median",ColumnName]=dataset[ColumnName].median()
            descriptive.loc["Mode",ColumnName]=dataset[ColumnName].mode()[0]
            descriptive.loc["Q1:25%",ColumnName]=dataset.describe()[ColumnName]["25%"]
            descriptive.loc["Q1:50%",ColumnName]=dataset.describe()[ColumnName]["50%"]
            descriptive.loc["Q1:75%",ColumnName]=dataset.describe()[ColumnName]["75%"]
            #descriptive.loc["Q1:99%",ColumnName]=dataset.describe()[ColumnName]["99%"]
            descriptive.loc["Q1:100%",ColumnName]=dataset.describe()[ColumnName]["max"]
             ## IQR
            descriptive.loc["IQR",ColumnName]=dataset.describe()[ColumnName]["75%"] - dataset.describe()[ColumnName]["25%"]
            descriptive.loc["1.5 Rule",ColumnName]= 1.5 * descriptive.loc["IQR",ColumnName]
            descriptive.loc["Lesser",ColumnName]=dataset.describe()[ColumnName]["25%"] - descriptive.loc["1.5 Rule",ColumnName]
            descriptive.loc["Greater",ColumnName]=dataset.describe()[ColumnName]["75%"] + descriptive.loc["1.5 Rule",ColumnName]
            descriptive.loc["Min",ColumnName]=dataset[ColumnName].min()
            descriptive.loc["Max",ColumnName]=dataset[ColumnName].max()
        return descriptive

    def freqTable(ColumnName,dataset):
        freqTable=pd.DataFrame(columns=["Unique_Values","Frequency","Relative Frequency","Cusum"])
        freqTable["Unique_Values"]=dataset[ColumnName].value_counts().index
        freqTable["Frequency"]=dataset[ColumnName].value_counts().index
        freqTable["Relative Frequency"]=(freqTable["Frequency"]/103)
        freqTable["Cusum"]=freqTable["Relative Frequency"].cumsum()
        return freqTable

    lesser=[]
    greater=[]
    def findoutlier():
        for columnName in quan:
            if (descriptive.loc["Min"][columnName]<descriptive.loc["Lesser"][columnName]):
                lesser.append(columnName)
            if (descriptive.loc["Max"][columnName]>descriptive.loc["Greater"][columnName]):
                greater.append(columnName)
        return ()

    def replaceoutlier(ColumnName,dataset):
        for ColumnName in lesser:
            dataset[ColumnName][dataset[ColumnName]<descriptive.loc["Lesser",ColumnName]] = descriptive.loc["Lesser",ColumnName]
        for ColumnName in greater:
            dataset[ColumnName][dataset[ColumnName]>descriptive.loc["Greater",ColumnName]] = descriptive.loc["Greater",ColumnName]
        return(ColumnName,dataset)