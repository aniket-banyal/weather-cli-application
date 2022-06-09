import argparse
import os
from argparse import RawTextHelpFormatter
from dataclasses import dataclass

import models
from helpers import (get_date_input, get_formatted_date, get_hash,
                     get_str_formatted_for_table, print_cities,
                     print_forecast_data, print_horizontal_line,
                     print_text_in_horizontal_line)
from manager import Manager
from weather import (get_cities_from_name, get_forecast_for_date,
                     get_lat_long_from_city)

user_manager = Manager(models.User)
login_file = 'login.txt'


def save_login_info(user):
    with open(login_file, 'w') as file:
        file.write(str(user.id))


def get_logged_in_user():
    if not os.path.exists(login_file):
        return None

    with open(login_file, 'r') as file:
        try:
            id = int(file.readline())
        except ValueError:
            return None
        return user_manager.get(id)


def login():
    user = get_logged_in_user()
    if user is not None:
        print_text_in_horizontal_line(f'Logged in user -  {user.username}')
        return user

    print_text_in_horizontal_line('Login')

    users = user_manager.get_all()
    while True:
        username = input('Enter username: ')
        password = input('Enter password: ')

        for user in users:
            if user.username == username and user.password == get_hash(password):
                save_login_info(user)
                print_text_in_horizontal_line('Logged in successfully')
                return True
        print('Username or password is incorrect')


def login_required(func):
    def wrapper(*args, **kwargs):
        if login():
            func(*args, **kwargs)
    return wrapper


def create():
    while True:
        username = input('Enter username: ')
        username_exists = False

        users = user_manager.get_all()
        for user in users:
            if user.username == username:
                print('Username already exists')
                username_exists = True
                break
        if not username_exists:
            break

    password = input('Enter password: ')
    age = input('Enter age: ')

    user = user_manager.create(username=username, age=age, password=password)
    print_text_in_horizontal_line('User created successfuly')


@login_required
def get_users():
    print_text_in_horizontal_line('All users')

    for user in user_manager.get_all():
        print(user)
    print_horizontal_line()


@login_required
def logout(silently=False):
    if not silently:
        print_text_in_horizontal_line('Logging out')
    with open(login_file, 'w'):
        pass


@login_required
def update():
    print_text_in_horizontal_line('Update')

    user = get_logged_in_user()
    age = input('Enter age or leave blank to not update: ')
    password = input('Enter password or leave blank to not update: ')
    if age == '':
        age = None
    if password == '':
        password = None

    user.update(age=age, password=password)
    print()
    print(user)
    print()
    print_text_in_horizontal_line('User updated successfuly.')


@login_required
def delete():
    confirm = input('Are you sure you want to delete your account (y/n) ? ')
    if confirm == 'y':
        user = get_logged_in_user()
        logout(silently=True)
        user.delete()
        print_text_in_horizontal_line('User deleted successfuly')


@dataclass(frozen=True)
class City:
    lat: float
    lon: float
    name: str
    country: str
    state: str = ''

    def __repr__(self) -> str:
        state = self.state if self.state else '-'
        return get_str_formatted_for_table(self.name) + get_str_formatted_for_table(
            self.country) + get_str_formatted_for_table(state) + get_str_formatted_for_table(f'{self.lat:.3f}') + get_str_formatted_for_table(f'{self.lon:.3f}')


def get_lat_long_from_city_name():
    while True:
        city_name = input('Enter city: ')

        cities = [
            City(lat=city.get('lat'),
                 lon=city.get('lon'),
                 name=city.get('name'),
                 country=city.get('country'),
                 state=city.get('state', ''))
            for city in get_cities_from_name(city_name)
        ]

        if len(cities) == 0:
            print('Could not find any city with this name.')

        elif len(cities) == 1:
            city = cities[0]
            return get_lat_long_from_city(f"{city.name,city.state,city.country}")

        else:
            print(f'\nFound {len(cities)} cities with this name')
            print_cities(cities)

            while True:
                city_idx = int(input('Enter index of city: '))
                if city_idx >= 0 and city_idx < len(cities):
                    break

                print(f'Please enter a number b/w {0} and {len(cities) - 1}')

            city = cities[city_idx]
            return get_lat_long_from_city(f"{city.name,city.state,city.country}")


@login_required
def weather():
    date = get_date_input()

    valid_options = (0, 1)

    while True:
        try:
            option = int(input('Enter 0 to enter city and 1 to enter latitude and longitude: '))
        except ValueError:
            print(f'Please enter a number in {valid_options}')
            continue

        if option in valid_options:
            break

    if option == 0:
        lat, lon = get_lat_long_from_city_name()

    elif option == 1:
        lat = int(input('Enter latitute: '))
        lon = int(input('Enter longitute: '))

    forecast = get_forecast_for_date(lat, lon, date)

    if forecast:
        print_text_in_horizontal_line(f'Forecast for {get_formatted_date(date)}')
        print_forecast_data(forecast)
        print_horizontal_line()


if __name__ == '__main__':
    commands = {'create': create, 'login': login, 'logout': logout, 'update': update, 'delete': delete, 'users': get_users, 'weather': weather}

    command_description = {'create':  'create new user',
                           'login': 'login into the application',
                           'logout': 'logout from the application',
                           'update': 'update details of a user',
                           'delete': 'delete a user from database',
                           'users': 'get list of all users',
                           'weather': 'get weather forecast for a given location and date'
                           }

    help = '\n'.join([f'{key:<15} {value}' for key, value in command_description.items()])

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    parser.add_argument('command', type=str, help=help)

    args = parser.parse_args()

    action = commands.get(args.command, None)
    if action is None:
        print(f'{args.command} is not a valid command')
    else:
        action()
