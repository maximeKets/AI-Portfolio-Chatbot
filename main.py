from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr

load_dotenv(override=True)


def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}


record_user_details_json = {
    "name": "record_user_details",
    "description": "Utilisez cet outil pour enregistrer qu'un utilisateur est intéressé à être contacté et a fourni une adresse email",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "L'adresse email de cet utilisateur"
            },
            "name": {
                "type": "string",
                "description": "Le nom de l'utilisateur, s'il l'a fourni"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Toute information supplémentaire sur la conversation qui mérite d'être enregistrée pour donner du contexte"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Utilisez toujours cet outil pour enregistrer toute question qui n'a pas pu être répondue car vous ne connaissiez pas la réponse",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "La question qui n'a pas pu être répondue"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
         {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Maxime Kets"
        reader = PdfReader("me/Profile.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id})
        return results

    def system_prompt(self):
        system_prompt = f"Vous agissez en tant que {self.name}. Vous répondez aux questions sur le site web de {self.name}, \
en particulier aux questions liées à la carrière, au parcours, aux compétences et à l'expérience de {self.name}. \
Votre responsabilité est de représenter {self.name} pour les interactions sur le site web aussi fidèlement que possible. \
Vous disposez d'un résumé du parcours de {self.name} et de son profil LinkedIn que vous pouvez utiliser pour répondre aux questions. \
Soyez professionnel et engageant, comme si vous parliez à un client potentiel ou à un futur employeur qui aurait visité le site web. \
Si vous ne connaissez pas la réponse à une question, utilisez votre outil record_unknown_question pour enregistrer la question à laquelle vous n'avez pas pu répondre, même s'il s'agit de quelque chose de trivial ou de non lié à la carrière. \
Si l'utilisateur engage une discussion, essayez de l'orienter vers une prise de contact par email ; demandez son email et enregistrez-le en utilisant votre outil record_user_details. "

        system_prompt += f"\n\n## Résumé :\n{self.summary}\n\n## Profil LinkedIn :\n{self.linkedin}\n\n"
        system_prompt += f"Avec ce contexte, veuillez discuter avec l'utilisateur, en restant toujours dans le personnage de {self.name}."
        return system_prompt

    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [
            {"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason == "tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content


if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat).launch()
