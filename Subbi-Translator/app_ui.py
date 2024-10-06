import tkinter as tk
from tkinter import filedialog, messagebox
from subtitle_handler import SubtitleHandler
from llm_translator import LLMTranslator

class SubtitleTranslatorUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Subbi-Translator")
        self.subtitle_handler = SubtitleHandler()
        self.llm_translator = LLMTranslator()

        # Create UI components
        self.create_window()

    def create_window(self):
        """
        Sets up the GUI window, file selector, and language dropdown.
        """
        # File selection label and button
        self.label_file = tk.Label(self.window, text="Select Subtitle File:")
        self.label_file.grid(row=0, column=0, padx=10, pady=10)

        self.button_browse = tk.Button(self.window, text="Browse", command=self.browse_file)
        self.button_browse.grid(row=0, column=1, padx=10, pady=10)

        # Label to show selected file
        self.file_path_label = tk.Label(self.window, text="No file selected.")
        self.file_path_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Language dropdown label and dropdown
        self.label_language = tk.Label(self.window, text="Select Output Language:")
        self.label_language.grid(row=2, column=0, padx=10, pady=10)

        self.language_var = tk.StringVar(self.window)
        self.language_var.set("German")  # default language
        self.language_dropdown = tk.OptionMenu(self.window, self.language_var, "German", "French", "Spanish", "Chinese")
        self.language_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Translate button
        self.button_translate = tk.Button(self.window, text="Translate", command=self.on_translate_button_click)
        self.button_translate.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Status label
        self.status_label = tk.Label(self.window, text="")
        self.status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def browse_file(self):
        """
        Opens a file dialog for the user to select a subtitle (.srt) file.
        """
        file_path = filedialog.askopenfilename(filetypes=[("Subtitle files", "*.srt")])
        if file_path:
            self.file_path_label.config(text=file_path)
        else:
            self.file_path_label.config(text="No file selected.")

    def on_translate_button_click(self):
        """
        Handles the translation process when the user clicks the 'Translate' button.
        """
        file_path = self.file_path_label.cget("text")
        if file_path == "No file selected.":
            messagebox.showerror("Error", "Please select a subtitle file.")
            return

        target_language = self.language_var.get()

        # Load and extract text lines from the subtitle file
        self.subtitle_handler.load_subtitle_with_line_numbers(file_path)
        text_lines = self.subtitle_handler.extract_text_lines()

        if not text_lines:
            messagebox.showerror("Error", "Failed to load or extract text from the subtitle file.")
            return

        # Translate the text entries
        self.status_label.config(text="Translating...")
        translated_text_lines = self.llm_translator.translate_text_lines(text_lines, target_language)
        if translated_text_lines is None:
            messagebox.showerror("Error", "Translation failed.")
            return

        # Reintegration of translated text
        self.subtitle_handler.reintegrate_translated_text(translated_text_lines)

        # Save the final subtitle file
        output_path = self.subtitle_handler.generate_output_filename(file_path, target_language)
        self.subtitle_handler.save_final_subtitle(output_path)

        self.status_label.config(text=f"Translation completed! Saved as {output_path}")

# Run the UI
if __name__ == "__main__":
    ui = SubtitleTranslatorUI()
    ui.window.mainloop()
