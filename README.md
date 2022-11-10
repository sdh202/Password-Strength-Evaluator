# Password-Strength-Evaluator
AWS amplify hosted website that leverages AWS services, including lambda, S3, API Gateway, and DynamoDB.

Link: https://dev3165.d3b9dyx33ftyo7.amplifyapp.com/

- Evaluates inputted password out of 10

- Compares inputted password against a text file in an S3 bucket, which contains 200 most commonly used passwords

- If the password matches any of the common passwords in the file, the score is 0/10, and a message is displayed to let the user know the password is very common 

