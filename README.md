# Customer Support Chatbot with Amazon Bedrock Flows & AgentCore

*Project from the Udacity Future AWS Agent Engineer program (TODO Cindy: confirm the program and completion date).*

## Summary
I built a customer-support chatbot for a fictional online shop. Every customer message gets sorted into one of three groups, and each group is handled differently:
- **Bug reports**: the assistant asks follow-up questions until it has a description, the steps to reproduce the bug, and the environment. Then it creates a ticket through a tool.
- **Platform questions** (shipping, returns, payments, accounts): it answers only from the shop's FAQ, and when the FAQ doesn't cover something it sends the customer to a person instead of guessing.
- **Other requests**: it politely sends the customer to human support.

## Problem
Support teams lose time sorting incoming messages and chasing customers for missing bug details. The goal was to automate that routing and collect complete bug reports without making up answers.

## Architecture
```
CustomerInput -> MessageClassifier -> RouteByCategory
  BUG_REPORT        -> AgentCore harness -> AgentCore Gateway -> Lambda (CreateBugReport) -> DynamoDB
  PLATFORM_QUESTION -> FAQ prompt (grounded in online_shop_faq.md) -> output
  OTHER / default   -> human-support prompt -> output
```

## AWS services and tools
Amazon Bedrock Flows (prompt nodes and condition routing), Amazon Bedrock AgentCore (harness and Gateway), AWS Lambda (Python 3.11), Amazon DynamoDB, Amazon S3, Amazon Bedrock Model Evaluation (Builtin.Correctness, Amazon Nova Pro as the evaluator), boto3, and prompt engineering.

## Files
| File | Purpose |
|---|---|
| `prompts/classifier.txt` | MessageClassifier prompt that returns exactly one label |
| `prompts/system_prompt.txt` | Agent rules: bug-report field collection, FAQ grounding, prompt-injection defense |
| `prompts/faq_prompt_template.txt` | FAQ responder template (paste the FAQ where marked) |
| `tools.json` | Tool schema for `create_bug_report` |
| `chat.py` | Command-line chat client that streams responses from the AgentCore harness |
| `evaluation/flow-tests.json` | 9 test scenarios: bug reports, FAQ, uncovered FAQ, other, ambiguous, prompt injection |
| `evaluation/evaluation_config.json` | Bedrock evaluation job config (placeholders) |

## How to run
```bash
pip install -r requirements.txt
aws configure            # your own credentials, never commit them
python chat.py --harness-arn <YOUR_HARNESS_ARN> --region us-east-1
```
Fill in `<YOUR_S3_BUCKET>` and `<YOUR_FLOW_ALIAS_ARN>` in `evaluation/evaluation_config.json` before you start an evaluation job.

## Results
**Results: rerun in progress — real results from my AWS account coming soon.**

## Skills demonstrated
LLM intent classification and routing, designing guardrails (FAQ grounding, no invented ticket IDs, prompt-injection resistance), tool and function calling through an MCP gateway, serverless integration (Lambda and DynamoDB), and test-scenario design plus LLM evaluation.
