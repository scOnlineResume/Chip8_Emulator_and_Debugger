from cpu import CPU

class CircuitBoard():
    def __init__(self):
        self.cpu = CPU(self)

        # Memory array, represents the Random Access Memory
        self.memory = [0x00] * 4096

        # Call stack that's used to keep track of function calls
        self.call_stack = []

        # Array that represents screen
        self.display = [0] * (64*32)

        # SPECIAL VARIABLE - maybe delete later
        self.font_location_start = 0


        self.font_init()

    ##### MEMORY MANIPULATION #####
    def read_memory(self,address):
        if address >= 0 and address <= 4096:
            return self.memory[address]
    
    def write_memory(self,address,data):
        if address >= 0 and address <= 4096:
            self.memory[address] = data

    def get_full_memory(self):
        return self.memory

    ##### CALL STACK MANIPULATION #####
    def push_address(self,address):
        self.call_stack.append(address)

    def pop_address(self):
        if len(self.call_stack) > 0:
            _addr = self.call_stack[-1]
            self.call_stack.pop()
            return _addr

    def get_callstack_element(self,index):
        return self.call_stack[index]

    def get_callstack_length(self):
        return len(self.call_stack)

    ##### DISPLAY MANIPULATION #####
    def get_display(self):
        return self.display

    def get_display_pixel(self,x,y):
        # Handle for errors
        if x < 0 or x > 63 or y < 0 or y > 31:
            return None
        return self.display[64*y + x]

    def set_display(self,value,x,y):
        # Handle for errors
        x = x % 64
        y = y % 32
        self.display[64*y + x] = value

    def clear_display(self):
        for ii in range(len(self.display)):
            self.display[ii] = 0

    ##### GET CPU #####
    def get_cpu(self):
        return self.cpu

    ##### FONT #####
    def get_font_location_start(self):
        return self.font_location_start

    ##### INITIALIZATION #####
    def font_init(self):
        _font_array = [
            0xf0 ,0x90, 0x90 ,0x90, 0xf0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xf0, 0x10, 0xf0, 0x80, 0xf0, # 2
            0xf0, 0x10, 0xf0, 0x80, 0xf0, # 3
            0x90, 0x90, 0xf0, 0x10, 0x10, # 4
            0xf0, 0x80, 0xf0, 0x10, 0xf0, # 5
            0xf0, 0x80, 0xf0, 0x90, 0xf0, # 6
            0xf0, 0x10, 0x20, 0x40, 0x40, # 7
            0xf0, 0x90, 0xf0, 0x90, 0xf0, # 8
            0xf0, 0x90, 0xf0, 0x90, 0xf0, # 9
            0xf0, 0x90, 0xf0, 0x90, 0x90, # a
            0xe0, 0x90, 0xe0, 0x90, 0xe0, # b
            0xf0, 0x80, 0x80, 0x80, 0xf0, # c
            0xe0, 0x90, 0x90, 0x90, 0xe0, # d
            0xf0, 0x80, 0xf0, 0x80, 0xf0, # e
            0xf0, 0x80, 0xf0, 0x80, 0x80  # f
        ]

        for ii in range(len(_font_array)):
            self.memory[ii + self.font_location_start] = _font_array[ii]

