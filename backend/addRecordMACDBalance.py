import pymongo

myclient = pymongo.MongoClient(
    "mongodb+srv://sysadmin:Nerv-19830228@cluster0.9wtze.mongodb.net/test")
mydb = myclient["VTC_individual_project"]


def addRecordMACDBalance(balance):
    mycol = mydb["macdBalance"]
    mydict = {"balance": balance}
    x = mycol.insert_one(mydict)
    return x


if __name__ == '__main__':
    print(addRecordMACDBalance(456).inserted_id)
