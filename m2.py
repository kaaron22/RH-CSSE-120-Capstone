"""
The Python Capstone Project.

CSSE 120 - Introduction to Software Development.
Team members: Natalie Allen, Aaron Kaye, Alexa Kovacs (all of them).

The primary author of this module is: Aaron Kaye.
"""
# DONE: Put the names of ALL team members in the above where indicated.
#       Put YOUR NAME in the above where indicated.

import m0
import m1
import m3
import m4

import tkinter
from tkinter import ttk
import rosebot.standard_rosebot as rb
import rosebot.faux_rosebot as frb
import time

def main():
    pass


def my_frame(root, dc):
    """
    Constructs and returns a   ttk.Frame   on the given root window.
    The frame contains all of this module's widgets.
    Does NOT   grid   the Frame, since the caller will do that.
    Also sets up callbacks for this module's widgets.

    The first argument is the  root  window (a tkinter.Tk object)
    onto which the   ttk.Frame  returned from this function
    will be placed.  The second argument is the shared DataContainer
    object that is CONSTRUCTED in m0 but USED in m1, m2, m3 and m4.

    Preconditions:
      :type root: tkinter.Tk
      :type dc:   m0.DataContainer
    """
    my_frame = ttk.Frame(root, padding=10, relief='raised')

    connect_widget(my_frame, dc)

    disconnect_widget(my_frame, dc)

    move_until_sensor_button = ttk.Button(my_frame, text='Move Using Sensors')
    move_until_sensor_button.grid()
    move_until_sensor_button['command'] = (lambda: move_until_sensor_widget(dc))

    return my_frame


def foo(move_until_sensor_root, dc):
    while True:
        # move (initially forward) until proximity sensor reading exceeds
        # threshold (greater than if moving forward; less than if moving back)
        sensor_move_callback(move_until_sensor_root, dc)

        # after each 'pause', check bump sensors for their last is_pressed reading
        # and break from process if either is True (sensor pressed)
        if dc.sensor_reading[0] == True or dc.sensor_reading[1] == True:
            break

        # otherwise, switch direction because we've either been moving forward
        # and obtained a proximity sensor reading greater than the threshold
        # or been moving back and obtained a reading less than the threshold
        """if dc.textvariable[1].get() == 'forward':
            dc.textvariable[1].set('back')
        else:
            dc.textvariable[1].set('forward')"""


