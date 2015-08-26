__author__ = 'Chris Brown'

try:
    import socket
    from threading import Thread
    from multiprocessing.pool import ThreadPool
    from curses import *
    from curses.panel import *
    from os import linesep
    from time import sleep
except ImportError, e:
    print 'Error: %s' % str(e)
    exit()

try:
    from atexit import register
except ImportError, e:
    pass
else:
    def exiting(clientObj, thread):
        try:
            if clientObj.recv.is_alive():
                clientObj.recv.join(1)
        except:
            pass
        try:
            if thread.is_alive:
                thread.join(1)
        except:
            pass


class Menu:

    def __init__(self):
        self.stdscr = initscr()
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.box = newwin(self.max_y, self.max_x, 0, 0)
        curs_set(False)
        noecho()
        self.stdscr.keypad(True)
        start_color()
        init_pair(1, COLOR_WHITE, COLOR_BLACK)
        init_pair(2, COLOR_BLACK, COLOR_WHITE)
        init_pair(3, COLOR_BLUE, COLOR_WHITE)
        self.box.bkgd(color_pair(1))
        self.box.addstr(int(self.max_y/4)-1, int((self.max_x/2)-(self.max_x/8)), 'Arrow Keys to Navigate - Enter to Continue', A_BOLD)

        self.input_box = newwin(int(self.max_y / 2), int(self.max_x / 2), int(self.max_y / 4), int(self.max_x / 4))
        self.input_box.bkgd(color_pair(2))
        self.input_box.box()

        self.input_panel = new_panel(self.input_box)
        self.box_panel = new_panel(self.box)

        self.text_pos = (int(self.input_box.getmaxyx()[0] / 4), int(self.input_box.getmaxyx()[0] / 4) * 3,
                         int(self.input_box.getmaxyx()[1] / 4), int(self.input_box.getmaxyx()[1] / 2))

        # Above is the starting positions for the below Text and User Input

        self.input_box.addstr(self.input_box.getmaxyx()[0] - 1, int(self.input_box.getmaxyx()[1]/8),'Connect', color_pair(3 ))
        self.input_box.addstr(self.text_pos[1], self.text_pos[2], ' Username:')
        self.input_box.addstr(self.text_pos[0], self.text_pos[2], 'Host Port:', A_STANDOUT)
        self.input_box.move(self.input_box.getyx()[0], self.text_pos[3])

        self.box_panel.show()
        self.input_panel.show()
        update_panels()
        doupdate()
        self.key = -1
        self.string = [str(), str()]
        self.highlighted = 1
        self.running = True

    def get_input(self):
        while self.running:
            self.input_panel.show()
            update_panels()
            doupdate()
            self.key = self.stdscr.getch()
            if self.key == 27:  # if <ESC> is pressed
                self.close()    # Close and Exit
                exit()
            if self.key == KEY_UP:      # Highlight 'Host Port:'
                self.input_box.addstr(self.text_pos[1], self.text_pos[2], ' Username:')
                self.input_box.addstr(self.text_pos[0], self.text_pos[2], 'Host Port:', A_STANDOUT)
                self.input_box.move(self.input_box.getyx()[0], len(self.string[0]) + self.text_pos[3])
                self.highlighted = 1
            elif self.key == KEY_DOWN:  # Highlight ' Username:'
                self.input_box.addstr(self.text_pos[0], self.text_pos[2], 'Host Port:')
                self.input_box.addstr(self.text_pos[1], self.text_pos[2], ' Username:', A_STANDOUT)
                self.input_box.move(self.input_box.getyx()[0], len(self.string[1]) + self.text_pos[3])
                self.highlighted = 2
            elif self.key == 10:  # If <Enter> is pressed
                self.close()
                return [self.string[0].split(' '), self.string[1]]
            elif 126 >= self.key >= 32:
                if not self.input_box.getyx()[1] >= self.input_box.getmaxyx()[1] - 1:
                    self.string[self.highlighted - 1] += chr(self.key)
                    self.input_box.addstr(chr(self.key))
            elif self.key == KEY_BACKSPACE:
                if not self.input_box.getyx()[1] <= self.text_pos[3]:
                    self.input_box.addstr(self.input_box.getyx()[0], self.input_box.getyx()[1] - 1, ' ')
                    self.input_box.move(self.input_box.getyx()[0], self.input_box.getyx()[1] - 1)
                    self.string[self.highlighted - 1] = self.string[self.highlighted - 1][:-1]
        return [self.string[0].split(), self.string[1]]

    def close(self):
        echo()
        self.stdscr.clear()
        endwin()


