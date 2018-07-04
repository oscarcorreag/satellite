from enum import Enum
import re
import satellite.models as models
import pdb

HELLO_COMMAND = 'HELLO'
ERROR_COMMAND = 'EVENTERROR'
HOUSE_COMMAND = 'HOUSEKEEPING_TM'


class Event(Enum):
    Error = 1
    Hello = 2
    Housekeeping = 3


class TmFileManager:
    def __init__(self):
        self.current_type = 0
        self.event = None

    def process_line(self, line, line_number):
        # If line contains "Received TM command" string, a new event is created.
        m = re.search('Received TM command\s*:?\s*(\w+)', line)
        if m is not None:
            # But first, save the previous event if it exists.
            if self.event is not None:
                self.event.save()
                self.event = None
            # Which event type?
            type_ = m.group(1)
            # Capture sequence number which is present in all types.
            m = re.search('Sequence Number\s*:?\s*(\d+)', line)
            if m is None:
                raise ValueError('Sequence Number was expected after "Received TM command" in line {}.'.format(line_number))
            seq_number = int(m.group(1))
            # Create corresponding event object based on type. Moreover, set attributes captured in this line.
            # IMPORTANT: Set the current type which is needed for coming lines.
            if type_ == ERROR_COMMAND:
                self.current_type = Event.Error
                self.event = models.EventErrComm()
                # Capture and set event name which is present in ERROR events only.
                m = re.search('Event Name\s*:?\s*(\w+)', line)
                if m is None:
                    raise ValueError('Event Name was expected after "Sequence Number" in line {}.'.format(line_number))
                self.event.eve_name = m.group(1)
            elif type_ == HELLO_COMMAND or type_ == HOUSE_COMMAND:
                if type_ == HELLO_COMMAND:
                    self.current_type = Event.Hello
                    self.event = models.HelloComm()
                else:
                    self.current_type = Event.Housekeeping
                    self.event = models.HouseKeepComm()
                # Capture operating mode which is present in two types, i.e., HELLO and HOUSEKEEPING.
                m = re.search('Operating Mode\s*:?\s*(\w+)', line)
                if m is None:
                    raise ValueError('Operating Mode was expected after "Sequence Number" in line {}.'.format(line_number))
                self.event.ope_mode = m.group(1)
            else:
                # raise NotImplementedError('Received TM command has not been implemented.')
                return
            # Set sequence number which is present in all types
            self.event.seq_number = seq_number
        else:
            if self.event is None:
                raise ValueError('Received TM command was expected at the beginning.')
            # If mission clock is captured is set regardless the type.
            m = re.search('Mission Clock\s*:?\s*(\d+)', line)
            if m is not None:
                self.event.mis_clock = int(m.group(1))
            # When any other attribute is captured, the type is checked, i.e., the attribute is not set for ERROR type.
            m = re.search('p3V3_TM\s*:?\s*(\d+)', line)
            if m is not None:
                if self.current_type == Event.Hello or self.current_type == Event.Housekeeping:
                    self.event.p3v3_tm = int(m.group(1))
            m = re.search('p5V_TM\s*:?\s*(\d+)', line)
            if m is not None:
                if self.current_type == Event.Hello or self.current_type == Event.Housekeeping:
                    self.event.p5v_tm = int(m.group(1))
            m = re.search('p15V_TM\s*:?\s*(\d+)', line)
            if m is not None:
                if self.current_type == Event.Hello or self.current_type == Event.Housekeeping:
                    self.event.p15v_tm = int(m.group(1))
            m = re.search('n15V_TM\s*:?\s*(\d+)', line)
            if m is not None:
                if self.current_type == Event.Hello or self.current_type == Event.Housekeeping:
                    self.event.n15v_tm = int(m.group(1))
            m = re.search('RW_P5V\s*:?\s*(FALSE|TRUE)', line)
            if m is not None:
                if self.current_type == Event.Hello or self.current_type == Event.Housekeeping:
                    self.event.rw_p5v = m.group(1)
            m = re.search('MTS_VBUS\s*:?\s*(FALSE|TRUE)', line)
            if m is not None:
                if self.current_type == Event.Hello or self.current_type == Event.Housekeeping:
                    self.event.mts_vbus = m.group(1)
            m = re.search('BOOM1_VBUS\s*:?\s*(FALSE|TRUE)', line)
            if m is not None:
                if self.current_type == Event.Hello or self.current_type == Event.Housekeeping:
                    self.event.boom1_vbus = m.group(1)
            m = re.search('BOOM2_VBUS\s*:?\s*(FALSE|TRUE)', line)
            if m is not None:
                if self.current_type == Event.Hello or self.current_type == Event.Housekeeping:
                    self.event.boom2_vbus = m.group(1)
            m = re.search('TTC_STAT\s*:?\s*(FALSE|TRUE)', line)
            if m is not None:
                if self.current_type == Event.Hello or self.current_type == Event.Housekeeping:
                    self.event.ttc_stat = m.group(1)
            m = re.search('Battery\s*:?\s*(\w+)', line)
            if m is not None:
                if self.current_type == Event.Hello or self.current_type == Event.Housekeeping:
                    self.event.battery = m.group(1)

    def process(self, file_name):
        f = open(file_name)
        for line_number, line in enumerate(f):
            self.process_line(line, line_number)