def move_until_sensor_widget(dc):
    move_until_sensor_root = tkinter.Tk()
    my_frame = ttk.Frame(move_until_sensor_root)
    my_frame.grid()

    # Speed Label/Entry Setup
    parameter_label_entry_setup(my_frame, dc, 'Enter a speed (20-255):', 0)

    # Direction Label/Entry Setup
    parameter_label_entry_setup(my_frame, dc,
                                'Enter a direction (forward, back, left, right):', 1)

    # Left Bump Sensor Label/Button Setup
    sensor_label_button_setup(my_frame, dc, 'Bump Sensor (L): ', 0)
    dc.sensor_button[0]['command'] = (lambda: sensor_on_off(dc, 0))

    # Right Bump Sensor Label/Button Setup
    sensor_label_button_setup(my_frame, dc, 'Bump Sensor (R): ', 1)
    dc.sensor_button[1]['command'] = (lambda: sensor_on_off(dc, 1))

    # Left Reflectance Sensor Label/Button Setup
    sensor_label_button_setup(my_frame, dc, 'Reflectance Sensor (L): ', 2)
    dc.sensor_button[2]['command'] = (lambda: sensor_on_off(dc, 2))

    # Left Reflectance Threshold Label/Entry Setup
    parameter_label_entry_setup(my_frame, dc,
                                'Enter a left reflectance sensor threshold (0-4095):',
                                2)

    # Middle Reflectance Sensor Label/Button Setup
    sensor_label_button_setup(my_frame, dc, 'Reflectance Sensor (M): ', 3)
    dc.sensor_button[3]['command'] = (lambda: sensor_on_off(dc, 3))

    # Middle Reflectance Threshold Label/Entry Setup
    parameter_label_entry_setup(my_frame, dc,
                                'Enter a middle reflectance sensor threshold (0-4095):',
                                3)

    # Right Reflectance Sensor Label/Button Setup
    sensor_label_button_setup(my_frame, dc, 'Reflectance Sensor (R): ', 4)
    dc.sensor_button[4]['command'] = (lambda: sensor_on_off(dc, 4))

    # Right Reflectance Threshold Label/Entry Setup
    parameter_label_entry_setup(my_frame, dc,
                                'Enter a right reflectance sensor threshold (0-4095):',
                                4)

    # Front Proximity Sensor Label/Button Setup
    sensor_label_button_setup(my_frame, dc, 'Proximity Sensor (F): ', 5)
    dc.sensor_button[5]['command'] = (lambda: sensor_on_off(dc, 5))

    # Front Proximity Threshold Label/Entry Setup
    parameter_label_entry_setup(my_frame, dc,
                                'Enter a front proximity sensor threshold (0-4095):', 5)

    # Status labels
    movement_status_label_setup(my_frame, dc, 'Status: No command given', 0)
    movement_status_label_setup(my_frame, dc,
                                ('Left Bump Sensor Pressed: ' +
                                 str(dc.sensor_reading[0])), 1)
    movement_status_label_setup(my_frame, dc,
                                ('Right Bump Sensor Pressed: ' +
                                 str(dc.sensor_reading[1])), 2)
    movement_status_label_setup(my_frame, dc,
                                ('Left Reflectance Sensor (value/threshold): '
                                 + str(dc.sensor_reading[2]) + '/' +
                                 str(dc.parameters[2])), 3)
    movement_status_label_setup(my_frame, dc,
                                ('Middle Reflectance Sensor (value/threshold): '
                                 + str(dc.sensor_reading[3]) + '/' +
                                 str(dc.parameters[3])), 4)
    movement_status_label_setup(my_frame, dc,
                                ('Right Reflectance Sensor (value/threshold): '
                                 + str(dc.sensor_reading[4]) + '/' +
                                 str(dc.parameters[4])), 5)
    movement_status_label_setup(my_frame, dc,
                                ('Front Proximity Sensor (value/threshold): '
                                 + str(dc.sensor_reading[5]) + '/' +
                                 str(dc.parameters[5])), 6)


    # Button to begin autonomous movement with sensor control
    sensor_auto_movement_button = ttk.Button(my_frame,
                                             text='Move Using Sensors')
    sensor_auto_movement_button.grid()
    sensor_auto_movement_button['command'] = (lambda: sensor_move_callback
                                              (move_until_sensor_root, dc))

    track_object_button = ttk.Button(my_frame, text='Track Object')
    track_object_button.grid()
    track_object_button['command'] = (lambda: foo(move_until_sensor_root, dc))


def sensor_label_button_setup(my_frame, dc, label_title, index):
    # Sensor Label/Status
    dc.sensor_label_title[index] = label_title
    dc.sensor_label_status[index] = 'Inactive'
    dc.sensor_label[index] = ttk.Label(my_frame, text=dc.sensor_label_title[index]
                                       + dc.sensor_label_status[index])
    dc.sensor_label[index].grid()

    # Sensor Button
    dc.next_button_press[index] = 'Activate'
    dc.sensor_button[index] = ttk.Button(my_frame, text=dc.next_button_press[index])
    dc.sensor_button[index].grid()
    dc.sensor_active[index] = False


def parameter_label_entry_setup(my_frame, dc, label_title, index):
    # Entry box label indicating what to enter
    dc.entry_label_title[index] = ttk.Label(my_frame, text=label_title)
    dc.entry_label_title[index].grid()

    # Entry box for providing desired parameters for sensor thresholds,
    # movement speed, and movement direction
    dc.textvariable[index] = tkinter.StringVar()
    dc.entry_parameters[index] = ttk.Entry(my_frame, textvariable=dc.textvariable[index])
    dc.entry_parameters[index].grid()


def movement_status_label_setup(my_frame, dc, label_info, index):
    dc.movement_sensor_status_messages[index] = ttk.Label(my_frame, text=label_info)
    dc.movement_sensor_status_messages[index].grid()


