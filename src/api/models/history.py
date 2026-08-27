""" conversation history for username """

MAX_HISTORY_MESSAGES = 40

_history_store: dict[str, list[dict]] = {}


class ChatHistoryService:
    @staticmethod
    def get_history(username: str) -> list[dict]:
        """ return username's chat history as a list of
        {'role': 'user'|'assistant', 'content': str} dicts, oldest first """
        return _history_store.get(username, [])

    @staticmethod
    def add_message(username: str, role: str, content: str) -> None:
        """ append a message and trim to the last MAX_HISTORY_MESSAGES """
        history = _history_store.setdefault(username, [])
        history.append({'role': role, 'content': content})
        if len(history) > MAX_HISTORY_MESSAGES:
            del history[:-MAX_HISTORY_MESSAGES]

    @staticmethod
    def clear_history(username: str) -> None:
        _history_store.pop(username, None)

    @staticmethod
    def as_prompt_text(username: str) -> str:
        """ flatten history into plain text suitable for prepending to a prompt """
        history = _history_store.get(username, [])
        return "\n".join(f"{h['role']}: {h['content']}" for h in history)
