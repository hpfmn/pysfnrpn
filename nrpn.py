nrpn_select_msb_cc = 99
nrpn_select_lsb_cc = 98
data_entry_lsb_cc = 38
data_entry_msb_cc = 6

#select msb always 120
#select lsb<100 = value
#select 100<=lsb<103 = ntimes*100/1000/10000

#data values are additive
#zero-offset at 0x2000 (8192) = add 0
#data_change = ((msb<<7) + (lsb)) - 0x2000

import mido
mido.set_backend('mido.backends.rtmidi')
globalchan=0
output = mido.open_output("Python NRPN", virtual=True)

def send_value_to_generator(value, generator):
    select_generator(generator)
    send_message(value)

def select_generator(generator):
    gen_sel_startmsg = mido.Message('control_change', \
                                channel=globalchan, \
                                control=nrpn_select_msb_cc, \
                                value=120)
    times100=0
    times1000=0
    times10000=0
    lastvalue=0
    gen=generator
    while gen>0:
        if gen>10000:
            times10000+=1
            gen-10000
        elif gen>1000:
            times1000+=1
            gen-1000
        elif gen>100:
            times100+=1
            gen-100
        else:
            lastvalue=gen
            gen-=lastvalue
    output.send(gen_sel_startmsg)
    msg10000=mido.Message('control_change', \
                          channel=globalchan, \
                          control=nrpn_select_lsb_cc,\
                          value=102)
    for i in range(times10000):
        output.send(msg10000)
    msg1000=mido.Message('control_change', \
                          channel=globalchan, \
                          control=nrpn_select_lsb_cc,\
                          value=101)
    for i in range(times1000):
        output.send(msg1000)
    msg100=mido.Message('control_change', \
                        channel=globalchan, \
                        control=nrpn_select_lsb_cc,\
                        value=100)
    for i in range(times100):
        output.send(msg100)
    lastmsg=mido.Message('control_change', \
                         channel=globalchan, \
                         control=nrpn_select_lsb_cc,\
                         value=lastvalue)
    output.send(lastmsg)

def send_message(value):
    value+=0x2000 # add offset
    lsb=value&127
    msb=(value>>7)&127
    msbmsg=mido.Message('control_change',\
                        channel=globalchan, \
                        control=data_entry_msb_cc,\
                        value=msb)
    lsbmsg=mido.Message('control_change',\
                        channel=globalchan, \
                        control=data_entry_lsb_cc,\
                        value=msb)
    output.send(msbmsg)
    output.send(lsbmsg)


from IPython import embed
embed()
