import os
import re

class SubtitleHandler:
    def __init__(self):
        self.numbered_lines = []

    def load_subtitle_with_line_numbers(self, file_path):
        """
        Loads the .srt subtitle file into memory and assigns a unique line number to every line.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self.numbered_lines = [f"{index + 1}:{line.strip()}" for index, line in enumerate(lines)]
            print(f"Successfully loaded and numbered subtitle file: {file_path}")

        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error loading subtitle file: {str(e)}")

    def extract_text_lines(self):
        """
        Extracts only the text lines that need to be translated from the numbered lines.
        """
        text_lines = []

        for line in self.numbered_lines:
            # Extract lines that are not empty, timestamps, or numbers (including all dialogue)
            if re.match(r'^\d+:.*', line) and not re.match(r'^\d+:\d+$', line) and not re.match(r'^\d+:\d{2}:\d{2}:\d{2},\d{3}.*', line):
                text_lines.append(line)
        
        return text_lines

    def reintegrate_translated_text(self, translated_text_lines):
        """
        Replaces the original text lines with translated text lines.
        """
        translated_dict = {}
        for line in translated_text_lines:
            parts = line.split(':', 1)
            if len(parts) == 2:
                line_number = int(parts[0])
                text = parts[1].strip()
                translated_dict[line_number] = text

        final_lines = []

        for line in self.numbered_lines:
            line_number = int(line.split(':', 1)[0])
            if line_number in translated_dict:
                # Replace the original line with the translated version
                final_lines.append(f"{line_number}: {translated_dict[line_number]}")
            else:
                # Keep the original line (timestamps, numbers, etc.)
                final_lines.append(line)

        self.numbered_lines = final_lines

    def save_final_subtitle(self, output_path):
        """
        Saves the final subtitle file after removing line numbers.
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for line in self.numbered_lines:
                # Remove the numbering before saving
                line_content = line.split(':', 1)[1] if ':' in line else line
                f.write(line_content + "\n")

        print(f"Successfully saved final subtitle file: {output_path}")

    def generate_output_filename(self, original_file_path, language_code):
        base, ext = os.path.splitext(original_file_path)
        return f"{base}_{language_code}.srt"