import pygame
from circuitboard import CircuitBoard
import sys
import COLORS
from random import randint


class Emulator():
    def __init__(self,arguments):
        # Debug
        self.DEBUG_MODE = True if ("DEBUG" in arguments) else False

        self.circuitboard = CircuitBoard()

        # Initialise Pygame
        pygame.init()
        self.SCREEN_W = 950
        self.SCREEN_H = 750
        self.canvas = pygame.Surface((self.SCREEN_W,self.SCREEN_H))
        self.screen = pygame.display.set_mode((self.SCREEN_W,self.SCREEN_H))

        # Initialise font
        self.initialise_font()

        # Emulator Status
        self.running = False if (self.DEBUG_MODE) else True
        self.turned_on = True


        # User Input
        self.actions = {"1":False, "2":False, "3":False, "4":False,
        "q":False,"w":False,"e":False,"r":False,
        "a":False,"s":False,"d":False,"f":False,
        "z":False,"x":False,"c":False,"v":False,
        "p": False, "o":False, "u": False, "i": False
        }

        ## TODO - change later
        # Current Game
        self.current_game_path = arguments[1]

        ## TODO - timing
        self.dt, self.prev_time = 0,0
        self.clock = pygame.time.Clock()

        # UI Elements
        self.register_UI = (700,50)
        self.instructions_UI = (700,300)
        self.call_stack_UI = (500,50)
        self.memory_UI = (20,400)
        self.screen_UI = (20,20)
        self.commands_UI = (20,300)

        self.display_pixel_size = 7 if self.DEBUG_MODE else 14

        self.instructions_to_display = []
        self.memory_addresses_to_display = [0x00,0x10,0x20,0x30,0x40,0x50,0x60,0x70,0x80,0x90,0xa0,0xb0,0xc0,0xd0,0xe0,0xf0]
        self.mem_scroll_offset = 0

        # SPECCIAL VARIABLE
        self.special_timer = 0



    

    def master_loop(self):
        # Call the functions like update, display etc here

        self.load_game()


        while self.turned_on:

            self.clock.tick(140)
            self.get_events()
            self.update()
            self.render()

            self.special_timer = (self.special_timer + 1) % 2






    ##### USER INPUT #####
    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.actions["1"] = True
                if event.key == pygame.K_2:
                    self.actions["2"] = True
                if event.key == pygame.K_3:
                    self.actions["3"] = True
                if event.key == pygame.K_4:
                    self.actions["4"] = True
                if event.key == pygame.K_q:
                    self.actions["q"] = True
                if event.key == pygame.K_w:
                    self.actions["w"] = True
                if event.key == pygame.K_e:
                    self.actions["e"] = True
                if event.key == pygame.K_r:
                    self.actions["r"] = True
                if event.key == pygame.K_a:
                    self.actions["a"] = True
                if event.key == pygame.K_s:
                    self.actions["s"] = True
                if event.key == pygame.K_d:
                    self.actions["d"] = True
                if event.key == pygame.K_f:
                    self.actions["f"] = True
                if event.key == pygame.K_z:
                    self.actions["z"] = True
                if event.key == pygame.K_x:
                    self.actions["x"] = True
                if event.key == pygame.K_c:
                    self.actions["c"] = True
                if event.key == pygame.K_v:
                    self.actions["v"] = True
                if event.key == pygame.K_p:
                    self.actions["p"] = True
                if event.key == pygame.K_o:
                    self.actions["o"] = True
                if event.key == pygame.K_u:
                    self.actions["u"] = True
                if event.key == pygame.K_i:
                    self.actions["i"] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    self.actions["1"] = False
                if event.key == pygame.K_2:
                    self.actions["2"] = False
                if event.key == pygame.K_3:
                    self.actions["3"] = False
                if event.key == pygame.K_4:
                    self.actions["4"] = False
                if event.key == pygame.K_q:
                    self.actions["q"] = False
                if event.key == pygame.K_w:
                    self.actions["w"] = False
                if event.key == pygame.K_e:
                    self.actions["e"] = False
                if event.key == pygame.K_r:
                    self.actions["r"] = False
                if event.key == pygame.K_a:
                    self.actions["a"] = False
                if event.key == pygame.K_s:
                    self.actions["s"] = False
                if event.key == pygame.K_d:
                    self.actions["d"] = False
                if event.key == pygame.K_f:
                    self.actions["f"] = False
                if event.key == pygame.K_z:
                    self.actions["z"] = False
                if event.key == pygame.K_x:
                    self.actions["x"] = False
                if event.key == pygame.K_c:
                    self.actions["c"] = False
                if event.key == pygame.K_v:
                    self.actions["v"] = False
                if event.key == pygame.K_p:
                    self.actions["p"] = False
                if event.key == pygame.K_o:
                    self.actions["o"] = False
                if event.key == pygame.K_u:
                    self.actions["u"] = False
                if event.key == pygame.K_i:
                    self.actions["i"] = False
                
    def reset_keys(self):
        for action in self.actions:
            self.actions[action] = False


    ##### LOAD GAME ######
    def load_game(self):
        # Read the ROM from file
        _tmp_data = []
        file = open(self.current_game_path,"rb")
        data_read_size = 1
        content = file.read(data_read_size)
        if content == b'':
            # FILE EMPTY, ERROR
            print("NO DATA IN ROM")
            return
        _tmp_data.append(int.from_bytes(content))
        while content != b'':
            content = file.read(data_read_size)
            if content != b'': _tmp_data.append(int.from_bytes(content))

        file.close()

        # Write to memory
        _addr_to_write = 0x200
        for data in _tmp_data:
            self.circuitboard.write_memory(_addr_to_write,data)
            _addr_to_write = _addr_to_write + 1


    ###### UPDATE STATE #####
    def update(self):
        # Case where emulator not paused
        if self.running == True:
            self.circuitboard.get_cpu().execute_single_cycle(self.actions)
            
            # Update delay timer
            if self.special_timer == 1:
                self.circuitboard.get_cpu().increment_delay()

            if self.actions["p"]:
                self.running = False
                self.reset_keys()
        # Case where emulator paused
        if self.DEBUG_MODE == True:
            if self.running == False:
                if self.actions["p"]:
                    self.running = True
                    self.reset_keys()
                elif self.actions["o"]:
                    self.reset_keys()
                    self.circuitboard.get_cpu().execute_single_cycle(self.actions)

                    # WARNING - Could Cause Issues
                    if self.special_timer == 1:
                        self.circuitboard.get_cpu().increment_delay()
                    

                if self.actions["i"] == True:
                    self.reset_keys()
                    # Scroll up
                    self.mem_scroll_offset += 0x10
                    if self.mem_scroll_offset > 0xf00:
                        self.mem_scroll_offset = 0xf00
                if self.actions["u"] == True:
                    self.reset_keys()
                    # Scroll down
                    self.mem_scroll_offset -= 0x10
                    if self.mem_scroll_offset < 0:
                        self.mem_scroll_offset = 0

        

    #### RENDERING #####
    def render(self):
        # Need to render the following:
        # => the game display
        # => the register information
        # => the instructions and the memory address of instructions
        # => the call stack

        self.canvas.fill(COLORS.BLUE)

        if self.DEBUG_MODE:
            self.display_registers()
            self.display_instructions()
            self.display_call_stack()
            self.display_commands()
            self.display_memory()


        self.display_screen()

        ## NOTE - just having basic display for now
        self.screen.blit(pygame.transform.scale(self.canvas,(self.SCREEN_W,self.SCREEN_H)),(0,0))
        pygame.display.flip()

    def display_registers(self):
        _xPos = self.register_UI[0]
        _yPos = self.register_UI[1]

        self.draw_text("Registers", _xPos, _yPos, self.emulator_font_big,COLORS.WHITE)
        self.draw_text(f"PC: 0x{self.circuitboard.get_cpu().get_PC()+2:02x}", _xPos,_yPos + 50,self.emulator_font_small,COLORS.WHITE)
        self.draw_text(f"SP: 0x{self.circuitboard.get_cpu().get_index_register():02x}",_xPos,_yPos + 70,self.emulator_font_small,COLORS.WHITE)
        self.draw_text(f"DR: 0x{self.circuitboard.get_cpu().get_delay_register():02x}",_xPos,_yPos + 90,self.emulator_font_small,COLORS.WHITE)
        self.draw_text(f"SR: 0x{self.circuitboard.get_cpu().get_sound_register():02x}",_xPos,_yPos + 110,self.emulator_font_small,COLORS.WHITE)

        _vregisters = self.circuitboard.get_cpu().get_v_registers()
        for ii in range(6):
            self.draw_text(f"v{ii:01x}: 0x{_vregisters[ii]:02x}",_xPos, _yPos + 130 + ii*20,self.emulator_font_small,COLORS.WHITE)

        for ii in range(10):
            self.draw_text(f"v{ii+6:01x}: 0x{_vregisters[ii + 6]:02x}",_xPos + 100, _yPos + 50 + ii*20,self.emulator_font_small,COLORS.WHITE)


    def display_instructions(self):
        _xPos = self.instructions_UI[0]
        _yPos = self.instructions_UI[1]

        self.draw_text("Instructions", _xPos,_yPos,self.emulator_font_big,COLORS.WHITE)

        ## TODO - get instruction addresses from memory, based on the instruction pointer
        _current_PC = self.circuitboard.get_cpu().get_PC()

        # Check if current PC is in the instruction list
        _b_PC_in_list = (_current_PC +2 in self.instructions_to_display)

        if _b_PC_in_list == False:
            self.instructions_to_display.clear()
            # Displaying 16 instructions, that's why there's 16 there
            # also, each instruction is 2 memory addresses apart. If
            # different instructions had different lengths, then would
            # need a dictionary to keep track of the lengths of each 
            # instruction
            for ii in range(16):
                self.instructions_to_display.append(_current_PC + 2*ii)

        # Now, draw the instructions
        for ii in range(len(self.instructions_to_display)):
            _memAddr = self.instructions_to_display[ii]
            _inst = self.circuitboard.get_cpu().disassemble_instruction(_memAddr)

            _string_to_display = f"0x{_memAddr:02x}" + "   " + _inst

            # The current instruction should be displayed as red
            _col = COLORS.WHITE
            if _memAddr -2 == self.circuitboard.get_cpu().get_PC():
                _col = COLORS.RED

            self.draw_text(_string_to_display, _xPos,_yPos + 50 + ii*20,self.emulator_font_medium,_col)

            
        

    def display_commands(self):
        _xPos = self.commands_UI[0]
        _yPos = self.commands_UI[1]

        _emulator_state_string = "RUNNING" if self.running else "PAUSED"

        self.draw_text("P: Toggle pause and run emulator",_xPos,_yPos,self.emulator_font_medium,COLORS.WHITE)
        self.draw_text("O: Step single instruction",_xPos,_yPos+25,self.emulator_font_medium,COLORS.WHITE)
        self.draw_text(f"Emulator State: {_emulator_state_string}",_xPos,_yPos+50,self.emulator_font_medium,COLORS.WHITE)
        self.draw_text("Memory scroll commands  I: scroll down  U: scroll up",_xPos,_yPos + 75,self.emulator_font_medium,COLORS.WHITE)




    def display_call_stack(self):
        _xPos = self.call_stack_UI[0]
        _yPos = self.call_stack_UI[1]

        self.draw_text("Call Stack",_xPos,_yPos,self.emulator_font_big,COLORS.WHITE)

        ## TODO - display the call stack
        _cs_length = self.circuitboard.get_callstack_length()
        if (_cs_length > 0 and _cs_length <= 5):
            # Display entire callstack
            for ii in range(_cs_length):
                _addr = self.circuitboard.get_callstack_element(ii)
                _addr_str = f"{ii+1}: 0x{_addr:02x}"
                self.draw_text(_addr_str, _xPos, _yPos + 50 + ii*20,self.emulator_font_medium,COLORS.WHITE)
        if (_cs_length > 5):
            # Display the final 5 addresses
            _index = _cs_length - 5 + ii
            _addr = self.circuitboard.get_callstack_element(_index)
            _addr_str = f"{ii+1}: 0x{_addrr:02x}"
            self.draw_text(_addr_str,_xPos,_yPos + 50 + ii+20,self.emulator_font_medium,COLORS.WHITE)


    def display_screen(self):
        _xPos = self.screen_UI[0]
        _yPos = self.screen_UI[1]

        _screen_array = self.circuitboard.get_display()
        _pixel_size = self.display_pixel_size
        for ii in range(len(_screen_array)):
            # Test, draw different colors
            col = (0,0,0)

            if _screen_array[ii] == 0: col = COLORS.BLACK
            if _screen_array[ii] == 1: col = COLORS.PINK


            _temprect = pygame.Rect(_xPos + (ii%64)*_pixel_size,_yPos + (ii//64)*_pixel_size,_pixel_size,_pixel_size)
            pygame.draw.rect(self.canvas,col,_temprect)

        
    def display_memory(self):
        _xPos = self.memory_UI[0]
        _yPos = self.memory_UI[1]

        self.draw_text("Memory",_xPos,_yPos,self.emulator_font_big,COLORS.WHITE)

        ## Display the memory
        for ii in range(14):
            # First draw address locations
            self.draw_text(f"0x{ii*16 + self.mem_scroll_offset:02x}",_xPos,_yPos +50+ ii*20,self.emulator_font_small,COLORS.WHITE)
            # Now draw the memory values
            for kk in range(16):
                self.draw_text(f"{self.circuitboard.read_memory(self.mem_scroll_offset + ii*16 + kk):02x}", _xPos + 50 + kk *20,_yPos + 50 + ii*20,self.emulator_font_small,COLORS.WHITE)



        _memory_array = self.circuitboard.get_full_memory()

        for ii in range(len(_memory_array)):
            pass



    ##### FONT AND TEXT #####
    def initialise_font(self):
        pygame.font.init()
        self.emulator_font_tiny = pygame.font.SysFont('arial',8)
        self.emulator_font_small = pygame.font.SysFont('arial',14)
        self.emulator_font_medium = pygame.font.SysFont('arial',20)
        self.emulator_font_big = pygame.font.SysFont('arial',40)

    def draw_text(self,text,x,y,font,color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.left = x
        text_rect.top = y
        self.canvas.blit(text_surface,text_rect)




