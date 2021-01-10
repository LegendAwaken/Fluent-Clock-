from fluentapp.windoweffect import WindowBlur

try:
    with open('assets/metadata_settings/trt_value.dll', 'rb') as reader:
        if str(reader.read().decode()) == 'ON':
            # blur the window background

            # handling the exception
            try:
                with open('assets/metadata_settings/radx32.dll', 'r+b') as blur_radius:
                    _blur_ = str(blur_radius.read().decode())
                    if _blur_ == '':
                        blur_radius.write(b'8')
                    try:
                        _int_blur_ = int(_blur_)
                    except ValueError:
                        _int_blur_ = int(_blur_[0])
                    with open('assets/metadata_settings/ag_lightv.dll', 'rb') as reader_data:
                        reader_two = str(reader_data.read().decode())
                        if reader_two == 'ON':
                            WindowBlur(radius=8)
                        else:
                            WindowBlur(radius=_int_blur_)

            # if there is no such file then create one
            except FileNotFoundError:
                with open('assets/metadata_settings/blur_radius.txt', 'w') as default_value:
                    default_value.write('10')

except FileNotFoundError:
    with open('assets/metadata_settings/trt_value.dll', 'wb') as default_value:
        default_value.write(b'ON')

# change the value for alarm cross
with open('assets/metadata_settings/cross_alarm.bin', 'wb') as reader:
    reader.write(b'False')

# rewrite nothing in alarm notifier
with open('assets/metadata_settings/alarm_notifier.bin', 'wb') as writer:
    writer.write(b'')

# importing libraries
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from win32api import GetSystemMetrics
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
import pyttsx3
from threading import Thread


# main screen manager
class WindowManager(ScreenManager):
    Window.size = (GetSystemMetrics(0), GetSystemMetrics(1))
    Window.left = 0
    Window.top = 0
    Window.borless = True

    @staticmethod
    def close():
        Window.close()

    def color_manager(self, *args):
        with open('assets/metadata_settings/darken.bin', 'rb') as reader:
            try:
                read = int(reader.read().decode())
            except ValueError:
                read = int(reader.read().decode()[0])

        with open('assets/metadata_settings/trt_value.dll', 'rb') as read_transparent:
            read_transparent_value = str(read_transparent.read().decode())
        with open('assets/metadata_settings/lxdg1.dll', 'rb') as reader_data:
            if read_transparent_value == 'OFF':
                return 0, 0, 0, 1
            elif str(reader_data.read().decode()) == 'OFF':
                return 0, 0, 0, 0
            elif read == 10:
                return 0, 0, 0, 0
            elif 10 < read < 20:
                return 0, 0, 0, 0.2
            elif 20 < read < 30:
                return 0, 0, 0, 0.3
            elif 30 < read < 40:
                return 0, 0, 0, 0.38
            elif 40 < read < 50:
                return 0, 0, 0, 0.4
            elif 50 < read < 60:
                return 0, 0, 0, 0.5
            elif 60 < read < 70:
                return 0, 0, 0, 0.6
            elif 70 < read < 80:
                return 0, 0, 0, 0.7
            elif 80 < read < 90:
                return 0, 0, 0, 0.8
            elif 90 < read < 95:
                return 0, 0, 0, 0.9
            elif 95 < read < 100:
                return 0, 0, 0, 1
            else:
                return 0, 0, 0, 0.3

    @staticmethod
    def main_toggle_effect():
        with open('assets/metadata_settings/trt_value.dll', 'rb') as read_data:
            reader = str(read_data.read().decode())
            with open('assets/metadata_settings/ag_lightv.dll', 'rb') as reader_data:
                read_me = str(reader_data.read().decode())
                if reader == 'OFF':
                    return 0, 0, 0, 1
                elif read_me == 'ON':
                    return 0, 0, 0, 0.58
                else:
                    return 0, 0, 0, 0.8


class MainScreen(Screen):

    # ######################################### FORMAT OF TIME ####################################### #
    def twelve_format_caller(self, *args):
        Clock.schedule_interval(self.twelve_hour_format, 1.0)

    def twelve_hour_format(self, *args):
        from datetime import datetime

        time = datetime.now()

        formatted = time.strftime('%I:%M:%p')

        self.ids.clock.text = formatted

        format_for_alarm = time.strftime('%I:%M:%S:%p')

        return str(format_for_alarm)

    def twenty_format_caller(self, *args):
        Clock.schedule_interval(self.twenty_four_format, 1.0)
        Clock.schedule_interval(self.date, 3.0)

    def twenty_four_format(self, *args):
        from datetime import datetime

        time = datetime.now()

        formatted = time.strftime('%H:%M:%S')

        self.ids.clock.text = formatted

        return str(formatted)

    def date(self, *args):
        from datetime import datetime

        # get time
        time = datetime.now()

        # filter the values
        date = time.strftime('%B %M %A %Y')

        try:
            with open('assets/metadata_settings/format_loader.dll', 'rb') as reader:
                value = str(reader.read().decode())
                if value == '12 hour':
                    Clock.schedule_once(self.twelve_format_caller)

                else:
                    Clock.schedule_once(self.twenty_format_caller)
        except FileNotFoundError:
            with open('assets/metadata_settings/format_loader.dll', 'wb') as writer:
                writer.write(b'12 hour')
        return f'{date}'


class Alarm(Screen):
    def labels(self, *args):
        thread = Thread(target=self.alarm_notifier)
        thread.start()
        return ' '

    def alarm_notifier(self, *args):

        with open('assets/metadata_settings/alarm.bin', 'rb') as reader:
            read = reader.read().decode()

            self.ids.alarm1_notifier.text = str(read[0:5])

            Clock.schedule_interval(self.cross_alarm, 1.0)

    # alarm 2 label

    def labels_alarm2(self, *args):
        Clock.schedule_once(self.alarm_notifier_2)
        return ' '

    def alarm_notifier_2(self, *args):

        with open('assets/metadata_settings/al2_mx32_module.dll', 'rb') as reader:
            read = reader.read().decode()

            self.ids.alarm2_notifier.text = str(read[0:5])

            Clock.schedule_interval(self.cross_alarm_2, 2.0)

    def cross_alarm(self, *args):
        try:
            with open('assets/metadata_settings/cross_alarm.bin', 'rb') as reader:
                read = str(reader.read().decode())

                if read == 'True':
                    self.ids.pause_alarm1.background_normal = 'assets/metadata_image/pause_alarm.png'

            Clock.schedule_interval(self.alarm_1_label_manager, 1.0)

        except FileNotFoundError:
            with open('assets/metadata_settings/cross_alarm.bin', 'wb') as writer:
                writer.write(b'False')

    def cross_alarm_2(self, *args):
        try:
            with open('assets/metadata_settings/cross_alarm2.dll', 'rb') as reader:
                read = str(reader.read().decode())

                if read == 'True':
                    self.ids.pause_alarm2.background_normal = 'assets/metadata_image/pause_alarm.png'

            Clock.schedule_interval(self.alarm_2_label_manager, 1.0)

        except FileNotFoundError:
            with open('assets/metadata_settings/cross_alarm2.dll', 'wb') as writer:
                writer.write(b'False')

    def alarm_1_label_manager(self, *args):
        with open('assets/metadata_settings/id.bin', 'rb') as reader:
            read = reader.read().decode()
            if read == '':
                self.ids.alarm1_label.text = 'Reserved'
            else:
                self.ids.alarm1_label.text = str(read)

    def alarm_2_label_manager(self, *args):
        with open('assets/metadata_settings/id_a.dll', 'rb') as reader:
            read = reader.read().decode()
            if read == '':
                self.ids.alarm2_label.text = 'Alarm 2'
            else:
                self.ids.alarm2_label.text = str(read)

    def stop(self):
        import pygame
        pygame.init()
        pygame.mixer.music.pause()
        self.ids.pause_alarm1.background_normal = 'assets/metadata_image/pause_alarm_fade.png'

    def toggle_info(self):

        # write toggle 1 state
        with open('assets/toggles/toggle1.bin', 'wb') as writer:
            writer.write(self.ids.toggle_alarm_1.text.encode())
        # write toggle 2 state
        with open('assets/toggles/toggle2.bin', 'wb') as writer:
            writer.write(self.ids.toggle_alarm_2.text.encode())
        # write toggle 3 state
        with open('assets/toggles/toggle3.bin', 'wb') as writer:
            writer.write(self.ids.toggle_alarm_3.text.encode())
        # write toggle 4 state
        with open('assets/toggles/toggle4.bin', 'wb') as writer:
            writer.write(self.ids.toggle_alarm_4.text.encode())
        # write toggle 5 state
        with open('assets/toggles/toggle5.bin', 'wb') as writer:
            writer.write(self.ids.toggle_alarm_5.text.encode())
        # write toggle 6 state
        with open('assets/toggles/toggle6.bin', 'wb') as writer:
            writer.write(self.ids.toggle_alarm_6.text.encode())

    @staticmethod
    def toggle_1_text():
        with open('assets/toggles/toggle1.bin', 'rb') as reader:
            read = str(reader.read().decode())
            return read

    @staticmethod
    def toggle_2_text():
        with open('assets/toggles/toggle2.bin', 'rb') as reader:
            read = str(reader.read().decode())
            return read

    @staticmethod
    def toggle_3_text():
        with open('assets/toggles/toggle3.bin', 'rb') as readerme:
            read = str(readerme.read().decode())
            return read

    @staticmethod
    def toggle_4_text():
        with open('assets/toggles/toggle4.bin', 'rb') as reader:
            read = str(reader.read().decode())
            return read

    @staticmethod
    def toggle_5_text():
        with open('assets/toggles/toggle5.bin', 'rb') as reader_id_2:
            read = str(reader_id_2.read().decode())
            return read

    @staticmethod
    def toggle_6_text():
        with open('assets/toggles/toggle6.bin', 'rb') as reader:
            read = str(reader.read().decode())
            return read


