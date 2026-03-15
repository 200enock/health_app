import requests, json, sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.logger import Logger
from plyer import notification

class MosquitoNetApp(App):
    def build(self):
        self.conn = sqlite3.connect('mosquito_net.db')
        self.cursor = self.conn.cursor()
        self.create_table()
        self.layout = BoxLayout(orientation='vertical')
        self.frames = self.create_frames()
        self.layout.add_widget(self.frames['login'])
        self.sync_data()
        return self.layout

    def create_table(self):
        tables = {
            'patients': 'CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, sex TEXT, location TEXT, nin TEXT, marital_status TEXT, marriage_period TEXT, education_level TEXT, household_size INTEGER, children_under_5 INTEGER, pregnant_women TEXT)',
            'distributions': 'CREATE TABLE IF NOT EXISTS distributions (id INTEGER PRIMARY KEY, patient_id INTEGER, date TEXT, location TEXT)',
            'local_patients': 'CREATE TABLE IF NOT EXISTS local_patients (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, sex TEXT, location TEXT, nin TEXT, marital_status TEXT, marriage_period TEXT, education_level TEXT, household_size INTEGER, children_under_5 INTEGER, pregnant_women TEXT)',
            'local_distributions': 'CREATE TABLE IF NOT EXISTS local_distributions (id INTEGER PRIMARY KEY, patient_id INTEGER, date TEXT, location TEXT)'
        }
        [self.cursor.execute(table) for table in tables.values()]
        self.conn.commit()

    def create_frames(self):
        frames = {
            'login': BoxLayout(orientation='vertical'),
            'registration': BoxLayout(orientation='vertical'),
            'distribution': BoxLayout(orientation='vertical'),
            'report': BoxLayout(orientation='vertical')
        }
        self.build_login_frame(frames['login'])
        self.build_registration_frame(frames['registration'])
        self.build_distribution_frame(frames['distribution'])
        self.build_report_frame(frames['report'])
        return frames

    def build_login_frame(self, frame):
        inputs = [{'hint_text': 'Username'}, {'hint_text': 'Password', 'password': True}]
        self.create_inputs(frame, inputs, self.login)

    def build_registration_frame(self, frame):
        inputs = [
            {'hint_text': 'Name'}, {'hint_text': 'Age'}, {'hint_text': 'Sex', 'type': 'spinner', 'values': ['Male', 'Female']},
            {'hint_text': 'Location'}, {'hint_text': 'National ID (NIN)'}, {'hint_text': 'Marital Status', 'type': 'spinner', 'values': ['Single', 'Married', 'Divorced', 'Widowed']},
            {'hint_text': 'Period of Marriage (years)'}, {'hint_text': 'Education Level', 'type': 'spinner', 'values': ['Primary', 'Secondary', 'Tertiary', 'University']},
            {'hint_text': 'Number of people in household'}, {'hint_text': 'Number of children under 5'}, {'hint_text': 'Pregnant Women', 'type': 'spinner', 'values': ['Yes', 'No']}
        ]
        self.create_inputs(frame, inputs, self.register_patient)

    def build_distribution_frame(self, frame):
        inputs = [{'hint_text': 'Patient ID'}]
        self.create_inputs(frame, inputs, self.distribute_net)

    def build_report_frame(self, frame):
        self.report_text = TextInput(multiline=True)
        frame.add_widget(self.report_text)
        Button(text='Generate Report', on_press=self.generate_report).bind(on_press=self.generate_report)

    def create_inputs(self, frame, inputs, callback):
        widgets = []
        for input in inputs:
            widget = Spinner(text=input['hint_text'], values=input['values']) if input.get('type') == 'spinner' else TextInput(hint_text=input['hint_text'], password=input.get('password', False))
            frame.add_widget(widget)
            widgets.append(widget)
        Button(text='Submit', on_press=lambda instance: callback(widgets)).bind(on_press=callback)

    def login(self, widgets):
        self.layout.clear_widgets()
        self.layout.add_widget(self.frames['registration'])

    def register_patient(self, widgets):
        data = [widget.text for widget in widgets]
        if self.check_internet_connection():
            self.sync_patient_data(*data)
        else:
            self.store_patient_data_locally(*data)
        notification.notify(title='Patient Registered', message='Patient registered successfully!')
        Logger.info('Patient registered successfully!')

    def distribute_net(self, widgets):
        patient_id = widgets[0].text
        self.cursor.execute('SELECT * FROM patients WHERE id=?', (patient_id,))
        patient = self.cursor.fetchone()
        if patient:
            age, location = patient[2], patient[4]
            if int(age) < 5 or location == 'High Risk Area':
                if self.check_internet_connection():
                    self.sync_distribution_data(patient_id, location)
                else:
                    self.store_distribution_data_locally(patient_id, location)
                notification.notify(title='Net Distributed', message='Mosquito net distributed successfully!')
                Logger.info('Mosquito Net Distributed Successfully!')
            else:
                notification.notify(title='Not Eligible', message='Patient is not eligible for a mosquito net.')
                Logger.info('Patient is not eligible for a mosquito net.')
        else:
            notification.notify(title='Patient Not Found', message='Patient not found.')
            Logger.info('Patient not found.')

    def generate_report(self, instance):
        self.cursor.execute('SELECT * FROM distributions')
        distributions = self.cursor.fetchall()
        report = '\n'.join([f'Patient ID: {distribution[1]}, Date: {distribution[2]}, Location: {distribution[3]}' for distribution in distributions])
        self.report_text.text = report
        notification.notify(title='Report Generated', message='Report generated successfully!')

    def check_internet_connection(self):
        try:
            requests.get('https://www.google.com')
            return True
        except requests.exceptions.RequestException:
            return False

    def store_patient_data_locally(self, *data):
        self.cursor.execute('INSERT INTO local_patients (name, age, sex, location, nin, marital_status, marriage_period, education_level, household_size, children_under_5, pregnant_women) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.conn.commit()

    def store_distribution_data_locally(self, patient_id, location):
        self.cursor.execute('INSERT INTO local_distributions (patient_id, date, location) VALUES (?, date("now"), ?)', (patient_id, location))
        self.conn.commit()

    def sync_data(self):
        if self.check_internet_connection():
            self.sync_patients()
            self.sync_distributions()

    def sync_patients(self):
        self.cursor.execute('SELECT * FROM local_patients')
        patients = self.cursor.fetchall()
        for patient in patients:
            self.sync_patient_data(*patient[1:])
            self.cursor.execute('DELETE FROM local_patients WHERE id=?', (patient[0],))
            self.conn.commit()

    def sync_distributions(self):
        self.cursor.execute('SELECT * FROM local_distributions')
        distributions = self.cursor.fetchall()
        for distribution in distributions:
            self.sync_distribution_data(distribution[1], distribution[3])
            self.cursor.execute('DELETE FROM local_distributions WHERE id=?', (distribution[0],))
            self.conn.commit()

    def sync_patient_data(self, *data):
        url = 'http://your-central-server.com/patients'
        try:
            response = requests.post(url, json=dict(zip(['name', 'age', 'sex', 'location', 'nin', 'marital_status', 'marriage_period', 'education_level', 'household_size', 'children_under_5', 'pregnant_women'], data)))
            if response.status_code == 200:
                Logger.info('Patient data synced successfully!')
            else:
                Logger.error('Failed to sync patient data!')
        except requests.exceptions.RequestException as e:
            Logger.error(f'Error syncing patient data: {e}')

    def sync_distribution_data(self, patient_id, location):
        url = 'http://your-central-server.com/distributions'
        try:
            response = requests.post(url, json={'patient_id': patient_id, 'location': location})
            if response.status_code == 200:
                Logger.info('Distribution data synced successfully!')
            else:
                Logger.error('Failed to sync distribution data!')
        except requests.exceptions.RequestException as e:
            Logger.error(f'Error syncing distribution data: {e}')

if __name__ == '__main__':
    MosquitoNetApp().run()
