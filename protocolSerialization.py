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
        return json.dumps(snakesObj)

    def ClientMoveMessage(self,id,position,direction):
        print("Client moved. Id : " +id+ " Head : "+str(position))
        return json.dumps({"type" : "move","id" : id,"position" : position,"direction" :direction})