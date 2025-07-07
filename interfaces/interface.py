import os
from tkinter import filedialog
from typing import Optional, Tuple

import customtkinter as ctk

from configurations import InterfaceConfig
from follower_comparator.follower_comparator import FollowerComparator
from repositories.followers_repository import FollowersRepository


class Interface(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.result_frame = ctk.CTkFrame(self)
        self.result_textbox = ctk.CTkTextbox(self.result_frame, height=100)
        self.result_label = ctk.CTkLabel(self.result_frame, text="Difference:")
        self.button_frame = ctk.CTkFrame(self)
        self.reset_btn = ctk.CTkButton(
            self.button_frame,
            text="Reset",
            command=self.reset,
            fg_color=InterfaceConfig.RESET_BUTTON_COLOR
        )
        self.compare_btn = ctk.CTkButton(
            self.button_frame,
            text="Compare Followers",
            command=self.compare_followers
        )
        self.current_frame = ctk.CTkFrame(self)
        self.current_btn = ctk.CTkButton(
            self.current_frame,
            text="Select",
            command=self.select_current_file
        )
        self.current_entry = ctk.CTkEntry(self.current_frame, width=200)
        self.current_label = ctk.CTkLabel(
            self.current_frame,
            text="Current followers file:"
        )
        self.old_frame = ctk.CTkFrame(self)
        self.old_btn = ctk.CTkButton(
            self.old_frame,
            text="Select",
            command=self.select_old_file
        )
        self.old_entry = ctk.CTkEntry(self.old_frame, width=200)
        self.old_label = ctk.CTkLabel(
            self.old_frame,
            text="Old followers file:"
        )
        self._configure_window()
        self._initialize_components()

        # Repositories and services
        self.repository: FollowersRepository = FollowersRepository()
        self.comparator: FollowerComparator = FollowerComparator()

        # Application state
        self.old_file: Optional[str] = None
        self.current_file: Optional[str] = None

    def _configure_window(self):
        """Configures basic window properties."""
        self.title(InterfaceConfig.TITLE)
        self.geometry(InterfaceConfig.WINDOW_SIZE)
        self.resizable(True, False)
        self.minsize(600, 500)

    def _initialize_components(self):
        """Initializes all interface components."""
        self._create_header()
        self._create_old_file_selector()
        self._create_current_file_selector()
        self._create_button_panel()
        self._create_result_panel()

    def _create_header(self):
        """Creates the application title."""
        title_label = ctk.CTkLabel(
            self,
            text=InterfaceConfig.TITLE,
            font=("Arial", 20)
        )
        title_label.pack(pady=20)

    def _create_old_file_selector(self):
        """Creates the selector for old followers file."""
        self.old_frame.pack(pady=10, padx=20, fill="x", expand=True)

        self.old_label.pack(side="left", padx=10)

        self.old_entry.pack(side="left", padx=10, fill="x", expand=True)
        self.old_entry.configure(state="disabled")

        self.old_btn.pack(side="right", padx=10)

    def _create_current_file_selector(self):
        """Creates the selector for current followers file."""
        self.current_frame.pack(pady=10, padx=20, fill="x", expand=True)

        self.current_label.pack(side="left", padx=10)

        self.current_entry.pack(side="left", padx=10, fill="x", expand=True)
        self.current_entry.configure(state="disabled")

        self.current_btn.pack(side="right", padx=10)

    def _create_button_panel(self):
        """Creates the action buttons panel."""
        self.button_frame.pack(pady=10, padx=10)

        self.compare_btn.pack(side="left", padx=5)

        self.reset_btn.pack(side="right", padx=5)

    def _create_result_panel(self):
        """Creates the results display panel."""
        self.result_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.result_label.pack(pady=10)

        self.result_textbox.configure(state="disabled")
        self.result_textbox.pack(padx=10, pady=10, fill="both", expand=True)

    def select_old_file(self):
        """Opens dialog to select old followers file."""
        file = self._open_selection_dialog("Select old followers file")
        if file:
            self.old_file = file
            self._change_state_entries("normal")
            self._update_input_field(self.old_entry, file)
            self._change_state_entries("disabled")

    def select_current_file(self):
        """Opens dialog to select current followers file."""
        file = self._open_selection_dialog("Select current followers file")
        if file:
            self.current_file = file
            self._change_state_entries("normal")
            self._update_input_field(self.current_entry, file)
            self._change_state_entries("disabled")

    @staticmethod
    def _open_selection_dialog(title: str) -> Optional[str]:
        """Opens a file selection dialog."""
        return filedialog.askopenfilename(
            title=title,
            filetypes=[("JSON Files", "*.json")]
        )

    @staticmethod
    def _update_input_field(field: ctk.CTkEntry, file_path: str):
        """Updates an input field with the filename."""
        field.delete(0, "end")
        field.insert(0, os.path.basename(file_path))

    def _update_result(self, text: str):
        """Updates the result field with the provided text."""
        self.result_textbox.configure(state="normal")
        self.result_textbox.delete("0.0", "end")
        self.result_textbox.insert("0.0", text)
        self.result_textbox.configure(state="disabled")

    def _validate_files(self) -> Tuple[bool, str]:
        """Validates if files have been selected."""
        if not self.old_file or not self.current_file:
            return False, "Error: Please select both files first."
        return True, ""

    def compare_followers(self):
        """Compares followers between the two selected files."""
        valid, error_message = self._validate_files()
        if not valid:
            self._update_result(error_message)
            return

        old_followers = self.repository.load_followers(self.old_file)
        current_followers = self.repository.load_followers(self.current_file)

        if old_followers is None or current_followers is None:
            self._update_result("Error loading files. Check if they are valid JSON.")
            return

        new_followers = self.comparator.find_new_followers(
            old_followers, current_followers
        )

        result = "\n".join(new_followers) if new_followers else "No new followers found."
        self._update_result(result)

    def reset(self):
        """Clears all fields and application state."""
        self.old_file = None
        self.current_file = None

        self._change_state_entries("normal")

        self.old_entry.delete(0, "end")
        self.current_entry.delete(0, "end")

        self._change_state_entries("disabled")

        self._update_result("Select files and click Compare")

    def _change_state_entries(self, state: str):
        """Changes the state of the interface components."""
        self.old_entry.configure(state=state)
        self.current_entry.configure(state=state)
