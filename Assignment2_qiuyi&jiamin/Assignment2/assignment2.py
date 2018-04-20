import pymysql
from numpy import*

#####Connect with SOL
def sqlconncetion():
 localhost = '127.0.0.1'
 name = 'root'
 password = '941024'
 tablename = 'subtables'
 db=pymysql.connect(localhost,name,password,tablename)
 return db

#####Import data to python
def dataimport(tablename):
    db=sqlconncetion()
    cursor = db.cursor()
    # SQL extract substation information
    sql = "SELECT * FROM %s" %(tablename)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        print("Error: unable to fetch data")
    return results

#####Task1: k-means clustring for measurements

## extract measurement information
db=sqlconncetion()
cursor=db.cursor()
results=dataimport('measurements')
try:
   name=[]
   time=[]
   for row in results:
     name.append(row[1])
     time.append(row[2])
   name_label=set(name)
   time_stamp=set(time)
   data=[]
   for i in time_stamp:
        sql_time_data="SELECT * FROM measurements WHERE Time = '%d' " % (i)
        cursor.execute(sql_time_data)
        results=cursor.fetchall()
        point = []
        for row in results:
           point.append(row[3])
        data.append(point)
        dataset = data
except:
       print ("Error: unable to fetch data")


#calculate distance Ecludistance
def distance(pointA,pointB):
    return sqrt(sum(power(pointA-pointB,2)))

#create centroid
# make sure the arbitrary centroids are within the range of all points
# def centroid(table,k):
#     n=len(name_label)
#     centroids=mat(zeros((k,n)))
#     for i in range(n):
#         mindata=min(table[:,i])
#         maxdata=max(table[:,i])
#         rangei=float(maxdata-mindata)
#         centroids[:,i]=mat(mindata+rangei*random.rand(k,1))
#     return centroids

##randomly choose initial centorids
centroids=mat(zeros((4,len(name_label))))
for i in range (len(name_label)):
 centroids[0,i]=dataset[0][i]
 centroids[1,i]=dataset[1][i]
 centroids[2,i]=dataset[2][i]
 centroids[3,i]=dataset[3][i]

#k-means clustering
def kmeans(dataset,k,dist=distance):
    npts=len(time_stamp)
    n=len(name_label)
    cluster=mat(zeros((npts,2)))
    centroidsarbitrary=centroids
    # print(centroidsarbitrary)
    modifyflag=True
    while modifyflag:
        modifyflag=False
        for i in range(npts):
           minlimit=inf;
           minindex=-1
           for j in range(k):
              newdistance=dist(centroidsarbitrary[j,:],dataset[i,:])
              if newdistance < minlimit:
                minlimit=newdistance;
                minindex=j
           if cluster[i,0] != minindex: modifyflag=True
           cluster[i,:]=minindex,minlimit**2
        # print(centroidsarbitrary)
        for m in range(k):
           pointsincluster = dataset[nonzero(cluster[:,0].A==m)[0]]
           centroidsarbitrary[m,:] = mean(pointsincluster,axis=0)
    return centroidsarbitrary,cluster
test=mat(dataset)
centroid,cluster=kmeans(test,4,dist=distance)
print(cluster)


##### Task2:KNN method

#import test data

results=dataimport('analog_values')
try:
   name=[]
   time=[]
   for row in results:
     name.append(row[1])
     time.append(row[2])
   name_label=set(name)
   time_stamp_test=set(time)
   testdata=[]
   for i in time_stamp_test:
        sql_time_data_test="SELECT * FROM analog_values WHERE Time = '%d' " % (i)
        cursor.execute(sql_time_data_test)
        results_test=cursor.fetchall()
        point_test = []
        for row in results_test:
           point_test.append(row[3])
        testdata.append(point_test)
        # dataset=mat(table)
        testdataset = testdata
except:
       print ("Error: unable to fetch data")


##assign labels to each points in measurements
def createdataset():
   label=list()
   for i in range(len(time_stamp)):
     label.append(cluster.tolist()[i][0])
   label = label
   return label

##find the most common label for one point
def mostcommonlabel(labellist,clusternumber):
    cluster=list()
    for i in range(clusternumber):
     cluster.append(labellist.count(i))
     commonlabel=cluster.index(max(cluster))
    return commonlabel

##knn method
def knntest(k,dataset,testset,dist=distance):
    label=createdataset()
    labelresult=list()
    for i in range(len(time_stamp_test)):
         distancelist = list()
         for j in range(len(time_stamp)) :
            distancelist.append(dist(testset[i],dataset[j]))
         distancetobig=sorted(distancelist)
         klabellist = list()
         for n in range (k):
             find=distancetobig[n]
             finddistance=distancelist.index(find)
             klabellist.append(label[finddistance])
         classificationresult=mostcommonlabel(klabellist,4)
         labelresult.append(classificationresult)
    return labelresult
data=mat(dataset)
test=mat(testdataset)

print(knntest(10,data,testdataset,dist=distance))
print(knntest(20,data,testdataset,dist=distance))
print(knntest(30,data,testdataset,dist=distance))
print(knntest(40,data,testdataset,dist=distance))
print(knntest(50,data,testdataset,dist=distance))