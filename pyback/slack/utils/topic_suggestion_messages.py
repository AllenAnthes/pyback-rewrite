def new_suggestion_community_message(user_id: str, suggestion: str) -> dict:
    return {
        'text': f":exclamation:<@{user_id}> just submitted a suggestion for a help topic:exclamation:\n"
                f"-- {suggestion}"
    }
