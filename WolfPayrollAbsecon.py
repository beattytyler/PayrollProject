import tkinter as tk
from datetime import datetime, timedelta
import os

class PayrollCalendar:
    def __init__(self, start_date, pay_period_length=14):
        try:
            self.start_date = start_date
            self.pay_period_length = pay_period_length
            self.payroll = {}
            self.current_period_start, self.current_period_end = self.calculate_current_pay_period()
            self.initialize_employees()
        except Exception as e:
            print(f"Error initializing PayrollCalendar: {e}")

    def calculate_current_pay_period(self):
        try:
            today = datetime.today()
            days_since_start = (today - self.start_date).days
            current_period_start = self.start_date + timedelta(days=(days_since_start // self.pay_period_length) * self.pay_period_length)
            current_period_end = current_period_start + timedelta(days=self.pay_period_length - 1)
            return current_period_start, current_period_end
        except Exception as e:
            print(f"Error calculating current pay period: {e}")

    def update_pay_period(self, direction='next'):
        try:
            if direction == 'next':
                today = datetime.today()
                if today > self.current_period_end:
                    self.current_period_start, self.current_period_end = self.calculate_current_pay_period()
            elif direction == 'previous':
                self.current_period_start = self.current_period_start - timedelta(days=self.pay_period_length)
                self.current_period_end = self.current_period_end - timedelta(days=self.pay_period_length)
        except Exception as e:
            print(f"Error updating pay period: {e}")

    def current_pay_period(self):
        try:
            return self.current_period_start, self.current_period_end
        except Exception as e:
            print(f"Error getting current pay period: {e}")
    
    def add_hours(self, employee_id, date, hours):
        try:
            if employee_id not in self.payroll:
                self.payroll[employee_id] = {}
            if date not in self.payroll[employee_id]:
                self.payroll[employee_id][date] = 0
            self.payroll[employee_id][date] += hours
        except Exception as e:
            print(f"Error adding hours: {e}")
    
    def add_extra_hours(self, employee_id, date, hours):
        try:
            self.add_hours(employee_id, date, hours)
        except Exception as e:
            print(f"Error adding extra hours: {e}")
        
    def remove_hours(self, employee_id, date, hours):
        try:
            if employee_id in self.employees:
                work_schedule = self.employees[employee_id]['work_schedule']
                added_hours = self.payroll.get(employee_id, {}).get(date, 0)
                
                if added_hours >= hours:
                    self.payroll[employee_id][date] -= hours
                    if self.payroll[employee_id][date] <= 0:
                        del self.payroll[employee_id][date]
                else:
                    remaining_hours = hours - added_hours
                    if added_hours > 0:
                        self.payroll[employee_id][date] = 0
                        del self.payroll[employee_id][date]
                
                if date in work_schedule:
                    current_hours = work_schedule[date]
                    if current_hours >= remaining_hours:
                        work_schedule[date] -= remaining_hours
                        if work_schedule[date] <= 0:
                            del work_schedule[date]
                    else:
                        print(f"Cannot remove {hours} hours. Only {current_hours + added_hours} hours available for {date}.")
                else:
                    print(f"No preset hours found for {date}.")
        except Exception as e:
            print(f"Error removing hours: {e}")

    def switch_shifts(self, employee_id_1, employee_id_2, date_1, date_2):
        try:
            if employee_id_1 in self.employees and employee_id_2 in self.employees:
                work_schedule_1 = self.employees[employee_id_1]['work_schedule']
                work_schedule_2 = self.employees[employee_id_2]['work_schedule']
                
                hours_1 = work_schedule_1.get(date_1, 0)
                hours_2 = work_schedule_2.get(date_2, 0)
                
                if hours_1 > 0 and hours_2 > 0:
                    self.remove_hours(employee_id_1, date_1, hours_1)
                    self.add_hours(employee_id_1, date_2, hours_2)
                    
                    self.remove_hours(employee_id_2, date_2, hours_2)
                    self.add_hours(employee_id_2, date_1, hours_1)
                    
                    print(f"Transferred {hours_1} hours from {employee_id_1} to {employee_id_2} and {hours_2} hours from {employee_id_2} to {employee_id_1}.")
                else:
                    print(f"Cannot switch shifts. One or both employees do not have hours on the specified dates.")
        except Exception as e:
            print(f"Error switching shifts: {e}")

    def initialize_employees(self):
        self.employees = {
            '1': {
                'name': 'John G',
                'work_schedule': self.generate_weekly_schedule({
                    0: 6.0,  # Monday
                    1: 0.0,  # Tuesday
                    2: 6.0,  # Wednesday
                    3: 0.0,  # Thursday
                    4: 0.0,  # Friday
                    5: 0.0,  # Saturday
                    6: 0.0   # Sunday
                })
            },
            '2': {
                'name': 'Cole B',
                'work_schedule': self.generate_weekly_schedule({
                    0: 0.0,  # Monday
                    1: 0.0,  # Tuesday
                    2: 0.0,  # Wednesday
                    3: 0.0,  # Thursday
                    4: 6.0,  # Friday
                    5: 0.0,  # Saturday
                    6: 0.0   # Sunday
                })
            },
            '3': {
                'name': 'Eric S',
                'work_schedule': self.generate_weekly_schedule({
                    0: 0.0,  # Monday
                    1: 0.0,  # Tuesday
                    2: 0.0,  # Wednesday
                    3: 6.0,  # Thursday
                    4: 0.0,  # Friday
                    5: 0.0,  # Saturday
                    6: 8.0   # Sunday
                })
            },
            '4': {
                'name': 'Michael F',
                'work_schedule': self.generate_weekly_schedule({
                    0: 0.0,  # Monday
                    1: 6.0,  # Tuesday
                    2: 0.0,  # Wednesday
                    3: 0.0,  # Thursday
                    4: 6.0,  # Friday
                    5: 8.0,  # Saturday
                    6: 0.0   # Sunday
                })
            },
            '5': {
                'name': 'Dean K',
                'work_schedule': self.generate_weekly_schedule({
                    0: 6.0,  # Monday
                    1: 6.0,  # Tuesday
                    2: 0.0,  # Wednesday
                    3: 0.0,  # Thursday
                    4: 0.0,  # Friday
                    5: 0.0,  # Saturday
                    6: 0.0   # Sunday
                })
            },
            '6': {
                'name': 'Tai T',
                'work_schedule': self.generate_weekly_schedule({
                    0: 0.0,  # Monday
                    1: 0.0,  # Tuesday
                    2: 6.0,  # Wednesday
                    3: 0.0,  # Thursday
                    4: 0.0,  # Friday
                    5: 0.0,  # Saturday
                    6: 0.0   # Sunday
                })
            },
                            '7': {
                    'name': 'Tyler B',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 0.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
                                '8': {
                    'name': 'Julie T',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 0.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
                                '9': {
                    'name': 'Chloe B',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 0.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
                                '10': {
                    'name': 'Jason T',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 0.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
                                '11': {
                    'name': 'Maeve M',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 0.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
                                '12': {
                    'name': 'Vincezo M',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 0.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
                                '13': {
                    'name': 'Sean D',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 0.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
                                '14': {
                    'name': 'Alexa K',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 0.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
                                '15': {
                    'name': 'Jameson M',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 0.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
                                '16': {
                    'name': 'Kayla D',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 0.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
                                '17': {
                    'name': 'Nick B',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 0.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
                                '17': {
                    'name': 'Belal H',
                    'work_schedule': self.generate_weekly_schedule({
                        0: 0.0,  # Monday
                        1: 0.0,  # Tuesday
                        2: 6.0,  # Wednesday
                        3: 0.0,  # Thursday
                        4: 0.0,  # Friday
                        5: 0.0,  # Saturday
                        6: 0.0   # Sunday
                    })
                },
            # Add more employees as needed
        }

    def generate_weekly_schedule(self, schedule_config):
        work_schedule = {}
        current_date = self.start_date
        while current_date <= self.current_period_end:
            weekday = current_date.weekday()
            if weekday in schedule_config:
                work_schedule[current_date] = schedule_config[weekday]
            current_date += timedelta(days=1)
        return work_schedule

    def get_employee_name(self, employee_id):
        return self.employees.get(employee_id, {}).get('name', 'Unknown')

    def get_employee_work_schedule(self, employee_id):
        return self.employees.get(employee_id, {}).get('work_schedule', {})

    def is_workday(self, employee_id, date):
        work_schedule = self.get_employee_work_schedule(employee_id)
        return date in work_schedule and work_schedule[date] > 0.0

    def get_work_hours(self, employee_id, date):
        work_schedule = self.get_employee_work_schedule(employee_id)
        return work_schedule.get(date, 0.0)

class PayrollApp:
    def __init__(self, root):
        self.payroll_calendar = PayrollCalendar(datetime(2024, 5, 27))

        self.root = root
        self.root.title("Wolf Payroll - Absecon")

        self.label_employee_id = tk.Label(root, text="Employee ID")
        self.label_employee_id.grid(row=0, column=0, padx=10, pady=5)
        self.entry_employee_id = tk.Entry(root)
        self.entry_employee_id.grid(row=0, column=1, padx=10, pady=5, sticky="W")
        
        self.label_employee_id_2 = tk.Label(root, text="Employee ID 2")
        self.label_employee_id_2.grid(row=0, column=2, padx=10, pady=5)
        self.entry_employee_id_2 = tk.Entry(root)
        self.entry_employee_id_2.grid(row=0, column=3, padx=10, pady=5, sticky="W")

        self.label_hours = tk.Label(root, text="Hours")
        self.label_hours.grid(row=1, column=0, padx=10, pady=5)
        self.entry_hours = tk.Entry(root)
        self.entry_hours.grid(row=1, column=1, padx=10, pady=5, sticky="W")

        self.label_date = tk.Label(root, text="Date: MM/DD/YYYY")
        self.label_date.grid(row=2, column=0, padx=10, pady=5)
        self.entry_date = tk.Entry(root)
        self.entry_date.grid(row=2, column=1, padx=10, pady=5, sticky="W")

        self.label_date_2 = tk.Label(root, text="Date 2: MM/DD/YYYY")
        self.label_date_2.grid(row=2, column=2, padx=10, pady=5)
        self.entry_date_2 = tk.Entry(root)
        self.entry_date_2.grid(row=2, column=3, padx=10, pady=5, sticky="W")

        self.button_add_hours = tk.Button(root, text="Add Hours", command=self.add_hours)
        self.button_add_hours.grid(row=3, column=0, padx=10, pady=5)
        
        self.button_switch_shifts = tk.Button(root, text="Switch Shifts", command=self.switch_shifts)
        self.button_switch_shifts.grid(row=3, column=1, padx=10, pady=5)

        self.button_remove_hours = tk.Button(root, text="Remove Hours", command=self.remove_hours)
        self.button_remove_hours.grid(row=3, column=2, padx=10, pady=5)

        self.button_previous_pay_period = tk.Button(root, text="Previous Pay Period", command=lambda: self.update_pay_period('previous'))
        self.button_previous_pay_period.grid(row=3, column=3, padx=10, pady=5)

        self.button_next_pay_period = tk.Button(root, text="Next Pay Period", command=lambda: self.update_pay_period('next'))
        self.button_next_pay_period.grid(row=3, column=4, padx=10, pady=5)

        self.text_payroll = tk.Text(root, height=20, width=100)
        self.text_payroll.grid(row=4, column=0, columnspan=6, padx=10, pady=5)

        self.text_pay_period = tk.Text(root, height=1, width=30)
        self.text_pay_period.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.update_payroll_display()

    def add_hours(self):
        employee_id = self.entry_employee_id.get()
        hours = float(self.entry_hours.get())
        date_str = self.entry_date.get()

        try:
            date = datetime.strptime(date_str, "%m/%d/%Y")
            self.payroll_calendar.add_hours(employee_id, date, hours)
            print(f"Added {hours} hours for Employee ID {employee_id} on {date}.")
        except ValueError:
            print(f"Invalid date format. Please use MM/DD/YYYY.")

        self.update_payroll_display()

    def remove_hours(self):
        employee_id = self.entry_employee_id.get()
        hours = float(self.entry_hours.get())
        date_str = self.entry_date.get()

        try:
            date = datetime.strptime(date_str, "%m/%d/%Y")
            self.payroll_calendar.remove_hours(employee_id, date, hours)
            print(f"Removed {hours} hours for Employee ID {employee_id} on {date}.")
        except ValueError:
            print(f"Invalid date format. Please use MM/DD/YYYY.")

        self.update_payroll_display()

    def switch_shifts(self):
        employee_id_1 = self.entry_employee_id.get()
        employee_id_2 = self.entry_employee_id_2.get()
        date_str_1 = self.entry_date.get()
        date_str_2 = self.entry_date_2.get()

        try:
            date_1 = datetime.strptime(date_str_1, "%m/%d/%Y")
            date_2 = datetime.strptime(date_str_2, "%m/%d/%Y")

            if self.payroll_calendar.current_period_start <= date_1 <= self.payroll_calendar.current_period_end and \
               self.payroll_calendar.current_period_start <= date_2 <= self.payroll_calendar.current_period_end:
                self.payroll_calendar.switch_shifts(employee_id_1, employee_id_2, date_1, date_2)
                self.update_payroll_display()
            else:
                print("Dates are not within the current pay period.")

        except ValueError:
            print("Invalid date format.")

    def update_pay_period(self, direction='next'):
        self.payroll_calendar.update_pay_period(direction)
        self.update_payroll_display()

    def update_payroll_display(self):
        scroll_pos = self.text_payroll.yview()[0]

        self.text_payroll.delete("1.0", tk.END)

        total_hours_summary = {}

        for employee_id, employee_data in self.payroll_calendar.employees.items():
            employee_name = employee_data['name']
            work_schedule = employee_data['work_schedule']
            total_hours_worked = 0.0
            self.text_payroll.insert(tk.END, f"Employee ID: {employee_id}, Name: {employee_name}\n")

            dates_to_display = set(work_schedule.keys())
            if employee_id in self.payroll_calendar.payroll:
                dates_to_display.update(self.payroll_calendar.payroll[employee_id].keys())
            
            for date in sorted(dates_to_display):
                if self.payroll_calendar.current_period_start <= date <= self.payroll_calendar.current_period_end:
                    preset_hours = work_schedule.get(date, 0)
                    if preset_hours > 0:
                        self.text_payroll.insert(tk.END, f"    Date: {date.strftime('%m/%d/%Y')}, Preset Hours: {preset_hours}\n")
                        total_hours_worked += preset_hours
                    
                    if employee_id in self.payroll_calendar.payroll and date in self.payroll_calendar.payroll[employee_id]:
                        added_hours = self.payroll_calendar.payroll[employee_id][date]
                        if added_hours > 0:
                            total_hours_worked += added_hours
                            self.text_payroll.insert(tk.END, f"    Date: {date.strftime('%m/%d/%Y')}, Added Hours: {added_hours}\n")

            self.text_payroll.insert(tk.END, f"    Total Hours Worked: {total_hours_worked}\n\n")
            total_hours_summary[employee_name] = total_hours_worked

        # Display summary in desired format
        self.text_payroll.insert(tk.END, "Hours Worked Summary:\n")
        for name, hours in total_hours_summary.items():
            self.text_payroll.insert(tk.END, f"{name}, {hours}\n")

        start, end = self.payroll_calendar.current_pay_period()
        self.text_pay_period.delete("1.0", tk.END)
        self.text_pay_period.insert(tk.END, f"{start.strftime('%m/%d/%Y')} - {end.strftime('%m/%d/%Y')}")

        self.text_payroll.yview_moveto(scroll_pos)

if __name__ == "__main__":
    root = tk.Tk()
    app = PayrollApp(root)
    root.mainloop()
