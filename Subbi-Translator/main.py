from app_ui import SubtitleTranslatorUI

def main():
    """
    Entry point for the Subbi-Translator application.
    Initializes the GUI and starts the app.
    """
    # Create the UI instance and start the Tkinter event loop
    ui = SubtitleTranslatorUI()
    ui.window.mainloop()

if __name__ == "__main__":
    main()