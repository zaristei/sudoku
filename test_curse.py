import curses, time
import tqdm
from io import StringIO

def main(stdscr: curses.window):
    stream = StringIO()
    t = tqdm.tqdm(total=5, file=stream, ascii=False)
    for i in range(5):
        t.update(1)
        stdscr.addstr(0, 0, stream.getvalue())
        stdscr.addstr(1, 0, "Hello")
        stdscr.refresh()
        time.sleep(1)
        stdscr.addstr(1, 0, "World")
        stdscr.refresh()
        time.sleep(1)

if __name__ == "__main__":
    curses.wrapper(main)