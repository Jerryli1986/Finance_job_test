import pandas as pd


def same_timeseries(ts1, ts2):
    """
    return True if timeseries ts1 == timeseries ts2.

    :param ts1: pandas Dataframe object
    :param ts2: pandas Dataframe object
    :return: True if ts1 and ts2 are at least identical (Allowed Difference - 0.00001).
    """
    if len(ts1) == len(ts2):
        return (sum(ts1.values - ts2.values) < 10**-5).all()
    else:
        return False


def find_differences(bbg_df, quandl_df, csv_file_path=None):
    """
    prints or saves to csv the differences between two timeseries files.

    :param bbg_df: pandas Dataframe object
    :param quandl_df: pandas Dataframe object
    :param csv_file_path: path to save the output csv file (default=None)
    If csv_file_path is not None, will save the output to a csv file.
    :return: None.

    for each ticker find the start date of data from both sources,
    and prints True/False if prices series match since the common start date.

    Compare (BBG 'price' to quandl 'close price')

    CSV output example:
    
        Ticker, Quantle Start Date, BBG Start Date, Match since common start date?
        DOC US Equity ,2000-01-01, 1990-01-01, True
        ABO US Equity ,1999-01-01, 1990-01-01, False
        ...
        ...
        ...
        ABO US Equity ,1999-01-01, 1990-01-01, False
    
    """
    
    # write your code here.
    result="".join(["Ticker", " Quantle_Start_Date", " BBG_Start_Date", " Match?"])
    # list the Tickers from quandl_data
    Tickers=set(pd.DataFrame(list(quandl_df.columns))[0])
    for line in Tickers:
        if line in list(match_df[0]) :
           index_row=[];
           index_row=list(match_df[0]).index(line)
           common_Start,common_End=[],[]
           if (line,"Close") in list(quandl_df.columns) :
              if (match_df[1][index_row],"price") in list(bbg_df.columns) :
                 # compare the date index to get common date
                 quandl_Start=quandl_df[(line,"Close")].first_valid_index()
                 bbg_Start=bbg_df[(match_df[1][index_row],"price")].first_valid_index()
                 if quandl_Start>=bbg_Start :
                     common_Start=quandl_Start
                 else:
                     common_Start=bbg_Start
                 quandl_End=quandl_df[(line,"Close")].last_valid_index()
                 bbg_End=bbg_df[(match_df[1][index_row],"price")].last_valid_index()
                 if quandl_End<=bbg_End :
                     common_End=quandl_End
                 else:
                     common_End=bbg_End
                 # get the price list beteen common start date and common end date
                 pricelist_quandl=quandl_df[(line,"Close")][common_Start:common_End]
                 pricelist_bbg=bbg_df[(match_df[1][index_row],"price")][common_Start:common_End]
                 
                 Match_or_not=str(same_timeseries(pricelist_quandl, pricelist_bbg))
                 
                 #print (line,match_df[1][index_row],quandl_Start,bbg_Start,Match_or_not,len(pricelist_quandl),len(pricelist_bbg))
                 
                 result_line=str(" ".join([line,quandl_Start,bbg_Start,Match_or_not]))
                 result=result+"\n"+result_line

                 # as there may be nan in both pricelist, in addition, the len of lists not the same ,so the result is false 
                 #further step could be done by dropping index of nan in both pricelist and then check if it is same
                 # not sure if it needs to be done
                 # this question could be done by SQL 
                 
                 
    # save csv if file path was specified:
    if csv_file_path:
        csv_file = open(csv_file_path, 'w')
        csv_file.write(result)
        csv_file.close()
    print (result)   
    

if __name__=="__main__":
    bbg_df = pd.read_csv("/Users/jerry/Downloads/question1revised/bbg_data_final.csv", header=[0,1], index_col=0)
    quandl_df = pd.read_csv("/Users/jerry/Downloads/question1revised/quandl_data_final.csv", header=[0,1], index_col=0)
    match_df = pd.read_csv("/Users/jerry/Downloads/question1revised/match_final.csv",header=None)
    find_differences(bbg_df, quandl_df, "/Users/jerry/Downloads/question1revised/output.csv")