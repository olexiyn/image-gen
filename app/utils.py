from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel
import json

imagen_model = ImageGenerationModel.from_pretrained('imagen-3.0-fast-generate-001')
gemini_pro_model = GenerativeModel('gemini-1.5-pro-002')


def content_gen(topic):
    prompt_text = f"Create 3 High-Quality Image Prompts to generate photos on given topic: {topic}"
    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                },
            },
            "required": ["prompt"],
        },
    }

    content = gemini_pro_model.generate_content(prompt_text,
                                                generation_config=GenerationConfig(
                                                    response_mime_type="application/json",
                                                    response_schema=response_schema
                                                ),
                                                stream=False
                                                )
    return json.loads(content.text)


def image_gen(prompt, aspect_ratio='16:9'):
    response = imagen_model.generate_images(
        prompt=prompt,
        language='en',
        guidance_scale=98.5,
        add_watermark=False,
        number_of_images=1,
        aspect_ratio=aspect_ratio
    )
    
    return response.images