import paho.mqtt.client as mqtt
from typing import *
import json
from collections.abc import Callable


class RpcNode(mqtt.Client):
    """
    一个RPC节点
    """

    def __init__(self,
                 self_node_name: str,
                 mqtt_address: str,
                 mqtt_port: int = 1883):
        super(RpcNode, self).__init__()
        self.connect(mqtt_address, mqtt_port)
        self.on_message = self.__on_message
        self.subscribe(f'/{self_node_name}/#')

        self.__functions: Dict[str, Callable] = {}
        self.__self_node_name = self_node_name

    def __on_message(self, client, userdata, msg: mqtt.MQTTMessage):
        topic = msg.topic
        content = msg.payload.decode('utf-8')
        content = json.loads(content)
        func_name = topic[len(self.__self_node_name) + 2:]
        if func_name in self.__functions.keys():
            self.__functions[func_name](*content)

    def register(self,
                 name: str,
                 callback: Callable):
        """
        注册被调用的异步回调函数
        :return:
        """
        self.__functions[name] = callback

    def call(self,
             remote_node_name: str,
             name: str,
             args: List = []):
        """
        异步调用远程函数
        :param remote_node_name: 远程节点名
        :param name:远程函数名
        :param args:函数参数列表
        :return:
        """
        self.publish('/%s/%s' % (remote_node_name, name), json.dumps(args))

    def spin(self):
        """
        回旋函数
        """
        self.loop()
