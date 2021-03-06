					
                                    #Sono Yazilim Technical Task

#Name: Duygu Turan
#Subject: prediction of a user's rating which is greater than three on a movie 
#Due Date: 28.08.2017
#Dataset page: http://files.grouplens.org/datasets/movielens/ml-latest-small-README.html
#Language: Python

#The dataset should have same path as your project.py

#I used first 1000 data instead of all dataset because it takes a long time. If you want to use all dataset, 
#you should change some of variables

#When you determine "k" value as you want and run project.py, accuracy of a model for MovieLens 100K dataset
#classification by using K-Nearest Neighbors Algorithm will be shown in console.
 
import pandas as pd
import numpy as np
import math


#This function represents an occupation as a number
def encodeOccupation(userOccupation, occupations):
    occupationId = 0
    for i in range(0, 21):
        if userOccupation == occupations.name[i]:
            occupationId = i;
    return occupationId

#This function gets a distance matrix. And it predicts a test data's rating in regard to 
#first kth distances' most frequent rating.
def predictLabel(sortedDistances, k):
    countOverThree = 0   #frequency of rating which is greater than three in first kth distances
    countUnderThree = 0    #frequency of rating which is less than and equal to three in first kth distances
    prediction = 0  
    for i in range(0, k):
        if sortedDistances[i,1] > 3:
            countOverThree = countOverThree+1
        elif sortedDistances[i,1] <= 3:
            countUnderThree = countUnderThree+1
    if countOverThree < countUnderThree:
        prediction = 0
    elif countOverThree == countUnderThree:
        prediction = 0
    else:
        prediction = 1
    return prediction

#This function gets a test and train data. Then, it calculates the distance between them
def calculateEuclideanDist(testPoint, trainPoint):  
    distance = 0
    a = 0
    b = 0
    for i in range(0,22):
        if testPoint[i] == trainPoint[i]:
            a = 0
            b = 0
        else:
            a = 0
            b = 1
        distance = distance + math.pow(a-b,2) 
    return math.sqrt(distance)

#This function gets predictionsAndReality matrix which stores rating predictions and actual ratings
#Then, it compares predictions and actual ratings and calculates accuracy of the model
def calculateAccuracy(predictionsAndReality):
    trueCount = 0.0
    for i in range(0,200):
        if predictionsAndReality[i][0] == predictionsAndReality[i][1]:
            trueCount = trueCount+1.0
    accuracy = trueCount/200.0
    print('Accuracy of the model: ',accuracy)

#This function gets test data and train data. It finds distances between train data and first test data by using
#the Euclidean distance as a distance metric. And it stores those distances and train data's ratings. Then, it sorts
#the distances and determines first kth distances' most frequent rating as first test data's rating. It stores first 
#test data's this rating prediction and actual class in predictionsAndReality matrix. Finally, it does this operation 
#for all test data and calculates accuracy for the given model by using predictionsAndReality matrix. 
def knn(test, train, k):
    predictionsAndReality = np.zeros((200,2))
    i=0
    for currentTest in test:
        distances = np.zeros((800,2))
        j=0
        for currentTrain in train:
            #Find distances between train data and a test data by using the Euclidean distance
            distances[j,0] = calculateEuclideanDist(currentTest,currentTrain)
            distances[j,1] = currentTrain[22] #Store the distances and train data's ratings
            j=j+1
        #Sort the distances
        sortedDistances = np.sort(distances.view('i8,i8'), order=['f0'], axis=0).view(np.float) 
        #Determine first kth distances' most frequent rating as a test data's rating
        #Store a test data's rating prediction and actual class in predictionsAndReality matrix
        predictionsAndReality[i, 0] = predictLabel(sortedDistances, k)
        if currentTest[22]>3:
            predictionsAndReality[i, 1] = 1
        elif currentTest[22]<=3:
            predictionsAndReality[i, 1] = 0
        i = i+1
    #Calculate accuracy of the model
    calculateAccuracy(predictionsAndReality)

    
##################START OF THE MAIN CODE####################

k = 10

#Load user, movie, rating and occupation data
userColumns = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('ml-100k/u.user', sep='|', names = userColumns, encoding='latin-1')

ratingColumns = ['user_id', 'movie_id', 'rating', 'unix_timestamp']
ratings = pd.read_csv('ml-100k/u.data', sep='\t', names = ratingColumns, encoding='latin-1')

movieColumns = ['movie_id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
 'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'FilmNoir', 'Horror', 'Musical', 'Mystery', 
 'Romance', 'SciFi', 'Thriller', 'War', 'Western']
movies = pd.read_csv('ml-100k/u.item', sep='|', names=movieColumns, encoding='latin-1')

occupationColumns = ['name']
occupations = pd.read_csv('ml-100k/u.occupation', sep='\t', names = occupationColumns, encoding='latin-1')

#data counts
ratingCount = 1000
userCount = 943
movieCount = 1682

#Concatenate a user, a movie and the user's rating on the movie data with the user's age, sex and occupation 
#and the movie's genres
data = np.zeros((ratingCount,23))
for i in range(0,ratingCount):       
    for j in range(0, userCount):
        if ratings.user_id[i] == users.user_id[j]:  
            data[i:i+1, :1] = users.age[j]      #user's age
            if users.sex[j] == 'M':             #user's sex
                data[i:i+1, 1:2] = 0
            else:
                data[i:i+1, 1:2] = 1 
            data[i:i+1, 2:3] = encodeOccupation(users.occupation[j], occupations) #user's occupation
    for k in range(0, movieCount):
        #movie's genres
        if ratings.movie_id[i] == movies.movie_id[k]:
            data[i:i+1, 3:4] = movies.Action[k]
            data[i:i+1, 4:5] = movies.Adventure[k]
            data[i:i+1, 5:6] = movies.Animation[k]
            data[i:i+1, 6:7] = movies.Childrens[k]
            data[i:i+1, 7:8] = movies.Comedy[k]
            data[i:i+1, 8:9] = movies.Crime[k]
            data[i:i+1, 9:10] = movies.Documentary[k]
            data[i:i+1, 10:11] = movies.Drama[k]
            data[i:i+1, 11:12] = movies.Fantasy[k]
            data[i:i+1, 12:13] = movies.FilmNoir[k]
            data[i:i+1, 13:14] = movies.Horror[k]
            data[i:i+1, 14:15] = movies.Musical[k]
            data[i:i+1, 15:16] = movies.Mystery[k]
            data[i:i+1, 16:17] = movies.Romance[k]
            data[i:i+1, 17:18] = movies.SciFi[k]
            data[i:i+1, 18:19] = movies.Thriller[k]
            data[i:i+1, 19:20] = movies.War[k]
            data[i:i+1, 20:21] = movies.Western[k]
            data[i:i+1, 21:22] = movies.unknown[k]
            break
    data[i:i+1, 22:23] = ratings.rating[i] #user's rating on movie



#I shuffled data to get different accuracy for each running
np.random.shuffle(data)

#Divide data as train and test
train = data[:800, :]
test = data[800:1000, :]

#Classify data
knn(test, train, k)

