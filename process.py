import mysql.connector
import pandas as pd
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import csv



hostname = 'mysqldbserverjune.database.windows.net'
username = 'myuserjune@mysqldbserverjune.database.windows.net'
password = 'JuneJune@8989'
database = 'my-sql-database-june'

def main():
    connect_str = "DefaultEndpointsProtocol=https;AccountName=p2glpb;AccountKey=oA1HLU32e5DEXl7nFZ4mRPQ8JToCMLSNjzz22AGSUmmk567bBfbaLKSHbhPFbycyeI/OE0t4tCn++ASthiKx8w==;EndpointSuffix=core.windows.net"
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    # Create a unique name for the container
    container_name = str(uuid.uuid4())
    # Create the container
    container_client = blob_service_client.create_container(container_name)
    print ('*********************** Processing File *****************************'),
    read_file = pd.read_csv (r'./docproc-invoice.txt')
    read_file.to_csv (r'./docproc.csv', index=None)
    print ('File has been processed')
    upload_file_path = os.path.join("./", "docproc.csv")
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob="docproc.csv")
    print("\nUploading to Azure Storage as blob: docproc.csv")
    # Upload the created file
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)

    data= pd.read_csv("./docproc.csv")

    cust_id = data.iloc[0,0]
    inv_id = data.iloc[1,0]
    print (cust_id)
    print (inv_id)

    print ('\n*************************************************************************')
    print ('Creating table invoice')
    conn = mysql.connector.connect(host=hostname, user=username, passwd=password, db=database)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS invoice (cust_id VARCHAR(255), inv_id VARCHAR(255))")
    print ('Inserting data into database')
    sql = "INSERT INTO invoice VALUES (%s, %s)"
    val = (cust_id, inv_id)
    cur.execute(sql, val)
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
