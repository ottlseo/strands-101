import json
import uuid
import boto3

agent_arn = "arn:aws:bedrock-agentcore:us-west-2:654654304740:runtime/strands_workshop_agent-w6Kx9QBoM6"
prompt = "80 / 4 * 5 의 제곱근은?"

client = boto3.client('bedrock-agentcore')

payload = json.dumps({"prompt": prompt}).encode()

response = client.invoke_agent_runtime(
    agentRuntimeArn=agent_arn,
    runtimeSessionId=str(uuid.uuid4()),
    payload=payload,
)

content = []
for chunk in response.get("response", []):
    content.append(chunk.decode('utf-8'))

result = json.loads(''.join(content))

print("\n" + "=" * 60)
print("🤖 Agent Response")
print("=" * 60 + "\n")

if 'result' in result and 'content' in result['result']:
    for item in result['result']['content']:
        if 'text' in item:
            print(item['text'])
else:
    print(json.dumps(result, indent=2, ensure_ascii=False))

print("\n" + "=" * 60 + "\n")

# import json
# import uuid
# import boto3

# agent_arn = "<<배포 시 출력된 Endpoint ARN을 입력하세요>>"
# region = "us-west-2"
# prompt = "일본 도쿄에 대해서 리서치 좀 해줄 수 있니? 그리고 거기로 3일 여행 계획도 세워줘. 여행에 필요한 제품도 추천해줘."

# client = boto3.client('bedrock-agentcore')

# payload = json.dumps({"prompt": prompt}).encode()

# print(f"\n\n프롬프트: {prompt}\n")
# print("⏳ 에이전트 호출 중...\n")
# print(f"📊 CloudWatch Logs에서 에이전트 로그를 확인하세요: https://console.aws.amazon.com/cloudwatch/home?region={region}#logsV2:log-groups\n\n")


# try:
#     response = client.invoke_agent_runtime(
#         agentRuntimeArn=agent_arn,
#         runtimeSessionId=str(uuid.uuid4()),
#         payload=payload,
#     )

#     # 응답 스트림 소비 (출력하지 않음)
#     for _ in response.get("response", []):
#         pass

#     print("✅ 에이전트 호출 완료\n")
# except Exception as e:
#     print("에이전트는 백그라운드에서 작동 중일 수 있습니다. CloudWatch에서 응답을 확인해주세요.\n")