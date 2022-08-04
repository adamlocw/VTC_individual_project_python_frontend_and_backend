import pymongo

myclient = pymongo.MongoClient(
    "mongodb+srv://sysadmin:Nerv-19830228@cluster0.9wtze.mongodb.net/test")
mydb = myclient["VTC_individual_project"]


def addRecordMartingaleBalance(balance):
    mycol = mydb["martingaleBalance"]
    mydict = {"balance": balance}
    x = mycol.insert_one(mydict)
    return x


if __name__ == '__main__':
    print(addRecordMartingaleBalance(456).inserted_id)