def sensor_on_off(dc, index):
    if dc.sensor_active[index] == False:  # then activate the sensor
        # update sensor active
        dc.sensor_active[index] = True

        # update sensor label
        dc.sensor_label_status[index] = 'Active'

        # update sensor button
        dc.next_button_press[index] = 'Deactivate'

        # update sensor reading to newly read value
        if index == 0:
            dc.sensor_reading[0] = dc.robot.sensor_reader.left_bump_sensor.is_pressed()
        elif index == 1:
            dc.sensor_reading[1] = dc.robot.sensor_reader.right_bump_sensor.is_pressed()
        elif index == 2:
            dc.sensor_reading[2] = dc.robot.sensor_reader.left_reflectance_sensor.reflectance_reading()
        elif index == 3:
            dc.sensor_reading[3] = dc.robot.sensor_reader.middle_reflectance_sensor.reflectance_reading()
        elif index == 4:
            dc.sensor_reading[4] = dc.robot.sensor_reader.right_reflectance_sensor.reflectance_reading()
        elif index == 5:
            dc.sensor_reading[5] = dc.robot.sensor_reader.front_proximity_sensor.distance_to_object_seen()
        update_status_messages(dc)

    else:  # deactivate the sensor
        # update sensor inactive
        dc.sensor_active[index] = False

        # update sensor label
        dc.sensor_label_status[index] = 'Inactive'

        # update sensor button
        dc.next_button_press[index] = 'Activate'

        # update sensor reading to -1
        dc.sensor_reading[index] = -1
        update_status_messages(dc)

    dc.sensor_label[index]['text'] = (dc.sensor_label_title[index] +
                                      dc.sensor_label_status[index])
    dc.sensor_button[index]['text'] = dc.next_button_press[index]


def sensor_move_callback(move_until_sensor_root, dc):
    # store new threshold values entered by user and update status messages
    dc.parameters[0] = int(dc.entry_parameters[0].get())  # speed (pwm)
    dc.parameters[1] = dc.entry_parameters[1].get()  # direction
    for k in range(2, 6):
        dc.parameters[k] = int(dc.entry_parameters[k].get())
    update_status_messages(dc)

    # make sure at least 1 sensor active before moving robot
    one_or_more_sensor_active = check_for_an_active_sensor(dc)

    if dc.connected and one_or_more_sensor_active:  # make sure robot connected as well

        # now verify no active sensors in a current state/reading that would stop
        # robot during movement
        active_sensors_clear = check_active_sensors_clear(dc)

        # update to show values potentially preventing movement
        update_status_messages(dc)

        if active_sensors_clear:
            dc.movement_sensor_status_messages[0]['text'] = ('Robot moving ' +
                                                             str(dc.parameters[1]) +
                                                             ' at speed ' +
                                                             str(dc.parameters[0]) +
                                                             '!')
            move_until_sensor_root.update()

            # start movement, at user's input speed and direction
            m1.infinite_move(dc.robot, dc.parameters[0], dc.parameters[1])

            # continually check active sensor readings
            while True:
                check_active_sensors(dc)
                update_status_messages(dc)
                move_until_sensor_root.update()
                active_sensor_clear = check_active_sensors_clear(dc)
                if active_sensor_clear == False:
                    # then stop robot
                    dc.robot.motor_controller.stop()
                    dc.movement_sensor_status_messages[0]['text'] = ('Robot stopped!')
                    update_status_messages(dc)
                    break
        else:
            # update movement status message
            dc.movement_sensor_status_messages[0]['text'] = ('Movement prohibited' +
                                                             ' due to current ' +
                                                             'sensor readings!')

    elif dc.connected == False:
        dc.movement_sensor_status_messages[0]['text'] = ('Status: No robot connection!')
    else:
        dc.movement_sensor_status_messages[0]['text'] = ('Status: Sensors inactive. ' +
                                                         'Movement command canceled!')


def update_status_messages(dc):
    dc.movement_sensor_status_messages[1]['text'] = ('Left Bump Sensor Pressed: ' +
                                                     str(dc.sensor_reading[0]))
    dc.movement_sensor_status_messages[2]['text'] = ('Right Bump Sensor Pressed: ' +
                                                     str(dc.sensor_reading[1]))
    dc.movement_sensor_status_messages[3]['text'] = ('Left Reflectance Sensor (value/threshold): '
                                                     + str(dc.sensor_reading[2]) + '/' +
                                                     str(dc.parameters[2]))
    dc.movement_sensor_status_messages[4]['text'] = ('Middle Reflectance Sensor (value/threshold): '
                                                     + str(dc.sensor_reading[3]) + '/' +
                                                     str(dc.parameters[3]))
    dc.movement_sensor_status_messages[5]['text'] = ('Right Reflectance Sensor (value/threshold): '
                                                     + str(dc.sensor_reading[4]) + '/' +
                                                     str(dc.parameters[4]))
    dc.movement_sensor_status_messages[6]['text'] = ('Front Proximity Sensor (value/threshold): '
                                                     + str(dc.sensor_reading[5]) + '/' +
                                                     str(dc.parameters[5]))


