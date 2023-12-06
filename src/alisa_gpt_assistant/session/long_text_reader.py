class LongTextReader:
    MAX_MESSAGE_LENGTH = 1020
    SEARCH_WORD_BORDER_RANGE = 20

    def __init__(self, continue_message: str):
        self._unread_dialog_text = ""
        self._continue_message = continue_message

    def _find_cutoff_point(self, text, max_length):
        cutoff = max_length
        while cutoff > max_length - self.SEARCH_WORD_BORDER_RANGE and cutoff > 0:
            if text[cutoff].isspace():
                break
            cutoff -= 1
        return cutoff if text[cutoff].isspace() else max_length

    def read_next_part(self):
        if len(self._unread_dialog_text) > self.MAX_MESSAGE_LENGTH:
            continue_message = f"... {self._continue_message}"
            max_length = self.MAX_MESSAGE_LENGTH - len(continue_message)
            cutoff = self._find_cutoff_point(self._unread_dialog_text, max_length)

            part = self._unread_dialog_text[:cutoff].rstrip()
            self._unread_dialog_text = self._unread_dialog_text[cutoff:].lstrip()

            return part + continue_message
        else:
            result = self._unread_dialog_text
            self._unread_dialog_text = ""
            return result

    def set_text_to_read(self, new_text):
        self._unread_dialog_text += new_text

    def clear_text(self):
        self._unread_dialog_text = ""

    def has_unread_text(self):
        return bool(self._unread_dialog_text)
