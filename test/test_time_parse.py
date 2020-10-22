
import sys
import time


SIGN_HOUR = "h"
SIGN_MIN = "m"
SIGN_SEC = "s"


def parse_time(time: str) -> float:
    result = 0
    temp = []
    
    for char in time:
        if str.isnumeric(char) or char == ".":
            temp.append(char)
            continue
        
        alpha = str.lower(char)
        num = float("".join(temp))
        temp.clear()
        
        if alpha == SIGN_HOUR:
            result += num * 3600
        elif alpha == SIGN_MIN:
            result += num * 60
        elif alpha == SIGN_SEC:
            result += num
        else:
            raise ValueError(
                "Invalid time format was detected. " + 
                "You can use charactors 's', 'm' and 'h' " + 
                "to represent the time format."
            )
    
    if len(temp):
        result += float("".join(temp))
        
    return result


if __name__ == "__main__":
    init_time = time.time()
    result = parse_time(sys.argv[1])
    exec_time = time.time() - init_time
    
    print(f"result: {result}, time: {exec_time}")