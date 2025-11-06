import helper
import random

class CPU():
    def __init__(self,circuitboard):
        
        self.circuitboard = circuitboard

        ## TODO - change default value of PC later
        # Instruction Pointer
        # WARNING - set PC to start at 0x1fe instead of 0x200, because
        # incrementing PC happens at start of FETCH-EXECUTE-DECODE cycle
        self.PC = 0x1fe

        # Index Register
        self.index_register = 0

        # Delay Timer
        self.delay_register_8bit = 0

        # Sound Timer
        self.sound_register_8bit = 0

        self.V_REGISTERS = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

        # TODO - fill the instruction dictionary
        self.instruction_dictionary = {}

    ##### UPDATE #####
    def execute_single_cycle(self,actions):
        # Increment PC
        self.PC += 2

        # Fetch current instruction word
        _instruction_first_word = self.circuitboard.read_memory(self.PC)
        _instruction_second_word = self.circuitboard.read_memory(self.PC +1)


        _digit1 = helper.extract_first_digit_s(_instruction_first_word)
        _digit2 = helper.extract_second_digit_s(_instruction_first_word)
        _digit3 = helper.extract_first_digit_s(_instruction_second_word)
        _digit4 = helper.extract_second_digit_s(_instruction_second_word)

        # Time to fetch the correct instruction, then execute
        
        # 00E0
        if (_digit1 == "0" and _digit4 == "0"):
            # Clear screen
            self.INST_00e0_clear()

        # 00EE
        if (_digit1 == "0" and _digit4 == "e"):
            # Return
            self.INST_00ee_return()

        # 1NNN
        if (_digit1 == "1"):
            # Jump
            self.INST_1NNN_jump(_digit2,_digit3,_digit4)

        # 2NNN
        if (_digit1 == "2"):
            self.INST_2NNN_call(_digit2,_digit3,_digit4)

        # 3XNN
        if (_digit1 == "3"):
            self.INST_3XNN(_digit1,_digit2,_digit3,_digit4)

        # 4XNN
        if (_digit1 == "4"):
            self.INST_4XNN(_digit1,_digit2,_digit3,_digit4)

        # 5XY0
        if (_digit1 == "5" and _digit4 == "0"):
            self.INST_5XY0(_digit1,_digit2,_digit3,_digit4)

        

        # 6XNN
        if (_digit1 == "6"):
            self.INST_6XNN(_digit2,_digit3,_digit4)

        # 7XNN
        if (_digit1 == "7"):
            self.INST_7XNN(_digit2,_digit3,_digit4)

        # 8XY0
        if (_digit1 == "8" and _digit4 == "0"):
            self.INST_8XY0(_digit2,_digit3)

        # 8XY1
        if (_digit1 == "8" and _digit4 == "1"):
            self.INST_8XY1(_digit1,_digit2,_digit3,_digit4)

        # 8XY2
        if (_digit1 == "8" and _digit4 == "2"):
            self.INST_8XY2(_digit1,_digit2,_digit3,_digit4)

        # 8XY3
        if (_digit1 == "8" and _digit4 == "3"):
            self.INST_8XY3(_digit1,_digit2,_digit3,_digit4)

        # 8XY4
        if (_digit1 == "8" and _digit4 == "4"):
            self.INST_8XY4(_digit1,_digit2,_digit3,_digit4)

        # 8XY5
        if (_digit1 == "8" and _digit4 == "5"):
            self.INST_8XY5(_digit1,_digit2,_digit3,_digit4)

        # 8XY6
        if (_digit1 == "8" and _digit4 == "6"):
            self.INST_8XY6(_digit1,_digit2,_digit3,_digit4)

        # 8XY7
        if (_digit1 == "8" and _digit4 == "7"):
            self.INST_8XY7(_digit1,_digit2,_digit3,_digit4)

        # 8XYe
        if (_digit1 == "8" and _digit4 == "e"):
            self.INST_8XYe(_digit1,_digit2,_digit3,_digit4)

        # 9XY0
        if (_digit1 == "9" and _digit4 == "0"):
            self.INST_9XY0(_digit1,_digit2,_digit3,_digit4)

        # ANNN
        if (_digit1 == "a"):
            self.INST_ANNN(_digit2,_digit3,_digit4)

        # BNNN
        if (_digit1 == "b"):
            self.INST_BNNN(_digit1,_digit2,_digit3,_digit4)

        # CXNN
        if (_digit1 == "c"):
            self.INST_CXNN(_digit1,_digit2,_digit3,_digit4)


        # DXYN
        if (_digit1 == "d"):
            self.INST_DXYN(_digit1,_digit2,_digit3,_digit4)

        # EX9E
        if (_digit1 == "e" and _digit3 == "9" and _digit4 == "e"):
            self.INST_EX9E(_digit1,_digit2,_digit3,_digit4,actions)

        # EXA1
        if (_digit1 == "e" and _digit3 == "a" and _digit4 == "1"):
            self.INST_EXA1(_digit1,_digit2,_digit3,_digit4,actions)

        # FX07
        if (_digit1 == "f" and _digit3 == "0" and _digit4 == "7"):
            self.INST_FX07(_digit1,_digit2,_digit3,_digit4)

        # FX0A
        if (_digit1 == "f" and _digit3 == "0" and _digit4 == "a"):
            self.INST_FX0A(_digit1,_digit2,_digit3,_digit4,actions)

        # FX15
        if (_digit1 == "f" and _digit3 == "1" and _digit4 == "5"):
            self.INST_FX15(_digit1,_digit2,_digit3,_digit4)

        # FX18
        if (_digit1 == "f" and _digit3 == "1" and _digit4 == "8"):
            self.INST_FX18(_digit1,_digit2,_digit3,_digit4)

        # FX1E
        if (_digit1 == "f" and _digit3 == "1" and _digit4 == "e"):
            self.INST_FX1E(_digit1,_digit2,_digit3,_digit4)

        # FX29
        if (_digit1 == "f" and _digit3 == "2" and _digit4 == "9"):
            self.INST_FX29(_digit1,_digit2,_digit3,_digit4)

        # FX33
        if (_digit1 == "f" and _digit3 == "3" and _digit4 == "3"):
            self.INST_FX33(_digit1,_digit2,_digit3,_digit4)

        # FX55
        if (_digit1 == "f" and _digit3 == "5" and _digit4 == "5"):
            self.INST_FX55(_digit1,_digit2,_digit3,_digit4)

        # FX65
        if (_digit1 == "f" and _digit3 == "6" and _digit4 == "5"):
            self.INST_FX65(_digit1,_digit2,_digit3,_digit4)



    

    ##### GETTER FUNCTIONS #####
    def get_PC(self):
        return self.PC

    def get_index_register(self):
        return self.index_register

    def get_delay_register(self):
        return self.delay_register_8bit

    def get_sound_register(self):
        return self.sound_register_8bit

    def get_v_registers(self):
        return self.V_REGISTERS

    def increment_delay(self):
        self.delay_register_8bit = (self.delay_register_8bit + 1) % 0xff


    ##### INSTRUCTIONS #####
    # Here, place the functions for the instructions 

    def INST_00e0_clear(self):
        self.circuitboard.clear_display()

    def INST_00ee_return(self):
        _addr = self.circuitboard.pop_address()
        self.PC = _addr #- 2

    def INST_1NNN_jump(self,digit2,digit3,digit4):
        final_address = (int(digit4,16) + int(digit3,16)*16 + int(digit2,16) * 16 * 16) - 2
        self.PC = final_address

    def INST_2NNN_call(self,digit2,digit3,digit4):
        _current_addr = self.PC
        self.circuitboard.push_address(_current_addr)
        _jump_address = (int(digit4,16) + int(digit3,16)*16 + int(digit2,16) * 16 * 16) -2
        self.PC = _jump_address

    def INST_3XNN(self,digit1,digit2,digit3,digit4):
        _register_index = int(digit2,16)
        _num = int(digit4,16) + int(digit3,16)*16

        #print(f"[***] DEBUG 3XNN _num = {_num}  r_index = {_register_index}")

        if self.V_REGISTERS[_register_index] == _num:
            #print("[*] DEBUG 3XNN skip instruction")
            self.PC += 2

    def INST_4XNN(self,digit1,digit2,digit3,digit4):
        _register_index = int(digit2,16)
        _num = int(digit4,16) + int(digit3,16)*16

        if self.V_REGISTERS[_register_index] != _num:
            self.PC += 2

    def INST_5XY0(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _index_y = int(digit3,16)

        if self.V_REGISTERS[_index_x] == self.V_REGISTERS[_index_y]:
            self.PC += 2

    

    def INST_6XNN(self,digit2,digit3,digit4):
        _rIndex = int(digit2,16)
        _value = int(digit4,16) + int(digit3,16)*16
        self.V_REGISTERS[_rIndex] = _value

    def INST_7XNN(self,digit2,digit3,digit4):
        _rIndex = int(digit2,16)
        _value = int(digit4,16) + int(digit3,16)*16
        self.V_REGISTERS[_rIndex] = (self.V_REGISTERS[_rIndex] + _value) % 0x100

    def INST_8XY0(self,digit2,digit3):
        _rxIndex = int(digit2,16)
        _ryIndex = int(digit3,16)
        _value = self.V_REGISTERS[_ryIndex]
        self.V_REGISTERS[_rxIndex] = _value

    def INST_8XY1(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _index_y = int(digit3,16)

        self.V_REGISTERS[_index_x] = (self.V_REGISTERS[_index_x]) | (self.V_REGISTERS[_index_y])

    def INST_8XY2(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _index_y = int(digit3,16)

        self.V_REGISTERS[_index_x] = (self.V_REGISTERS[_index_x]) & (self.V_REGISTERS[_index_y])

    def INST_8XY3(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _index_y = int(digit3,16)

        self.V_REGISTERS[_index_x] = (self.V_REGISTERS[_index_x]) ^ (self.V_REGISTERS[_index_y])

    def INST_8XY4(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _index_y = int(digit3,16)

        self.V_REGISTERS[0x0f] = 0

        _sum = self.V_REGISTERS[_index_x] + self.V_REGISTERS[_index_y]

        if _sum > 0xff:
            self.V_REGISTERS[0x0f] = 1
        
        self.V_REGISTERS[_index_x] = _sum % 0x100

    def INST_8XY5(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _index_y = int(digit3,16)

        self.V_REGISTERS[0x0f] = 1

        _result = self.V_REGISTERS[_index_x] - self.V_REGISTERS[_index_y]

        if _result < 0:
            self.V_REGISTERS[0x0f] = 0

        self.V_REGISTERS[_index_x] = _result % 0x100

    def INST_8XY6(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _index_y = int(digit3,16)

        _val = self.V_REGISTERS[_index_y] 
        _old_lsb = helper.get_nth_bit(_val,7)
        _val = (_val >> 1) & 0xff
        self.V_REGISTERS[_index_x] = _val

    def INST_8XY7(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _index_y = int(digit3,16)

        self.V_REGISTERS[0x0f] = 1
        _result = self.V_REGISTERS[_index_y] - self.V_REGISTERS[_index_x]

        if (_result < 0):
            self.V_REGISTERS[0x0f] = 0
        
        self.V_REGISTERS[_index_x] = _result % 0x100

    def INST_8XYe(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _index_y = int(digit3,16)

        _val = self.V_REGISTERS[_index_y]
        _old_msb = helper.get_nth_bit(_val,0)
        _val = (_val << 1) & 0xff
        self.V_REGISTERS[_index_x] = _val



    def INST_9XY0(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _index_y = int(digit3,16)

        if self.V_REGISTERS[_index_x] != self.V_REGISTERS[_index_y]:
            self.PC += 2

    def INST_ANNN(self,digit2,digit3,digit4):
        _value = int(digit4,16) + int(digit3,16)*16 + int(digit2,16)*16*16
        self.index_register = _value

    def INST_BNNN(self,digit1,digit2,digit3,digit4):
        _base = int(digit4,16) + int(digit3,16) * 16 + int(digit2,16) * 16*16
        _offset = self.V_REGISTERS[0x00]

        _jmp_addr = _base + _offset

        self.PC = _jmp_addr - 2

    def INST_CXNN(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _operand = int(digit4,16) + int(digit3,16)*16

        _result = random.randint(0,255) & _operand

        self.V_REGISTERS[_index_x] = _result




    def INST_DXYN(self,digit1,digit2,digit3,digit4):
        _xStartPos = (self.V_REGISTERS[int(digit2,16)]) % 64
        _yStartPos = (self.V_REGISTERS[int(digit3,16)]) % 32

        _x = _xStartPos
        _y = _yStartPos

        _I = self.get_index_register()
        _N_value = int(digit4,16)

        # Set VF to 0
        self.V_REGISTERS[0xf] = 0

        for ii in range(_N_value):
            _pixel_data = self.circuitboard.read_memory(_I + ii)
            for kk in range(8):
                _bit = helper.get_nth_bit(_pixel_data, kk)
                _can_draw = True


                # Error check
                #if (_x + kk) < 0 or (_x + kk) > 63:
                #    _can_draw = False
                #if (_y + ii) < 0 or (_y + ii) > 31:
                #    _can_draw = False
                
                #if (_can_draw):
                if (_bit == 1 and self.circuitboard.get_display_pixel(_x + kk,_y+ ii) == 1):
                    self.V_REGISTERS[0xf] = 1
                    self.circuitboard.set_display(0,_x + kk,_y + ii)
                elif (_bit == 1 and self.circuitboard.get_display_pixel(_x + kk,_y + ii) == 0):
                    self.circuitboard.set_display(1,_x + kk,_y + ii)

    def INST_EX9E(self,digit1,digit2,digit3,digit4,actions):
        _index_x = int(digit2,16)
        _hex_to_key = {0x01:"1",0x02:"2",0x03:"3",0x0c:"4",
        0x04:"q",0x05:"w",0x06:"e",0x0d:"r",
        0x07:"a",0x08:"s",0x09:"d",0x0e:"f",
        0x0a:"z",0x00:"x",0x0b:"c",0x0f:"v"
        }

        if self.V_REGISTERS[_index_x] < 0 or self.V_REGISTERS[_index_x] > 0x0f:
            #print("ERROR WITH INPUT INST_EX9E")
            #print("USING TRICKS TO FIX ERROR")
            self.V_REGISTERS[_index_x] = self.V_REGISTERS[_index_x] % 0x10
            return None
        _key_to_check = _hex_to_key[self.V_REGISTERS[_index_x]]
        #print(f"[*] DEBUG EX9E _key_to_check = {_key_to_check}")

        if actions[_key_to_check] == True:
            self.PC += 2



    def INST_EXA1(self,digit1,digit2,digit3,digit4,actions):
        _index_x = int(digit2,16)
        _hex_to_key = {0x01:"1",0x02:"2",0x03:"3",0x0c:"4",
        0x04:"q",0x05:"w",0x06:"e",0x0d:"r",
        0x07:"a",0x08:"s",0x09:"d",0x0e:"f",
        0x0a:"z",0x00:"x",0x0b:"c",0x0f:"v"
        }

        if self.V_REGISTERS[_index_x] < 0 or self.V_REGISTERS[_index_x] > 0x0f:
            print("ERROR WITH INPUT INST_EXA1")
            return None

        _key_to_check = _hex_to_key[self.V_REGISTERS[_index_x]]

        if actions[_key_to_check] == False:
            self.PC += 2



    def INST_FX07(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        self.V_REGISTERS[_index_x] = self.delay_register_8bit

    def INST_FX0A(self,digit1,digit2,digit3,digit4,actions):
        _index_x = int(digit2,16)
        _button_pressed = False

        _result = 0x00

        if actions["1"] == True:
            _result = 0x01
            _button_pressed = True
        if actions["2"] == True:
            _result = 0x02
            _button_pressed = True
        if actions["3"] == True:
            _result = 0x03
            _button_pressed = True
        if actions["4"] == True:
            _result = 0x0c
            _button_pressed = True
        if actions["q"] == True:
            _result = 0x04
            _button_pressed = True
        if actions["w"] == True:
            _result = 0x05
            _button_pressed = True
        if actions["e"] == True:
            _result = 0x06
            _button_pressed = True
        if actions["r"] == True:
            _result = 0x0d
            _button_pressed = True
        if actions["a"] == True:
            _result = 0x07
            _button_pressed = True
        if actions["s"] == True:
            _result = 0x08
            _button_pressed = True
        if actions["d"] == True:
            _result = 0x09
            _button_pressed = True
        if actions["f"] == True:
            _result = 0x0e
            _button_pressed = True
        if actions["z"] == True:
            _result = 0x0a
            _button_pressed = True
        if actions["x"] == True:
            _result = 0x00
            _button_pressed = True
        if actions["c"] == True:
            _result = 0x0b
            _button_pressed = True
        if actions["v"] == True:
            _result = 0x0f
            _button_pressed = True

        if (_button_pressed == True):
            self.V_REGISTERS[_index_x] = _result
        elif (_button_pressed == False):
            self.PC -= 2
            






    def INST_FX15(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        self.delay_register_8bit = self.V_REGISTERS[_index_x]

    def INST_FX18(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        self.sound_register_8bit = self.V_REGISTERS[_index_x]

    def INST_FX1E(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        self.index_register += self.V_REGISTERS[_index_x]

    def INST_FX29(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)
        _char_index = self.V_REGISTERS[_index_x]

        _char_loc = self.circuitboard.get_font_location_start() + _char_index*5

        self.index_register = _char_loc

    def INST_FX33(self,digit1,digit2,digit3,digit4):
        _index_x = int(digit2,16)

        _num = self.V_REGISTERS[_index_x]


        _I = self.index_register

        # Digits extracted in form (d1)(d2)(d3)
        _d1,_d2,_d3 = helper.extract_digits(_num)

        ## DEBUG
        print(f"[*] DEBUG FX33 _num = {_num}")
        print(f"digits = ({_d1})({_d2})({_d3})")
        print(f"index = 0x{_I:02x}")

        # Place values in memory
        self.circuitboard.write_memory(_I,_d1)
        self.circuitboard.write_memory(_I + 1, _d2)
        self.circuitboard.write_memory(_I + 2, _d3)

    def INST_FX55(self,digit1,digit2,digit3,digit4):
        _index = int(digit2,16)

        _I = self.index_register

        for ii in range(_index + 1):
            self.circuitboard.write_memory(_I + ii, self.V_REGISTERS[ii])

    def INST_FX65(self,digit1,digit2,digit3,digit4):
        _index = int(digit2,16)

        _I = self.index_register

        for ii in range(_index + 1):
            self.V_REGISTERS[ii] = self.circuitboard.read_memory(_I + ii)

                
                



        


    ##### DISASSEMBLY #####
    # Here, have functions related to disassembling the instuctions
    def disassemble_instruction(self,mem_addr):
        # First, get the instruction bytes
        _first = self.circuitboard.read_memory(mem_addr)
        _second = self.circuitboard.read_memory(mem_addr +1)

        _digit1 = helper.extract_first_digit_s(_first)
        _digit2 = helper.extract_second_digit_s(_first)
        _digit3 = helper.extract_first_digit_s(_second)
        _digit4 = helper.extract_second_digit_s(_second)

        inst = ""

        # 00e0
        if (_digit1 == "0" and _digit4 == "0"):
            inst += self.DISAS_00e0(_digit1,_digit2,_digit3,_digit4)

        # 00ee
        elif (_digit1 == "0" and _digit4 == "e"):
            inst += self.DISAS_00ee(_digit1,_digit2,_digit3,_digit4)

        # 1NNN
        elif (_digit1 == "1"):
            inst += self.DISAS_1NNN(_digit1,_digit2,_digit3,_digit4)

        # 2NNN
        elif (_digit1 == "2"):
            inst += self.DISAS_2NNN(_digit1,_digit2,_digit3,_digit4)

        # 3XNN
        elif (_digit1 == "3"):
            inst += self.DISAS_3XNN(_digit1,_digit2,_digit3,_digit4)

        # 4XNN
        elif (_digit1 == "4"):
            inst += self.DISAS_4XNN(_digit1,_digit2,_digit3,_digit4)

        # 5XY0
        elif (_digit1 == "5"):
            inst += self.DISAS_5XY0(_digit1,_digit2,_digit3,_digit4)

        # 6XNN
        elif (_digit1 == "6"):
            inst += self.DISAS_6XNN(_digit1,_digit2,_digit3,_digit4)

        #7XNN
        elif (_digit1 == "7"):
            inst += self.DISAS_7XNN(_digit1,_digit2,_digit3,_digit4)

        # 8XY0
        elif (_digit1 == "8" and _digit4 == "0"):
            inst += self.DISAS_8XY0(_digit1,_digit2,_digit3,_digit4)

        # 8XY1
        elif (_digit1 == "8" and _digit4 == "1"):
            inst += self.DISAS_8XY1(_digit1,_digit2,_digit3,_digit4)

        # 8XY2
        elif (_digit1 == "8" and _digit4 == "2"):
            inst += self.DISAS_8XY2(_digit1,_digit2,_digit3,_digit4)

        # 8XY3
        elif (_digit1 == "8" and _digit4 == "3"):
            inst += self.DISAS_8XY3(_digit1,_digit2,_digit3,_digit4)

        # 8XY4
        elif (_digit1 == "8" and _digit4 == "4"):
            inst += self.DISAS_8XY4(_digit1,_digit2,_digit3,_digit4)

        # 8XY5
        elif (_digit1 == "8" and _digit4 == "5"):
            inst += self.DISAS_8XY5(_digit1,_digit2,_digit3,_digit4)

        # 8XY6
        elif (_digit1 == "8" and _digit4 == "6"):
            inst += self.DISAS_8XY6(_digit1,_digit2,_digit3,_digit4)

        # 8XY7
        elif (_digit1 == "8" and _digit4 == "7"):
            inst += self.DISAS_8XY7(_digit1,_digit2,_digit3,_digit4)

        # 8XYe
        elif (_digit1 == "8" and _digit4 == "e"):
            inst += self.DISAS_8XYe(_digit1,_digit2,_digit3,_digit4)

        # 9XY0
        elif (_digit1 == "9"):
            inst += self.DISAS_9XY0(_digit1,_digit2,_digit3,_digit4)

        # aNNN
        elif (_digit1 == "a"):
            inst += self.DISAS_aNNN(_digit1,_digit2,_digit3,_digit4)

        # bNNN
        elif (_digit1 == "b"):
            inst += self.DISAS_bNNN(_digit1,_digit2,_digit3,_digit4)

        # cXNN
        elif (_digit1 == "c"):
            inst += self.DISAS_cXNN(_digit1,_digit2,_digit3,_digit4)

        # dXYN
        elif (_digit1 == "d"):
            inst += self.DISAS_dXYN(_digit1,_digit2,_digit3,_digit4)

        # eX9e
        elif (_digit1 == "e" and _digit4 == "e"):
            inst += self.DISAS_eX9e(_digit1,_digit2,_digit3,_digit4)

        # eXa1
        elif (_digit1 == "e" and _digit4 == "1"):
            inst += self.DISAS_eXa1(_digit1,_digit2,_digit3,_digit4)

        # fX07
        elif (_digit1 == "f" and _digit3 == "0" and _digit4 == "7"):
            inst += self.DISAS_fX07(_digit1,_digit2,_digit3,_digit4)

        # fX0a
        elif (_digit1 == "f" and _digit3 == "0" and _digit4 == "a"):
            inst += self.DISAS_fX0a(_digit1,_digit2,_digit3,_digit4)

        # fX15
        elif (_digit1 == "f" and _digit3 == "1" and _digit4 == "5"):
            inst += self.DISAS_fX15(_digit1,_digit2,_digit3,_digit4)

        # fX18
        elif (_digit1 == "f" and _digit3 == "1" and _digit4 == "8"):
            inst += self.DISAS_fX18(_digit1,_digit2,_digit3,_digit4)

        # fX1e
        elif (_digit1 == "f" and _digit3 == "1" and _digit4 == "e"):
            inst += self.DISAS_fX1e(_digit1,_digit2,_digit3,_digit4)

        # fX29
        elif (_digit1 == "f" and _digit3 == "2" and _digit4 == "9"):
            inst += self.DISAS_fX29(_digit1,_digit2,_digit3,_digit4)

        # fX33
        elif (_digit1 == "f" and _digit3 == "3" and _digit4 == "3"):
            inst += self.DISAS_fX33(_digit1,_digit2,_digit3,_digit4)

        # fX55
        elif (_digit1 == "f" and _digit3 == "5" and _digit4 == "5"):
            inst += self.DISAS_fX55(_digit1,_digit2,_digit3,_digit4)

        # fX65
        elif (_digit1 == "f" and _digit3 == "6" and _digit4 == "5"):
            inst += self.DISAS_fX65(_digit1,_digit2,_digit3,_digit4)


        

        return inst

    def DISAS_00e0(self,digit1,digit2,digit3,digit4):
        _disas = "clear"
        return _disas

    def DISAS_00ee(self,digit1,digit2,digit3,digit4):
        _disas = "return"
        return _disas

    def DISAS_1NNN(self,digit1,digit2,digit3,digit4):
        _disas = "jmp " + digit2 + digit3 + digit4 
        return _disas

    def DISAS_2NNN(self,digit1,digit2,digit3,digit4):
        _disas = "call " + digit2 + digit3 + digit4 
        return _disas

    def DISAS_3XNN(self,digit1,digit2,digit3,digit4):
        _disas = "if v" + digit2 + " != " + digit3 + digit4
        return _disas

    def DISAS_4XNN(self,digit1,digit2,digit3,digit4):
        _disas = "if v" + digit2 + " == " + digit3 + digit4
        return _disas

    def DISAS_5XY0(self,digit1,digit2,digit3,digit4):
        _disas = "if v" + digit2 + " != v" + digit3
        return _disas

    def DISAS_6XNN(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " := " + digit3 + digit4
        return _disas

    def DISAS_7XNN(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " += " + digit3 + digit4
        return _disas

    def DISAS_8XY0(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " := " + "v" + digit3
        return _disas

    def DISAS_8XY1(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " |= " + "v" + digit3
        return _disas

    def DISAS_8XY2(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " &= " + "v" + digit3
        return _disas

    def DISAS_8XY3(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " ^= " + "v" + digit3
        return _disas

    def DISAS_8XY4(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " += " + "v" + digit3
        return _disas

    def DISAS_8XY5(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " -= " + "v" + digit3
        return _disas

    def DISAS_8XY6(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " >>= " + "v" + digit3
        return _disas

    def DISAS_8XY7(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " =- " + "v" + digit3
        return _disas

    def DISAS_8XYe(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " <<= " + "v" + digit3
        return _disas

    def DISAS_9XY0(self,digit1,digit2,digit3,digit4):
        _disas = "if v" + digit2 + " == " + "v" + digit3
        return _disas

    def DISAS_aNNN(self,digit1,digit2,digit3,digit4):
        _disas = "i := " + digit2 + digit3 + digit4
        return _disas

    def DISAS_bNNN(self,digit1,digit2,digit3,digit4):
        _disas = "jump0 " + digit2 + digit3 + digit4
        return _disas

    def DISAS_cXNN(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " := random " + digit3 + digit4
        return _disas

    def DISAS_dXYN(self,digit1,digit2,digit3,digit4):
        _disas = "sprite v" + digit2 + " v" + digit3 + " " + digit4
        return _disas

    def DISAS_eX9e(self,digit1,digit2,digit3,digit4):
        _disas = "if v" + digit2 + " -key"
        return _disas

    def DISAS_eXa1(self,digit1,digit2,digit3,digit4):
        _disas = "if v" + digit2 + " key"
        return _disas

    def DISAS_fX07(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " := delay"
        return _disas

    def DISAS_fX0a(self,digit1,digit2,digit3,digit4):
        _disas = "v" + digit2 + " := key"
        return _disas

    def DISAS_fX15(self,digit1,digit2,digit3,digit4):
        _disas = "delay := v" + digit2
        return _disas

    def DISAS_fX18(self,digit1,digit2,digit3,digit4):
        _disas = "buzzer := v" + digit2
        return _disas

    def DISAS_fX1e(self,digit1,digit2,digit3,digit4):
        _disas = "i += v" + digit2
        return _disas

    def DISAS_fX29(self,digit1,digit2,digit3,digit4):
        _disas = "i := hex v" + digit2
        return _disas

    def DISAS_fX33(self,digit1,digit2,digit3,digit4):
        _disas = "bcd v" + digit2
        return _disas

    def DISAS_fX55(self,digit1,digit2,digit3,digit4):
        _disas = "save v" + digit2
        return _disas

    def DISAS_fX65(self,digit1,digit2,digit3,digit4):
        _disas = "load v" + digit2
        return _disas





