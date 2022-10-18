from link_tool_presets import presets


def get_SC_data():
    print("Pick one of the presets below, or enter 'custom' to enter a custom one.")
    print('Preset Missions', [key for key in presets.keys()])
    mission = input('Pick one: ')
    try:
        return presets[mission]
    except KeyError:
        if mission != 'Custom' and mission != 'custom':
            print(mission, 'not found, creating a Custom mission instead...')
        print('Enter celestial body.')
        Celes_body = input('Choose from Mercury, Venus, Earth, Moon, Mars, Jupiter, Saturn, Uranus, Neptune or Pluto: ')
        P_total = float(input('Enter total power in Watts: '))
        P_trans_sc = float(input('Enter spacecraft transmitting power in Watts: '))
        P_trans_grnd = float(input('Enter ground station transmitting power in Watts: '))
        L_fact_trans = float(input('Enter transmission loss factor (unitless): '))
        L_fact_rec = float(input('Enter receiver loss factor (unitless): '))
        f_down = float(input('Enter downlink frequency in GHz: '))
        turn_around_ratio = float(input(
            'Enter the turn-around-ratio (uplink frequency divided by downlink frequency, unitless): '
        ))
        d_ant_sc = float(input('Enter spacecraft antenna diameter in meter: '))
        d_ant_ground = float(input('Enter ground station antenna diameter in meter: '))
        h_orbit = float(input('Enter orbit height in METER: '))
        theta_elon = float(input('Enter elongation angle in degrees (irrelevant for Earth and Moon missions): '))
        theta_offpnt = float(input('Enter pointing angle of the spacecraft in degrees: '))
        r_up = float(input('Enter uplink data rate in bit/s: '))
        pay_theta_swath = float(input('Enter payload swath angle in degrees: '))
        pay_pixel_size = float(input('Enter payload pixel size in degrees (1 degree is 60 arcminutes): '))
        pay_bit_per_pixel = float(input('Enter the generated data in bits per pixel: '))
        pay_duty_cycle = float(input('Enter payload duty cycle as fraction of total cycle (eg. 0.9 if the spacecraft takes'
                               'pictures 90% of the time): '))
        pay_downlink_factor = float(input('Enter downlink factor time (eg. 6/24 if the spacecraft can communicate home 6'
                                    'hours a day: '))
        SNR_req = float(input('Enter required signal to noise ratio in dB: '))
        return {"Celes_body": Celes_body, "P_total": P_total, "P_trans_sc": P_trans_sc, "P_trans_grnd": P_trans_grnd,
                "L_fact_trans": L_fact_trans,
                 "L_fact_rec": L_fact_rec, "f_down": f_down, "turn_around_ratio": turn_around_ratio, "d_ant_sc": d_ant_sc, "d_ant_grnd": d_ant_ground,
                 "h_orbit": h_orbit, "theta_elon": theta_elon, "theta_offpnt": theta_offpnt, "r_up": r_up, "pay_theta_swath": pay_theta_swath,
                 "pay_pixel_size": pay_pixel_size, "pay_bit_per_pixel": pay_bit_per_pixel, "pay_duty_cycle": pay_duty_cycle, "pay_downlink_factor": pay_downlink_factor,
                 "SNR_req": SNR_req}
