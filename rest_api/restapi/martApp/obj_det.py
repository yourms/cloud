#!/usr/bin/env python
# coding: utf-8

# In[4]:


import json
import logging
import os
import torch
from PIL import Image
from torchvision import transforms
from torchvision import models
import torch.nn as nn

from cgi import test
import threading
import paho.mqtt.client as mqtt
from threading import Thread, Event
import paho.mqtt.publish as publisher


# In[5]:

# 예측 모델 선언

# class ResNet50(torch.nn.Module):
#     def __init__(self):
#         super(ResNet50, self).__init__()
#         model = models.resnet50(pretrained=True)
#         modules = list(model.children())[:-1]
#         self.feature_extract = nn.Sequential(*modules)
#         self.fc1 = nn.Linear(2048, 1000)
#         self.relu = nn.ReLU()
#         self.fc2 = nn.Linear(1000,7)

#     def forward(self, x):
#         x = self.feature_extract(x)
#         # x = x.mean(dim=(-2, -1))
#         # (batch, 2048, 4, 4)
#         x = torch.squeeze(x)
#         x = self.relu(self.fc1(x))
#         out = self.fc2(x)
#         return out


# # In[7]:


# def model_fn():
#     device = torch.device('cpu')
#     logger.info('Loading the model.')
#     model = ResNet50().to(device)

#     with open(os.path.join('./saved_models/', '/ResNet50_1e-05_rmsprop_example2.pth'), 'rb') as f:
#         model.load_state_dict(torch.load(f, map_location=device))

#     model.to(device).eval()
#     logger.info('Done loading model')
#     return model


# # In[8]:


# def input_fn(request_body, content_type='url/str'):
#     logger.info('Deserializing the input data.')
#     if content_type == 'url/str':
#         url = request_body
#         logger.info(f'Image url: {url}')
#         image_data = Image.open(request_body)

#         image_transform = transforms.Compose([
#             transforms.Resize(size=256),
#             transforms.CenterCrop(size=256),
#             transforms.ToTensor(),
#             transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
#         ])

#         return image_transform(image_data)
#     raise Exception(f'Requested unsupported ContentType in content_type: {content_type}')


# # In[9]:


# def output_fn(prediction_output, accept='application/json'):
#     logger.info('Serializing the generated output.')
#     # 각 분류기마다 다른 레이블 값을 가짐. 해당 레이블 값을 토대로 쿼리 진행
#     label = ['35102', '55701', '65753', '66304', '35192', '45661', '35954']
#     classes = {0: label[0], 1: label[1], 2: label[2], 3: label[3], 4: label[4], 5: label[5], 6: label[6]}

#     topk, topclass = prediction_output.topk(1, dim=0)
#     result = []

#     for i in range(1):
#         # 'score': f'{topk.cpu().numpy()[0] * 100}%'
#         pred = {'prediction': classes[topclass.cpu().numpy()[0]]}
#         logger.info(f'Adding pediction: {pred}')
#         result.append(pred)

#     if accept == 'application/json':
#         return json.dumps(result), accept
#     raise Exception(f'Requested unsupported ContentType in Accept: {accept}')


# # In[10]:


# def predict_fn(input_data, model):
#     logger.info('Generating prediction based on input parameters.')
#     if torch.cuda.is_available():
#         input_data = input_data.view(1, 3, 256, 256)
#     else:
#         input_data = input_data.view(1, 3, 256, 256)

#     with torch.no_grad():
#         model.eval()
#         out = model(input_data)

#     return out


# 통신 부분
class MqttWorker:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.exit_event = Event()

        # self.HC_SR04 = HC_SR04(self.client)
        # self.HC_SR04.start()

        # self.camera =  MyCamera(self.client)
        # self.camera.start(self.client)

    def signal_handler(self, signum, frame):
        print("signal_handler===================================")
        self.exit_event.set()  # 이벤트객체가 갖고 있는 플래그 변수가 True로 셋팅
        self.led.clean()
        # 현재 이벤트 발생을 체크하고 다른 작업을 수행하기 위한 코드 - 다른 메소드에서 처리
        if self.exit_event.is_set():
            print(
                "이벤트객체의 플래그변수가 Ture로 바뀜 - 이벤트가 발생하면 어떤 작업을 실행하기 위해서(다른 메소드 내부에서 반복문 빠져나오기~....)")
            exit(0)

    def mymqtt_connect(self):  # 사용자정의 함수 - mqtt서버연결과 쓰레드생성 및 시작을 사용자정의 함수로 정의
        try:
            print("브로커 연결 시작하기")
            self.client.connect("13.52.187.248", 1883, 60)
            mythreadobj = Thread(target=self.client.loop_forever)
            mythreadobj.start()
            publisher.single("android/productAI", "안녕하세요", hostname="13.52.187.248")

        except KeyboardInterrupt:
            pass
        finally:
            print("종료")

    def on_connect(self, client, userdata, flags, rc):  # broker접속에 성공하면 자동으로 호출되는 callback함수
        print("connect..." + str(rc))  # rc가 0이면 성공 접속, 1이면 실패
        if rc == 0:  # 연결이 성공하면 구독신청
            client.subscribe("iot/#")
            client.subscribe("web")
            client.subscribe("android/picture")
        else:
            print("연결실패.....")

    # 라즈베리파이가 메시지를 받으면 호출되는 함수이므로 받은 메시지에 대한 처리를 구현
    def on_message(self, client, userdata, message):
        try:
            print("test~~~~~")
            myval = message.payload.decode("utf-8")
            myval2 = message.topic.split("/")
            if myval2[1] == "start":
                camerathread = threading.Thread(target=self.cameratest)
                camerathread.start()
            elif myval2[1] == "picture":
                print(myval)
                print("start")
                print("")


        except:
            pass
        finally:
            pass


# 테스트 작업을 위한 클래스
if __name__ == '__main__':
    try:
        mqtt = MqttWorker()
        mqtt.mymqtt_connect()  # callback 함수가 아니므로 인스턴스 변수를 이용해서 호출해야 한다.
        for i in range(10):
            print(i)

    except KeyboardInterrupt:
        pass

    finally:

        print("종료")
