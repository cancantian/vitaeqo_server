from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = 'AKIDKQGqA2J3B5kAKDqLWR6WgOswrWyUPfHq'   # found this in 云API密钥
secret_key = '231CVl1DsaAqpk2JWoy2zqApTwX0JQM8'
region = 'ap-beijing'     # 替换为用户的 Region
token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填


class TXBucket:
    def __init__(self):
        self.client = self.__init_client()
        self.bucket_id = 'vitaeqo-bucket-1259011267'
        self.url_prefix = 'https://vitaeqo-bucket-1259011267.cos.ap-beijing.myqcloud.com/'

    def __init_client(self):
        try:
            config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
            client = CosS3Client(config)
            return client
        except Exception as err:
            print(err)

    def upload_img(self, fp, bucket_file_name):
        # with open(fp, 'rb') as fp:
        #     response = self.client.put_object(
        #         Bucket=self.bucket_id,
        #         Body=fp,
        #         Key=bucket_file_name,
        #         StorageClass='STANDARD',
        #         EnableMD5=False
        #     )
        response = self.client.put_object(
            Bucket=self.bucket_id,
            Body=fp,
            Key=bucket_file_name,
            StorageClass='STANDARD',
            EnableMD5=False
        )
        url = self.url_prefix + bucket_file_name
        return url


# if __name__ == '__main__':
#     fp = 'C:\\Users\\ygt\\Pictures\\7.png'
#     bfn = 'test2.png'
#     txb = TXBucket()
#     txb.update_img(fp, bfn)
