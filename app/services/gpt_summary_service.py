
# 서비스 계층
import requests


class DialogueService:
    @staticmethod
    def fetch_dialogue_logs(api_url: str):
        response = requests.get(api_url, headers={'accept': 'application/json'})
        if response.status_code == 200:
            return response.json()
        else:
            return None

    @staticmethod
    def summarize_dialogue_for_parents(dialogues, chatgpt_api_url: str, chatgpt_api_key: str):
        dialogue_texts = '\n'.join([f"{'User' if dialogue['log_type'] == 'USER_TALK' else 'Gree'}: {dialogue['content']}" for dialogue in dialogues])
        summary_request_message = f"5-7세 아동(User)의 대화 내용을 통해 아동의 의사소통 능력, 감정 표현, 사회적 상호작용 방식을 분석해주세요. 아래 대화 내용을 참고하여, 아동이 어떻게 친구들과 상호작용하는지, 일상적인 상황에서 어떤 감정과 행동을 보이는지 3,4줄 정도로 분석해주세요.\n\n대화 내용:\n{dialogue_texts}"

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": summary_request_message
                }
            ]
        }
        headers = {
            "Authorization": f"Bearer {chatgpt_api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(chatgpt_api_url, json=payload, headers=headers)
        if response.status_code == 200:
            summary = response.json().get("choices")[0].get("message")["content"].strip()
            return summary
        else:
            return f"요약을 완료할 수 없습니다. 오류 코드: {response.status_code}, 메시지: {response.text}"
