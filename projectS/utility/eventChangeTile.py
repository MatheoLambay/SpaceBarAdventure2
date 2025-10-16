
class eventChangeTile:
    def __init__(self,tile,new_tile,map):
        super().__init__()
        self.tile = tile
        self.new_tile = new_tile
        self.map = map
    

    def switch_tile(self):
      
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                
                if self.map[x][y] in self.tile:
                    self.map[x][y] = self.new_tile
      
        return self.map

       
        
        