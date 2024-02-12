import json
import pandas as pd

def flatten(xss):
    return [x for xs in xss for x in xs]

def process_mapping(mapping):
    entries = []
    model_mappings = {}

    for m in mapping:
        ids = m.keys()
        for id in ids:
            if id in m:
                msg_container = m[id]
                if msg_container != None:
                    if "message" in msg_container:
                        msg = msg_container["message"]
                        if msg and "content" in msg:
                            author = msg["author"]
                            role = author["role"]
                            create_time = msg["create_time"]
                            if "parts" in msg["content"]:
                                if "metadata" in msg:
                                    if "model_slug" in msg["metadata"]:
                                        model = msg["metadata"]["model_slug"]
                                        model_mappings[id] = model
                                    elif role == "user":
                                        # parent = msg_container["parent"]
                                        # if parent in model_mappings:
                                        #     model = model_mappings[parent]
                                        # else:
                                        #     model = ""
                                        model = "gpt-4"
                                    else:
                                        model = ""
                                    orig_parts = msg["content"]["parts"]
                                    if all([type(p) == str for p in orig_parts]):
                                        parts = " ".join(orig_parts)
                                        entries.append([
                                            model,
                                            role,
                                            parts,
                                            create_time
                                        ])

    return entries

if __name__ == "__main__":
    with open("conversations.json") as f:
        sessions = json.loads(f.read())
        topics = flatten(sessions)
    mapping = [s.get("mapping", {}) for s in sessions]  # Use get() to avoid KeyError

    entries = process_mapping(mapping)

    # print(entries)

    entries_df = pd.DataFrame(
        data=entries,
        columns=["model", "role", "parts", "create_time"])
    
    print(entries_df.head())