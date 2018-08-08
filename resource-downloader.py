# -*- coding: utf-8 -*-
import os
import boto3

'''
    pip install aws
    
'''

IMAGE_DOWNLOAD_PATH = '../app/src/main/res_down'   # 이미지 파일이 저장될 별도의 리소스 폴더
LOTTIE_DOWNLOAD_PATH = '../app/src/main/res_down'   #로티 파일이 저장될 별도의 리소스 폴더
SUPPORTED_LANGUAGE = ['ko', 'en', 'ja']
DEFAULT_LANGUAGE = 'en'


def assert_dir_exists(PATH):
    """
    Checks if directory tree in path exists. If not it created them.
    :param path: the path to check if it exists
    """
    try:
        if not os.path.exists(PATH):
            os.makedirs(PATH)
    except OSError as e:
        print(e)





def download_dir(client, bucket, PATH, target):
    """
    Downloads recursively the given S3 path to the target directory.
    :param client: S3 client to use.
    :param bucket: the name of the bucket to download from
    :param path: The S3 directory to download.
    :param target: the local directory to download the files to.
    """
    # print(os.path.join("PATH : ", PATH))

    # Handle missing / at end of prefix
    if not PATH.endswith('/'):
        PATH += '/'

    paginator = client.get_paginator('list_objects_v2')


    for result in paginator.paginate(Bucket=bucket, Prefix=PATH):
        # Download each file individually
        print(result)
        if result.get('Contents', None):
            for key in result['Contents']:
                # Calculate relative path
                rel_path = key['Key'][len(PATH):]
                # Skip paths ending in /
                if not key['Key'].endswith('/'):
                    local_file_path = os.path.join(target, rel_path)
                    # Make sure directories exist
                    local_file_dir = os.path.dirname(local_file_path)
                    assert_dir_exists(local_file_dir)
                    print(os.path.join("pathhh : ", local_file_path))
                    print(os.path.join("key : ", key['Key']))

                    client.download_file(bucket, key['Key'], local_file_path)



s3_client = boto3.client('s3')
BUCKET_NAME='client-resource-storage'


def download_image_from_s3():
    for language in SUPPORTED_LANGUAGE:
        path = IMAGE_DOWNLOAD_PATH

        if not os.path.exists(path):
            os.makedirs(path)

        if not path.endswith('/'):
            path += '/'

        if language == DEFAULT_LANGUAGE:
            path += 'drawable/'
        else :
            path += 'drawable-'+ language+ '/'

        if not os.path.exists(path):
            os.makedirs(path)

        download_dir(s3_client, BUCKET_NAME, 'image/'+ language, path)

def download_lottie_from_s3():
    for language in SUPPORTED_LANGUAGE:
        path = LOTTIE_DOWNLOAD_PATH

        if not os.path.exists(path):
            os.makedirs(path)

        if not path.endswith('/'):
            path += '/'

        if language == DEFAULT_LANGUAGE:
            path += 'raw/'
        else :
            path += 'raw-'+ language+ '/'

        if not os.path.exists(path):
            os.makedirs(path)

        download_dir(s3_client, BUCKET_NAME, 'lottie/'+ language, path)





if __name__ == '__main__':
    download_image_from_s3()
    download_lottie_from_s3()
