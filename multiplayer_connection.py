import os

import thread
from class_types.buildind_types import BuildingTypes
from class_types.road_types import RoadTypes


class Multiplayer_connection:

    def __init__(self):
        self.buffer_receive = ""
        self.buffer_send = ""
        self.builder = None

        pipe_name = "pythonToC"

        if os.path.exists(pipe_name):
            os.remove(pipe_name)

        os.mkfifo(pipe_name)

    def set_builder(self, builder):
        self.builder = builder

    
    def set_buffer_receive(self, buffer):
        self.buffer_receive = buffer
        return


    def set_buffer_send(self, buffer):
        self.buffer_send = buffer
        return

    
    def write(self, row, col, buildingType="destroy"):
        string = str(buildingType) + ";"+ str(row) + ";"+ str(col)
        self.buffer_send += string
        self.send()
        self.set_buffer_send("")
        return
    
    def read(self):
        tab = self.buffer_receive.split(";")
        type_str = tab[0]
        type_parts = type_str.split('.')
        type_name = type_parts[-1]

        if "RoadTypes" in type_str:
            type_value = getattr(RoadTypes, type_name)
        elif "BuildingTypes" in type_str:
            type_value = getattr(BuildingTypes, type_name)
        else:
            type_value = None

        self.builder.build_from_start_to_end(type_value, Multiplayer_connection.string_to_tuple(tab[1]), Multiplayer_connection.string_to_tuple(tab[2]))


    
    def send(self):
        pipe_name = "send_pipe"
        if os.path.exists(pipe_name):
            os.remove(pipe_name)
        os.mkfifo(pipe_name)
        pipe_out = os.open(pipe_name, os.O_WRONLY)
        message = self.buffer_send.encode("utf-8")

        os.write(pipe_out, message)
        thread.executer_code_c("./Online/send")
        os.close(pipe_out)

    def receive(self):
        pipe_name = "receive_pipe"
        if os.path.exists(pipe_name):
            os.remove(pipe_name)
        os.mkfifo(pipe_name)
        pipe_in = os.open(pipe_name, os.O_RDONLY)
        self.buffer_receive = os.read(pipe_in, 10000).decode("utf-8")
        os.close(pipe_in)

        if self.buffer_receive.replace(" ", "") != "":
            self.read()

    def string_to_tuple(string):
        string = string.replace("(", "")
        string = string.replace(")", "")
        string = string.replace(" ", "")

        tab = string.split(",")

        return (int(tab[0]), int(tab[1]))
        
        


        