def check_for_an_active_sensor(dc):
    for k in range(len(dc.sensor_active)):
        if dc.sensor_active[k] == True:
            return True
    return False


def check_active_sensors_clear(dc):
    check_active_sensors(dc)
    for k in range(2):
        if dc.sensor_active[k]:
            if dc.sensor_reading[k] == True:
                return False
    for k in range(2, 6):
        if dc.sensor_active[k]:
            if dc.parameters[1] == 'forward':
                if dc.sensor_reading[k] > dc.parameters[k]:
                    return False
            else:
                if dc.sensor_reading[k] < dc.parameters[k]:
                    return False
    return True


def check_active_sensors(dc):
    if dc.sensor_active[0]:
        dc.sensor_reading[0] = dc.robot.sensor_reader.left_bump_sensor.is_pressed()
    if dc.sensor_active[1]:
        dc.sensor_reading[1] = dc.robot.sensor_reader.right_bump_sensor.is_pressed()
    if dc.sensor_active[2]:
        dc.sensor_reading[2] = dc.robot.sensor_reader.left_reflectance_sensor.reflectance_reading()
    if dc.sensor_active[3]:
        dc.sensor_reading[3] = dc.robot.sensor_reader.middle_reflectance_sensor.reflectance_reading()
    if dc.sensor_active[4]:
        dc.sensor_reading[4] = dc.robot.sensor_reader.right_reflectance_sensor.reflectance_reading()
    if dc.sensor_active[5]:
        dc.sensor_reading[5] = dc.robot.sensor_reader.front_proximity_sensor.distance_to_object_seen()


def connect_widget(my_frame, dc):
    # Status message indicating result of attempt to connect or disconnect
    dc.connect_disconnect_attempt_result = ttk.Label(my_frame,
                                                     text='Attempt Result: None')
    dc.connect_disconnect_attempt_result.grid()

    # States the current status of connection
    dc.connection_status = ttk.Label(my_frame, text='Connection Status: None')
    dc.connection_status.grid()

    # States current type of robot to which we are connected (if any)
    dc.robot_type = ttk.Label(my_frame, text='Robot Type: None')
    dc.robot_type.grid()

    # States current port number if currently connected (i.e. 'sim', or 5)
    dc.currently_connected_port_label = ttk.Label(my_frame,
                                                  text='Connected to Port: None')
    dc.currently_connected_port_label.grid()

    # Connection Type (wired, wireless, sim)
    dc.connection_type = ttk.Label(my_frame, text='Connection Type: None')
    dc.connection_type.grid()

    # Connect Button (Sim)
    robot_connect_button_sim = ttk.Button(my_frame, text='Connect Faux')
    robot_connect_button_sim.grid()
    robot_connect_button_sim['command'] = (lambda: connect_callback(dc, 0, 'Sim'))

    # Enter Desired Connection Port (i.e. 5 or 'sim')
    port_label = ttk.Label(my_frame,
                           text='For wired/wireless, enter desired port connection ' +
                           '(a valid, available wired port or wireless robot number):')
    port_label.grid()
    dc.entry_port_for_connection = ttk.Entry(my_frame)
    dc.entry_port_for_connection.grid()

    # Connect Button (wired)
    robot_connect_button_wired = ttk.Button(my_frame, text="Connect Wired")
    robot_connect_button_wired.grid()
    robot_connect_button_wired['command'] = (lambda: connect_callback
                                             (dc, 1,
                                              dc.entry_port_for_connection.get()))

    # Connect Button (wireless)
    robot_connect_button_wireless = ttk.Button(my_frame, text="Connect Wireless")
    robot_connect_button_wireless.grid()
    robot_connect_button_wireless['command'] = (lambda: connect_callback
                                                (dc, 2,
                                                 dc.entry_port_for_connection.get()))


