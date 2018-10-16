import sys
import pandas as pd
import matplotlib.pyplot as plt
 

def plot_dr_ratio(portfolio_index, dr):
    """
	:param portfolio_index: pandas Dataframe object of the portfolio index
	:param dr: pandas Dataframe object of the DR ratio
	"""

    # due to the size of data and computer memory, using loop or moving window to show graph
    Beg=0
    End=0
    batch_size=400
    for N in range(0,len(portfolio_index),batch_size) :
        Beg=End
        End=Beg+400
        plt.clf()
        plt.plot(portfolio_index[Beg:End],'r',label="portfolio_index")
        plt.plot(dr["dr_rolling"][Beg:End],'b',label="dr_rolling_ratio")
        plt.title("Portfolio_index VS DR_rolling_ratio_"+str(N/batch_size))
        plt.xlabel("Date")
        plt.ylabel("Ratio")
        plt.legend()
        # do your magic here
        plt.show()


def rolling_dr_ratio(df, rolling_window_size=200):
    """
	calculates and plots the dr ratio.
	
    :param df: the dataframe contains the daily total return price change, the weights and the portfolio index.
    :param rolling_window_size: default to 200 days.
    :return: None.
    """
    # some tests
    
    # calculate the rolling DR ratio

    dr_list=[]
    last_index=-1
    # step 1
    for index,line in df.iterrows():
        if df.index.get_loc(index)==0:
           dr_line=100.0
        else:
           dr_line=round(dr_list[last_index]*(1+df[("TR_Change","Asset_1")][index]*df[("Weight","Asset_1")][index]
                                        +df[("TR_Change","Asset_2")][index]*df[("Weight","Asset_2")][index]
                                        +df[("TR_Change","Asset_3")][index]*df[("Weight","Asset_3")][index]
                                        +df[("TR_Change","Asset_4")][index]*df[("Weight","Asset_4")][index]),8)
        dr_list.append(dr_line)
        last_index=last_index+1
    # step 2 dr rolling ratio
    dr_all=pd.DataFrame(dr_list,columns=["dr_rolling"],index=df.index)
    dr=dr_all.rolling(window=rolling_window_size).mean()
    df["Portfolio_Index"]=df[("Portfolio_Index",str(1))].rolling(window=rolling_window_size).mean()
   
    # plot index and the rolling dr
    plot_dr_ratio(df["Portfolio_Index"], dr)


if __name__=="__main__":
    df = pd.read_csv("/Users/jerry/Downloads/question2/dr.csv", index_col=0, header=[0,1])
    rolling_dr_ratio(df)