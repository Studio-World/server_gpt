
import json, datetime, os 

def append_chatlog(role, message):
    # Fichar como JSON, linha
    log = {
        "role": role,
        "timestamp": datetime.datetime.utcnow(),
        "message": message
    }

    with open("chatlog.jsonl", "a") as f:
        f.write(json.dumps(log))
        f.write("p\n")

if __name__ == "__main__":
    append_chatlog("user", "Exemplo do log de chat")
    append_chatlog("dan", "Answer de chat")