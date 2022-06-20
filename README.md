# Project info 
This is a web application that allows users to upload the video in AWS(S3) and extract subtitles from that video which
user can search for any keywords from  the subtitles and 
in return the timestamp of the video against the matched keywords will be returned.
SRT file will be stored in DynamoDB.
### Built With

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)

### Prerequisites


* Python
* Django
* Celery
* Boto3
* Redis
* AWS S3
* DynamoDB
* Pysrt

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/inAsees/be_zen_Project.git
   ```
2. Install pip (package installer for Python)
   [here](https://pip.pypa.io/en/stable/installing/)
3. Install Python packages(once you are inside the root directory of the project)
   ```sh
   pip install -r requirements.txt
   ```
# Getting started

1. This Application only works with Linux(since windows does not support Celery). 
2. Before you can start using the application, it is assumed that you are having a 
valid AWS account configured with your system with permissions for S3 and Dynamodb services.
If you do not have an AWS account, you can sign up for one [here](https://aws.amazon.com/free/).
To know how to generate Access Key and Secret Key, please visit 
[AWS documentation](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html).
To know how to configure your AWS credentials, please visit
[AWS Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).
3. You also need to install Redis which will be used to create the queue for the tasks.
   [Click here](https://redis.io/docs/getting-started/installation/install-redis-on-linux/) to install Redis.
4. You need to install ccextractor(for Linux) package, which will be used to extract the subtitles from the video.
 Run the following command to install ccextractor:
   ```sh
   sudo apt-get install ccextractor
    ```
## How to run the application
1. Get into the root directory of the project(be_zen_Project) and run the following command:
    ```sh
    python create_table.py
    ```
2. Get into the directory video_uploader (where manage.py lives) and run the following command 
   in your terminal:
    ```sh
    python manage.py runserver
    ```
3. Now open another terminal and run the following command:
    ```sh
    celery -A video_uploader.celery worker -l INFO
    ```
