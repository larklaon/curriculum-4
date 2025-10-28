import json
import multiprocessing
import os
import platform
import random
import threading
import time

import psutil  # 외부 라이브러리


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        return self.env_values


class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.sensor = DummySensor()

    def get_sensor_data(self):
        while True:
            self.sensor.set_env()
            self.env_values = self.sensor.get_env()
            print(json.dumps(self.env_values, indent=4))
            time.sleep(5)

    def get_mission_computer_info(self):
        while True:
            info = {
                'os': platform.system(),
                'os_version': platform.version(),
                'cpu_type': platform.processor(),
                'cpu_core_count': os.cpu_count(),
                'memory_size(GB)': round(
                    os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024 ** 3), 2
                )
            }
            print(json.dumps(info, indent=4))
            time.sleep(20)

    def get_mission_computer_load(self):
        while True:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            load = {
                'cpu_usage(%)': round(cpu, 2),
                'memory_usage(%)': round(mem, 2)
            }
            print(json.dumps(load, indent=4))
            time.sleep(19)


def run_info(instance):
    instance.get_mission_computer_info()


def run_load(instance):
    instance.get_mission_computer_load()


def run_sensor(instance):
    instance.get_sensor_data()


def run_threads():
    run_computer = MissionComputer()

    t_info = threading.Thread(target=run_computer.get_mission_computer_info)
    t_load = threading.Thread(target=run_computer.get_mission_computer_load)
    t_sensor = threading.Thread(target=run_computer.get_sensor_data)

    t_info.start()
    t_load.start()
    t_sensor.start()

    t_info.join()
    t_load.join()
    t_sensor.join()


def run_processes():
    run_computer1 = MissionComputer()
    run_computer2 = MissionComputer()
    run_computer3 = MissionComputer()

    p_info = multiprocessing.Process(target=run_info, args=(run_computer1,))
    p_load = multiprocessing.Process(target=run_load, args=(run_computer2,))
    p_sensor = multiprocessing.Process(target=run_sensor, args=(run_computer3,))

    p_info.start()
    p_load.start()
    p_sensor.start()

    p_info.join()
    p_load.join()
    p_sensor.join()


def main():
    print('실행 모드를 선택하세요:')
    print('1: 멀티 스레드')
    print('2: 멀티 프로세스')
    choice = input('선택 (1/2): ').strip()

    if choice == '1':
        run_threads()
    elif choice == '2':
        run_processes()
    else:
        print('잘못된 입력입니다. 기본값(멀티 스레드)으로 실행합니다.')
        run_threads()


if __name__ == '__main__':
    main()
