#!/usr/bin/env python3

##############################################
def dprint(mesg, debug=False):

    if not debug:
        return

    print(mesg)

####### end read_config
##############################################


##############################################
def build_playlist(songs_dir, debug=False):

    songs = []
    if not os.path.exists(songs_dir):
        return songs

    for dfile in os.listdir(songs_dir):
        pfile = "%s/%s" % (songs_dir, dfile)
        if os.path.isfile(pfile):
            #print("Song is:", pfile)
            songs.append(pfile)

    return songs

##############################################

#################################################################
def read_config(cfgfile='XmasShowPi.cfg', debug=False):

    # Defaults
    config_data = {'songs_dir': 'songs',
                   'start_time_hour': datetime.time(hour=17),
                   'duration_hours': 5,
                   'outlet_idle_status': False,
                   'rf_sudo': False,
                   'outlets_enable': True,
                   'debug': False
                   }

    outlets = []
    sequences = []
    num_tokens = 0
    num_outlets = 0
    num_sequences = 0

    with open(cfgfile, mode='r') as f:
        configlines = f.read().splitlines()
    f.close()

    for i in range(0, len(configlines)):
        cline = configlines[i].split("=")

        if cline[0] == 'OUTLET':
            #print("Found Outlet:", cline[1])
            outlet_line = cline[1].split(",")
            outlet_cfg = {}

            outlet_cfg['cfgline'] = cline[1]
            outlet_cfg['name'] = outlet_line[0]
            outlet_cfg['GPIO'] = outlet_line[1]
            outlet_cfg['out_options'] = outlet_line[2]

            outlets.append(outlet_cfg)
            num_tokens += 1
            num_outlets += 1

        if cline[0] == 'RF_GPIO':
            # print("Found RF Transmitter:", cline[1])
            config_data['RF_GPIO'] = int(cline[1])
            num_tokens += 1

        if cline[0] == 'RF_FREQ':
            # print("Found RF Frequency:", cline[1])
            config_data['RF_FREQ'] = float(cline[1])
            num_tokens += 1

        if cline[0] == 'SONGS_DIR':
            # print("Found Songs dir:", cline[1])
            config_data['songs_dir'] = cline[1]
            num_tokens += 1

        if cline[0] == 'LIGHTS_ON_AT_HOUR':
            # print("Found Lights on time:", cline[1])
            config_data['lights_on_at_hour_text'] = cline[1]
            config_data['lights_on_at_hour'] = datetime.time(hour=int(cline[1]))
            num_tokens += 1

        if cline[0] == 'LIGHTS_OFF_AT_HOUR':
            # print("Found Lights on time:", cline[1])
            config_data['lights_off_at_hour_text'] = cline[1]
            config_data['lights_off_at_hour'] = datetime.time(hour=int(cline[1]))
            num_tokens += 1

        if cline[0] == 'SHOW_START_TIME_HOUR':
            # print("Found Start time:", cline[1])
            config_data['show_start_time_hour_text'] = cline[1]
            config_data['show_start_time_hour'] = datetime.time(hour=int(cline[1]))
            num_tokens += 1

        if cline[0] == 'SHOW_DURATION_HOURS':
            # print("Found duration hours:", cline[1])
            config_data['show_duration_hours'] = int(cline[1])
            num_tokens += 1

        if cline[0] == 'OUTLET_STATUS_WHEN_IDLE':
            # print("Found Outlet Status:", cline[1])
            if cline[1] == 'ON':
                config_data['outlet_idle_status'] = True
            num_tokens += 1

        if cline[0] == 'RF_SUDO':
            # print("Found RF Sudo:", cline[1])
            if cline[1] == 'ON':
                config_data['rf_sudo'] = True

        if cline[0] == 'OUTLETS_ENABLE':
            # print("Found Outlets enable:", cline[1])
            if cline[1] == 'OFF':
                config_data['outlets_enable'] = False

        if cline[0] == 'DEBUG':
            # print("Found Outlet Status:", cline[1])
            if cline[1] == 'ON':
                config_data['debug'] = True

        if cline[0] == 'SEQUENCE':
            # print("Found Sequence:", cline[1])
            # sequences.append(cline[1])
            seq_line = cline[1].split(",")
            sequence_cfg = {}

            sequence_cfg['cfgline'] = cline[1]
            sequence_cfg['name'] = seq_line[0]
            sequence_cfg['type'] = seq_line[1]
            sequence_cfg['seq_options'] = seq_line[2]

            sequences.append(sequence_cfg)
            num_sequences += 1
            num_tokens += 1

    if num_tokens < 3:
        print("Missing XmasShowPi configuration information")
        exit(-2)

    config_data['outlets'] = outlets
    config_data['num_outlets'] = num_outlets
    config_data['sequences'] = sequences
    config_data['num_sequences'] = num_sequences
    return config_data

####### end read_config
##############################################