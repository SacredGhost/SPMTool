import os
import sys
import time
import configparser
from typing import Callable, Any
from watches import ByteArrayMemoryWatch, Datatype, get_address, get_watch
from keypresses import PressRelease, keyCodeMap

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read('settings.config')
    key_code = config['Settings']['SplitKey']
    Enter6AgainSplit = config['Settings']['Enter6AgainSplit']
    Enter7AgainSplit = config['Settings']['Enter7AgainSplit']
    CountBleckSplit = config['Settings']['CountBleckSplit']

    if CountBleckSplit == 'True':
        CountBleckSplit = True
    elif CountBleckSplit == 'False':
        CountBleckSplit = False

    epitsplits = config['Settings']['ExtraPitSplits']

    print(f'{"[" + "Console" + "]":>15} SPM Auto Splitter [vBeta2]')

    def do_split(delay):
        current_framecount = frame_count.read()
        while frame_count.read() < current_framecount + delay:
            time.sleep(1 / FPS)
        PressRelease(keyCodeMap[key_code], 100)
        msec_wait(5000)

    def frame_wait(delay):
        current_framecount = frame_count.read()
        while frame_count.read() < current_framecount + delay:
            time.sleep(1 / FPS)

    def msec_wait(delay):
        frame_wait(delay / 1000 * FPS)

    FPS = get_watch("fps").read()
    SLEEP_TIME = 5 # DO NOT CHANGE
    START_OR_CREDITS_DELAY = 0 # DO NOT CHANGE
    STAR_BLOCK_SPLIT_DELAY = 240 # Default: 240 frames
    PURE_HEART_SPLIT_DELAY = 727 # Default: 727 frames
    ROCK_HEART_SPLIT_DELAY = 721 # Default: 721 frames
    DOOR_CLOSE_SPLIT_DELAY = 0 # Default: 0 frames
    FADEOUT_DOOR_SPLIT_DELAY = 84 # Default: 84 frames
    RETURN_SPLIT_DELAY = 426 # Default: 426 frames
    CB_DEFEAT_DELAY = 150 # Default: 150 frames
    SD_DEFEAT_DELAY = 40 # Default: 40 frames
    RETURN_PIPE_DELAY = 282 # Default: 282 frames
    DOWN_PIPE_DELAY = 156 # Default: 156 frames 

    ANY_SPLIT_MAPS = ("mac_02", "mac_12", "ls4_10")
    PIT_MAPS = ("dan_01", "dan_02", "dan_03", "dan_04", "dan_41", "dan_42", "dan_43", "dan_44")
    PIT_10_MAPS = ("dan_21", "dan_22", "dan_23", "dan_24", "dan_30", "dan_61", "dan_62", "dan_63", "dan_64", "dan_70")

    RECIPE_BIT_MASK = 0x20

    EVT_ENTRY_SIZE = 0x1a8
    EVT_ENTRY_SCRIPT_PTR_OFFSET = 0x198

    STAR_BLOCK_EVT_SCRIPT = get_address("star_block_evt_script")
    PURE_HEART_EVT_SCRIPT = get_address("pure_heart_evt_script")
    DOOR_CLOSE_EVT_SCRIPT = get_address("door_close_evt_script")
    RETURN_EVT_SCRIPT = get_address("return_evt_script")
    CB_DEFEAT_EVT_SCRIPT = get_address("CB_defeat_evt_script")
    SD_DEFEAT_EVT_SCRIPT = get_address("SD_defeat_evt_script")
    CREDITS_START_SCRIPT = get_address("credits_start_evt_script")
    RETURN_PIPE_SCRIPT = get_address("return_pipe_evt_script")
    DOWN_PIPE_EVT_SCRIPT = get_address("down_pipe_evt_script")
    TOWN_DOOR_EVT_SCRIPT = get_address("town_door_evt_script")

    evt_entry_count = get_watch("evt_entry_count").read()
    evt_entries = ByteArrayMemoryWatch(get_watch("evt_entries_ptr").read(), evt_entry_count * EVT_ENTRY_SIZE)
    frame_count = get_watch("frameCount")
    sequence_position = get_watch("SequencePosition")
    mariox = get_watch("Mario_X")
    marioz = get_watch("Mario_Z")
    map = get_watch("CurrentMap")
    effcurcount = get_watch("EffTypeStats_curCount")
    textopacity1 = get_watch("text_opacity_1")
    textopacity2 = get_watch("text_opacity_2")
    buttonsBUTHeld = get_watch("buttonsBUTHeld")
    buttonsPADHeld = get_watch("buttonsPADHeld")
    seqLoadWork_state = get_watch('seqLoadWork_state')
    knownRecipe_Byte6 = get_watch("knownRecipesByte6")
    knownRecipe_Byte7 = get_watch("knownRecipesByte7")
    buttonsBUTHeld = get_watch("buttonsBUTHeld")
    buttonsPADHeld = get_watch("buttonsPADHeld")
    gsw1 = get_watch("GSW(1)")

    text_box_count1 = 0
    text_box_count2 = 0
    fileError = False
    filestart = True
    pit_run = False
    hundo_run = False
    hundo_sequence = 0
    flopPit = 1

    extra_pit_splits = epitsplits

    current_framecount = frame_count.read()
    current_map = map.read()
    current_map_p = current_map[:3]
    current_sequence = sequence_position.read()
    current_effcurcount = effcurcount.read()
    current_text_opacity_1 = textopacity1.read()
    current_text_opacity_2 = textopacity2.read()
    current_loadSeq = seqLoadWork_state.read()
    current_recipeByte6 = knownRecipe_Byte6.read()
    current_recipeByte7 = knownRecipe_Byte6.read() 
    currentBUTbutton = buttonsBUTHeld.read()
    currentPADbutton = buttonsPADHeld.read()
    currentGSW1 = gsw1.read()

    def findInStructArray(arr: ByteArrayMemoryWatch, struct_size: int, offset: int, to_find: list[int], to_find_datatype: Datatype, callback: Callable[[int], Any]):
        for i in range(arr.size // struct_size):
            val = arr.read(i * struct_size + offset, to_find_datatype)

            if val not in to_find:
                continue

            if callback is not None:
                callback(val)

    def evt_entry_cb(script_ptr: int):
        global current_map
        global current_effcurcount
        global current_text_opacity_1
        global current_text_opacity_2
        global text_box_count1
        global text_box_count2
        global current_loadSeq
        global current_framecount
        global pit_run
        global hundo_run
        global extra_pit_splits
        global hundo_sequence

        if script_ptr == STAR_BLOCK_EVT_SCRIPT:
            print(f'{"[" + "Console" + "]":>15} Detected Star Block Hit')
            do_split(STAR_BLOCK_SPLIT_DELAY)
            if hundo_sequence == 12:
                print(f'{"[" + "Console" + "]":>15} GG :)')

        if script_ptr == PURE_HEART_EVT_SCRIPT:
            print(f'{"[" + "Console" + "]":>15} Pure Heart Detected')
            if current_map == "wa1_27":
                do_split(ROCK_HEART_SPLIT_DELAY)
            else:
                do_split(PURE_HEART_SPLIT_DELAY)
        
        if script_ptr == RETURN_EVT_SCRIPT:
            print(f'{"[" + "Console" + "]":>15} Return Cutscene')
            do_split(RETURN_SPLIT_DELAY)

        if script_ptr == DOOR_CLOSE_EVT_SCRIPT and (current_map in ANY_SPLIT_MAPS or current_map in PIT_MAPS or current_map in PIT_10_MAPS):
            marioposx = mariox.read()
            currentGSW1 = gsw1.read()
            current_map = map.read()

            valid_door = True
            split_delay = DOOR_CLOSE_SPLIT_DELAY
            door_name = 'None'

            if current_map == 'mac_02':
                if current_sequence == 9 and (-490 <= marioposx <= -410):
                    door_name = 'Chapter 1'
                elif current_sequence == 65 and (-340 <= marioposx <= -260):
                    door_name = 'Chapter 2'
                elif current_sequence == 100 and (-190 <= marioposx <= -110):
                    door_name = 'Chapter 3'
                elif current_sequence == 134 and (-40 <= marioposx <= 40):
                    door_name = 'Chapter 4'
                elif current_sequence == 178 and (110 <= marioposx <= 190):
                    door_name = 'Chapter 5'
                elif 222 <= current_sequence <= 224 and (260 <= marioposx <= 340):
                    door_name = 'Chapter 6'
                elif Enter6AgainSplit:
                    if current_sequence == 281 and (260 <= marioposx <= 340):
                        door_name = 'Chapter 6-?'
                elif Enter7AgainSplit:
                    if current_sequence == 303 and (410 <= marioposx <= 490):
                        door_name = 'Chapter 7'
            elif current_map == "mac_12":
                if current_sequence in (356,357) and (-80 <= marioposx <= -80):
                    door_name = 'Chapter 8'
            elif current_sequence == 409 and (1100 <= marioposx <= 1200):
                door_name = 'Bleck'
                split_delay = FADEOUT_DOOR_SPLIT_DELAY
            elif current_map in PIT_MAPS or current_map in PIT_10_MAPS:
                if current_map in PIT_MAPS:
                    if extra_pit_splits:
                        split_delay = FADEOUT_DOOR_SPLIT_DELAY
                        door_name = "Pit"
                    elif current_map in PIT_MAPS:
                        valid_door = False
                    if currentGSW1 == 99 and extra_pit_splits == False:
                        if current_map == "dan_04" or current_map == "dan_44":
                            split_delay = FADEOUT_DOOR_SPLIT_DELAY
                            door_name = "Room 99"
                            if flopPit == 1:
                                valid_door = False
                            else:
                                valid_door = True
                if current_map in PIT_10_MAPS:
                    if current_map != "dan_30" or current_map != "dan_70":
                        if marioposx > 250:
                            split_delay = FADEOUT_DOOR_SPLIT_DELAY
                            door_name = "Pit Checkpoint"
                            valid_door = True
                        else:
                            valid_door = False
            elif current_map == "mac_02" and current_sequence == 127:
                if (-490 <= marioposx <= -410):
                    door_name = "1.89 million Point Grind"
                    split_delay = FADEOUT_DOOR_SPLIT_DELAY
                    print(f'{"[" + "Console" + "]":>15} 100% run detected')
                else:
                    valid_door = False
            elif hundo_run:
                if hundo_sequence == 0 and current_map == "mac_02":
                    if (-490 <= marioposx <= -410):
                        door_name = 'Enter Chapter 1'
                        hundo_sequence = 1
                        split_delay = FADEOUT_DOOR_SPLIT_DELAY
                elif hundo_sequence == 11 and current_map == "mac_02":
                    if (260 <= marioposx <= 340):
                        door_name = "100 Sammers"
                        hundo_sequence = 12
                        split_delay = FADEOUT_DOOR_SPLIT_DELAY
                    else:
                        valid_door = False
            else:
                valid_door = False    
            if (valid_door):
                if door_name != None:
                    print(f'{"[" + "Console" + "]":>15} Valid Door: {door_name} Door Detected')
                    do_split(split_delay)

        if script_ptr == CB_DEFEAT_EVT_SCRIPT:
            if CountBleckSplit:
                print(f'{"[" + "Console" + "]":>15} Count Bleck Defeated')
                frame_wait(FPS *2)
                while current_effcurcount != 1:
                    time.sleep(0.01)
                    current_effcurcount = effcurcount.read()
                do_split(CB_DEFEAT_DELAY)

        if script_ptr == SD_DEFEAT_EVT_SCRIPT:
            print(f'{"[" + "Console" + "]":>15} Super Dimentio Defeated')
            do_split(SD_DEFEAT_DELAY)

        if script_ptr == CREDITS_START_SCRIPT:
            if current_map == "mac_22":
                print(f'{"[" + "Console" + "]":>15} Credits Detected')
                frame_wait(FPS *2)
                current_text_opacity_1 = textopacity1.read()
                current_text_opacity_2 = textopacity2.read()
                while current_text_opacity_1 != 255 and current_text_opacity_2 != 255:
                    current_text_opacity_1 = textopacity1.read()
                    current_text_opacity_2 = textopacity2.read()
                if current_text_opacity_1 == 255:
                    current_text_opacity = current_text_opacity_1
                    text_box_count = text_box_count1
                    textopacity = textopacity1
                elif current_text_opacity_2 == 255:
                    current_text_opacity = current_text_opacity_2
                    text_box_count = text_box_count2
                    textopacity = textopacity2  
                if current_text_opacity == 255:    
                    text_box_count += 1
                    while text_box_count <= 5:
                        if current_text_opacity == 255:
                            while current_text_opacity > 0:
                                current_text_opacity = textopacity.read()
                                pass
                        frame_wait(FPS * 2)
                        current_text_opacity = textopacity.read()
                        text_box_count += 1
                    while current_text_opacity != 0:
                        current_text_opacity = textopacity.read()
                    do_split(START_OR_CREDITS_DELAY)
                    text_box_count = 0
                    if hundo_run == False:
                        print(f'{"[" + "Console" + "]":>15} GG :)')
                    else:
                        hundo_sequence = 0

        if script_ptr == DOWN_PIPE_EVT_SCRIPT:
            valid_pipe = True
            marioposx = mariox.read()
            if current_map == "mac_05" or current_map == "mac_15" or current_map in PIT_10_MAPS:
                if current_map == "mac_05" and marioposx < 45:
                    valid_pipe = False
                if current_map == "mac_15" and marioposx > -45:
                    valid_pipe = False
                if valid_pipe:
                    if sequence_position == 99:
                        print(f'{"[" + "Console" + "]":>15} All Pixls run detected')
                    print(f'{"[" + "Console" + "]":>15} Pipe split detected')
                    do_split(DOWN_PIPE_DELAY)
                    if current_map == "dan_70" and flopPit == 1:
                        flopPit = 2
                    elif current_map == "dan_70" and flopPit == 2:
                        if hundo_run == False:
                            print(f'{"[" + "Console" + "]":>15} GG :)')
                        elif hundo_sequence == 1:
                            hundo_sequence = 2
                        elif hundo_sequence == 2:
                            hundo_sequence = 3
                    elif current_map == "dan_30":
                        if hundo_run == False or current_sequence <= 73:
                            print(f'{"[" + "Console" + "]":>15} GG :)')
        
        if script_ptr == RETURN_PIPE_SCRIPT:
            if current_map == "mi1_07" and current_sequence == 73:
                print(f'{"[" + "Console" + "]":>15} Pit% Return Pipe Detected')
                do_split(RETURN_PIPE_DELAY)
            elif hundo_run:
                current_map_p = current_map[:3]
                if hundo_sequence == 3 and current_map_p == "gn2":
                    do_split(RETURN_PIPE_DELAY)
                    hundo_sequence = 4
                elif hundo_sequence == 4 and current_map_p == "an1":
                    do_split(RETURN_PIPE_DELAY)
                    hundo_sequence = 5
                elif hundo_sequence == 5 and current_map_p == "ls4":
                    do_split(RETURN_PIPE_DELAY)
                    hundo_sequence = 6
                elif hundo_sequence == 8 and current_map_p == "gn3":
                    do_split(RETURN_PIPE_DELAY)
                    hundo_sequence = 9

        if script_ptr == TOWN_DOOR_EVT_SCRIPT:
            valid_door = True
            if hundo_sequence == 9 and current_map == "mac_09":
                marioposx = mariox.read()
                marioposz = marioz.read()
                if -240 <= marioposx <= -160:
                    print(f'{"[" + "Console" + "]":>15} Valid Door: Card Shop Door Detected')
                    while marioposz > 1750 or marioposz == 0:
                        marioposz = marioz.read()
                        print(marioposz)
                    do_split(START_OR_CREDITS_DELAY)
                    hundo_sequence = 10
            elif hundo_sequence == 10 and current_map == "mac_09":
                marioposz = marioz.read()
                if marioposz > 1739:
                    valid_door = False
                print(f'{"[" + "Console" + "]":>15} Valid Door: Card Shop Door Detected')
                if valid_door:
                    while marioposz < 1750:
                        marioposz = marioz.read()
                    do_split(START_OR_CREDITS_DELAY)
                    hundo_sequence = 11

    runstarted = False # True = debug

    if runstarted == False:
        current_loadSeq = seqLoadWork_state.read()
        while current_loadSeq > 10:
            errormessage = False
            print(f'{"[" + "Console" + "]":>15} Please go back to file select')
            errormessage = True
            while errormessage and current_loadSeq > 10:
                current_loadSeq = seqLoadWork_state.read()
        errormessage = False

    # Initial split

    while runstarted == False:
        currentPADbutton = buttonsPADHeld.read()
        currentBUTbutton = buttonsBUTHeld.read()
        print(f'{"[" + "Console" + "]":>15} Auto Splitter Ready! Please select your file.')
        while seqLoadWork_state.read() != 0x12d:
            time.sleep(1 / FPS)
        print(f'{"[" + "Console" + "]":>15} File select split detected.')
        print(f'{"[" + "Console" + "]":>15} Please wait a moment...')
        framewaitcount = 0
        while framewaitcount < FPS:
            currentPADbutton = buttonsPADHeld.read()
            if currentPADbutton != 0:
                print(f'{"[" + "Console" + "]":>15} Split canceled, please go back to file select')
                fileError = True
                break
            msec_wait(1000 / FPS)
            framewaitcount += 1
        if fileError == False:
            print(f'{"[" + "Console" + "]":>15} Ready! Press 2 to begin your run.')
            filestart = True
            while currentBUTbutton != 1:
                currentPADbutton = buttonsPADHeld.read()
                currentBUTbutton = buttonsBUTHeld.read()
                while currentPADbutton != 0:
                    if errormessage == False:
                        print(f'{"[" + "Console" + "]":>15} Split canceled, please go back to file select')
                    errormessage = True
                    filestart = False
                    break
                time.sleep(1 / FPS)
        if filestart and fileError == False:
            PressRelease(keyCodeMap[key_code], 100)
            print(f'{"[" + "Console" + "]":>15} Good Luck!')
            time.sleep(10)
            runstarted = True
            errormessage = False
        else:
            errormessage = False
            fileError = False
            current_loadSeq = seqLoadWork_state.read()
            while current_loadSeq > 10:
                errormessage = False
                if framewaitcount < FPS:
                    print(f'{"[" + "Console" + "]":>15} Please close the current textbox.')
                errormessage = True
                while errormessage and current_loadSeq > 10:
                    current_loadSeq = seqLoadWork_state.read()
            print(f'{"[" + "Console" + "]":>15} Please wait a moment...')
            time.sleep(3)

    while True:
        try:
            current_map = map.read()
            current_sequence = sequence_position.read()
            if current_map == "ls4_11" and CountBleckSplit:
                current_effcurcount = effcurcount.read()

            findInStructArray(evt_entries, EVT_ENTRY_SIZE, EVT_ENTRY_SCRIPT_PTR_OFFSET, [STAR_BLOCK_EVT_SCRIPT, PURE_HEART_EVT_SCRIPT, DOOR_CLOSE_EVT_SCRIPT, RETURN_EVT_SCRIPT, CB_DEFEAT_EVT_SCRIPT, SD_DEFEAT_EVT_SCRIPT, CREDITS_START_SCRIPT, RETURN_PIPE_SCRIPT, DOWN_PIPE_EVT_SCRIPT, TOWN_DOOR_EVT_SCRIPT], Datatype.WORD, evt_entry_cb)

            if hundo_sequence == 6:
                current_recipeByte6 = knownRecipe_Byte6.read()
                binary_rep = bin(current_recipeByte6)[2:].zfill(8)
                if binary_rep[5] == '1':
                    do_split(START_OR_CREDITS_DELAY)
                    hundo_sequence = 7

            if hundo_sequence == 7:
                current_recipeByte7 = knownRecipe_Byte7.read()
                binary_rep = bin(current_recipeByte7)[2:].zfill(8)
                if binary_rep[6] == '1':
                    do_split(START_OR_CREDITS_DELAY)
                    hundo_sequence = 8
        except RuntimeError as e: # If dolphin is disconnected, should not error for any other reason
            print(f'{"[" + "Console" + "]":>15} {e}')
            time.sleep(1)
            print(f'{"[" + "Console" + "]":>15} Dolphin not detected, restarting...')
            time.sleep(3)
            restart_program()