class Alarm2(Screen):
    def seconds(self, *args):
        from datetime import datetime
        time = datetime.now()
        seconds = time.strftime('%S')
        self.ids.timer_seconds.hint_text = str(seconds)
        return seconds

    def minutes(self, *args):
        from datetime import datetime
        time = datetime.now()
        formatted = time.strftime('%M')
        self.ids.timer_minute.hint_text = str(formatted)
        Clock.schedule_interval(self.seconds, 1.0)
        return formatted

    def hour(self):
        with open('assets/metadata_settings/format_loader.dll', 'rb') as reader:
            read = str(reader.read().decode())
            from datetime import datetime
            time = datetime.now()
            Clock.schedule_interval(self.minutes, 1.0)
            if read == '12 hour':
                formatted = time.strftime('%I')

                return formatted
            else:
                formatted = time.strftime('%H')

                return formatted

    def alarm_time(self):
        with open('assets/metadata_settings/al2_mx32_module.dll', 'wb') as writer_id_1:
            hour_timer = self.ids.timer_hour.text
            current_hour = str(self.hour)
            with open('assets/metadata_settings/format_loader.dll', 'rb') as reader_id_1:
                read = str(reader_id_1.read().decode())
                if read == '24 hour':
                    if len(hour_timer) == 1:
                        writer_id_1.write(b'0' + hour_timer.encode() + b':')
                    elif len(hour_timer) > 2 and hour_timer > 24:
                        writer_id_1.write(b'23' + b':')
                    elif len(hour_timer) == 2:
                        writer_id_1.write(hour_timer.encode() + b':')
                    elif hour_timer == '':
                        writer_id_1.write(current_hour.encode() + b':')
                    else:
                        writer_id_1.write(hour_timer.encode() + b':')

                    # write the minutes
                    minutes = self.ids.timer_minute.text

                    if len(minutes) == 1:
                        writer_id_1.write(b'0' + minutes.encode() + b':')

                    elif len(minutes) > 2 and minutes > 60:
                        writer_id_1.write(b'59' + b':')

                    elif len(minutes) == 2:
                        writer_id_1.write(minutes.encode() + b':')

                    elif minutes == '':
                        writer_id_1.write(minutes.encode() + b':')

                    else:
                        writer_id_1.write(b'00' + b':')

                    # write the seconds
                    seconds = self.ids.timer_seconds.text

                    if len(seconds) == 1:
                        writer_id_1.write(b'0' + seconds.encode())
                    elif len(seconds) == 2:
                        writer_id_1.write(b'00' + b':')
                    elif len(seconds) > 2 and seconds > 60:
                        writer_id_1.write(b'59')
                    elif str(seconds) == '':
                        writer_id_1.write(b'00' + b':')
                    else:
                        writer_id_1.write(b'00')

                else:
                    from datetime import datetime

                    time = datetime.now()

                    am_pm = time.strftime('%p')

                    with open('assets/metadata_settings/al2_mx32_module.dll', 'wb') as writer_id_1:

                        hour_timer = self.ids.timer_hour.text
                        current_hour = str(self.hour())
                        if len(hour_timer) == 1:
                            writer_id_1.write(b'0' + hour_timer.encode() + b':')
                        elif len(hour_timer) > 2 and int(hour_timer) > 12:
                            writer_id_1.write(b'12' + b':')
                        elif len(hour_timer) == 2:
                            writer_id_1.write(hour_timer.encode() + b':')
                        elif hour_timer == '':
                            writer_id_1.write(current_hour.encode() + b':')
                        else:
                            writer_id_1.write(hour_timer.encode() + b':')

                        # write the minutes
                        minutes = self.ids.timer_minute.text

                        if len(minutes) == 1:
                            writer_id_1.write(b'0' + minutes.encode() + b':')
                        elif len(minutes) > 60 and minutes > 60:
                            writer_id_1.write(b'59' + b':')
                        elif len(minutes) == 2:
                            writer_id_1.write(minutes.encode() + b':')
                        elif minutes == '':
                            writer_id_1.write(b'00' + b':')
                        else:
                            writer_id_1.write(minutes.encode() + b':')

                        # write the seconds
                        seconds = str(self.ids.timer_seconds.text)

                        if len(seconds) == 1:
                            writer_id_1.write(b'0' + seconds.encode() + b':')
                        elif len(seconds) > 60 and int(seconds) > 60:
                            writer_id_1.write(b'59' + b':')
                        elif len(seconds) == 2:
                            writer_id_1.write(seconds.encode() + b':')
                        elif seconds == '':
                            writer_id_1.write(b'00' + b':')
                        else:
                            writer_id_1.write(b'00' + b':')
                        # write the am or pm
                        writer_id_1.write(am_pm.encode())

    def save_alarm(self):

        with open('assets/metadata_settings/sound_a.dll', 'wb') as write:
            writer_id_two = self.ids.alarm_sound.text.encode()

            write.write(writer_id_two)

        with open('assets/metadata_settings/id_a.dll', 'wb') as write:
            get_alarm_label = self.ids.alarm_label.text

            if len(get_alarm_label) > 8:

                slice_alarm_label = get_alarm_label[0:8]

                writer_id_two = slice_alarm_label.encode()

                write.write(writer_id_two)
            else:
                write.write(get_alarm_label.encode())

        self.start_alarm_event = Clock.schedule_interval(self.start_alarm, 1.0)

    def start_alarm(self, *args):
        with open('assets/toggles/toggle2.bin', 'rb') as reader:

            read = str(reader.read().decode())

            if read == 'Status : ON':
                # initialise the pygame to start alarm sound
                import pygame
                import mutagen.mp3

                # load the current music
                with open('assets/metadata_settings/sound_a.dll', 'rb') as reader:

                    read = reader.read().decode()

                    # get the bitrate sample of the mp3
                    try:
                        self.mp3_bitrate = mutagen.mp3.MP3(f'assets/sounds/{str(read)}.mp3')
                    except mutagen.MutagenError:
                        self.mp3_bitrate = mutagen.mp3.MP3(f'assets/sounds/flute2.mp3')
                    try:
                        pygame.mixer.init(frequency=self.mp3_bitrate.info.sample_rate)
                        pygame.mixer.music.load(f'assets/sounds/{str(read)}.mp3')
                    except pygame.error:
                        pygame.mixer.music.load(f'assets/sounds/flute2.mp3')

                with open('assets/metadata_settings/al2_mx32_module.dll', 'rb') as alarm_reader:

                    value = str(alarm_reader.read().decode())

                    instance_time = MainScreen()

                    twelve_time = instance_time.twelve_hour_format()

                    twenty_time = instance_time.twenty_four_format()

                    if value == str(twelve_time):

                        pygame.mixer.music.play(100)

                        self.start_alarm_event.cancel()

                        with open('assets/metadata_settings/cross_alarm2.dll', 'wb') as writer:
                            writer.write(b'True')

                    elif value == str(twenty_time):

                        pygame.mixer.music.play(100)

                        self.start_alarm_event.cancel()

                        with open('assets/metadata_settings/cross_alarm2.dll', 'wb') as writer:
                            writer.write(b'True')

                    else:
                        with open('assets/metadata_settings/cross_alarm2.dll', 'wb') as writer:
                            writer.write(b'False')


class Alarm3(Screen):
    pass


class Alarm4(Screen):
    pass


class Alarm5(Screen):
    pass


class Alarm6(Screen):
    pass


