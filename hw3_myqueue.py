class Stack:
    def __init__(self): 
        self.arr = []
    def push(self, item): 
        self.arr.append(item)
    def pop(self): 
        return self.arr.pop()
    def peek(self): 
        return self.arr[len(self.arr)-1]
    def isEmpty(self):
        if len(self.arr) == 0:
            return True
        else:
            return False
        
class MyQueue:
    def __init__(self):
        self.stack1 = Stack()
        self.stack2 = Stack() 
    def enqueue(self, item): 
        self.stack1.push(item)    
    def dequeue(self):
        for i in range(len(self.stack1.arr)):
            self.stack2.push(self.stack1.pop())
        item = self.stack2.arr.pop()
        for i in range(len(self.stack2.arr)):
            self.stack1.push(self.stack2.pop())        
        return item
    def peek(self):
        return self.stack1.arr[0]
    def isEmpty(self): 
        if len(self.stack1.arr) == 0:
            return True
        else:
            return False
        
items = [1,2,3,4,1,5]
     
my = MyQueue()
for item in items:
    my.enqueue(item)
    print(my.stack1.arr)
print('queued')
print(my.peek())
for i in range(len(items)+1):
    if my.isEmpty() == False:
        my.dequeue()
        print(my.stack1.arr)
    else:
        print('queue is empty')