def connect_callback(dc, attempt_connection_type, attempt_connection_port):
    # check if trying to connect to the same robot/port
    same_connection = check_same_connection(dc, attempt_connection_type,
                                            attempt_connection_port)
    if same_connection:
        dc.connect_disconnect_attempt_result['text'] = dc.connect_status_message[0]
    elif attempt_connection_type == 0:
        # we are connecting to the Faux robot (Sim)
        dc.robot = frb.RoseBot()
        dc.robot.connector.connect()
        set_connection_info(dc, True, 'Faux', 'Connected', 'Sim', 'Sim', 0,
                            dc.connect_status_message[1])
    else:
        # we are connecting to standard robot either wired or wirelessly, so
        # first attempt to convert desired port from entry box contents to an integer
        desired_port = attempt_convert_desired_port_to_int(attempt_connection_port)
        if desired_port == None:
            # we could not convert contents of port entry box to an integer
            dc.connect_disconnect_attempt_result['text'] = (dc.connect_status_message[2] +
                                                            attempt_connection_port + ')')
        else:
            # we successfully converted to an int, so now attempt connection based
            # on connection type (wired or wireless)
            if attempt_connection_type == 1:
                # we are connecting to the Standard Robot with a wired connection
                attempted_robot = attempt_connect_to_robot(desired_port, 1)
            else:
                # we are connecting to the Standard Robot with a wireless connection
                attempted_robot = attempt_connect_to_robot(desired_port, 2)

            # now check if successful connection
            if attempted_robot == None:
                dc.connect_disconnect_attempt_result['text'] = (dc.connect_status_message[2] +
                                                                attempt_connection_port + ')')
            else:
                # we successfully connected
                dc.robot = attempted_robot
                if attempt_connection_type == 1:
                    connection_type = 'Wired'
                else:
                    connection_type = 'Wireless'
                set_connection_info(dc, True, 'Standard', 'Connected',
                                    attempt_connection_port, connection_type,
                                    attempt_connection_type,
                                    dc.connect_status_message[1])


def attempt_connect_to_robot(desired_port, connection_type):
    attempted_robot = rb.RoseBot()
    if connection_type == 1:
        try:
            attempted_robot.connector.connect(desired_port)
            return attempted_robot
        except Exception:
            # if we could not connect, the port number did not match what was listed
            # in the PC Device Manager (wired connection) or there was some other
            # problem in connection; we leave any current connection intact
            return None
    elif connection_type == 2:
        try:
            attempted_robot.connector.connect_wireless(desired_port)
            return attempted_robot
        except Exception:
            # if we could not connect, the port number did not match a valid
            # Robot number (wireless connection) or there was some other
            # problem in connection; we leave any current connection intact
            return None


def attempt_convert_desired_port_to_int(desired_port):
    try:
        port_num = int(desired_port)
        return port_num
    except ValueError:
        return None


def check_same_connection(dc, attempt_connection_type, attempt_connection_port):
    # if the attempted connection type (0 = Sim, 1 = Wired, 2 = Wireless) and the
    # attempted connection port are the same, then we are trying to connect
    # to the same place
    if (attempt_connection_type == dc.connection_type_flag and
        attempt_connection_port == dc.currently_connected_port):
        return True
    return False


def disconnect_widget(my_frame, dc):
    # Disconnect Button
    robot_disconnect_button = ttk.Button(my_frame, text="Disconnect")
    robot_disconnect_button.grid()
    robot_disconnect_button['command'] = (lambda: disconnect_callback(dc))


def disconnect_callback(dc):
    if dc.connected == False:
        # we are already disconnected
        dc.connect_disconnect_attempt_result['text'] = 'Attempt Result: Already Disconnected!'
    else:
        dc.robot.connector.disconnect()
        dc.robot = None
        set_connection_info(dc, False, 'None', 'Disconnected', 'None', 'None', None,
                            'Attempt Result: Disconnect Successful!')


def set_connection_info(dc, connected, robot_type, status, connected_port_label,
                        connection_type, connection_type_flag, result):
    dc.connected = connected
    dc.robot_type['text'] = 'Robot Type: ' + robot_type
    dc.connection_status['text'] = 'Connection Status: ' + status
    dc.currently_connected_port_label['text'] = ('Connected to Port: '
                                                 + connected_port_label)
    dc.currently_connected_port = connected_port_label
    dc.connection_type['text'] = 'Connection Type: ' + connection_type
    dc.connection_type_flag = connection_type_flag
    dc.connect_disconnect_attempt_result['text'] = result


# ----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
# ----------------------------------------------------------------------
if __name__ == '__main__':
    m0.main()