class NewAlarm(Screen):
    def seconds(self, *args):
        from datetime import datetime
        time = datetime.now()
        seconds = time.strftime('%S')
        self.ids.timer_seconds.hint_text = str(seconds)
        return seconds

    def minutes(self, *args):
        from datetime import datetime
        time = datetime.now()
        formatted = time.strftime('%M')
        self.ids.timer_minute.hint_text = str(formatted)
        Clock.schedule_interval(self.seconds, 1.0)
        return formatted

    def hour(self):
        with open('assets/metadata_settings/format_loader.dll', 'rb') as reader:
            read = str(reader.read().decode())
            from datetime import datetime
            time = datetime.now()
            Clock.schedule_interval(self.minutes, 1.0)
            if read == '12 hour':
                formatted = time.strftime('%I')

                return formatted
            else:
                formatted = time.strftime('%H')

                return formatted

    def alarm_time(self):
        with open('assets/metadata_settings/alarm.bin', 'wb') as writer_id_1:
            hour_timer = self.ids.timer_hour.text
            current_hour = str(self.hour)
            with open('assets/metadata_settings/format_loader.dll', 'rb') as reader_id_1:
                read = str(reader_id_1.read().decode())
                if read == '24 hour':
                    if len(hour_timer) == 1:
                        writer_id_1.write(b'0' + hour_timer.encode() + b':')
                    elif len(hour_timer) > 2 and hour_timer > 24:
                        writer_id_1.write(b'23' + b':')
                    elif len(hour_timer) == 2:
                        writer_id_1.write(hour_timer.encode() + b':')
                    elif hour_timer == '':
                        writer_id_1.write(current_hour.encode() + b':')
                    else:
                        writer_id_1.write(hour_timer.encode() + b':')

                    # write the minutes
                    minutes = self.ids.timer_minute.text

                    if len(minutes) == 1:
                        writer_id_1.write(b'0' + minutes.encode() + b':')

                    elif len(minutes) > 2 and minutes > 60:
                        writer_id_1.write(b'59' + b':')

                    elif len(minutes) == 2:
                        writer_id_1.write(minutes.encode() + b':')

                    elif minutes == '':
                        writer_id_1.write(minutes.encode() + b':')

                    else:
                        writer_id_1.write(b'00' + b':')

                    # write the seconds
                    seconds = self.ids.timer_seconds.text

                    if len(seconds) == 1:
                        writer_id_1.write(b'0' + seconds.encode())
                    elif len(seconds) == 2:
                        writer_id_1.write(b'00' + b':')
                    elif len(seconds) > 2 and seconds > 60:
                        writer_id_1.write(b'59')
                    elif str(seconds) == '':
                        writer_id_1.write(b'00' + b':')
                    else:
                        writer_id_1.write(b'00')

                else:
                    from datetime import datetime

                    time = datetime.now()

                    am_pm = time.strftime('%p')

                    with open('assets/metadata_settings/alarm.bin', 'wb') as writer_id_1:

                        hour_timer = self.ids.timer_hour.text
                        current_hour = str(self.hour())
                        if len(hour_timer) == 1:
                            writer_id_1.write(b'0' + hour_timer.encode() + b':')
                        elif len(hour_timer) > 2 and int(hour_timer) > 12:
                            writer_id_1.write(b'12' + b':')
                        elif len(hour_timer) == 2:
                            writer_id_1.write(hour_timer.encode() + b':')
                        elif hour_timer == '':
                            writer_id_1.write(current_hour.encode() + b':')
                        else:
                            writer_id_1.write(hour_timer.encode() + b':')

                        # write the minutes
                        minutes = self.ids.timer_minute.text

                        if len(minutes) == 1:
                            writer_id_1.write(b'0' + minutes.encode() + b':')
                        elif len(minutes) > 60 and minutes > 60:
                            writer_id_1.write(b'59' + b':')
                        elif len(minutes) == 2:
                            writer_id_1.write(minutes.encode() + b':')
                        elif minutes == '':
                            writer_id_1.write(b'00' + b':')
                        else:
                            writer_id_1.write(minutes.encode() + b':')

                        # write the seconds
                        seconds = str(self.ids.timer_seconds.text)

                        if len(seconds) == 1:
                            writer_id_1.write(b'0' + seconds.encode() + b':')
                        elif len(seconds) > 60 and int(seconds) > 60:
                            writer_id_1.write(b'59' + b':')
                        elif len(seconds) == 2:
                            writer_id_1.write(seconds.encode() + b':')
                        elif seconds == '':
                            writer_id_1.write(b'00' + b':')
                        else:
                            writer_id_1.write(b'00' + b':')
                        # write the am or pm
                        writer_id_1.write(am_pm.encode())

    def save_alarm(self):

        with open('assets/metadata_settings/sound.bin', 'wb') as write:
            writer_id_two = self.ids.alarm_sound.text.encode()

            write.write(writer_id_two)

        with open('assets/metadata_settings/id.bin', 'wb') as write:
            get_alarm_label = self.ids.alarm_label.text

            if len(get_alarm_label) > 8:

                slice_alarm_label = get_alarm_label[0:8]

                writer_id_two = slice_alarm_label.encode()

                write.write(writer_id_two)
            else:
                write.write(get_alarm_label.encode())

        self.start_alarm_event = Clock.schedule_interval(self.start_alarm, 1.0)

    def start_alarm(self, *args):
        with open('assets/toggles/toggle1.bin', 'rb') as reader:

            read = str(reader.read().decode())

            if read == 'Status : ON':
                # initialise the pygame to start alarm sound
                import pygame
                import mutagen.mp3

                # load the current music
                with open('assets/metadata_settings/sound.bin', 'rb') as reader:

                    read = reader.read().decode()

                    # get the bitrate sample of the mp3
                    try:
                        self.mp3_bitrate = mutagen.mp3.MP3(f'assets/sounds/{str(read)}.mp3')
                    except mutagen.MutagenError:
                        self.mp3_bitrate = mutagen.mp3.MP3(f'assets/sounds/flute2.mp3')
                    try:
                        pygame.mixer.init(frequency=self.mp3_bitrate.info.sample_rate)
                        pygame.mixer.music.load(f'assets/sounds/{str(read)}.mp3')
                    except pygame.error:
                        pygame.mixer.music.load(f'assets/sounds/flute2.mp3')

                with open('assets/metadata_settings/alarm.bin', 'rb') as alarm_reader:

                    value = str(alarm_reader.read().decode())

                    instance_time = MainScreen()

                    twelve_time = instance_time.twelve_hour_format()

                    twenty_time = instance_time.twenty_four_format()

                    if value == str(twelve_time):

                        pygame.mixer.music.play(100)

                        self.start_alarm_event.cancel()

                        with open('assets/metadata_settings/cross_alarm.bin', 'wb') as writer:
                            writer.write(b'True')

                    elif value == str(twenty_time):

                        pygame.mixer.music.play(100)

                        self.start_alarm_event.cancel()

                        with open('assets/metadata_settings/cross_alarm.bin', 'wb') as writer:
                            writer.write(b'True')

                    else:
                        with open('assets/metadata_settings/cross_alarm.bin', 'wb') as writer:
                            writer.write(b'False')


class Timer(Screen):

    def timer_hour(self):
        if self.ids.timer_hour.text == '':
            return 0

        else:
            get_hour = int(self.ids.timer_hour.text)

            return get_hour

    def timer_minute(self):
        if self.ids.timer_minute.text == '':
            return 0

        else:
            get_minute = int(self.ids.timer_minute.text)

            return get_minute

    def timer_seconds(self):
        if self.ids.timer_seconds.text == '':
            return 0
        else:
            get_seconds = int(self.ids.timer_seconds.text)

            return get_seconds

    def set_image(self, *args):

        # change the images first
        self.ids.play_button.background_normal = 'assets/metadata_image/buttons/play_fade.png'

        self.ids.pause_button.background_normal = 'assets/metadata_image/buttons/pause.png'

        self.ids.timer_seconds.text = '00'

        Clock.schedule_interval(self.start_timer, 1.0)

    def start_timer(self, *args):
        label = 0
        label += 1

        with open('assets/metadata_settings/timer_value.txt', 'w') as writer:
            writer.write(str(label))

        with open('assets/metadata_settings/timer_value.txt', 'w+') as reader:
            string = str(label)
            read_me = reader.read()
            if string == read_me:
                label += (int(string)) + 1

            self.ids.timer_seconds.text = str(label)

    def timer_pause(self):
        self.ids.play_button.background_normal = 'assets/metadata_image/buttons/play.png'

        self.ids.pause_button.background_normal = 'assets/metadata_image/buttons/pause_fade.png'


class Stopwatch(Screen):
    pass


