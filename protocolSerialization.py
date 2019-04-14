import json
import random
import json

class ProtocolSerialization:
    def ServerStratMessage(self,position,direction):
        print("Server send Start message")
        return json.dumps({"type" : "start","position" : position,"direction" :direction})

    def ClientStartMessage(self,id):
        print("Client ask to start")
        return json.dumps({"type" : "start","id" : id})

    def ClientQuitMessage(self,id):
        print("Client ask to quit")
        return json.dumps({"type" : "quit","id" : id})
    
    def ServerMoveMessage(self,snakes):
        print("Server sent the game update")
        snakesObj = []
        for snake in snakes:
             snakesObj.append({"id":snake.name,"position":snake.position,"alive":snake.alive,"score":snake.score,"direction" :snake.direction})
        snakesObj.append({"id":"654654","position":[[10,10],[10,11],[10,12],[10,14],[10,15]],"alive":True,"score":0,"direction" :3})
        # snakesObj.append({"id":"654654","position":[[12,10],[12,11],[12,12],[12,14],[12,15]],"alive":True,"score":0,"direction" :4})
        # snakesObj.append({"id":"654654","position":[[0,20],[1,20],[2,20],[3,20],[4,20]],"alive":True,"score":0,"direction" :1})
        out = json.dumps(snakesObj)
        print(out)
        return out

    def ClientMoveMessage(self,id,position,direction):
        print("Client moved. Id : " +id+ " Head : "+str(position[0]))
        return json.dumps({"type" : "move","id" : id,"position" : position,"direction" :direction})