# AI Editor - Copyright (C) 2026 Kalpit
#
# This file is part of AI Editor.
#
# AI Editor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# AI Editor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with AI Editor.  If not, see <https://www.gnu.org/licenses/>.

from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QMessageBox, QPushButton, QTextEdit, QHBoxLayout, QPushButton, QVBoxLayout, QStatusBar, QToolBar, QGridLayout, QSizePolicy, QListWidget, QAbstractItemView, QLabel, QListWidgetItem
from PySide6.QtGui import QAction, QActionGroup, QIcon
from PySide6.QtCore import Signal, QObject, QSize
import ollama
from version import __version__
import os
from datetime import datetime
import json

class RAG_Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("RAG Tool")
        
        layout = QVBoxLayout()
        self.label = QLabel("Kalpit Rathod")
        layout.addWidget(self.label)
        self.setLayout(layout)

class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(f"AI Editor v{__version__}")
        
        menu_bar = self.menuBar()
        
        self.filename_r = ""
        
        file_menu = menu_bar.addMenu("File")
        
        new_file_action = QAction("New", self)
        new_file_action.triggered.connect(self.new_file)
        new_file_action = file_menu.addAction(new_file_action)
        
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_conversation)
        save_action = file_menu.addAction(save_action)
        
        action_quit = QAction("Quit", self)
        action_quit.triggered.connect(self.quit_app)
        file_menu.addAction(action_quit)
        
        self.selected_model = None
        response = ollama.list()
        model_menu = menu_bar.addMenu("Model")
        
        # Create an action group so only one can be selected
        self.model_group = QActionGroup(self)
        self.model_group.setExclusive(True)  # Only one checked at a time
        self.model_group.triggered.connect(self.model_selected)
        
        self.statusBar().showMessage("Status Log: trying to fetch models")
        QApplication.processEvents()
        # Add models as checkable actions
        for i, model_info in enumerate(response.models):
            action_model = QAction(model_info.model, self)
            action_model.setCheckable(True)
            if i == 0:
                action_model.setChecked(True)  # Default selection
                self.selected_model = model_info.model
            self.model_group.addAction(action_model)
            model_menu.addAction(action_model)
        self.statusBar().showMessage("Status Log: ollama models fetched successfully")
        QApplication.processEvents()
        
        help_menu = menu_bar.addMenu("Help")
        action_about = QAction("About", self)
        action_about.triggered.connect(self.button_clicked_about)
        help_menu.addAction(action_about)
        
        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(25, 25))
        self.addToolBar(toolbar)
        
        new_file_tool = QAction(QIcon("icons/newfile.png"), "New Chat", self)
        new_file_tool.setStatusTip("New chat has been created")
        toolbar.addAction(new_file_tool)
        new_file_tool.triggered.connect(self.new_file)
        
        RAG_tool = QAction(QIcon("icons/RAG.png"), "RAG", self)
        toolbar.addAction(RAG_tool)
        RAG_tool.triggered.connect(self.show_RAG_Tool)
        
        self.rag_window = None
        
        # toolbar.addSeparator()
        
        self.messages = [] # store full data
        self.conversation = [] # store full data
        
        self.text_edit = QTextEdit()
        self.text_chat_history = QTextEdit()
        
        current_text_button = QPushButton("Send")
        current_text_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        current_text_button.clicked.connect(self.current_text_button_clicked)
        
        self.conversations_list_widget = QListWidget(self)
        self.conversations_list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.chat_files()
        self.conversations_list_widget.currentItemChanged.connect(self.current_item_changed)
        
        button_new_file = QPushButton("New")
        button_new_file.clicked.connect(self.new_file)
        
        button_delete_conversation = QPushButton("Delete")
        button_delete_conversation.clicked.connect(self.delete_conversation)
        
        self.chat_label = QLabel("New Chat")
        self.chat_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.setStatusBar(QStatusBar(self))
        
        add_remove_layout_h = QHBoxLayout()
        add_remove_layout_h.addWidget(button_new_file)
        add_remove_layout_h.addWidget(button_delete_conversation)
        
        grid_layout = QGridLayout()
        grid_layout.addLayout(add_remove_layout_h,0,0)
        grid_layout.addWidget(self.chat_label,0,1,1,2)
        grid_layout.addWidget(self.conversations_list_widget,1,0,2,1)
        grid_layout.addWidget(self.text_chat_history,1,1,1,2)
        grid_layout.addWidget(self.text_edit,2,1)
        grid_layout.addWidget(current_text_button,2,2)
        
        # Control how much space each column takes
        grid_layout.setColumnStretch(0, 2)  # make column 0 wider
        grid_layout.setColumnStretch(1, 8)  # keep column 1 narrower
        grid_layout.setColumnStretch(2, 2)  # keep column 1 narrower
        
        # grid_layout.setRowStretch(0, 5)  # chat history row grows more
        grid_layout.setRowStretch(1, 5)  # input row grows less
        grid_layout.setRowStretch(2, 1)  # input row grows less
        
        # Central widget for QMainWindow
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
        self.setCentralWidget(central_widget)
        
    def show_RAG_Tool(self):
        if self.rag_window is None:
            self.rag_window = RAG_Window()
            
        self.rag_window.resize(800,600)
        
        self.rag_window.show()
    
    def delete_conversation(self):
        current_item = self.conversations_list_widget.currentItem()
        
        if current_item:
            filename = current_item.text()
            file_path = os.path.join("chat", filename)
            
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                
                row = self.conversations_list_widget.currentRow()
                self.conversations_list_widget.takeItem(row)
                
                self.new_file()
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not delete file: {e}")
        else:
            QMessageBox.warning(self, "Delete", "Please select a conversation to delete.")
    
    def cl_summary(self):
        
        existing_title = next((m for m in self.messages if m.get("role") == "title"), None)

        if existing_title:
            # Update the dictionary in place
            self.chat_label.setText(existing_title["content"])
            existing_title["saved_time"] = datetime.now().isoformat()
        else:
            res = ollama.chat(
                model="llama3.2",
                messages=[
                    {"role": "user", "content": f"Summarize chat in one small sentence dont be verbose {self.conversation}"},
                ],
            )
            new_title = res["message"]["content"]
            # Create it for the first time
            self.messages.append({
                "role": "title",
                "content": new_title,
                "model": self.selected_model,
                "saved_time": datetime.now().isoformat()
            })
            self.chat_label.setText(new_title)
    
    def model_selected(self, action):
        """Triggered when a model is selected."""
        self.selected_model = action.text()
        QMessageBox.information(self, "Model Selected", f"You selected: {self.selected_model}")
        print(f"User selected model: {self.selected_model}")
        self.statusBar().showMessage("Status Log: successfully model changed")
        QApplication.processEvents()
        
    def chat_files(self):
        chat_folder = "chat/"
        json_files =  [f for f in os.listdir(chat_folder) if f.endswith(".json")]
        self.conversations_list_widget.clear()
        self.conversations_list_widget.addItems(json_files)
    
    def quit_app(self):
        QApplication.quit()

    def current_item_changed(self, item):
        # self.save_conversation()
        self.conversation = []
        self.messages = []
        if not item:
            return

        filename = os.path.join("chat", item.text()) 
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.messages = json.load(f)  
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load conversation: {e}")
            return
        
        for msg in self.messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            time_asked = msg.get("asked_time") 
            time_replied = msg.get("reply_time")
            
            if time_asked == "":
                self.conversation.append({
                    "role": role,
                    "content": content,
                    "reply_time": time_replied,
                })
            else:
                self.conversation.append({
                    "role": role,
                    "content": content,
                    "asked_time": time_asked,
                })
        
        self.cl_summary()
        self.set_plain_text()
        self.filename_r = filename
        print(self.filename_r)

    def button_clicked_about(self):
        QMessageBox.about(
            self,
            "About",
            f"Developer: Kalpit Rathod\nVersion: {__version__}\nLicence: GPLv3"
        )
        
    def current_text_button_clicked(self):
        self.chat()
        
    def generate_filename(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"conversation_{timestamp}.json"
    
    def save_conversation(self):
        if self.filename_r == "":
            self.cl_summary()
            filename = f"chat/{self.generate_filename()}"
            
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
                
            self.chat_files()
        else: 
            with open(self.filename_r, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, indent=2, ensure_ascii=False)
                
            self.chat_files()

        self.new_file()
                
    def new_file(self):
        self.text_edit.clear()
        self.chat_label.setText("New Chat")
        self.filename_r = ""
        self.messages = []
        self.conversation = []
        self.set_plain_text()
                            
    def save_chat_clicked(self):
        self.save_conversation()
        self.statusBar().showMessage("Status Log: chat saved successfully.")
        QApplication.processEvents()
        
    def chat(self):
        # ensure /chat folder exists
        os.makedirs("chat", exist_ok=True)

        # create a unique file for this session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        userinput = self.text_edit.toPlainText()
        if not userinput:
            QMessageBox.warning(self, "Empty Input", "Please type something before sending.")
            return
        self.statusBar().showMessage("Status Log: input success")
        QApplication.processEvents()
        
        # add user message to history
        self.messages.append({
            "role": "user",
            "content": userinput,
            "model": self.selected_model,
            "asked_time": datetime.now().isoformat()
        })
        self.statusBar().showMessage("Status Log: message append success")
        QApplication.processEvents()
        
        # add user message to history
        self.conversation.append({
            "role": "user",
            "content": userinput,
            "asked_time": datetime.now().isoformat()
        })
        self.statusBar().showMessage("Status Log: conversation append success")
        QApplication.processEvents()
        
        self.set_plain_text()
        self.statusBar().showMessage("Status Log: UI text updated")
        QApplication.processEvents()
        
        # check if model supports chat
        if "embed" in self.selected_model.lower():
            QMessageBox.warning(self, "Unsupported Model",
                                f"Model '{self.selected_model}' does not support chat.")
            return
        self.statusBar().showMessage("Status Log: chat feature supported bu model")
        QApplication.processEvents()
        
        try:
            # stream response
            res = ollama.chat(
                model=self.selected_model,
                messages=self.conversation,
                stream=True,
            )
            self.statusBar().showMessage("Status Log: wait! response is being generated")
            QApplication.processEvents()
            
            response_text = ""
            for chunk in res:
                print(chunk["message"]["content"], end="", flush=True)
                response_text += chunk["message"]["content"]
            print()
            self.statusBar().showMessage("Status Log: successfully fetched response")
            QApplication.processEvents()
            
            # add assistant response to history
            self.messages.append({
                "role": "assistant",
                "content": response_text,
                "model": self.selected_model,
                "reply_time": datetime.now().isoformat(),
                "conversation_id": timestamp
            })
            
            # add assistant response to conversation
            self.conversation.append({
                "role": "assistant",
                "content": response_text,
                "reply_time": datetime.now().isoformat(),
            })
            self.statusBar().showMessage("Status Log: messages and conversation updated")
            QApplication.processEvents()
            
            self.set_plain_text()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Chat failed: {e}")

    def set_plain_text(self):
        chat_history = "<html><body style='font-family:Arial; font-size:12pt;'>"

        for msg in self.messages:
            raw_role = msg.get("role", "").lower()

            if raw_role in ["user", "assistant"]:
                role = raw_role.capitalize()
                content = msg.get("content", "").replace("\n", "<br>")
                time_raw = msg.get("asked_time") or msg.get("reply_time") or ""

                try:
                    dt = datetime.fromisoformat(time_raw)
                    time_str = dt.strftime("%d %b %Y, %I:%M %p")
                except Exception:
                    time_str = time_raw

                chat_history += f"""
                <p>
                    <b>{role}</b> <span style="color:gray;">[{time_str}]</span><br>
                    {content}
                </p>
                """

        chat_history += "</body></html>"
        self.text_chat_history.setHtml(chat_history)
        
        cursor = self.text_chat_history.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.text_chat_history.setTextCursor(cursor)