class SettingsScreen(Screen):

    # ####################################### BLUR INTENSITY ############################################
    # handle the event created by the slider
    def blur_intensity(self):
        # write the slider value to a file
        with open('assets/metadata_settings/radx32.dll.', 'wb') as blur_value:
            blur_ = str(self.ids.blur_intensity.value)

            # sliced blur
            sliced_blur_value = blur_[0:2]

            # write the sliced value to the file
            blur_value.write(sliced_blur_value.encode())

        # read the value and pass it to the label
        with open('assets/metadata_settings/radx32.dll', 'rb') as read_value:
            value = str(read_value.read().decode())

            self.ids.slider_value.text = value

    @staticmethod
    def blur_text_return():
        # read the file and give it to label
        with open('assets/metadata_settings/radx32.dll', 'rb') as value:
            reader = value.read().decode()

            return str(reader)

    @staticmethod
    def slider_value():
        with open('assets/metadata_settings/radx32.dll', 'rb') as value:
            reader = value.read().decode()

            try:
                return int(reader)
            except ValueError:
                new = str(reader)
                new2 = new[0]
                new3 = int(new2)
                return new3

    # ###################################### END OF BLUR INTENSITY ####################################################

    def save_toggle_value(self):
        with open('assets/metadata_settings/trt_value.dll', 'wb') as toggle_value:

            # get toggle value and write it
            value = str(self.ids.toggle.text)

            if value == '':
                toggle_value.write(b'ON')

            else:
                toggle_value.write(value.encode())

        with open('assets/metadata_settings/trt_value.dll', 'rb') as read:
            get_value = str(read.read().decode())

            self.ids.toggle.text = get_value

        # save the time format to a file
        with open('assets/metadata_settings/format_loader.dll', 'wb') as time_format:
            time_format.write(self.ids.time_format.text.encode())

    @staticmethod
    def toggle_reader():

        with open('assets/metadata_settings/trt_value.dll', 'rb') as read_toggle:
            reader = str(read_toggle.read().decode())

            return reader

    def time_format(self):

        with open('assets/metadata_settings/format_loader.dll', 'rb') as value_grabber:
            get_value = str(value_grabber.read().decode())

            self.ids.time_format.text = get_value

            return str(get_value)

    def user_name(self):

        with open('assets/metadata_settings/usr.dat', 'wb') as write_data:
            write_data.write(self.ids.user_name.text.encode())

    def user_return(self):
        with open('assets/metadata_settings/usr.dat', 'rb') as read_data:
            data = str(read_data.read().decode())

        return data

    # ################################### END OF TOGGLE ################################################

    def dark_slider_handler(self):
        get_value = str(self.ids.dark_slider.value)
        with open('assets/metadata_settings/darken.bin', 'wb') as write_dark:
            write_dark.write(get_value.encode()[0:2])

        with open('assets/metadata_settings/darken.bin', 'rb') as reader:
            self.ids.dark_label.text = str(reader.read().decode())

    @staticmethod
    def get_label():
        try:
            with open('assets/metadata_settings/darken.bin', 'rb') as reader:
                returner = str(reader.read().decode())
            return returner
        except FileNotFoundError:
            return '0'

    @staticmethod
    def value_grabber():
        with open('assets/metadata_settings/darken.bin', 'rb') as reader:
            return int(reader.read().decode())

    def dark_toggle(self):
        with open('assets/metadata_settings/lxdg1.dll', 'wb') as writer_data:
            get_value = self.ids.slider_toggle.text.encode()
            writer_data.write(get_value)

    @staticmethod
    def return_text_toggle():
        with open('assets/metadata_settings/lxdg1.dll', 'rb') as data_reader:
            reader = str(data_reader.read().decode())

        return reader

    # #################################### ACRYLIC BLUR EFFECT ############################## #
    def get_value(self):
        with open('assets/metadata_settings/ag_lightV.dll', 'wb') as writer_data:
            __get = self.ids.ac_blur.text.encode()
            writer_data.write(__get)

    def reader_data(self):
        try:
            with open('assets/metadata_settings/ag_lightv.dll', 'rb') as reader:
                read = str(reader.read().decode())
            return read
        except FileNotFoundError:
            with open('assets/metadata_settings/ag_lightv.dll', 'wb') as writer_data:
                writer_data.write(b'OFF')


class Reminders(Screen):
    def seconds(self, *args):
        from datetime import datetime

        time = datetime.now()

        seconds = time.strftime('%S')

        self.ids.seconds.hint_text = str(seconds)

        return seconds

    def minutes(self, *args):
        from datetime import datetime
        time = datetime.now()
        formatted = time.strftime('%M')

        self.ids.minutes.hint_text = str(formatted)
        Clock.schedule_interval(self.seconds, 1.0)
        return formatted

    def hour(self):
        with open('assets/metadata_settings/format_loader.dll', 'rb') as reader:
            read = str(reader.read().decode())
            from datetime import datetime
            time = datetime.now()
            Clock.schedule_interval(self.minutes, 1.0)
            if read == '12 hour':
                formatted = time.strftime('%I')

                return formatted
            else:
                formatted = time.strftime('%H')

                return formatted

    def reminder_time(self):
        """This function saves the reminders data into binary file"""
        with open('assets/metadata_settings/reminder_cache/time.bin', 'wb') as writer:
            hour = self.ids.hour.text
            current_hour = str(self.hour())
            with open('assets/metadata_settings/format_loader.dll', 'rb') as reader:
                read = str(reader.read().decode())
                if read == '24 hour':
                    if len(hour) == 1:
                        writer.write(b'0' + hour.encode() + b':')
                    elif len(hour) > 2 and hour > 24:
                        writer.write(b'23' + b':')
                    elif hour == '':
                        writer.write(current_hour.encode() + b':')
                    else:
                        writer.write(hour.encode() + b':')

                    # write the minutes
                    minutes = self.ids.minutes.text
                    current_min = str(self.minutes())

                    if len(minutes) == 1:
                        writer.write(b'0' + minutes.encode() + b':')

                    elif len(minutes) > 2 and minutes > 60:
                        writer.write(b'59' + b':')

                    elif minutes == '':
                        writer.write(current_min.encode() + b':')

                    else:
                        writer.write(minutes.encode() + b':')

                    # write the seconds
                    seconds = self.ids.seconds.text

                    if len(seconds) == 1:
                        writer.write(b'0' + seconds.encode())

                    elif len(seconds) > 2 and seconds > 60:
                        writer.write(b'59' + b':')

                    elif seconds == '':
                        writer.write(b'00' + b':')

                    else:
                        writer.write(seconds.encode())

                else:
                    from datetime import datetime

                    time = datetime.now()

                    am_pm = time.strftime('%p')

                    with open('assets/metadata_settings/reminder_cache/time.bin', 'wb') as writer:

                        hour = self.ids.hour.text

                        if len(hour) == 1:
                            writer.write(b'0' + hour.encode() + b':')
                        elif len(hour) > 2 and hour > 12:
                            writer.write(b'12' + b':')
                        elif hour == '':
                            writer.write(b'00' + b':')
                        else:
                            writer.write(hour.encode() + b':')

                        # write the minutes
                        minutes = self.ids.minutes.text

                        if len(minutes) == 1:
                            writer.write(b'0' + minutes.encode() + b':')

                        elif len(minutes) > 60 and minutes > 60:
                            writer.write(b'59' + b':')

                        elif minutes == '':
                            writer.write(b'00' + b':')
                        else:
                            writer.write(minutes.encode() + b':')

                        # seconds

                        seconds = self.ids.seconds.text

                        if len(seconds) == 1:
                            writer.write(b'0' + seconds.encode() + b':')

                        elif seconds == '':
                            writer.write(b'00' + b':')

                        elif len(seconds) > 60 and seconds > 60:
                            writer.write(b'59' + b':')

                        elif minutes == '':
                            writer.write(b'00' + b':')
                        else:
                            writer.write(minutes.encode() + b':')

                        # write the am or pm
                        writer.write(am_pm.encode())

    def remind_label(self):
        with open('assets/metadata_settings/reminder_cache/remind_label.bin', 'wb') as writer:
            grab_label = self.ids.what_to_do.text.encode()
            writer.write(grab_label)
        Clock.schedule_interval(self.start_reminder, 1.0)

    @staticmethod
    def start_reminder(*args):
        speech_engine = pyttsx3.init()
        import random
        with open('assets/metadata_settings/reminder_cache/time.bin', 'rb') as reader:
            read = str(reader.read().decode())

            # object of the main screen
            object_main = MainScreen()

            current_time_twelve = object_main.twelve_hour_format()

            current_time_twenty = object_main.twenty_four_format()

            if read == str(current_time_twelve):

                with open('assets/metadata_settings/reminder_cache/remind_label.bin', 'rb') as reader:

                    with open('assets/metadata_settings/usr.dat', 'rb') as read_data:
                        user_name = str(read_data.read().decode())

                        sliced_name = user_name

                    read = str(reader.read().decode())

                    engine_read_text = [f'{sliced_name} you reminded me that {read}',
                                        f'its time for your work {sliced_name} ']

                    speech_engine.say(random.choice(engine_read_text))

                    speech_engine.runAndWait()

            elif read == str(current_time_twenty):
                with open('assets/metadata_settings/reminder_cache/remind_label.bin', 'rb') as reader:

                    read = str(reader.read().decode())

                    speech_engine.say(read)

                    speech_engine.runAndWait()
            else:
                print('No event')


class Restart(Screen):
    @staticmethod
    def restart():
        import os
        os.system('start ./FluentClock.exe')
        Window.close()


