import numpy as np
from link_tool_UI import get_SC_data

SC_data = get_SC_data()
target_celes_body = SC_data["Celes_body"]
P_total = SC_data["P_total"]  # irrelevant, total spacecraft power
P_trans_sc = SC_data["P_trans_sc"]  # W spacecraft transmitter power
P_trans_grnd = SC_data["P_trans_grnd"]  # W ground station transmitter power
L_fact_trans = SC_data["L_fact_trans"]  # - Loss factor transmitter
L_fact_rec = SC_data["L_fact_rec"]  # - Loss factor receiver
f_down = SC_data["f_down"]  # GHz frequency downlink
turn_around_ratio = SC_data["turn_around_ratio"]  # - f_uplink/f_down
f_up = turn_around_ratio*f_down  # GHz frequency uplink
d_ant_sc = SC_data["d_ant_sc"]  # m diameter antenna on spacecraft (parabolic)
d_ant_grnd = SC_data["d_ant_grnd"]  # m diameter antenna on ground (parabolic)
h_orbit = SC_data["h_orbit"]  # m height of orbit above surface of earth
theta_elon = SC_data["theta_elon"]  # DEG, elongation angle
theta_offpnt = SC_data["theta_offpnt"]  # DEG, pointing offset angle
r_up = SC_data["r_up"]  # bit/s, uplink rate
pay_theta_swath = SC_data["pay_theta_swath"]  # DEG payload swath width angle
pay_pixel_size = SC_data["pay_pixel_size"]  # DEG payload pixel size
pay_bit_per_pixel = SC_data["pay_bit_per_pixel"]  # - bit per pixel
pay_duty_cycle = SC_data["pay_duty_cycle"]  # - payload duty cycle, as part of orbital period
pay_downlink_factor = SC_data["pay_downlink_factor"]  # -, payload time for transmitting data
SNR_req = SC_data["SNR_req"]
coding_type = None  # coding type
BER_allow = 1e-6  # maximum bit error rate

radii_dict = {'Mercury': 2439.7e3, 'Venus': 6051.8e3, 'Earth': 6371e3, 'Moon': 1737.4e3, 'Mars': 3389.5e3,
           'Jupiter': 69911e3, 'Saturn': 58232e3, 'Uranus': 25362e3, 'Neptune': 24622e3, 'Pluto': 1188.3e3}
mu_dict = {'Mercury': 22032.09e9, 'Venus': 324859e9, 'Earth': 398600.436e9, 'Moon': 4902.8e9, 'Mars': 42828e9,
           'Jupiter': 126686531e9, 'Saturn': 37931206e9, 'Uranus': 5793951e9, 'Neptune': 6835099e9, 'Pluto': 869.6e9}
r_orbit_dict = {'Mercury': 4.6e10, 'Venus': 1.07477e11, 'Earth': 1.496e11, 'Mars': 2.279e11,
                'Jupiter': 8.16363e11, 'Saturn': 1.43353e12, 'Uranus': 3.00639e12, 'Neptune': 4.54e12, 'Pluto': 7.37e12}
c = 2.998e8


def convert_to_dB(x: float):
    return 10*np.log10(x)

def convert_from_dB(x: float):
    return 10**(x/10)

def calculate_space_loss(frequency, distance):
    return convert_to_dB((c/(4*np.pi*distance*frequency*1e9))**2)

def calculate_pointing_loss(offset_angle_trans, offset_angle_rec, half_power_angle_trans, half_power_angle_rec):
    loss_trans = -12*(offset_angle_trans/half_power_angle_trans)**2
    loss_rec = -12*(offset_angle_rec/half_power_angle_rec)**2
    return loss_trans+loss_rec

def calculate_half_power_angle(frequency, diameter):
    angle_deg = 21/(frequency*diameter)
    return angle_deg

def calculate_capacity(bandwidth, signal_to_noise):
    # bandwidth in Hz, returns capacity in bit/s
    return bandwidth*np.log2(1+signal_to_noise)

def calculate_antenna_gain(diameter, frequency, efficiency):
    return 20*np.log10(diameter) + 20*np.log10(frequency) + 17.8
    # return convert_to_dB((np.pi*diameter*frequency*1e9/c)**2*efficiency)

def calculate_distance(celes_body: str, elon_angle, height):
    if celes_body != 'Earth' and celes_body != 'Moon':
        return calculate_interplanetary_distance(celes_body, elon_angle)
    elif celes_body == 'Moon':
        return 4.054e8
    else:
        return calculate_LEO_distance(height)

def calculate_interplanetary_distance(celes_body, elon_angle):
    elon_angle = elon_angle*np.pi/180
    sun_earth_distance = r_orbit_dict['Earth']
    sun_target_distance = r_orbit_dict[celes_body]
    return np.sqrt(
        sun_earth_distance**2+sun_target_distance**2-2*sun_earth_distance*sun_target_distance*np.cos(elon_angle)
    )

