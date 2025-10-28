import random
import time
import json
import platform
import os
import threading
import multiprocessing
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
                'memory_size(GB)': round(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024 ** 3), 2)
            }
            print(json.dumps(info, indent=4))
            time.sleep(20)

    def get_mission_computer_load(self):
        # psutil.cpu_percent(interval=1)은 1초 측정 후 평균치를 반환합니다.
        # 20초 주기를 유지하려면 이후 sleep을 19로 설정해 총 ~20초가 되게 합니다.
        while True:
            cpu_pct = psutil.cpu_percent(interval=1)         # 1초 측정
            mem_pct = psutil.virtual_memory().percent        # 현재 메모리 사용률
            load = {
                'cpu_usage(%)': round(cpu_pct, 2),
                'memory_usage(%)': round(mem_pct, 2)
            }
            print(json.dumps(load, indent=4))
            time.sleep(19)  # 위의 1초 측정 포함 총 ~20초 주기


def run_info():
    run_computer = MissionComputer()
    run_computer.get_mission_computer_info()


def run_load():
    run_computer = MissionComputer()
    run_computer.get_mission_computer_load()


def run_sensor():
    run_computer = MissionComputer()
    run_computer.get_sensor_data()


if __name__ == '__main__':
    # 멀티 스레드 실행 예시
    thread1 = threading.Thread(target=MissionComputer().get_mission_computer_info)
    thread2 = threading.Thread(target=MissionComputer().get_mission_computer_load)
    thread3 = threading.Thread(target=MissionComputer().get_sensor_data)

    thread1.start()
    thread2.start()
    thread3.start()

    # 멀티 프로세스 실행 예시
    process1 = multiprocessing.Process(target=run_info)
    process2 = multiprocessing.Process(target=run_load)
    process3 = multiprocessing.Process(target=run_sensor)

    process1.start()
    process2.start()
    process3.start()
