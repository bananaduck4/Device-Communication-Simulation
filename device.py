from collections import  namedtuple
Message = namedtuple('Message', ['type', 'msg', 'time', 'sender', 'to'])

class Device:
    def __init__(self, ID : str):
        self.id = int(ID)
        self.propagate_device = None #Stores what device the msg is sent
        self.propagate_time = None
        self.ev_msg = {} #Store all ev
        self.sent_msgs = [] #Store msg that is already sent

    def get_ev_time(self): #get the time all ev that is still running
        return [m.time for m in self.ev_msg if self.ev_msg[m]]

    def add_propagate(self, rule : list): #set up device propagate rule
        self.propagate_device, self.propagate_time = int(rule[2]), int(rule[3])

    def update_msg(self, msg : Message) -> None: #update alert or cancel
        ev : Message
        for ev in [e for e in self.ev_msg.copy() if e.msg == msg.msg]: #update ev that have the same msg

            if ev.type == msg.type:
                if self.ev_msg[ev]: #update the time of the msg
                    self.ev_msg[msg] = self.ev_msg.pop(ev)
                return

            #Canel all alerts that happened before the cancellation
            elif msg.type == 'CANCELLATION' and ev.type == 'ALERT' and msg.time < ev.time:
                self.ev_msg[ev] = False

            #cancel the alert if there is already a cancellation msg
            elif msg.type == 'ALERT' and ev.type == 'CANCELLATION' and msg.time > ev.time:
                self.ev_msg[msg] = False
                return

        self.ev_msg[msg] = True

    def _send_msg(self, msg : Message) -> None:
        if msg not in self.sent_msgs: #Check if msg has not been sent
            print(
                f'@{msg.time}: #{self.id} SENT {msg.type} TO #{self.propagate_device}: {msg.msg}')

            self.sent_msgs.append(msg) #add msg to sent_msg so that it does not send again

    def rcv_msg(self, msg : Message) -> None:
        self.update_msg(msg)

        print(
        f'@{msg.time}: #{self.id} RECEIVED {msg.type} FROM #{msg.sender}: {msg.msg}')

    def update(self, curr_time : int) -> list[Message]:
        msg_output = [] #stores list of all ev that has finish propagating

        ev : Message
        for ev in [e for e in self.ev_msg if self.ev_msg[e]]: #Check each alerts

            if curr_time == ev.time:
                self._send_msg(ev)

            #Return to be received after its propagation time
            elif curr_time - ev.time == self.propagate_time:
                #cancel all alerts and cancel with the same msg after propagated
                if ev.type == 'CANCELLATION':
                    for msgs in [m for m in self.ev_msg if m.msg == ev.msg]:
                        if (msgs.type == 'CANCELLATION') or (msgs.type == "ALERT" and msgs.time < ev.time):
                            self.ev_msg[msgs] = False

                msg_output.append(Message(ev.type, ev.msg, curr_time, self.id,
                                          self.propagate_device))
        return msg_output