gui = Builder.load_string(
    """WindowManager:
    #: import NoTransition kivy.uix.screenmanager.NoTransition
    transition: NoTransition()
    canvas:
        Rectangle:
            size: self.size
            pos: self.pos
            source: './assets/blur_window.png'
        Color:
            id: main_canvas_color
            rgba: root.color_manager()
        Rectangle:
            size: 10000, root.height/7
            pos: root.width/-10, root.height/1.04
        RoundedRectangle:
            size: root.width/3.32, root.height/1.06
            radius: [15,]
            pos: root.width/1000, root.height/150.9
        Color:
            rgba: root.main_toggle_effect()
        Rectangle:
            size: self.size
            pos:self.pos

    MainScreen:
    Alarm:
    NewAlarm:
    Alarm2:
    Alarm3:
    Alarm4:
    Alarm5:
    Alarm6:
    Timer:
    Stopwatch:
    SettingsScreen:
    Reminders:
    Restart:

<MainScreen>:
    name: 'clock'
    canvas:
        Color:
            rgba: 0,0,0,0.3
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/1.19
            radius: [20,]
        Color:
            rgba: 0,0,0,0.5
        RoundedRectangle:
            size: root.width/4.9, root.height/12
            pos: root.width/1.7, root.height/18.
            radius: [23,]
    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Label:
        id: clock
        size_hint: (None, None)
        pos: root.width/1.53,root.height/1.48
        size: root.width/30, root.height/40
        font_size: root.height/7
        bold: True
    Label:
        text: root.date()
        size_hint: (None, None)
        pos: root.width/1.49,root.height/1.73
        size: root.width/50, root.height/50
        font_size: root.height/39
        bold: True
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'
    Button:
        text: 'Add Reminder '
        size_hint: (None,None)
        size: root.width/4.9, root.height/12
        pos: root.width/1.65, root.height/18.
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'reminder'
    Button:
        text: '+'
        size_hint: (None,None)
        size: root.width/4.9, root.height/12
        pos: root.width/1.89, root.height/18.
        font_size: root.height/20
        background_color: 0,0,0,0
        on_press: app.root.current = 'reminder'

<Alarm>:
    name: 'alarms'
    canvas:
        Color:
            rgba: 0,0,0,0.3
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/1.38
            radius: [20,]
        RoundedRectangle:
            size: root.width/9.8, root.height/12
            pos: root.width/1.14, root.height/25.9
            radius: [20,]
        # alarms label 1
        RoundedRectangle:
            size: root.width/2.01, root.height/12
            pos: root.width/2.9, root.height/1.21
            radius: [23,]
        # alarms label 2
        RoundedRectangle:
            size: root.width/2.01, root.height/12
            pos: root.width/2.9, root.height/1.42
            radius: [23,]
        # alarms label 3
        RoundedRectangle:
            size: root.width/2.01, root.height/12
            pos: root.width/2.9, root.height/1.71
            radius: [23,]
        # alarms label 4
        RoundedRectangle:
            size: root.width/2.01, root.height/12
            pos: root.width/2.9, root.height/2.16
            radius: [23,]
        # alarms label 5
        RoundedRectangle:
            size: root.width/2.01, root.height/12
            pos: root.width/2.9, root.height/3
            radius: [23,]
        # alarms label 6
        RoundedRectangle:
            size: root.width/2.01, root.height/12
            pos: root.width/2.9, root.height/4.9
            radius: [23,]

    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Label:
        text: '+'
        size_hint: (None, None)
        pos: root.width/1.118, root.height/14.4
        background_color: 0,0,0,0
        size: root.width/50, root.height/30
        font_size: root.height/25
    Button:
        text: 'New'
        size_hint: (None, None)
        size: root.width/2.9, root.height/15
        pos: root.width/1.13, root.height/19.9
        size: root.width/10, root.height/13
        font_size: root.height/38
        background_color: 0,0,0,0
        on_release: app.root.current = 'set alarm'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'
    # label alarm 1
    Label:
        id: alarm1_label
        size_hint: (None, None)
        size: root.width/2.01, root.height/12
        pos: root.width/6.8, root.height/1.21
        text: root.labels()
        font_size: root.height/38
    # label alarm 2
    Label:
        id: alarm2_label
        size_hint: (None, None)
        size: root.width/2.01, root.height/12
        pos: root.width/6.8, root.height/1.42
        text: root.labels_alarm2()
        font_size: root.height/38
    # label alarm 3
    Label:
        id: alarm3_label
        size_hint: (None, None)
        size: root.width/2.01, root.height/12
        pos: root.width/6.8, root.height/1.71
        text: 'Alarm 3'
        font_size: root.height/38
    # label alarm 4
    Label:
        id: alarm4_label
        size_hint: (None, None)
        size: root.width/2.01, root.height/12
        pos: root.width/6.8, root.height/2.16
        text: 'Alarm 4'
        font_size: root.height/38
    # label alarm 5
    Label:
        id: alarm5_label
        size_hint: (None, None)
        size: root.width/2.01, root.height/12
        pos: root.width/6.8, root.height/3
        text: 'Alarm 5'
        font_size: root.height/38
    # label alarm 6
    Label:
        id: alarm6_label
        size_hint: (None, None)
        size: root.width/2.01, root.height/12
        pos: root.width/6.8, root.height/4.9
        text: 'Alarm 6'
        font_size: root.height/38
    # time label 1
    Label:
        id: alarm1_notifier
        size_hint: (None, None)
        size: root.width/2.01, root.height/12
        pos: root.width/1.9, root.height/1.21
        font_size: root.height/38
    # alarm 2 notifier
    Label:
        id: alarm2_notifier
        size_hint: (None, None)
        size: root.width/2.01, root.height/12
        pos: root.width/1.9, root.height/1.42
        font_size: root.height/38
    # pause alarm 1

    Button:
        id: pause_alarm1
        size_hint: (None, None)
        background_normal: 'assets/metadata_image/pause_alarm_fade.png'
        background_down: 'assets/metadata_image/pause_alarm_fade.png'
        pos: root.width/1.43, root.height/1.21
        size: root.width/20, root.height/12
        font_size: root.height/38
        on_press: root.stop()
    # pause alarm 2
    Button:
        id: pause_alarm2
        size_hint: (None, None)
        background_normal: 'assets/metadata_image/pause_alarm_fade.png'
        background_down: 'assets/metadata_image/pause_alarm_fade.png'
        pos: root.width/1.43, root.height/1.42
        size: root.width/20, root.height/12
        font_size: root.height/38
        on_press: root.stop()
    # pause alarm 3
    Button:
        id: pause_alarm3
        size_hint: (None, None)
        background_normal: 'assets/metadata_image/pause_alarm_fade.png'
        background_down: 'assets/metadata_image/pause_alarm_fade.png'
        pos: root.width/1.43,root.height/1.70
        size: root.width/20, root.height/12
        font_size: root.height/38
        on_press: root.stop()
    # pause alarm 4
    Button:
        id: pause_alarm4
        size_hint: (None, None)
        background_normal: 'assets/metadata_image/pause_alarm_fade.png'
        background_down: 'assets/metadata_image/pause_alarm_fade.png'
        pos: root.width/1.43, root.height/2.15
        size: root.width/20, root.height/12
        font_size: root.height/38
        on_press: root.stop()
    # pause alarm 5
    Button:
        id: pause_alarm5
        size_hint: (None, None)
        background_normal: 'assets/metadata_image/pause_alarm_fade.png'
        background_down: 'assets/metadata_image/pause_alarm_fade.png'
        pos: root.width/1.43, root.height/3.0
        size: root.width/20, root.height/12
        font_size: root.height/38
        on_press: root.stop()
    # pause alarm 6
    Button:
        id: pause_alarm6
        size_hint: (None, None)
        background_normal: 'assets/metadata_image/pause_alarm_fade.png'
        background_down: 'assets/metadata_image/pause_alarm_fade.png'
        pos: root.width/1.43, root.height/4.84
        size: root.width/20, root.height/12
        font_size: root.height/38
        on_press: root.stop()
    # toggle status alarm 1
    ToggleButton:
        id: toggle_alarm_1
        size_hint: (None, None)
        text: root.toggle_1_text()
        on_state:
            self.text = {'normal': 'Status : ON', 'down': 'Status : OFF'} [self.state]
            down: root.toggle_info()
        pos:root.width/2.1, root.height/1.21
        size: root.width/10, root.height/13
        background_color: 0,0,0,0
        font_size: root.height/39
        # toggle status alarm 2
    ToggleButton:
        id: toggle_alarm_2
        size_hint: (None, None)
        text: root.toggle_2_text()
        on_state:
            self.text = {'normal': 'Status : ON', 'down': 'Status : OFF'} [self.state]
            down: root.toggle_info()
        pos:root.width/2.1,root.height/1.42
        size: root.width/10, root.height/13
        background_color: 0,0,0,0
        font_size: root.height/39
        # toggle status alarm 3
    Button:
        id: alarm_2_edit
        size_hint: (None, None)
        text: 'Edit'
        font_size: root.height/39
        size: root.width/15, root.height/12
        pos: root.width/1.59, root.height/1.42
        background_color: 0,0,0,0
        on_press: app.root.current = 'alarm2'
    ToggleButton:
        id: toggle_alarm_3
        size_hint: (None, None)
        text: root.toggle_3_text()
        on_state:
            self.text = {'normal': 'Status : OFF', 'down': 'Status : ON'} [self.state]
            down: root.toggle_info()
        pos:root.width/2.1, root.height/1.70
        size: root.width/10, root.height/13
        background_color: 0,0,0,0
        font_size: root.height/39
    Button:
        id: alarm_3_edit
        size_hint: (None, None)
        text: 'Edit'
        font_size: root.height/39
        size: root.width/15, root.height/12
        pos: root.width/1.59, root.height/1.70
        background_color: 0,0,0,0
        on_press: app.root.current = 'alarm3'
        # toggle status alarm 4
    ToggleButton:
        id: toggle_alarm_4
        size_hint: (None, None)
        text: root.toggle_4_text()
        on_state:
            self.text = {'normal': 'Status : OFF', 'down': 'Status : ON'} [self.state]
            down: root.toggle_info()
        pos:root.width/2.1,root.height/2.15
        size: root.width/10, root.height/13
        background_color: 0,0,0,0
        font_size: root.height/39
    Button:
        id: alarm_4_edit
        size_hint: (None, None)
        text: 'Edit'
        font_size: root.height/39
        size: root.width/15, root.height/12
        pos: root.width/1.59, root.height/2.15
        background_color: 0,0,0,0
        on_press: app.root.current = 'alarm4'
        # toggle status alarm 5
    ToggleButton:
        id: toggle_alarm_5
        size_hint: (None, None)
        text: root.toggle_5_text()
        on_state:
            self.text = {'normal': 'Status : OFF', 'down': 'Status : ON'} [self.state]
            down: root.toggle_info()
        pos:root.width/2.1, root.height/3.0
        size: root.width/10, root.height/13
        background_color: 0,0,0,0
        font_size: root.height/39
    Button:
        id: alarm_5_edit
        size_hint: (None, None)
        text: 'Edit'
        font_size: root.height/39
        size: root.width/15, root.height/12
        pos: root.width/1.59, root.height/3.0
        background_color: 0,0,0,0
        on_press: app.root.current = 'alarm5'
        # toggle status alarm 6
    ToggleButton:
        id: toggle_alarm_6
        size_hint: (None, None)
        text: root.toggle_6_text()
        on_state:
            self.text = {'normal': 'Status : OFF', 'down': 'Status : ON'} [self.state]
            down: root.toggle_info()
        pos:root.width/2.1, root.height/4.84
        size: root.width/10, root.height/13
        background_color: 0,0,0,0
        font_size: root.height/39
    Button:
        id: alarm_6_edit
        size_hint: (None, None)
        text: 'Edit'
        font_size: root.height/39
        size: root.width/15, root.height/12
        pos: root.width/1.59, root.height/4.84
        background_color: 0,0,0,0
        on_press: app.root.current = 'alarm6'


<NewAlarm>:
    name: 'set alarm'
    canvas:
        Color:
            rgba: 0,0,0,0.3
        # selected menu
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/1.38
            radius: [20,]
        # toolbox
        RoundedRectangle:
            size: root.width/6.1, root.height/12
            pos: root.width/1.21, root.height/20.9
            radius: [20,]
        Color:
            rgba: 0,0,0,0.5
        # Name
        RoundedRectangle:
            size: root.width/4.9, root.height/12
            pos: root.width/2.9, root.height/1.89
            radius: [23,]
        RoundedRectangle:
            size: root.width/4.9, root.height/12
            pos: root.width/1.5, root.height/1.89
            radius: [23,]
    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Button:
        background_normal: 'assets/metadata_image/fluent_save.png'
        background_down:'assets/metadata_image/fluent_save.png'
        size_hint: (None, None)
        size: root.width/2.9, root.height/15
        pos: root.width/1.07, root.height/15.6
        size: 40, 40
        on_press: root.save_alarm()
        on_release: app.root.current = 'alarms'
    Button:
        id: back_button
        background_normal: 'assets/metadata_image/fluent_back.png'
        background_down:'assets/metadata_image/fluent_back.png'
        size_hint: (None, None)
        size: root.width/2.9, root.height/15
        pos: root.width/3.2, root.height/1.11
        size: 37, 37
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Save'
        size_hint: (None, None)
        size: root.width/2.9, root.height/15
        pos: root.width/1.15, root.height/16
        background_color: 0,0,0,0
        size: 60, 45
        font_size: root.height/31
        on_press: root.save_alarm()
        on_release: app.root.current = 'alarms'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'
    # hour
    TextInput:
        id: timer_hour
        size_hint: (None, None)
        pos: root.width/2.4,root.height/1.5
        size: root.width/7.99, root.height/4
        multiline: False
        hint_text: root.hour()
        focus: True
        font_size: root.height/5.5
        background_color: 0,0,0,0
        cursor_color: 0,0,0,0
        foreground_color: 1,1,1,1
        on_text_validate: root.alarm_time()
        on_text: root.alarm_time()
    Label:
        size_hint: (None, None)
        pos: root.width/1.76,root.height/1.25
        size: root.width/50.1, root.height/50
        text: ':'
        bold: True
        font_size: root.height/5
    # minute
    TextInput:
        id: timer_minute
        size_hint: (None, None)
        pos: root.width/1.64,root.height/1.5
        size: root.width/7.99, root.height/4
        multiline: False
        focus: True
        font_size: root.height/5.5
        background_color: 0,0,0,0
        cursor_color: 0,0,0,0
        foreground_color: 1,1,1,1
        on_text: root.alarm_time()
        on_text_validate: root.alarm_time()

    Label:
        size_hint: (None, None)
        pos: root.width/1.301,root.height/1.25
        size: root.width/50.1, root.height/50
        text: ':'
        bold: True
        font_size: root.height/5
    # seconds
    TextInput:
        id: timer_seconds
        size_hint: (None, None)
        pos: root.width/1.22,root.height/1.5
        size: root.width/7.99, root.height/4
        multiline: False
        focus: True
        font_size: root.height/5.5
        background_color: 0,0,0,0
        cursor_color: 0,0,0,0
        foreground_color: 1,1,1,1
        on_text_validate: root.alarm_time()
        on_text: root.alarm_time()
    TextInput:
        id: alarm_label
        size_hint: (None,None)
        pos: root.width/2.76, root.height/1.92
        size: root.width/6, root.height/13
        hint_text: 'Alarm Label'
        font_size: root.height/35
        multiline: False
        background_color: 0,0,0,0
        cursor_color: 0,0,0,0
        foreground_color: 1,1,1,1
    TextInput:
        id: alarm_sound
        size_hint: (None,None)
        pos: root.width/1.45, root.height/1.92
        size: root.width/6, root.height/13
        hint_text: 'Alarm Sound'
        text: 'flute1'
        on_text: root.save_alarm()
        font_size: root.height/35
        multiline: False
        background_color: 0,0,0,0
        cursor_color: 0,0,0,0
        foreground_color: 1,1,1,1


# timer GUI from here
<Timer>:
    name: 'timer'
    canvas:
        Color:
            rgba: 0,0,0,0.3
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/1.67
            radius: [20,]
    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'
    # timer label
    Label:
        id: timer_label
        pos: root.width/5.7,root.height/5.1
        font_size: root.height/7
        bold: True

    Label:
        id: notification
        font_size: root.height/35
        size_hint: (None, None)
        pos: root.width/1.29, root.height/1.199
    Label:
        text: 'This is a trial version of this program, [b]128 features have been removed by the developer.[/b]'
        size_hint: (None,None)
        size: root.height/20, root.width/12
        pos: root.width/1.5, root.height/2
        markup: True
        font_size: root.height/45
    Label:
        text: ' Contact or support us at LegendsAwaken4@gmail.com'
        size_hint: (None,None)
        size: root.height/20, root.width/12
        pos: root.width/1.5, root.height/2.4
        markup: True
        font_size: root.height/45

# stopwatch from here
<Stopwatch>:
    name: 'stopwatch'
    canvas:
        Color:
            rgba: 0,0,0,0.3
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/2.1
            radius: [20,]

    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'
    Label:
        text: 'This is a trial version of this program, [b]128 features have been removed by the developer.[/b]'
        size_hint: (None,None)
        size: root.height/20, root.width/12
        pos: root.width/1.5, root.height/2
        markup: True
        font_size: root.height/45
    Label:
        text: ' Contact or support us at LegendsAwaken4@gmail.com'
        size_hint: (None,None)
        size: root.height/20, root.width/12
        pos: root.width/1.5, root.height/2.4
        markup: True
        font_size: root.height/45
    

# this is settings window
<SettingsScreen>:
    name: 'settings'
    #: import rgba kivy.utils.get_color_from_hex
    canvas:
        Color:
            rgba: 0,0,0,0.3
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/2.86
            radius: [20,]
        Color:
            rgba: 0,0,0,0.5
        # transparency effect
        RoundedRectangle:
            size: root.width/4.9, root.height/12
            pos: root.width/2.9, root.height/1.21
            radius: [23,]
        # blur intensity
        RoundedRectangle:
            size: root.width/3.9, root.height/12
            pos: root.width/1.6, root.height/1.21
            radius: [23,]
        # save
        RoundedRectangle:
            size: root.width/7.5, root.height/12
            pos: root.width/1.18, root.height/20.9
            radius: [20,]
        # accent color
        RoundedRectangle:
            size: root.width/2.1, root.height/3
            pos: root.width/2.9, root.height/2.31
            radius: [20,]
        # time format
        RoundedRectangle:
            size: root.width/5.3, root.height/12
            pos: root.width/2.9, root.height/3.55
            radius: [23,]
        # ACRYLIC BLUR EFFECT
        RoundedRectangle:
            size: root.width/5.3, root.height/12
            pos: root.width/2.9, root.height/7.2
            radius: [23,]
        # usr_id
        RoundedRectangle:
            size: root.width/5.3, root.height/12
            pos: root.width/1.6, root.height/3.55
            radius: [23,]
    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'
    Label:
        text: 'Transparency Effect : '
        size_hint: (None, None)
        pos: root.width/2.63, root.height/1.25
        font_size: root.height/45
        size: root.width/11, root.height/7

    ToggleButton:
        id: toggle
        text: root.toggle_reader()
        on_state:
            self.text = {'normal': 'ON', 'down': 'OFF'} [self.state]
        size_hint: (None,None)
        pos: root.width/2.17, root.height/1.176
        size: root.width/11.2, root.height/25
        background_color: 0,0,0,0
        font_size: root.height/45
    Label:
        text: 'Blur Intensity : '
        size_hint: (None, None)
        pos: root.width/1.62, root.height/1.23
        font_size: root.height/45
        size: root.width/7, root.height/9
    Label:
        id: slider_value
        size_hint: (None, None)
        text: root.blur_text_return()
        pos: root.width/1.37, root.height/1.19
        font_size: root.height/45
        size: root.width/7, root.height/10
    Slider:
        id: blur_intensity
        min: 3
        max: 99
        value: root.slider_value()
        orientation: 'horizontal'
        size_hint: (None,None)
        pos: root.width/1.37, root.height/1.34
        size: root.width/6.8, root.height/4,
        on_value: root.blur_intensity()
    Button:
        id: save_button
        background_normal: 'assets/metadata_image/save60.png'
        background_down:'assets/metadata_image/save60.png'
        size_hint: (None, None)
        size: root.width/2.9, root.height/15
        pos: root.width/1.08, root.height/15.6
        size: root.width/30, root.height/19
        on_press: root.save_toggle_value()
        on_release: app.root.current = 'restart'
    Button:
        text: 'Save'
        size_hint: (None, None)
        size: root.width/2.9, root.height/15
        pos: root.width/1.143, root.height/13.4
        background_color: 0,0,0,0
        size: root.width/40, root.height/30
        bold: True
        font_size: root.height/28
        on_press: root.save_toggle_value()
        on_release: app.root.current = 'restart'
    Label:
        text: 'Accent Color'
        font_size: root.height/45
        size_hint: (None,None)
        pos: root.width/2.7, root.height/1.43
        size: root.width/10, root.height/14
    Label:
        size_hint: (None,None)
        size: root.width/40.1, root.height/30
        pos: root.width/2.5, root.height/1.77
        text: 'Dark Effect'
        font_size: root.height/45
    Label:
        id: dark_label
        text: root.get_label()
        size_hint: (None,None)
        size: root.width/40.1, root.height/30
        pos: root.width/2.13, root.height/1.9
        font_size: root.height/38
    Slider:
        id: dark_slider
        size_hint: (None,None)
        size: root.width/4.4, root.height/20
        pos: root.width/2.69, root.height/2.01
        max: 99
        min: 
        on_value: root.dark_slider_handler()
        value: root.value_grabber()
    ToggleButton:
        id: slider_toggle
        size_hint: (None,None)
        size:root.width/30, root.height/20
        background_color: 0,0,0,0
        text: root.return_text_toggle()
        font_size: root.height/45
        pos: root.width/1.6, root.height/2.01
        on_state:
            self.text = {'normal': 'ON', 'down': 'OFF'} [self.state]
            root.dark_toggle()
    # red
    Button:
        id: red
        size_hint: (None, None)
        pos: root.width/2.61, root.height/1.58
        background_color: 204,0,0,1
        size: root.width/30, root.height/20


    # green
    Button:
        size_hint: (None, None)
        pos: root.width/2.3, root.height/1.58
        background_color: 0,204,0,1
        size: root.width/30, root.height/20
        group: 'accentcolor'
    # yellow
    ToggleButton:
        size_hint: (None, None)
        pos: root.width/2.05, root.height/1.58
        background_color: 204,204,0,1
        size: root.width/30, root.height/20
        group: 'accentcolor'
    # pink
    ToggleButton:
        size_hint: (None, None)
        pos: root.width/1.85, root.height/1.58
        background_color: 204,51,255,1
        size: root.width/30, root.height/20
        group: 'accentcolor'
    # black
    ToggleButton:
        size_hint: (None, None)
        pos: root.width/1.69, root.height/1.58
        background_color: 0,0,0,1
        size: root.width/30, root.height/20
        group: 'accentcolor'
    # pure white
    ToggleButton:
        size_hint: (None, None)
        pos: root.width/1.55, root.height/1.58
        background_color: 1,1,1,1
        size: root.width/30, root.height/20
        group: 'accentcolor'
    # orange
    ToggleButton:
        size_hint: (None, None)
        pos: root.width/1.43, root.height/1.58
        background_color: 0,102,0,1
        size: root.width/30, root.height/20
        group: 'accentcolor'
    ToggleButton:
        size_hint: (None, None)
        pos: root.width/2.61, root.height/1.58
        background_color: 204,0,0,1
        size: root.width/30, root.height/20
        group: 'accentcolor'
    ToggleButton:
        size_hint: (None, None)
        pos: root.width/2.61, root.height/1.58
        background_color: 204,0,0,1
        size: root.width/30, root.height/20
        group: 'accentcolor'
    ToggleButton:
        id: time_format
        size_hint: (None, None)
        text: root.time_format()
        pos: root.width/2.17, root.height/3.44
        background_color: 0,0,0,0
        size: root.width/23, root.height/15
        on_state:
            self.text = {'normal': '24 hour', 'down': '12 hour'} [self.state]
        font_size: root.height/49
        italic: True
    Label:
        text: 'Time Format : '
        size_hint: (None, None)
        pos: root.width/2.78, root.height/3.9
        font_size: root.height/45
        size: root.width/11, root.height/7

    # user id
    TextInput:
        id: user_name
        hint_text: 'Your name'
        text: root.user_return()
        size_hint: (None, None)
        size: root.width/6.3, root.height/12
        pos: root.width/1.54, root.height/3.73
        multiline: False
        font_size: root.height/45
        background_color: 0,0,0,0
        foreground_color: 1,1,1,1
        on_text: root.user_name()

    # acrylic blur
    Label:
        text: 'Acrylic Blur : '
        size_hint: (None, None)
        font_size: root.height/45
        size: root.width/11, root.height/7
        pos: root.width/2.78, root.height/8.7
    ToggleButton:
        id: ac_blur
        text: root.reader_data()
        on_state:
            self.text = {'normal': 'ON', 'down': 'OFF'} [self.state]
            root.get_value()
        size_hint: (None, None)
        pos: root.width/2.22, root.height/6.58
        background_color: 0,0,0,0
        size: root.width/23, root.height/15
        font_size: root.height/49
        italic: True

# reminder screen
<Reminders>:
    name: 'reminder'
    canvas:
        Color:
            rgba: 0,0,0,0.4
        RoundedRectangle:
            size: root.width/4.01, root.height/12
            pos: root.width/2.9, root.height/1.7
            radius: [23,]
        # hour
        RoundedRectangle:
            size: root.width/8.5, root.height/12
            pos: root.width/2.9, root.height/1.36
            radius: [23,]
        # minutes
        RoundedRectangle:
            size: root.width/8.5, root.height/12
            pos: root.width/2.01, root.height/1.36
            radius: [23,]
        # seconds
        RoundedRectangle:
            size: root.width/8.5, root.height/12
            pos: root.width/1.54, root.height/1.36
            radius: [23,]
        # save
        RoundedRectangle:
            size: root.width/7.5, root.height/12
            pos: root.width/1.18, root.height/20.9
            radius: [20,]
    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'
    Label:
        text: 'Reminder'
        size_hint: (None, None)
        size: root.width/40, root.height/30
        pos: root.width/1.50, root.height/1.12
        font_size: root.height/15
        bold: True
    TextInput:
        id: what_to_do
        size_hint: (None, None)
        size: root.width/4.5, root.height/12
        pos: root.width/2.8, root.height/1.73
        hint_text: 'What to remind?'
        font_size: root.height/29
        background_color: 0,0,0,0
        foreground_color: 1,1,1,1
        multiline: False
    TextInput:
        id: hour
        size_hint: (None, None)
        size: root.width/17.5, root.height/12
        pos: root.width/2.7, root.height/1.37
        hint_text: root.hour()
        font_size: root.height/29
        background_color: 0,0,0,0
        foreground_color: 1,1,1,1
        multiline: False
        on_text: root.reminder_time()
        on_text_validate: root.reminder_time()
    TextInput:
        id: minutes
        size_hint: (None, None)
        size: root.width/18.5, root.height/12
        pos: root.width/1.91, root.height/1.37
        font_size: root.height/29
        background_color: 0,0,0,0
        foreground_color: 1,1,1,1
        multiline: False
        on_text: root.reminder_time()
        on_text_validate: root.reminder_time()
    TextInput:
        id: seconds
        size_hint: (None, None)
        size: root.width/18.5, root.height/12
        pos: root.width/1.48, root.height/1.37
        font_size: root.height/29
        background_color: 0,0,0,0
        foreground_color: 1,1,1,1
        multiline: False
        on_text: root.reminder_time()
        on_text_validate: root.reminder_time()
    Button:
        text: 'Save'
        size_hint: (None, None)
        size: root.width/2.9, root.height/15
        pos: root.width/1.143, root.height/13.4
        background_color: 0,0,0,0
        size: root.width/40, root.height/30
        bold: True
        font_size: root.height/28
        on_release: app.root.current = 'clock'
        on_press: root.remind_label()
    Button:
        id: save_button
        background_normal: 'assets/metadata_image/save60.png'
        background_down:'assets/metadata_image/save60.png'
        size_hint: (None, None)
        size: root.width/2.9, root.height/15
        pos: root.width/1.08, root.height/15.6
        size: root.width/30, root.height/19
        on_release: app.root.current = 'clock'
        on_press: root.remind_label()

<Restart>:
    name: 'restart'
    canvas:
        Color:
            rgba: 0,0,0,0.9
        Rectangle:
            size: self.size
            pos: self.pos
    Label:
        text: 'Restart the app to see the effects.'
        size_hint: (None,  None)
        size: root.width/1.8, root.height/15
        pos: root.width/4.5, root.height/1.5
        font_size: root.height/30
    Button:
        text: 'Accept'
        size_hint: (None,None)
        size: root.width/6.8, root.height/13
        pos: root.width/3.01, root.height/1.9
        font_size: root.height/34
        background_color: 0, 0, 0, 0
        on_press: root.restart()
    Button:
        text: 'Decline'
        size_hint: (None,None)
        size: root.width/6.8, root.height/13
        pos: root.width/2.01, root.height/1.9
        font_size: root.height/34
        background_color: 0, 0, 0, 0
        on_press: app.root.current = 'settings'

# ################################# Alarms  ############################## #
<Alarm2>:
    name: 'alarm2'
    canvas:
        Color:
            rgba: 0,0,0,0.3
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/1.38
            radius: [20,]
        Color:
            rgba: 0,0,0,0.3
        # selected menu
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/1.38
            radius: [20,]
        # toolbox
        RoundedRectangle:
            size: root.width/6.1, root.height/12
            pos: root.width/1.21, root.height/20.9
            radius: [20,]
        Color:
            rgba: 0,0,0,0.5
        # Name
        RoundedRectangle:
            size: root.width/4.9, root.height/12
            pos: root.width/2.9, root.height/1.89
            radius: [23,]
        RoundedRectangle:
            size: root.width/4.9, root.height/12
            pos: root.width/1.5, root.height/1.89
            radius: [23,]
    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'
    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Button:
        background_normal: 'assets/metadata_image/fluent_save.png'
        background_down:'assets/metadata_image/fluent_save.png'
        size_hint: (None, None)
        size: root.width/2.9, root.height/15
        pos: root.width/1.07, root.height/15.6
        size: 40, 40
        on_press: root.save_alarm()
        on_release: app.root.current = 'alarms'
    Button:
        id: back_button
        background_normal: 'assets/metadata_image/fluent_back.png'
        background_down:'assets/metadata_image/fluent_back.png'
        size_hint: (None, None)
        size: root.width/2.9, root.height/15
        pos: root.width/3.2, root.height/1.11
        size: 37, 37
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Save'
        size_hint: (None, None)
        size: root.width/2.9, root.height/15
        pos: root.width/1.15, root.height/16
        background_color: 0,0,0,0
        size: 60, 45
        font_size: root.height/31
        on_press: root.save_alarm()
        on_release: app.root.current = 'alarms'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'
    # hour
    TextInput:
        id: timer_hour
        size_hint: (None, None)
        pos: root.width/2.4,root.height/1.5
        size: root.width/7.99, root.height/4
        multiline: False
        hint_text: root.hour()
        focus: True
        font_size: root.height/5.5
        background_color: 0,0,0,0
        cursor_color: 0,0,0,0
        foreground_color: 1,1,1,1
        on_text_validate: root.alarm_time()
        on_text: root.alarm_time()
    Label:
        size_hint: (None, None)
        pos: root.width/1.76,root.height/1.25
        size: root.width/50.1, root.height/50
        text: ':'
        bold: True
        font_size: root.height/5
    # minute
    TextInput:
        id: timer_minute
        size_hint: (None, None)
        pos: root.width/1.64,root.height/1.5
        size: root.width/7.99, root.height/4
        multiline: False
        focus: True
        font_size: root.height/5.5
        background_color: 0,0,0,0
        cursor_color: 0,0,0,0
        foreground_color: 1,1,1,1
        on_text: root.alarm_time()
        on_text_validate: root.alarm_time()

    Label:
        size_hint: (None, None)
        pos: root.width/1.301,root.height/1.25
        size: root.width/50.1, root.height/50
        text: ':'
        bold: True
        font_size: root.height/5
    # seconds
    TextInput:
        id: timer_seconds
        size_hint: (None, None)
        pos: root.width/1.22,root.height/1.5
        size: root.width/7.99, root.height/4
        multiline: False
        focus: True
        font_size: root.height/5.5
        background_color: 0,0,0,0
        cursor_color: 0,0,0,0
        foreground_color: 1,1,1,1
        on_text_validate: root.alarm_time()
        on_text: root.alarm_time()
    TextInput:
        id: alarm_label
        size_hint: (None,None)
        pos: root.width/2.76, root.height/1.92
        size: root.width/6, root.height/13
        hint_text: 'Alarm Label'
        font_size: root.height/35
        multiline: False
        background_color: 0,0,0,0
        cursor_color: 0,0,0,0
        foreground_color: 1,1,1,1
    TextInput:
        id: alarm_sound
        size_hint: (None,None)
        pos: root.width/1.45, root.height/1.92
        size: root.width/6, root.height/13
        hint_text: 'Alarm Sound'
        text: 'flute1'
        on_text: root.save_alarm()
        font_size: root.height/35
        multiline: False
        background_color: 0,0,0,0
        cursor_color: 0,0,0,0
        foreground_color: 1,1,1,1


<Alarm3>:
    name: 'alarm3'
    canvas:
        Color:
            rgba: 0,0,0,0.3
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/1.38
            radius: [20,]

    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'


<Alarm4>:
    name: 'alarm4'
    canvas:
        Color:
            rgba: 0,0,0,0.3
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/1.38
            radius: [20,]

    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'


<Alarm5>:
    name: 'alarm5'
    canvas:
        Color:
            rgba: 0,0,0,0.3
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/1.38
            radius: [20,]

    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'


<Alarm6>:
    name: 'alarm6'
    canvas:
        Color:
            rgba: 0,0,0,0.3
        RoundedRectangle:
            size: root.width/3.8, root.height/12
            pos: root.width/110, root.height/1.38
            radius: [20,]

    Label:
        text: 'Alarms & Clock'
        size_hint: (None, None)
        font_size: root.height/51
        pos: root.width/30, root.height/1.078
        size: root.width/40, root.height/9
    Button:
        text: 'X'
        font_size: root.height/43
        size_hint: (None,None)
        pos: root.width/1.05, root.height/1.040
        background_color: 0,0,0,0
        size: 100, 40
        on_press: app.root.close()
    Button:
        text: 'Clock'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.19
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'clock'
    Button:
        text: 'Alarms'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.38
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'alarms'
    Button:
        text: 'Timer'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/1.67
        background_color: 0,0,0,0
        font_size: root.height/34
        on_press: app.root.current = 'timer'
    Button:
        text: 'Stopwatch'
        size_hint: (None, None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.1
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'stopwatch'
    Button:
        text: 'Preferences'
        size_hint: (None,None)
        size: root.width/3.8, root.height/13
        pos: root.width/110, root.height/2.86
        font_size: root.height/34
        background_color: 0,0,0,0
        on_press: app.root.current = 'settings'
""")


class BuildApp(App):

    def build(self):
        """This function runs the app"""
        return gui


BuildApp().run()
