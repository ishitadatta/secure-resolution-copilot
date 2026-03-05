from datetime import datetime, timezone


def execute_mock_action(action_name: str, ticket_id: int) -> str:
    timestamp = datetime.now(timezone.utc).isoformat()
    return f"{action_name} executed for ticket {ticket_id} at {timestamp}Z"