class Window:
    def __init__(self):
        pass

    def splash_screen(self):  # Splash Screen
        self.splash_window = newwin(self.max_y, self.max_x, 0, 0)
        self.splash_panel = new_panel(self.splash_window)
        self.splash_text = '' \
                           '   *******      /**    /**      /*******        /********       /********      /*******    ' \
                           '  **////***     /**    /**      /**////**       /**//////       /**/////       /**////**   ' \
                           ' **    ///      /**    /**      /**   /**       /**             /**            /**    /**  ' \
                           '/**             /**    /**      /*******        /*********      /*******       /**    /**  ' \
                           '/**             /**    /**      /**///**        ////////**      /**////        /**    /**  ' \
                           '//**    ***     /**    /**      /**  //**              /**      /**            /**   /**   ' \
                           ' //*******      //*******       /**   //**      /*********      /********      /*******    ' \
                           '  ///////        ///////        //     //       ////////        ////////       ///////     ' \
                           '               *******       /**     /**          ****          **********                 ' \
                           '              **//// **      /**     /**         **//**        /////**///                  ' \
                           '             /**    //       /**********        **  //**           /**                     ' \
                           '             /**             /**//////**       **********          /**                     ' \
                           '             //**    **      /**     /**      /**//////**          /**                     ' \
                           '              //******       /**     /**      /**     /**          /**                     ' \
                           '               //////        //      //       //      //           //                      '
        self.splash_pos = dict(x=int((self.max_x - 91) / 2), y=int((self.max_y - 15) / 2))
        for i in range(15):
            self.splash_window.addstr(self.splash_pos['y'] + i, self.splash_pos['x'],
                      self.splash_text[91 * i:91 * (i + 1)])
            sleep(0.2)
            self.splash_panel.show()
            update_panels()
            doupdate()
        sleep(2)
        del self.splash_window, self.splash_panel, self.splash_pos, self.splash_text

    def start(self): # initialize chat screen
        self.stdscr = initscr()
        start_color()
        init_pair(1, COLOR_CYAN, COLOR_BLACK)
        self.stdscr.timeout(0050)
        noecho()
        curs_set(False)
        self.stdscr.keypad(True)
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.splash_screen()
        self.running = True
        self.line = str()
        self.inW = newwin(3, self.max_x, self.max_y - 1, 0)  # Send Messages Window
        self.outW = newwin(self.max_y - 1, self.max_x, 0, 0)  # Receive Messages Window
        self.outW.scrollok(True)  # Allow Out Window to
        self.outW.idlok(True)  # Scroll through Messages
        self.inP = new_panel(self.inW)
        self.outP = new_panel(self.outW)
        self.key = int()
        self.message = str()
        self.out_bot = self.outW.getmaxyx()[0]  # Bottom of Out Window / Receive Window
        self.line_num = 1
        self.max_msg_length = self.max_x - 2
        update_panels()
        doupdate()

    def get_input(self):
        self.inW.addstr(username+'> ', color_pair(1)+A_BOLD)
        curs_set(True)
        while self.running:

            self.outP.show()
            self.inP.show()
            update_panels()
            doupdate()
            self.key = self.stdscr.getch()
            if self.key == 27:
                self.running = False
                self.close()
                exit()
            elif self.key == KEY_BACKSPACE:
                if self.inW.getyx()[0] == 0 and not self.inW.getyx()[1] == 2:
                    self.inW.delch(self.inW.getyx()[0], self.inW.getyx()[1] - 1)
                    self.line = self.line[:-1]
            elif self.key == 10:  # If <ENTER> is pressed
                if self.line:
                    self.message = self.line
                    self.send_message(self.message)  # Send message
                    
                    self.inW.move(0, 0)  # Clear the
                    self.inW.clrtoeol()  # Input Line
                    
                    self.inW.move(0, 0)
                    self.inW.addstr(username+'> ', color_pair(1)+A_BOLD)

                    if self.line_num > self.outW.getmaxyx():  # If you have reached the end
                        wscrl(self.outW, lines=1)         # of the output screen scroll the text up
                    self.line = str()
                    self.line_num += 1
            elif 0 <= self.key <= 250:
                if not len(username +'> '+ self.line) == self.max_msg_length:
                    self.inW.addstr(chr(self.key))
                    self.line += chr(self.key)
                else:
                    flash() # If User has reached the end of the input line flash screen as a warning
            elif 258 <= self.key <= 261:
                continue
                # <---- Add Scrolling w/Arrow Keys Here

    def recv_message(self, msg):
        user = msg.split()[0]  # Seperating the username from the message to add color
        self.outW.addstr(user, color_pair(1) + A_BOLD)
        self.outW.addstr(' ' +' '.join(msg.split()[1:])+ '\n')

    def send_message(self, msg):
        client.socket.send(username + '> ' + msg + '\n')

    def close(self):
        endwin()
        client.close()


class ChatClient:
    def __init__(self, host, port):
        try:
            self.socket = socket.create_connection((host, port))
        except socket.error:
            self.connected = False
        else:
            self.connected = True
        self.terminator = '\n'
        self.buffer = []
        self.recv = Thread(target=self.collect_incoming_data)
        self.recv.start() if self.connected == True else self.close()

    def collect_incoming_data(self):
        self.socket.settimeout(0.05)
        while True:
            if not self.connected:
                return
            try:
                data = self.socket.recv(512)
            except socket.timeout:
                continue
            if data:
                if ''.join(data).find(self.terminator) == len(data) - 1:
                    self.buffer.append(data[:-1])
                    self.found_terminator()
                else:
                    self.buffer.append(data)

    def found_terminator(self):
        msg = ''.join(self.buffer)
        main_window.recv_message(msg)
        self.buffer = []

    def close(self):
        if hasattr(self,'socket'):
            if self.connected:
                self.connected = False
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()


def main():
    global main_window, main_menu, username, client, t
    main_window = Window()
    main_menu = Menu()
    host_port, username = main_menu.get_input()
    if len(host_port) == 2:
        try:
            client = ChatClient(host_port[0], int(host_port[1]))
        except ValueError, e:
            print 'Port must be a number.'
            exit()
        if not client.connected:
            print 'Connection Failed.'
            exit()
    else:
        main()
        return
    main_window.start()

    t = Thread(target=main_window.get_input)
    t.daemon = True
    register(exiting, clientObj=client, thread=t)
    t.start()

tmp = initscr().getmaxyx(); endwin()
if tmp[0] >= 15 and tmp[1] >= 91:
    main()
else:
    print 'Please resize your Terminal to or above \'15 Tall\' and \'91 Wide\''
    exit()