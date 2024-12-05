from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel

imagen_model = ImageGenerationModel.from_pretrained('imagen-3.0-generate-001')
gemini_pro_model = GenerativeModel('gemini-1.5-pro-002')