def calculate_LEO_distance(height):
    # calculate distance for LEO satellites
    r_earth = 6.371e6
    return np.sqrt((r_earth+height)*(r_earth+height)-r_earth*r_earth)

def calculate_generated_pay_data_rate(height, celes_body: str, pixel_angle, scanning_angle, duty_cycle, bits_per_pixel):
    pixels_per_line = scanning_angle/pixel_angle
    r_celes_body = radii_dict[celes_body]
    mu_celes_body = mu_dict[celes_body]
    period = 2*np.pi*np.sqrt(((height+r_celes_body)**3)/mu_celes_body)
    angle_covered_per_second = 360/period
    lines_per_second = angle_covered_per_second/pixel_angle
    pixels_per_second = lines_per_second*pixels_per_line
    bits_per_second = pixels_per_second*bits_per_pixel*duty_cycle
    return bits_per_second

def calculate_path_loss():
    return -0.5

def calculate_link_signal_to_noise(P_trans,
        L_trans,
        G_trans,
        L_path,
        G_rec,
        L_space,
        L_point,
        L_rec,
        data_rate,
        T_syst_noise,
        SNR_req,
    ):
    """
    All in dB!!!
    P_trans: transmitter power, W
    L_trans: transmitter loss factor, -
    G_trans: transmitter gain, -
    L_path: transmission path loss, -
    G_rec: receiver gain, -
    L_space: space loss, -
    L_point: antenna pointing loss, -
    L_rec: receiver loss, -
    data_rate: datarate, bit/s
    T_syst_noise: system noise temperature, K
    SNR_req: required signal to noise ratio (from charts)
    :return: the signal to noise
    """
    # """
    print('All values in dB')
    print('Transmission Power ', P_trans)
    print('Transmisser Loss ', L_trans)
    print('Transmitter Gain ', G_trans)
    print('Path Loss ', L_path)
    print('Receiver Gain ', G_rec)
    print('Space Loss ', L_space)
    print('Pointing Loss ', L_point)
    print('Receiver Loss ', L_rec)
    print('Data Rate ', -data_rate)
    print('System Noise Temperature ', -T_syst_noise)
    # """
    k_boltz = 1.380649e-23  # J/K, Boltzmann constant
    k_boltz = convert_to_dB(k_boltz)
    margin = P_trans+L_trans+G_trans+L_path+G_rec+L_space+L_point+L_rec-data_rate-k_boltz-T_syst_noise-SNR_req
    print('Boltzmann Constant ', -k_boltz)
    print('Total Signal to Noise ', margin)
    return margin

print('Downlink Link Budget')
calculate_link_signal_to_noise(
    P_trans=convert_to_dB(P_trans_sc),
    L_trans=convert_to_dB(L_fact_trans),
    G_trans=calculate_antenna_gain(d_ant_sc, f_down, 0.55),
    L_path=calculate_path_loss(),
    G_rec=calculate_antenna_gain(d_ant_grnd, f_down, 0.55),
    L_space=calculate_space_loss(f_down, calculate_distance(target_celes_body, theta_elon, h_orbit)),
    L_point=calculate_pointing_loss(
        offset_angle_trans=theta_offpnt,
        offset_angle_rec=calculate_half_power_angle(f_down, d_ant_grnd)*0.1,
        half_power_angle_trans=calculate_half_power_angle(f_down, d_ant_sc),
        half_power_angle_rec=calculate_half_power_angle(f_down, d_ant_grnd)
    ),
    L_rec=convert_to_dB(L_fact_rec),
    data_rate=convert_to_dB(calculate_generated_pay_data_rate(
        height=h_orbit,
        celes_body=target_celes_body,
        pixel_angle=pay_pixel_size,
        scanning_angle=pay_theta_swath,
        duty_cycle=pay_duty_cycle,
        bits_per_pixel=pay_bit_per_pixel
    )/pay_downlink_factor),
    T_syst_noise=convert_to_dB(290),
    SNR_req=SNR_req
)

print()
print('Uplink Link Budget')
calculate_link_signal_to_noise(
    P_trans=convert_to_dB(P_trans_grnd),
    L_trans=convert_to_dB(L_fact_rec),
    G_trans=calculate_antenna_gain(d_ant_grnd, f_up, 0.55),
    L_path=calculate_path_loss(),
    G_rec=calculate_antenna_gain(d_ant_sc, f_up, 0.55),
    L_space=calculate_space_loss(f_up, calculate_distance(target_celes_body, theta_elon, h_orbit)),
    L_point=calculate_pointing_loss(
        offset_angle_trans=calculate_half_power_angle(f_up, d_ant_grnd)*0.1,
        offset_angle_rec=theta_offpnt,
        half_power_angle_trans=calculate_half_power_angle(f_up, d_ant_grnd),
        half_power_angle_rec=calculate_half_power_angle(f_up, d_ant_sc)
    ),
    L_rec=convert_to_dB(L_fact_trans),
    data_rate=convert_to_dB(r_up),
    T_syst_noise=convert_to_dB(290),
    SNR_req=SNR_req
)
