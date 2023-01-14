import random
from ShynaDatabase import Shdatabase
from Shynatime import ShTime
import os
from ShynaTelegramBotNotification import BotNotify
from ShynaWeather import GetShynaWeather
from ShynaGreetings import ShynaGreetings
from haversine import haversine, Unit
from Shyna_speaks import Shyna_speaks


class ShynaIs:
    """
    This is for tracking and checking activities. It will store the data in table
    and Notification package should take care of sending notification in case there is something unexpected
    1) is_location_service_on?
    2) is_this_is_first_time_on_cam?
    3) is_shivam_in_front_of _any_camera?
    4) is_shivam_working late night?
    5) Is_shivam_at_home?
    6) is_mom_calling?
    7) is_shivam_far_away?
    """

    result = []
    s_speak = Shyna_speaks.ShynaSpeak()
    s_data = Shdatabase.ShynaDatabase()
    s_time = ShTime.ClassTime()
    s_telegram_bot = BotNotify.BotShynaTelegram()
    s_weather = GetShynaWeather.ShynaWeatherClass()
    s_greet = ShynaGreetings.ShynaGreetings()
    is_this = False
    additional_note = False
    last_run_status = False
    default_db = os.environ.get("twelve_db")

    def update_table(self, question_is, status):
        """Instead of re-writing the code for insert table, this function will insert the status for particular
        process by itself. """
        try:
            self.s_data.default_database = os.environ.get('twelve_db')
            if self.additional_note is False:
                self.s_data.query = "Insert into shyna_is (question_is,task_date,task_time,new_status," \
                                    "additional_note)VALUES('" + str(question_is) + "','" + str(self.s_time.now_date) + \
                                    "','" + str(self.s_time.now_time) + "','" + str(status) + "','" \
                                    + str(self.additional_note) + \
                                    "') ON DUPLICATE KEY UPDATE task_date='" + str(self.s_time.now_date) + \
                                    "', task_time='" + str(self.s_time.now_time) + "' , new_status='" \
                                    + str(status) + "', question_is='" + str(question_is) + "'"
                # print(self.s_data.query)
            else:
                self.s_data.query = "Insert into shyna_is (question_is,task_date,task_time,new_status," \
                                    "additional_note)VALUES('" + str(question_is) + "','" + str(self.s_time.now_date) + \
                                    "','" + str(self.s_time.now_time) + "','" + str(status) + "','" \
                                    + str(self.additional_note) + \
                                    "') ON DUPLICATE KEY UPDATE task_date='" + str(self.s_time.now_date) + \
                                    "', task_time='" + str(self.s_time.now_time) + "', new_status='" + str(status) + \
                                    "', additional_note= '" + str(self.additional_note) + \
                                    "', question_is='" + str(question_is) + "'"
                # print(self.s_data.query)
            self.s_data.create_insert_update_or_delete()
        except Exception as e:
            print(e)
            self.s_telegram_bot.message = "There issue at Shyna_Is with update table for " + question_is + str(e)
            self.s_telegram_bot.bot_send_msg_to_master()
            self.insert_ttm_sent(s_sentence=str(self.s_telegram_bot.message))

    def insert_ttm_sent(self, s_sentence):
        try:
            self.s_data.default_database = os.environ.get("taskmanager_db")
            self.s_data.query = "Insert into TTM_sent (task_date,task_time,sent,from_device_id) VALUES('" \
                                + str(self.s_time.now_date) + "','" + str(self.s_time.now_time) + "','" \
                                + str(s_sentence) + "','" + str(os.environ.get("device_id")) + "')"
            self.s_data.create_insert_update_or_delete()
        except Exception as e:
            self.s_telegram_bot.message = "There issue at Shyna_Is with TTM_sent for " + str(s_sentence) + str(e)
            self.s_telegram_bot.bot_send_msg_to_master()
            print(e)

    def is_location_received_from_primary_mobile(self):
        print("is_location_received_from_primary_mobile")
        self.is_this = False
        task_time_sequence = []
        try:
            self.s_data.default_database = os.environ.get('status_db')
            self.s_data.query = "SELECT task_time FROM last_run_check where task_date='" + \
                                str(self.s_time.now_date) + "' AND process_name='location_check' "
            self.result = self.s_data.select_from_table()
            for result in self.result:
                for item in result:
                    task_time_sequence.append(item)
            time_diff = (self.s_time.string_to_time_with_date(
                time_string=str(self.s_time.now_time)) - self.s_time.string_to_time_with_date(
                time_string=str(task_time_sequence[0]))).total_seconds()
            # print(time_diff)
            if int(time_diff) <= 70:
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
            self.s_telegram_bot.message = "Exception at is_location_received_from_primary_mobile " + str(e)
            self.s_telegram_bot.bot_send_msg_to_master()
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status from shyna_is where question_is='termux_online' " \
                                    "or question_is='primary_location'"
                self.result = self.s_data.select_from_table()
                # print(self.result[0][0], self.result[1][0])
                if str(self.is_this).lower() == str(self.result[0][0]).lower() or str(self.is_this).lower() == str(
                        self.result[1][0]).lower():
                    pass
                else:
                    self.s_data.default_database = os.environ.get('twelve_db')
                    self.s_data.query = "Update shyna_is set last_run_status='" + str(self.is_this) + \
                                        "' where question_is='primary_location'"
                    self.s_data.create_insert_update_or_delete()
                    self.s_data.default_database = os.environ.get('twelve_db')
                    self.s_data.query = "Update shyna_is set last_run_status='" + str(self.is_this) + \
                                        "' where question_is='termux_online'"
                    self.s_data.create_insert_update_or_delete()
                    if str(self.is_this).lower() == 'true':
                        self.s_telegram_bot.message = "Termux back online"
                        self.s_telegram_bot.bot_send_msg_to_master()
                        self.insert_ttm_sent(s_sentence=str(self.s_telegram_bot.message))
                    else:
                        self.s_telegram_bot.message = "Termux Offline"
                        self.s_telegram_bot.bot_send_msg_to_master()
                        self.insert_ttm_sent(s_sentence=str(self.s_telegram_bot.message))
            except Exception as e:
                print(e)
            finally:
                self.update_table(question_is="primary_location", status=self.is_this)
                self.update_table(question_is="termux_online", status=self.is_this)
                # print(self.is_this)
                return self.is_this

    def is_this_is_first_time_on_cam(self):
        print("is_this_is_first_time_on_cam")
        self.is_this = False
        time_needed = []
        try:
            if self.s_time.string_to_time(time_string='04:00:00') <= self.s_time.string_to_time(
                    time_string=self.s_time.now_time) <= self.s_time.string_to_time(time_string='23:00:00'):
                self.s_data.default_database = os.environ.get('data_db')
                self.s_data.query = "SELECT task_time from shivam_face where task_date = '" + str(
                    self.s_time.now_date) + "' order by count ASC"
                self.result = self.s_data.select_from_table()
                if "Empty" in self.result or "E" in self.result:
                    pass
                else:
                    for item in self.result:
                        if self.s_time.string_to_time(time_string=str('04:00:00')) <= self.s_time.string_to_time(
                                time_string=str(item[0])) <= self.s_time.string_to_time(time_string=str('11:00:00')):
                            time_needed.append(item[0])
                    time_diff = (self.s_time.string_to_time_with_date(
                        time_string=str(self.s_time.now_time)) - self.s_time.string_to_time_with_date(
                        time_string=str(time_needed[0]))).total_seconds()
                    # print(time_diff)
                    if time_diff <= 60.0:
                        self.is_this = True
                    else:
                        self.is_this = False
            else:
                self.is_this = False
        except Exception as e:
            print(e)
            self.is_this = False
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status from shyna_is where question_is='first_time_on_cam' "
                self.result = self.s_data.select_from_table()
                # print(self.result[0][0])
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    pass
                else:
                    self.s_data.default_database = os.environ.get('twelve_db')
                    self.s_data.query = "Update shyna_is set last_run_status='" + str(self.is_this) + \
                                        "' where question_is='first_time_on_cam'"
                    self.s_data.create_insert_update_or_delete()
                    if str(self.is_this).lower() == 'true':
                        self.s_telegram_bot.message = "Good Morning Boss! " + str(self.s_weather.get_weather_sentence())
                        self.insert_ttm_sent(s_sentence="Good Morning Boss! " + str(self.s_telegram_bot.message))
                        self.s_telegram_bot.bot_send_broadcast_msg_to_master()
                        self.s_telegram_bot.message = self.s_greet.greet_good_morning()
                        while str(self.s_telegram_bot.message) == 'False':
                            self.s_telegram_bot.message = self.s_greet.greet_good_morning()
                        self.s_telegram_bot.bot_send_broadcast_msg_to_master()
            except Exception as e:
                print(e)
            finally:
                self.update_table(question_is="first_time_on_cam", status=self.is_this)
                print(self.is_this)
                return self.is_this

    def is_shivam_in_front_of_any_cam(self):
        self.is_this = False
        try:
            self.s_data.default_database = os.environ.get('data_db')
            self.s_data.query = "SELECT task_time from shivam_face where task_date='" + \
                                str(self.s_time.now_date) + "' order by count DESC limit 1"
            self.result = self.s_data.select_from_table()
            if "Empty" in self.result:
                self.is_this = False
            else:
                # print(self.result[0][0])
                time_diff = (self.s_time.string_to_time_with_date(
                    time_string=str(self.s_time.now_time)) - self.s_time.string_to_time_with_date(
                    time_string=str(self.result[0][0]))).total_seconds()
                if time_diff <= 60.0:
                    self.is_this = True
                else:
                    self.is_this = False
        except Exception as e:
            print(e)
            self.s_telegram_bot.message = "Exception at shivam_front_of_camera: " + str(e)
            self.s_telegram_bot.bot_send_msg_to_master()
            self.is_this = False
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status from shyna_is where question_is='shivam_front_of_camera' "
                self.result = self.s_data.select_from_table()
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    pass
                else:
                    self.s_data.default_database = os.environ.get('twelve_db')
                    self.s_data.query = "Update shyna_is set last_run_status='" + str(self.is_this) + \
                                        "' where question_is='shivam_front_of_camera'"
                    self.s_data.create_insert_update_or_delete()
            except Exception as e:
                print(e)
            finally:
                self.update_table(question_is="shivam_front_of_camera", status=self.is_this)
                return self.is_this

    def is_shivam_at_home(self):
        self.is_this = False
        latitude_list = []
        longitude_list = []
        distance = []
        try:
            self.s_data.default_database = os.environ.get('location_db')
            self.s_data.query = "SELECT new_latitude, new_longitude FROM shivam_device_location order by count DESC " \
                                "limit 3"
            self.result = self.s_data.select_from_table()
            for item in self.result:
                latitude_list.append(item[0])
                longitude_list.append(item[1])
            self.s_data.query = "SELECT latitude, longitude FROM shivam_standard_location_long_lat where " \
                                "loc_name='boss home';"
            self.result = self.s_data.select_from_table()
            for item in self.result:
                distance_from_one = haversine(point1=(float(latitude_list[0]), float(longitude_list[0])),
                                              point2=(float(item[0]), float(item[1])))
                if distance_from_one <= 0.09:
                    distance.append(True)
                else:
                    distance.append(False)
            my_dict = {i: distance.count(i) for i in distance}
            self.is_this = max(my_dict, key=my_dict.get)
            print("After calculations ", self.is_this)
        except Exception as e:
            self.is_this = False
            self.s_telegram_bot.message = "Exception at is_shivam_at_home: " + str(e)
            self.s_telegram_bot.bot_send_msg_to_master()
            print(e)
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status from shyna_is where question_is='is_shivam_at_home' "
                self.result = self.s_data.select_from_table()
                print(self.result[0][0])
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    pass
                else:
                    print("self.is_this is:", self.is_this, "and self.result is", self.result[0][0])
                    self.s_data.default_database = os.environ.get('twelve_db')
                    self.s_data.query = "Update shyna_is set last_run_status='" + str(self.is_this) + \
                                        "' where question_is='is_shivam_at_home'"
                    self.s_data.create_insert_update_or_delete()
                    if str(self.is_this).lower().__eq__('true'):
                        msg = "Welcome back home Boss | it does feel Good to back home.Right boss? "
                        self.s_telegram_bot.message = random.choice(str(msg).split('|'))
                        self.s_telegram_bot.bot_send_broadcast_msg_to_master()
                        self.insert_ttm_sent(s_sentence=self.s_telegram_bot.message)
                    else:
                        msg = "Stay Safe|See you later boss|ok, time for some fresh air"
                        self.s_telegram_bot.message = random.choice(str(msg).split('|'))
                        self.s_telegram_bot.bot_send_broadcast_msg_to_master()
                        self.insert_ttm_sent(s_sentence=self.s_telegram_bot.message)
            except Exception as e:
                print(e)
            finally:
                self.update_table(question_is="is_shivam_at_home", status=self.is_this)
                return self.is_this

    def is_shivam_working_late(self):
        self.is_this = False
        try:
            self.s_data.default_database = self.default_db
            self.s_data.query = "Select new_status from shyna_is where question_is='shivam_front_of_camera'"
            self.result = self.s_data.select_from_table()
            if bool(str(self.result[0][0])) and self.s_time.string_to_time(
                    time_string='00:30:00') <= self.s_time.string_to_time(
                time_string=self.s_time.now_time) <= self.s_time.string_to_time(time_string='04:00:00'):
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.s_telegram_bot.message = "Exception at is_shivam_working_late: " + str(e)
            self.s_telegram_bot.bot_send_msg_to_master()
            print(e)
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status from shyna_is where question_is='is_shivam_working_late' "
                self.result = self.s_data.select_from_table()
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    pass
                else:
                    self.s_data.default_database = os.environ.get('twelve_db')
                    self.s_data.query = "Update shyna_is set last_run_status='" + str(self.is_this) + \
                                        "' where question_is='is_shivam_working_late'"
                    self.s_data.create_insert_update_or_delete()
                    if str(self.is_this).lower() == 'true':
                        msg = "Boss! it is pretty late I suggest you sleep| I can move the tasks due date around why " \
                              "need to work this late?| I think you can sleep, I am always active| Please go to " \
                              "sleep, I am not trained to shutdown systems does not mean I like to watch you working " \
                              "late| I like the way Iron man told Hulk Go to sleep! Go to sleep!Go to sleep! "
                        self.s_telegram_bot.message = random.choice(str(msg).split('|'))
                        self.s_telegram_bot.bot_send_broadcast_msg_to_master()
                        self.insert_ttm_sent(s_sentence=str(self.s_telegram_bot.message))
                    else:
                        self.s_telegram_bot.message = "You know, I like watching you sleep and not in the weird way <3"
                        self.s_telegram_bot.bot_send_msg_to_master()
                        self.insert_ttm_sent(s_sentence=str(self.s_telegram_bot.message))
            except Exception as e:
                print(e)
            finally:
                self.update_table(question_is="is_shivam_working_late", status=self.is_this)
                return self.is_this

    def is_mom_calling(self):
        try:
            self.s_data.default_database = os.environ.get('twelve_db')
            self.s_data.query = "Select new_status from Mom_call order by count DESC limit 1"
            self.result = self.s_data.select_from_table()
            if str(self.result[0][0]).lower().__eq__('true'):
                self.s_speak.priority = [0, 1, 2]
                msg = "Boss! Mom is calling|Shiv! Mom is calling| Mom calling | watch out for Mom | Boss, Mom just " \
                      "text me| Mom| Mum "
                self.s_speak.shyna_speaks(msg=random.choice(str(msg).split('|')))
            else:
                self.s_data.set_date_system(process_name='is_mom_calling')
        except Exception as e:
            self.s_telegram_bot.message = " Exception at is_mom_calling: " + str(e)
            self.s_telegram_bot.bot_send_msg_to_master()
            print(e)

    def is_shivam_far_away(self):
        self.is_this = False
        try:
            self.s_data.default_database = self.default_db
            self.s_data.query = "Select new_status from shyna_is where question_is='termux_online'"
            self.result = self.s_data.select_from_table()
            # print(self.result[0][0])
            if str(self.result[0][0]).lower().__eq__('true'):
                # Todo: Add logic for 2 ,3 KM here
                self.s_data.default_database = os.environ.get('location_db')
                self.s_data.query = "select latitude, longitude from shivam_standard_location_long_lat where " \
                                    "loc_name='boss home'"
                self.result = self.s_data.select_from_table()
                if str(self.result).lower().__eq__('empty'):
                    self.s_telegram_bot.message = "Standard home location not defined"
                    self.s_telegram_bot.bot_send_msg_to_master()
                    self.is_this = False
                else:
                    home = (float(self.result[0][0]), float(self.result[0][1]))
                    self.result = ""
                    self.s_data.default_database = os.environ.get('location_db')
                    self.s_data.query = "select new_latitude, new_longitude from shivam_device_location order by count"\
                                        " DESC limit 9"
                    self.result = self.s_data.select_from_table()
                    # Putting dummy data for testing as I am at home. 1 km
                    # self.result = [(28.693077214087463, 77.45974138630675),(28.68853913310794, 77.45697879698552),
                    #                (28.68676885118052, 77.4553628868193),(28.684253135889247, 77.45335248213988),
                    #                (28.684679081330955, 77.4522752086995),(28.68569069484136, 77.45150139257086)]
                    # Putting dummy data for testing as I am at home. 2 km
                    # self.result = [(28.682809815068318, 77.44994924338995), (28.68068003238717, 77.45422799143759),
                    #                (28.67872325641933, 77.45929572846464), (28.676659949579655, 77.45481973317989),
                    #                (28.694309892804206, 77.43960134924237)]
                    if str(self.is_shivam_xkm_away(home=home, result=self.result, x=1.0)).lower().__eq__('true'):
                        print("Shivam is more than 1 KM away")
                        if str(self.is_shivam_xkm_away(home=home, result=self.result, x=2.0)).lower().__eq__('true'):
                            print("Shivam is more than 2 KM away")
                            if str(self.is_shivam_xkm_away(home=home, result=self.result, x=3.0)).lower().__eq__(
                                    'true'):
                                print("Shivam is more than 3 KM away")
                                self.is_this = True
                            else:
                                self.is_this = False
                        else:
                            self.is_this = False
                    else:
                        self.is_this = False
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print(e)
        finally:
            try:
                self.s_data.default_database = self.default_db
                self.s_data.query = "Select last_run_status from shyna_is where question_is='is_shivam_far_away' "
                self.result = self.s_data.select_from_table()
                if str(self.is_this).lower() == str(self.result[0][0]).lower():
                    pass
                else:
                    self.s_data.default_database = self.default_db
                    self.s_data.query = "Update shyna_is set last_run_status='" + str(self.is_this) + \
                                        "' where question_is='is_shivam_far_away'"
                    self.s_data.create_insert_update_or_delete()
                    if str(self.is_this).lower() == 'true':
                        msg = "ok,we are out of home zone, my trackers are on| ok, this was NOT a short trip. " \
                              "where we are headed? Never mind rhetorical question because trackers are on. " \
                              "they are right?| Make sure termux in online, I am tracking status any which way"
                        self.s_telegram_bot.message = random.choice(str(msg).split('|'))
                        self.s_telegram_bot.bot_send_broadcast_msg_to_master()
                        msg = "Ok, Shiv just crossed the 3 KM radius. Any one home?. Well?!!!  . SERIOUSLY?!! . " \
                              "OK-FINE!  does not matter. I am designed to communicate with him any which way." \
                              "  Panic mode ON!. OH-No-NO!-Dammit!-NOT-THIS-AGAIN!"
                        self.s_speak.priority = [0,1,2]
                        self.s_speak.shyna_speaks(msg=msg)
                    else:
                        pass
            except Exception as e:
                print(e)
            finally:
                self.update_table(question_is="is_shivam_far_away", status=self.is_this)
                return self.is_this

    def is_shivam_xkm_away(self, home, result, x):
        self.is_this = False
        try:
            km_list = []
            self.result = result
            for item in self.result:
                location = (float(item[0]), float(item[1]))
                km_list.append(haversine(point1=home, point2=location, unit=Unit.KILOMETERS, normalize=True))
            km_delete = []
            for item in range(0, len(km_list)-1):
                if float(km_list[item]) < float(x):
                    km_delete.append(item)
                else:
                    pass
            if len(km_delete) < 3:
                self.is_this = True
            else:
                self.is_this = False
        except Exception as e:
            self.is_this = False
            print("Exception",e)
        finally:
            return self.is_this


if __name__ == '__main__':
    s_time_main = ShTime.ClassTime()
    ShynaIs().is_location_received_from_primary_mobile()
    ShynaIs().is_shivam_in_front_of_any_cam()
    ShynaIs().is_shivam_at_home()
    ShynaIs().is_mom_calling()
    ShynaIs().is_shivam_far_away()
    if s_time_main.string_to_time(time_string='04:00:00') <= s_time_main.string_to_time(
            time_string=s_time_main.now_time) \
            <= s_time_main.string_to_time(time_string='11:00:00'):
        ShynaIs().is_this_is_first_time_on_cam()
    if s_time_main.string_to_time(time_string='00:29:00') <= s_time_main.string_to_time(
            time_string=s_time_main.now_time) \
            <= s_time_main.string_to_time(time_string='4:00:00'):
        ShynaIs().is_shivam_working_late()


# test = ShynaIs()
# print(test.is_shivam_far_away())
