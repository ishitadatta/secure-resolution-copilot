from datetime import datetime


def execute_mock_action(action_name: str, ticket_id: int) -> str:
    timestamp = datetime.utcnow().isoformat()
    return f"{action_name} executed for ticket {ticket_id} at {timestamp}Z"
