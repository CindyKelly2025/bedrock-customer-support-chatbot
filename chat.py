import argparse
import uuid
import boto3

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--harness-arn", required=True)
    p.add_argument("--region", default="us-east-1")
    args = p.parse_args()

    client = boto3.client("bedrock-agentcore", region_name=args.region)
    session_id = str(uuid.uuid4())
    print("AgentCore customer-support chat")
    print("Session:", session_id)

    while True:
        user_text = input("\nYou: ").strip()
        if user_text.lower() in {"exit", "quit"}:
            break
        response = client.invoke_harness(
            harnessArn=args.harness_arn,
            runtimeSessionId=session_id,
            messages=[{"role":"user","content":[{"text":user_text}]}]
        )
        print("Assistant:", end=" ")
        for event in response["stream"]:
            if "contentBlockDelta" in event:
                delta = event["contentBlockDelta"].get("delta", {})
                if "text" in delta:
                    print(delta["text"], end="", flush=True)
                if "toolUse" in delta:
                    print(f"\n[tool call] {delta['toolUse'].get('name','')}", end="")
        print()

if __name__ == "__main__":
    main()
