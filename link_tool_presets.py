presets = {
    "Starlink": {"Celes_body": "Earth", "P_total": 200, "P_trans_sc": 70, "P_trans_grnd": 400, "L_fact_trans": 0.8,
                 "L_fact_rec": 0.7, "f_down": 2.2, "turn_around_ratio": 221/240, "d_ant_sc": 0.2, "d_ant_grnd": 0.5,
                 "h_orbit": 500e3, "theta_elon": None, "theta_offpnt": 0.1, "r_up": 1e8, "pay_theta_swath": 20,
                 "pay_pixel_size": 0.05/60, "pay_bit_per_pixel": 8, "pay_duty_cycle": 0.5, "pay_downlink_factor": 4/24,
                 "SNR_req": 6.4},
    "CAPSTONE": {"Celes_body": "Moon", "P_total": 100, "P_trans_sc": 25, "P_trans_grnd": 400, "L_fact_trans": 0.8,
                 "L_fact_rec": 0.7, "f_down": 8.4, "turn_around_ratio": 749/880, "d_ant_sc": 0.1, "d_ant_grnd": 34,
                 "h_orbit": 1600e3, "theta_elon": None, "theta_offpnt": 1, "r_up": 1e4, "pay_theta_swath": 45,
                 "pay_pixel_size": 0.1/60, "pay_bit_per_pixel": 8, "pay_duty_cycle": 0.75, "pay_downlink_factor": 1/24,
                 "SNR_req": 6.4},
    "MESSENGER": {"Celes_body": "Mercury", "P_total": 450, "P_trans_sc": 100, "P_trans_grnd": 1000, "L_fact_trans": 0.8,
                  "L_fact_rec": 0.7, "f_down": 8.4, "turn_around_ratio": 749/880, "d_ant_sc": 3, "d_ant_grnd": 34,
                  "h_orbit": 250e3, "theta_elon": 5, "theta_offpnt": 0.1, "r_up": 1e6, "pay_theta_swath": 20,
                  "pay_pixel_size": 0.3/60, "pay_bit_per_pixel": 8, "pay_duty_cycle": 0.5, "pay_downlink_factor": 18/24,
                  "SNR_req": 6.4},
    "Hope": {"Celes_body": "Mars", "P_total": 1800, "P_trans_sc": 400, "P_trans_grnd": 1000, "L_fact_trans": 0.8,
             "L_fact_rec": 0.7, "f_down": 8.4, "turn_around_ratio": 749/880, "d_ant_sc": 2, "d_ant_grnd": 34,
             "h_orbit": 20000e3, "theta_elon": 20, "theta_offpnt": 0.1, "r_up": 1e6, "pay_theta_swath": 5,
             "pay_pixel_size": 0.01/60, "pay_bit_per_pixel": 8, "pay_duty_cycle": 0.5, "pay_downlink_factor": 18/24,
             "SNR_req": 6.4},
    "Cassini": {"Celes_body": "Saturn", "P_total": 900, "P_trans_sc": 200, "P_trans_grnd": 1000, "L_fact_trans": 0.8,
                "L_fact_rec": 0.7, "f_down": 8.5, "turn_around_ratio": 749/880, "d_ant_sc": 4, "d_ant_grnd": 34,
                "h_orbit": 20000e3, "theta_elon": 10, "theta_offpnt": 0.1, "r_up": 1e6, "pay_theta_swath": 20,
                "pay_pixel_size": 0.5/60, "pay_bit_per_pixel": 8, "pay_duty_cycle": 0.25, "pay_downlink_factor": 18/24,
                "SNR_req": 6.4},
}

target_celes_body = 'Mars'
P_total = 20  # irrelevant, total spacecraft power
P_trans_sc = 8  # W spacecraft transmitter power
P_trans_grnd = 400  # W ground station transmitter power
L_fact_trans = 0.8  # - Loss factor transmitter
L_fact_rec = 0.7  # - Loss factor receiver
f_down = 8.4 # GHz frequency downlink
turn_around_ratio = 749/880  # - f_uplink/f_down
f_up = turn_around_ratio*f_down  # GHz frequency uplink
d_ant_sc = 1  # m diameter antenna on spacecraft (parabolic)
d_ant_grnd = 10  # m diameter antenna on ground (parabolic)
h_orbit = 500e3  # m height of orbit above surface of earth
theta_elon = 10  # DEG, elongation angle
theta_offpnt = 1  # DEG, pointing offset angle
r_up = 1e5  # bit/s, uplink rate
pay_theta_payload = 30  # DEG payload swath width angle
pay_pixel_size = 0.2/60  # DEG payload pixel size
pay_bit_per_pixel = 8  # - bit per pixel
pay_duty_cycle = 1  # - payload duty cycle, as part of orbital period
pay_downlink_factor = 12/24  # -, payload time for transmitting data
coding_type = None  # coding type
BER_allow = 1  # maximum bit error rate