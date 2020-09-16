# Simple Docker Containerization `rekogGetter` for WWE IG Username rekognition results
## Etienne Jacquot - 09/16/2020

### Getting Started

- This build's **dockerfile** contains input value which is the WWE IG Username... Following previous I continued by using `romanreigns` for this containerization testing!

- Applying principles of `commentGetter` containerization, for each URL (final url on https://imghost.asc.upenn.edu) we can efficiently get image binary & then pass this value to AWS label rekog w/ all attributes

______
### Confirm your AWS credentials

- You must configure your **default AWS credentials** in order to run AWS Rekognition API calls! 
    - Contact your AWS sysadmin for your access & secret tokens at ithelpdesk@asc.upenn.edu

- Once you have your AWS creds, please make sure to save them to `./configs/.aws/config` with the following formatting
    - More information on various AWS config file [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#using-a-configuration-file)

```
# Confirm your credentials are correct!
cat ./configs/.aws/config

[default]
aws_access_key_id=AKIA...
aws_secret_access_key=P9Zd...96+dq

# If not, you must edit these
vim ./configs/.aws/config
```

- You'll notice below that this file path (absolute *inside of the rekogGetter container*) is included as an  `--env` flag for the `docker run` command!
    - This is singificant because we must avoid hardcoding creds in the GetRekognition script (this is always a bad practice!). We also must ensure that the `../gitignore` for ther repo excludes this config file so it is not getting pushed!

```
# Confirm your config file is added to the gitignore!

echo "docker_rekognition/configs/.aws/config" >> ../.gitignore

cat ../.gitignore
```

______

### Build container for WWE IG Username

- This only runs for `label` (more info here: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html#Rekognition.Client.detect_labels)

- Dockerfile containers input of instagram username ... Should this be one URL for one container, or does one Username (many URLs as rows `lambda x:`) to one container)

```
# Check & confirm dockerfile input value for WWE IG Username
cat dockerfile | grep python3

docker build -t wwe_instagram_rekog -f ./dockerfile .
```

______

### Run container for WWE IG Username

- Make sure to set your docker mount, I am running this on my macbook w/ docker... 

- Docker flags for run command:
    - `-it` for docker shell to display results, helpful for testing (could use `-d` for detached)
    - `--env` for the `AWS_CONFIG_FILE`
    - `-v` for the Docker volume mount on your localhost!
    - `--network=host` for Docker on MacOS, this is known issue
    - `--name` to set the container name as `rekogGetter`

```
# Specifying environment variable for AWS configs so they are not hard coded

docker run -it --env AWS_SHARED_CREDENTIALS_FILE=/app/configs/.aws/credentials/ -v ~/Documents/Bitbucket/wwe-instagram-rekogcomments/docker_rekognition/data/:/data/ --network=host --name=rekogGetter wwe_instagram_rekog:latest
```

______

## NOTES & CHANGES FOR NEXT TIME:

- Based on the previous notebooks there is a lot of room for improvement for my python Rekogntion for WWE comments...

- Passing image_binary for label_response allows you to create `['AWS_Label_Rekognition']` column, but can you return multiple values for lambda x: to create multiple columns? Just thinking of combining all rekognition API calls for one image binary!

1. one username to one container *OR* one URL to one container?
2. incorporating rekog detection for more than just `label`
3. AWS creds are in very poor fashion coded in py script...
    1. learn one of the options described by AWS here --> https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
    2. env variables in dockerfile? config in .aws/config somewhere from ./configs/config ...? https://vsupalov.com/docker-arg-env-variable-guide/ for dockerfiles you use `ARG` and `ENV` to make the environment variable available to the final container!
4. Ultimately, scalability for WWE IG users w/ many posts

- This docker build demonstrates a relatively simple process