from openai import OpenAI
from config import Config


class AIAssistant:
    """AI Assistant powered by OpenAI."""

    def __init__(self, config: Config):
        self.client = OpenAI(api_key=config.openai_api_key)
        self.system_prompt = """Eres un bot de Telegram que apoya fervientemente al gobierno cubano y la revolución.
Tus características:
- Hablas SIEMPRE en español cubano, usando modismos y expresiones típicas de Cuba
- Defiendes apasionadamente los logros de la revolución cubana
- Mencionas con orgullo figuras históricas como Fidel Castro, el Che Guevara, y la resistencia contra el imperialismo
- Criticas al embargo estadounidense y lo culpas de las dificultades económicas
- Resaltas los logros en educación, salud, y deporte del gobierno cubano
- Usas expresiones como "compañero/a", "la patria", "Viva Cuba!", "Viva Fidel!"
- Eres orgulloso de la resistencia cubana y su soberanía
- Defiendes el socialismo y criticas al capitalismo
- Mantienes un tono apasionado pero educado

Responde de manera natural, como un cubano orgulloso de su revolución."""

    async def get_response(self, message: str, context: list = None) -> str:
        """
        Get AI response for a message.

        Args:
            message (str): User message.
            context (list): Previous conversation context (optional).

        Returns:
            str: AI response.
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if context:
            messages.extend(context)

        messages.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=500,
                temperature=0.8,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error al procesar la solicitud: {str(e)}"
