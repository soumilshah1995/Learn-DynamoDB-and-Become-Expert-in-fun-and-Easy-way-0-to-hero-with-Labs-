import json


data = "{\"sk\": \"like#e01a3232-ad30-4041-b7d9-a9c34bcb3109#user#user#c37efe78-8360-4af0-930e-55ecff2802de\", \"user_post_gsi\": \"user#c37efe78-8360-4af0-930e-55ecff2802de\", \"pk\": \"like#e01a3232-ad30-4041-b7d9-a9c34bcb3109\", \"post_user_likes_gsi\": \"post_id#5875ae56-6994-4d96-9b27-f127c112febb\", \"awsRegion\": \"us-east-1\", \"eventID\": \"0161b5c7-4be2-4dc1-9c0f-77a4aef54a45\", \"eventName\": \"INSERT\", \"eventSource\": \"aws:dynamodb\"}"
print(json.loads(
    data
))

