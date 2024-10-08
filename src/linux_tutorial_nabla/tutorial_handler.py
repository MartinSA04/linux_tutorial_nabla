
import pathlib
import copy
import json
from typing import List
from linux_tutorial_nabla.colors import Colors
from linux_tutorial_nabla.common import NablaModel, user_data_path
from linux_tutorial_nabla.tutorial import Tutorial
from linux_tutorial_nabla.tutorials import tutorial_list


class TutorialHandler(NablaModel):
    tutorials: List[Tutorial] = tutorial_list
    selected_tutorial_name: str | None = None

    def get_data(self, username):
        if not pathlib.Path(user_data_path).exists():
            data = {}
            with open(user_data_path, "w") as f:
                json.dump(data, f)
        with open(user_data_path, "r") as f:
            data = json.load(f)
        return data

    def read_user_data(self, username):
        data = self.get_data(username)
        if username not in data:
            return
        for tutorial in self.tutorials:
            if tutorial.name in data[username]["completed_tutorials"]:
                tutorial.completed = True

    def write_user_data(self, username):
        data = self.get_data(username)
        data[username] = {"completed_tutorials": self.completed_tutorials}
        with open(user_data_path, "w") as f:
            json.dump(data, f)

    def get_tutorial(self, name):
        for tutorial in self.tutorials:
            if tutorial.name == name:
                return tutorial
        return None

    @property
    def completed_tutorials(self):
        return [tutorial.name for tutorial in self.tutorials if tutorial.completed]

    @property
    def selected_tutorial(self):
        return self.get_tutorial(self.selected_tutorial_name)

    def get_available_tutorials(self):
        return [tutorial for tutorial in self.tutorials if tutorial.available]

    def get_completed_tutorials(self):
        return [tutorial for tutorial in self.tutorials if tutorial.completed]
    
    def update_tutorials(self):
        for tutorial in self.tutorials:
            tutorial.update_available(self.completed_tutorials)
    
    def print_tutorials(self):
        print(Colors.g("\nAvailable tutorials:"))
        for tutorial in self.tutorials:
            print(str(tutorial))
        
        print(Colors.g("\nTo start a tutorial, type") + f" {Colors.M('start <tutorial name>')} " + Colors.g("and press enter.\n"))
        if self.selected_tutorial:
            print(Colors.g("\nSelected tutorial:") + f" {Colors.B(self.selected_tutorial.name)}")
    
    def start_tutorial(self, name):
        tutorial = self.get_tutorial(name)
        if tutorial:
            tutorial.completed = False
            self.selected_tutorial_name = tutorial.name
            print(f"\n{Colors.g('Starting tutorial:')} {Colors.B(tutorial.name)}\n")
            print(Colors.g(tutorial.description) + "\n")
            tutorial.step_status()
            tutorial.get_step().initialize()
        else:
            print(f"{Colors.g('Could not find tutorial:')} {Colors.B(name)}")

    def print_status(self):
        self.update_tutorials()
        self.print_tutorials()
        if self.selected_tutorial:
            self.selected_tutorial.step_status()

    def check_command(self, command):
        original_command = copy.deepcopy(command)
        command = command.split(" ")
        match command[0]:
            case "start":
                if len(command) == 2:
                    self.start_tutorial(command[1])
                elif len(command) == 1:
                    self.print_status()
                else:
                    print(f"{Colors.g('Invalid command. Please type')} {Colors.M('start <tutorial name>')}")
                return ""
            case "status":
                self.print_status()
                return ""
            case "reset":
                self.selected_tutorial.get_step().initialize()
                self.selected_tutorial.step_status()
                return ""
            case _:
                return original_command
    
    def print_completed(self, name):
        print("\n" + Colors.G("Good job! You have completed the following tutorial: " + Colors.G(name)))

    def check_completion(self, command, pwd):
        if self.selected_tutorial:
            complete = self.selected_tutorial.check_completion(command, pwd)
            if complete:
                self.print_completed(self.selected_tutorial.name)
                self.completed_tutorials.append(self.selected_tutorial.name)
                self.selected_tutorial_name = None
                self.print_status()
            return complete
        return False