import requests
from datetime import datetime
import os


class JsonParser:
    def __init__(self):
        try:
            self.users = requests.get('https://json.medrating.org/users').json()
            self.tasks = requests.get('https://json.medrating.org/todos').json()
        except Exception as e:
            print(e)
    

    def find_tasks(self, user):
        completed_tasks = []
        uncompleted_tasks = []
        for todo in self.tasks:
            if todo.get('userId') == user['id']:
                if todo.get('completed'):
                    if len(todo.get('title')) > 50:
                        title = f"{todo.get('title')[:50]}..."
                    else:
                        title = todo.get('title')
                    completed_tasks.append(title)
                else:
                    if len(todo.get('title')) > 50:
                        title = f"{todo.get('title')[:50]}..."
                    else:
                        title = todo.get('title')
                    uncompleted_tasks.append(title)

        return completed_tasks, uncompleted_tasks
    

    @staticmethod
    def make_report(user, completed_tasks, not_completed_tasks):
            report = f"{user['name']} <{user['email']}> {datetime.now().strftime('%d.%m.%Y %H:%M')}\n{user['company']['name']}\n\nЗавершённые задачи:\n"
            for task in completed_tasks:
                report += task + "\n"
            report += "\nОставшиеся задачи:\n"
            for task in not_completed_tasks:
                report += task + "\n"
            return report
    

    @staticmethod
    def check_report(file_path):    
        if os.path.exists(file_path + ".txt"):
            time = os.path.getmtime(file_path + '.txt')
            creation_time = datetime.fromtimestamp(time).strftime('%Y-%m-%dT%H:%M')
            os.rename(file_path + ".txt", file_path + f"_{creation_time}.txt")

    def main(self):
        path = os.path.join(os.getcwd(), 'tasks')
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
        try:
            for user in self.users:
                file_path = os.path.join(path, f"{user['username']}")
                completed_tasks, uncompleted_tasks = self.find_tasks(user)
                report = self.make_report(user, completed_tasks, uncompleted_tasks)
                self.check_report(file_path)
                open(os.path.join(path, f"{user['username']}") + ".txt", "w").write(report)
        except KeyError:
            pass


if __name__ == "__main__":
    parser = JsonParser()
    parser.main()
