import ddddocr
import requests as req
from io import BytesIO

ocr = ddddocr.DdddOcr()
# try:
#     with open(f'jmsyzm.jpg', 'rb') as f:
#         img_bytes = f.read()
# except IOError as ercode:
#     print('文件打开错误，错误代码：%s', str(ercode))
# else:
#     print("识别中......")
#     res = ocr.classification(img_bytes)
#     print(f'Image jmsyzm 识别结果:{res}')
#     f.close()
getimg = req.get(
    "https://camo.githubusercontent.com/ef9f5e5f7b1245c54fc794cb0138d2152a08fb14c91eb6cec815499a40345605/68747470733a2f2f63646e2e77656e616e7a68652e636f6d2f696d672f37386237663537642d333731642d346236352d616662322d6431393630386165313839322e706e67")
# img_bytes = BytesIO(getimg.content)
res = ocr.classification(getimg.content)
print(f'Image jmsyzm 识别结果:{res}')
