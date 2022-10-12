import json
import boto3
import string
from time import gmtime, strftime
import csv

#Getting DynamoDB Table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('passwords')
now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

#Reading Text File in S3 Bucket that contains a list of the 200 most common passwords
#Passwords in file sourced from: https://nordpass.com/most-common-passwords-list/ 
s3 = boto3.client('s3')
s3_object = s3.get_object(Bucket='mypassbucket1', Key='BadPass2.txt')
data = s3_object['Body'].read().decode('utf-8').splitlines()
lines = csv.reader(data)
headers = next(lines)

#Password Evaluation Function
def eval(password):
    score = 0

#Evaluating if or not given password contains uppercase, lowercase, special, or numerical characters 
    upper_case = any([1 if c in string.ascii_uppercase else 0 for c in password])
    lower_case = any([1 if c in string.ascii_lowercase else 0 for c in password])
    special = any([1 if c in string.punctuation else 0 for c in password])
    digits = any([1 if c in string.digits else 0 for c in password])
        
    characters = [upper_case, lower_case, special, digits]
    length = len(password)

#Totaling score based on below criteria
    if length > 4:
        score += 1
    if length > 8:
        score += 1    
    if length > 12:
        score += 1
    if length > 16:
        score += 2
    if length > 20:
        score += 1
    if sum(characters) > 1:
        score += 1
    if sum(characters) > 2:
        score += 1
    if sum(characters) > 3:
        score += 2
    return str(score)
        

def lambda_handler(event, context):    
    Result = 0
    
#Iterates through file lines and if line matches input, provides appropriate json message. Otherwise, evaluate input and provide result     
    for line in data:
        if (line == event['sc']):
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},    
                'body': json.dumps("Your score for " + "'" + event['sc'] + "'" + " is " + str(0) + "/10." + " This is very commonly used and easy to guess!")
            }
    else:
        Result = eval((event['sc']))

#Evaluate the strength of the score        
        if int(Result) < 4:
            Strength = ("weak password.")
        elif 6 > int(Result) >= 4:
            Strength = ("ok password.")
        elif 4 < int(Result) <= 6:
            Strength = ("good password.")
        elif int(Result) > 7:
            Strength = ("strong password.")

#Record score in DynamoDB             
        response = table.put_item(
        Item={
            'ID': str(Result),
            'LatestGreetingTime':now
            }
        )    
            
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps("Your score for " + "'" + event['sc'] + "'" + " is " + str(Result) + "/10." + " This is a " + Strength)
        }   