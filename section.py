class Section:
    def __init__(self, old_text, new_text):
        self.old_text = old_text
        self.new_text = new_text
        self.old_attributes = {}
        self.new_attributes = {}

    def __str__(self):
        return f"(old) {self.old_text} - {self.old_attributes}\n(new) {self.new_text} - {self.new_attributes}"