# Модель: Стрільба по рухомій цілі
# Автор: Пасат Іван, група АІ-232

import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, atan, radians, degrees

import os

print("Student:", os.getenv("STUDENT_NAME"))
print("Group:", os.getenv("GROUP"))
print("Mode:", os.getenv("MODE"))


class MovingTargetCalculator:
    def __init__(self):
        self.results = {}

    def calculate_lead(self, target_speed, distance, bullet_speed, angle_degrees):
        """
        Розрахунок випередження для рухомої цілі
        """
        flight_time = distance / bullet_speed

        angle_rad = radians(angle_degrees)
        linear_lead = target_speed * flight_time * cos(angle_rad)

        angular_lead_mils = (linear_lead / distance) * 1000
        angular_lead_degrees = degrees(atan(linear_lead / distance))

        return {
            'flight_time': flight_time,
            'linear_lead': linear_lead,
            'angular_lead_mils': angular_lead_mils,
            'angular_lead_degrees': angular_lead_degrees
        }

    def simulate_trajectory(self, target_speed, distance, bullet_speed, angle_degrees, time_steps=100):
        flight_time = distance / bullet_speed
        t = np.linspace(0, flight_time * 1.2, time_steps)

        angle_rad = radians(angle_degrees)

        # Траєкторія цілі
        target_x = target_speed * t * cos(angle_rad)
        target_y = target_speed * t * sin(angle_rad)

        lead_info = self.calculate_lead(target_speed, distance, bullet_speed, angle_degrees)
        lead_angle = atan(lead_info['linear_lead'] / distance)

        bullet_x = bullet_speed * t * cos(lead_angle)
        bullet_y = bullet_speed * t * sin(lead_angle)

        return {
            'time': t,
            'target_x': target_x,
            'target_y': target_y,
            'bullet_x': bullet_x,
            'bullet_y': bullet_y,
            'impact_time': flight_time
        }

    def analyze_sensitivity(self, base_target_speed, base_distance, base_bullet_speed, base_angle):
        parameters = {
            'target_speed': np.linspace(base_target_speed * 0.5, base_target_speed * 1.5, 10),
            'distance': np.linspace(base_distance * 0.5, base_distance * 1.5, 10),
            'bullet_speed': np.linspace(base_bullet_speed * 0.8, base_bullet_speed * 1.2, 10),
            'angle': np.linspace(base_angle - 45, base_angle + 45, 10)
        }

        sensitivity = {}
        for param_name, param_values in parameters.items():
            leads = []
            for value in param_values:
                if param_name == 'target_speed':
                    result = self.calculate_lead(value, base_distance, base_bullet_speed, base_angle)
                elif param_name == 'distance':
                    result = self.calculate_lead(base_target_speed, value, base_bullet_speed, base_angle)
                elif param_name == 'bullet_speed':
                    result = self.calculate_lead(base_target_speed, base_distance, value, base_angle)
                else:
                    result = self.calculate_lead(base_target_speed, base_distance, base_bullet_speed, value)

                leads.append(result['linear_lead'])

            sensitivity[param_name] = (param_values, leads)

        return sensitivity


def main():
    calculator = MovingTargetCalculator()

    # Базові параметри
    target_speed = 5
    distance = 300
    bullet_speed = 900
    angle = 30

    print("=== РОЗРАХУНОК ВИПЕРЕДЖЕННЯ ДЛЯ РУХОМОЇ ЦІЛІ ===")
    print(f"Швидкість цілі: {target_speed} м/с")
    print(f"Відстань до цілі: {distance} м")
    print(f"Швидкість кулі: {bullet_speed} м/с")
    print(f"Кут руху цілі: {angle}°\n")

    result = calculator.calculate_lead(target_speed, distance, bullet_speed, angle)

    print("Результати:")
    print(f" Час польоту: {result['flight_time']:.3f} с")
    print(f" Лінійне випередження: {result['linear_lead']:.2f} м")
    print(f" Кутове випередження: {result['angular_lead_mils']:.1f} міл")
    print(f" Кутове випередження: {result['angular_lead_degrees']:.2f}°\n")

    trajectory = calculator.simulate_trajectory(target_speed, distance, bullet_speed, angle)

    # ---- Графіки ----
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

    ax1.plot(trajectory['target_x'], trajectory['target_y'], 'r-', label='Траєкторія цілі', linewidth=2)
    ax1.plot(trajectory['bullet_x'], trajectory['bullet_y'], 'b-', label='Траєкторія кулі', linewidth=2)
    ax1.set_title('Траєкторії руху цілі та кулі')
    ax1.set_xlabel('X (м)')
    ax1.set_ylabel('Y (м)')
    ax1.grid(True)
    ax1.legend()
    ax1.axis('equal')

    sensitivity = calculator.analyze_sensitivity(target_speed, distance, bullet_speed, angle)

    speeds, leads = sensitivity['target_speed']
    ax2.plot(speeds, leads, 'b-o')
    ax2.set_title('Чутливість до швидкості цілі')
    ax2.set_xlabel('Швидкість (м/с)')
    ax2.set_ylabel('Випередження (м)')
    ax2.grid(True)

    distances, leads = sensitivity['distance']
    ax3.plot(distances, leads, 'g-o')
    ax3.set_title('Чутливість до відстані')
    ax3.set_xlabel('Відстань (м)')
    ax3.set_ylabel('Випередження (м)')
    ax3.grid(True)

    angles, leads = sensitivity['angle']
    ax4.plot(angles, leads, 'r-o')
    ax4.set_title('Чутливість до кута')
    ax4.set_xlabel('Кут (°)')
    ax4.set_ylabel('Випередження (м)')
    ax4.grid(True)

    plt.tight_layout()
    plt.savefig("plot.png")
    print("Graph saved")

    print("\n=== ТАБЛИЦЯ РЕЗУЛЬТАТІВ ===")
    print("Швидк | Відст | Кут | Випередження | Час польоту")
    print("-" * 55)

    test_cases = [
        (3, 200, 0),
        (5, 300, 30),
        (7, 400, 45),
        (10, 500, 60),
        (2, 150, 90)
    ]

    for speed, dist, ang in test_cases:
        res = calculator.calculate_lead(speed, dist, bullet_speed, ang)
        print(f"{speed:6.1f} | {dist:6.0f} | {ang:3.0f} | {res['linear_lead']:12.2f} | {res['flight_time']:10.3f}")


if __name__ == "__main__":
    main()