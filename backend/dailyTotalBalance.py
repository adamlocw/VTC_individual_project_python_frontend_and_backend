import pymongo
from sendEmail import sendEmail
from datetime import datetime, timedelta

def dailyTotalBalance():
    # Mongodb connection
    myclient = pymongo.MongoClient("mongodb+srv://sysadmin:Nerv-19830228@cluster0.9wtze.mongodb.net/test")
    # Select the database
    mydb = myclient["VTC_individual_project"]
    # Set up the collection
    macdBalanceCol = mydb["macdBalance"]
    martingaleBalanceCol = mydb["martingaleBalance"]
    cryptoBalanceCol = mydb["cryptoBalance"]
    # Init array
    macdBalanceArray = []
    martingaleBalanceArray = []
    # Get all Balance
    for x in macdBalanceCol.find():
        macdBalanceArray.append(x['balance'])
    for x in martingaleBalanceCol.find():
        martingaleBalanceArray.append(x['balance'])
    # Get the latest Balance
    latestMACDBalance = macdBalanceArray[-1]
    latestmartingaleBalance = martingaleBalanceArray[-1]
    # Sum all Balance
    totalBalance = float(latestMACDBalance) + float(latestmartingaleBalance)
    # Add sum balance to cryptoBalance
    sumBalance = {"balance":totalBalance}
    x = cryptoBalanceCol.insert_one(sumBalance)
    # Send email to log the batch is running successfully
    emailTo = "adamlocw@gmail.com"
    emailSubject = "Daily balance is completed."
    emailBody = f"Daily balance is completed. {datetime.now()}"
    sendEmail(emailTo, emailSubject, emailBody)
    return (x)

if __name__ == '__main__':
    print(dailyTotalBalance().inserted_id)
