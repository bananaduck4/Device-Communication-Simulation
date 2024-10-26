from device import  Device, Message

class DEVICE_MANAGER:
    def __init__(self, rules : list):
        self.sim_length = int(rules.pop().split()[1])
        self.scheduled_msg = []
        self.devices = []

        for r in rules:
            rule = r.split()

            if rule[0] == 'DEVICE':
                #create device and add them to the list
                device = Device(rule[1])
                self.devices.append(device)

            elif rule[0] == 'PROPAGATE':
                #assign propagation rule to correct device
                device = self.devices[int(rule[1]) - 1]
                device.add_propagate(rule)

            else:
                self.scheduled_msg.append(rule) #store all the starter event

    def run(self):
        # assign each event to corresponding device
        for ev in self.scheduled_msg:

            if ev[0] == 'CANCEL':
                ev_msg = Message('CANCELLATION', ev[2], int(ev[3]), 0, 0)

            else:
                ev_msg = Message(ev[0], ev[2], int(ev[3]), 0, 0)

            self.devices[int(ev[1]) - 1].update_msg(ev_msg) #setup the ev

        curr_time = 0
        while curr_time < self.sim_length:

            device : Device
            for device in self.devices: #update each device

                new_msg = device.update(curr_time)

                # Check if a device has finish propagating and send all the ev to other devices
                while new_msg:
                    msg = new_msg[0]
                    receiver_id = msg.to - 1
                    self.devices[receiver_id].rcv_msg(msg) #recieve the new msg

                    #update previous device in list if device sent it backward in the list
                    if receiver_id < (device.id - 1):
                        self.devices[receiver_id].update(curr_time)

                    new_msg.pop(0)

            #get all time of all future ev
            all_ev_time = [time for device in self.devices for time in device.get_ev_time() if time > curr_time]
            #get time of all ev after they propagate
            all_prop_time = [time + device.propagate_time for device in self.devices for time in device.get_ev_time() if time + device.propagate_time > curr_time]

            #check if the is any event to be run
            ev_time = all_prop_time + all_ev_time

            if ev_time:
                curr_time = min(ev_time) #Jump to the next event time

            else:
                curr_time = self.sim_length #End if there is no more ev to run


        print(f'@{curr_time}: END')