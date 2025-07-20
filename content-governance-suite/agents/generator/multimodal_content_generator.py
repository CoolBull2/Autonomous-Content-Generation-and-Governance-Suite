from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import os
from pathlib import Path
from ..base_agent import BaseAgent

class MultiModalContentGeneratorAgent(BaseAgent):
    """Multimodal content generator that adapts to available dependencies"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("MultiModalContentGeneratorAgent", config)
        
        # Initialize components based on available modules
        self.text_llm = None
        self.video_pipeline = None
        
        self._init_text_generation()
        self._init_video_generation()
        
        # Create output directories
        self.output_dir = Path("generated_content")
        self.video_dir = self.output_dir / "videos"
        self.video_dir.mkdir(parents=True, exist_ok=True)
    
    def _init_text_generation(self):
        """Initialize text generation with flexible imports"""
        if not self.available_modules.get('langchain'):
            self.log_activity("LangChain not available, text generation disabled")
            return
        
        try:
            # Try different import paths based on available packages
            if self.available_modules.get('langchain_perplexity'):
                from langchain_perplexity import ChatPerplexity
                self.text_llm = ChatPerplexity(
                    model="llama-3-sonar-large-32k-online",
                    temperature=0.7,
                    pplx_api_key=os.getenv("PPLX_API_KEY")
                )
            elif self.available_modules.get('langchain_community'):
                try:
                    from langchain_community.chat_models import ChatPerplexity
                    self.text_llm = ChatPerplexity(
                        model="llama-3-sonar-large-32k-online",
                        temperature=0.7,
                        api_key=os.getenv("PPLX_API_KEY")
                    )
                except ImportError:
                    # Fallback to basic LLM if available
                    from langchain.llms import OpenAI
                    self.text_llm = OpenAI(
                        temperature=0.7,
                        openai_api_key=os.getenv("OPENAI_API_KEY")
                    )
            
            self.log_activity("Text generation initialized successfully")
            
        except Exception as e:
            self.log_activity("Text generation initialization failed", {"error": str(e)})
            self.text_llm = None
    
    def _init_video_generation(self):
        """Initialize video generation with flexible imports"""
        if not (self.available_modules.get('torch') and self.available_modules.get('diffusers')):
            self.log_activity("Video generation dependencies not available")
            return
        
        try:
            import torch
            from diffusers import DiffusionPipeline
            
            # Try to load video generation pipeline
            device = "cuda" if torch.cuda.is_available() else "cpu"
            torch_dtype = torch.float16 if device == "cuda" else torch.float32
            
            # Try different models based on availability
            model_options = [
                "damo-vilab/text-to-video-ms-1.7b",
                "ali-vilab/text-to-video-ms-1.7b"
            ]
            
            for model_id in model_options:
                try:
                    self.video_pipeline = DiffusionPipeline.from_pretrained(
                        model_id,
                        torch_dtype=torch_dtype,
                        variant="fp16" if device == "cuda" else None,
                        use_safetensors=True
                    )
                    self.video_pipeline = self.video_pipeline.to(device)
                    
                    # Enable optimizations if available
                    if hasattr(self.video_pipeline, 'enable_xformers_memory_efficient_attention'):
                        try:
                            self.video_pipeline.enable_xformers_memory_efficient_attention()
                        except:
                            pass
                    
                    self.log_activity(f"Video generation initialized with {model_id}")
                    break
                    
                except Exception as model_error:
                    self.log_activity(f"Failed to load {model_id}", {"error": str(model_error)})
                    continue
            
            if not self.video_pipeline:
                self.log_activity("No video generation models could be loaded")
                
        except Exception as e:
            self.log_activity("Video generation initialization failed", {"error": str(e)})
            self.video_pipeline = None
    
    def process(self, content_request: Dict[str, Any]) -> Dict[str, Any]:
        """Process content generation request with fallbacks"""
        content_type = content_request.get("type", "text")
        
        try:
            if content_type == "video":
                return self._generate_video_or_spec(content_request)
            elif content_type == "text_and_video":
                return self._generate_text_and_video(content_request)
            else:
                return self._generate_text_or_fallback(content_request)
                
        except Exception as e:
            self.log_activity("Content processing failed", {"error": str(e)})
            return {
                "status": "error",
                "error": str(e),
                "content_type": content_type,
                "fallback_available": True
            }
    
    def _generate_text_or_fallback(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate text with fallback to template-based generation"""
        if self.text_llm:
            return self._generate_text_with_llm(request)
        else:
            return self._generate_text_template(request)
    
    def _generate_text_with_llm(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate text using LLM"""
        try:
            topic = request.get("topic", "")
            style_guide = request.get("style_guide", {})
            target_audience = request.get("target_audience", "general")
            
            prompt = self._build_prompt(topic, style_guide, target_audience)
            
            # Generate content
            if hasattr(self.text_llm, 'invoke'):
                response = self.text_llm.invoke(prompt)
                generated_text = response.content if hasattr(response, 'content') else str(response)
            else:
                generated_text = self.text_llm(prompt)
            
            return {
                "content_type": "text",
                "content": generated_text,
                "metadata": {
                    "topic": topic,
                    "target_audience": target_audience,
                    "generation_method": "llm",
                    "generation_timestamp": datetime.now().isoformat()
                },
                "status": "generated"
            }
            
        except Exception as e:
            self.log_activity("LLM generation failed, using template fallback", {"error": str(e)})
            return self._generate_text_template(request)
    
    def _generate_text_template(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback text generation using templates"""
        topic = request.get("topic", "Content Topic")
        style_guide = request.get("style_guide", {})
        tone = style_guide.get("tone", "professional")
        length = style_guide.get("length", "medium")
        
        templates = {
            "professional": f"""# {topic}

## Overview
This document provides comprehensive information about {topic}. The content has been structured to deliver valuable insights in a professional manner.

## Key Points
- {topic} represents an important area of focus in today's environment
- Understanding the implications and applications is crucial for success
- Implementation requires careful consideration of various factors

## Analysis
The current landscape surrounding {topic} continues to evolve rapidly. Organizations and individuals must stay informed about developments and best practices.

## Conclusion
{topic} remains a critical consideration for future planning and decision-making processes.""",
            
            "casual": f"""# All About {topic}

Hey there! Let's talk about {topic} - it's pretty interesting stuff.

So, what's the deal with {topic}? Well, it's become super important lately, and here's why you should care about it.

## The Basics
{topic} is one of those things that sounds complicated but is actually pretty straightforward once you get the hang of it.

## Why It Matters
- It affects a lot of people
- It's changing how we do things
- It's worth understanding

## Wrapping Up
At the end of the day, {topic} is something worth paying attention to. Hope this helps!""",
            
            "friendly": f"""# Understanding {topic}

Welcome! I'm excited to share some insights about {topic} with you.

{topic} is a fascinating subject that touches many aspects of our lives. Let me walk you through what makes it so important.

## What You Should Know
{topic} has become increasingly relevant, and understanding it can really help you in various ways.

## Key Benefits
- Provides valuable knowledge
- Helps with decision-making
- Opens up new opportunities

## Moving Forward
I hope this overview of {topic} has been helpful! Feel free to explore further and discover how it applies to your specific situation."""
        }
        
        content = templates.get(tone, templates["professional"])
        
        # Adjust length if needed
        if length == "short":
            content = content.split('\n\n')[0] + '\n\n' + content.split('\n\n')[1]
        elif length == "long":
            content += f"""

## Additional Considerations
When working with {topic}, it's important to consider the broader context and long-term implications. Success often depends on taking a holistic approach.

## Best Practices
- Stay informed about latest developments
- Consult with experts when needed
- Regular review and updates
- Document your findings and decisions

## Resources
Continue your learning journey by exploring additional resources and staying connected with the {topic} community."""
        
        return {
            "content_type": "text",
            "content": content,
            "metadata": {
                "topic": topic,
                "generation_method": "template",
                "template_tone": tone,
                "generation_timestamp": datetime.now().isoformat()
            },
            "status": "generated"
        }
    
    def _generate_video_or_spec(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate video or detailed specification"""
        if self.video_pipeline:
            return self._generate_video_with_model(request)
        else:
            return self._generate_video_specification(request)
    
    def _generate_video_with_model(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate actual video using AI model"""
        prompt = request.get("prompt", request.get("topic", ""))
        duration = min(request.get("duration", 3), 10)
        
        try:
            self.log_activity("Starting video generation", {"prompt": prompt})
            
            num_frames = duration * 8
            video_frames = self.video_pipeline(
                prompt,
                num_frames=num_frames,
                height=512,
                width=512,
                num_inference_steps=20,
                guidance_scale=9.0
            ).frames[0]
            
            video_filename = self._save_video(video_frames, prompt)
            
            return {
                "content_type": "video",
                "content": prompt,
                "video_path": str(self.video_dir / video_filename),
                "video_filename": video_filename,
                "metadata": {
                    "prompt": prompt,
                    "duration": duration,
                    "generation_method": "ai_model",
                    "generation_timestamp": datetime.now().isoformat()
                },
                "status": "generated"
            }
            
        except Exception as e:
            self.log_activity("Video generation failed, creating specification", {"error": str(e)})
            return self._generate_video_specification(request)
    
    def _generate_video_specification(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate detailed video production specification"""
        prompt = request.get("prompt", request.get("topic", ""))
        duration = request.get("duration", 3)
        
        specification = {
            "title": f"Video Production Guide: {prompt[:50]}...",
            "description": prompt,
            "technical_specs": {
                "duration": f"{duration} seconds",
                "resolution": "1920x1080 (Recommended)",
                "fps": "30 fps",
                "format": "MP4",
                "aspect_ratio": "16:9"
            },
            "visual_elements": self._suggest_visual_elements(prompt),
            "production_steps": [
                "1. Script development and storyboarding",
                "2. Asset collection (footage, images, audio)",
                "3. Video editing and post-production",
                "4. Color correction and audio mixing",
                "5. Final export and quality check"
            ],
            "recommended_tools": [
                "Free: DaVinci Resolve, OpenShot",
                "Professional: Adobe Premiere Pro, Final Cut Pro",
                "AI-assisted: RunwayML, Synthesia"
            ],
            "estimated_cost": "Free - $50/month (depending on tools used)"
        }
        
        return {
            "content_type": "video_specification",
            "content": prompt,
            "video_specification": specification,
            "metadata": {
                "prompt": prompt,
                "duration": duration,
                "generation_method": "specification",
                "generation_timestamp": datetime.now().isoformat()
            },
            "status": "specification_generated"
        }
    
    def _generate_text_and_video(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate both text and video content"""
        text_result = self._generate_text_or_fallback(request)
        
        if text_result.get("status") != "generated":
            return text_result
        
        # Extract video prompt
        video_prompt = self._extract_video_prompt(text_result["content"], request.get("topic", ""))
        video_request = {
            "prompt": video_prompt,
            "duration": request.get("video_duration", 5)
        }
        video_result = self._generate_video_or_spec(video_request)
        
        # Combine results
        combined = {
            "content_type": "text_and_video",
            "text_content": text_result["content"],
            "video_prompt": video_prompt,
            "metadata": {
                "topic": request.get("topic", ""),
                "text_method": text_result["metadata"]["generation_method"],
                "video_method": video_result["metadata"]["generation_method"],
                "generation_timestamp": datetime.now().isoformat()
            },
            "status": "generated"
        }
        
        # Add video data
        if video_result.get("video_path"):
            combined["video_path"] = video_result["video_path"]
            combined["video_filename"] = video_result["video_filename"]
        elif video_result.get("video_specification"):
            combined["video_specification"] = video_result["video_specification"]
        
        return combined
    
    def _build_prompt(self, topic: str, style_guide: Dict, target_audience: str) -> str:
        """Build generation prompt"""
        tone = style_guide.get("tone", "professional")
        length = style_guide.get("length", "medium")
        
        return f"""Create {length} content about: {topic}
        
Target audience: {target_audience}
Tone: {tone}

Requirements:
- Be informative and accurate
- Use clear, engaging language
- Include relevant examples
- Structure content logically
- Make it valuable for the target audience

Content:"""
    
    def _extract_video_prompt(self, text_content: str, topic: str) -> str:
        """Extract video prompt from text"""
        sentences = text_content.split('.')
        if sentences and len(sentences[0].strip()) < 100:
            return sentences[0].strip()
        return f"Visual representation of {topic}"
    
    def _suggest_visual_elements(self, prompt: str) -> List[str]:
        """Suggest visual elements for video"""
        keywords = {
            "business": ["Office environments", "Professional meetings", "Charts"],
            "technology": ["Modern interfaces", "Innovation", "Digital elements"],
            "education": ["Learning spaces", "Knowledge visualization", "Interactive elements"],
            "health": ["Medical facilities", "Wellness imagery", "Professional healthcare"]
        }
        
        suggestions = []
        for category, elements in keywords.items():
            if category in prompt.lower():
                suggestions.extend(elements[:2])
        
        if not suggestions:
            suggestions = ["Professional stock footage", "Clean animations", "Text overlays"]
        
        return suggestions[:4]
    
    def _save_video(self, frames: List, prompt: str) -> str:
        """Save video frames"""
        try:
            import imageio
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_prompt = "".join(c for c in prompt[:20] if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_prompt = safe_prompt.replace(' ', '_')
            filename = f"video_{timestamp}_{safe_prompt}.mp4"
            
            filepath = self.video_dir / filename
            imageio.mimsave(str(filepath), frames, fps=8, quality=8)
            
            return filename
            
        except Exception as e:
            self.log_activity("Video save failed", {"error": str(e)})
            raise e
