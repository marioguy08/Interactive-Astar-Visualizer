from tkinter import Tk, Canvas, Frame, BOTH, Button, Label
import time
import math
class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

class Astar(Frame):
    
    def __init__(self):                             ##### All these values can be adjusted
        self.dimension = 850                        ##### dimensions of window
        self.ncells = 50                            ##### number oc cells in row/collumn
        self.isclicked  = 0
        self.mousex = 0
        self.mousey = 0
        self.start = (1, 1)                         ##### starting coords
        self.end = (self.ncells-2, self.ncells-2)   ##### ending coords
        super().__init__()

        self.initUI()

    def update1(self,event):# if left mouse button is clicked
        self.isclicked += 1

    def update2(self,event):# if mouse is released
        self.isclicked -= 1

    def update3(self,event):# if mouse is moving, return x and y positions
        self.mousex = event.x
        self.mousey = event.y
    
    def estimateIndex(self,x,y):# given x and y mouse coords, finds corresponding index for matching rectangle object
        collumn = 0
        row = 0
        while(x>0):
            x-=self.cell_length
            collumn+=1
        while(y>0):
            y-=self.cell_length
            row+=1
        return collumn-1,row-1
 
    def initUI(self):
        self.cell_length = self.dimension/self.ncells
        self.rect = {}
        self.canvas = Canvas(self, width = self.dimension, height = self.dimension)
        self.text = Label(self, text="Welcome to the interactive A* Pathfinding visualizer! Click and drag to draw walls and rightclick to start ( You can also draw over squeares after alg is finished)", background = "black")
        self.text.config(fg='white')
        self.text.pack()
        
        self.pack(fill=BOTH , expand=1)
        for column in range(self.ncells):#create board
            for row in range(self.ncells):
                x1 = column*self.cell_length
                y1 = row*self.cell_length
                x2 = x1+self.cell_length
                y2 = y1+self.cell_length
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="black", tags="rect")

        tempid5 = self.rect[self.start[0],self.start[1]]
        self.canvas.itemconfig(tempid5, fill = "white")
        tempid5 = self.rect[self.end[0],self.end[1]]
        self.canvas.itemconfig(tempid5, fill = "white")
        button = Button(self, text="Clear Cells", fg="red",command = self.restart)
        button.pack(side='bottom')

        self.master.title("A*")
        self.canvas.pack(fill=BOTH, expand=1)
        self.redraw(1)
    
    def astarsearch(self,start,end):
        tempid = 0
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0
        open_list = []
        closed_list = []
        open_list.append(start_node)
        tempid = self.rect[start[0],start[1]]
        self.canvas.itemconfig(tempid, fill = "blue")
        
        while len(open_list) > 0:
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            open_list.pop(current_index)
            tempid3 = self.rect[current_node.position[0],current_node.position[1]]
            self.canvas.itemconfig(tempid3, fill = "gray10")
            
            
            closed_list.append(current_node)

            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                
                return path[::-1] # Return reversed path

            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                if node_position[0] > (self.ncells - 1) or node_position[0] < 0 or node_position[1] > (self.ncells-1) or node_position[1] < 0:
                    continue
                tempid = self.rect[node_position[0],node_position[1]]
                color = self.canvas.itemcget(tempid,"fill")
                if color == 'green':
                    continue
                if Node(current_node,node_position) in closed_list:
                    continue
                new_node = Node(current_node, node_position)
                tempid2 = self.rect[node_position[0],node_position[1]]
                self.canvas.itemconfig(tempid2, fill = "gray20")
                self.canvas.update_idletasks()
                time.sleep(.001)
                children.append(new_node)


            # Loop through children
            for child in children:
            # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        break
                else:
                # Create the f, g, and h values
                    child.g = current_node.g + 1
                    child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
                    child.f = child.g + child.h

                    # Child is already in the open list
                    for open_node in open_list:
                    # check if the new path to children is worst or equal 
                    # than one already in the open_list (by measuring g)
                        if child == open_node and child.g >= open_node.g:
                            break
                    else:
                    # Add the child to the open list
                        open_list.append(child)
    def restart(self):
        
        for column in range(self.ncells):#create board
            for row in range(self.ncells):
                tempid6 = self.rect[column,row]
                self.canvas.itemconfig(tempid6, fill = "black")
        tempid6 = self.rect[self.start[0],self.start[1]]
        self.canvas.itemconfig(tempid6, fill = "white")
        tempid6 = self.rect[self.end[0],self.end[1]]
        self.canvas.itemconfig(tempid6, fill = "white")
        
    def startAstar(self,event):
       
        
        ex = self.astarsearch(self.start,self.end)

        for coord in ex:# go back and recolor the shortest path purple
            tempid4 = self.rect[coord[0],coord[1]]
            self.canvas.itemconfig(tempid4, fill = "purple")
        return

    def redraw(self, delay):
        if(self.isclicked<0):
            self.isclicked+=1
        
        self.canvas.bind('<Button-1>', self.update1)
        self.canvas.bind('<Button-2>',self.startAstar)
        self.canvas.bind('<Button-3>', self.startAstar)
        self.canvas.bind('<ButtonRelease>', self.update2)
        self.canvas.bind('<Motion>',self.update3)
        print(self.isclicked)
        collumn,row = self.estimateIndex(self.mousex,self.mousey)
        if self.isclicked == 1 and collumn >-1 and row > -1 and collumn <= self.ncells-1 and row <=self.ncells-1: # if mouse if currently being clicked/depressed start coloring squares
            id = self.rect[row,collumn]
            self.canvas.itemconfig(id, fill = "green")
        self.after(delay, lambda: self.redraw(delay))
        
def main():
    root = Tk()
    ex = Astar()
    root.mainloop()
if __name__ == '__main__':
    main()