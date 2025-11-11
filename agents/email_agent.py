

import os
from typing import Optional


def generate_email_response(
    email_text: str,
    tone: str = "Professional",
    important_info: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Generate AI response using Gemini API.
    Falls back to template if API unavailable.
    
    Args:
        email_text: Original email to respond to
        tone: Professional/Friendly/Apologetic/Persuasive
        important_info: Optional context to include
        api_key: Gemini API key (if not in environment)
        
    Returns:
        Generated draft response
    """
    # Try to use Gemini API
    try:
        import google.generativeai as genai
        
        # Get API key
        if not api_key:
            api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            raise ValueError("No API key provided")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Build prompt
        prompt = _build_gemini_prompt(email_text, tone, important_info)
        
        # Generate response
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            raise ValueError("Empty response from API")
            
    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fallback to template
        return _generate_template_response(email_text, tone, important_info)


def _build_gemini_prompt(
    email_text: str,
    tone: str,
    important_info: Optional[str]
) -> str:
    """
    Build prompt for Gemini API.
    
    Args:
        email_text: Original email
        tone: Desired tone
        important_info: Additional context
        
    Returns:
        Formatted prompt string
    """
    tone_instructions = {
        "Professional": "professional, formal, and business-like",
        "Friendly": "warm, friendly, and conversational",
        "Apologetic": "apologetic, understanding, and empathetic",
        "Persuasive": "persuasive, confident, and compelling"
    }
    
    tone_desc = tone_instructions.get(tone, "professional and polite")
    
    prompt = f"""You are an email assistant. Generate a {tone_desc} reply to the following email.

Original Email:
---
{email_text}
---

"""
    
    if important_info:
        prompt += f"""Important Information to Include:
{important_info}

"""
    
    prompt += f"""Instructions:
1. Write a clear, concise reply in a {tone_desc} tone
2. Address the main points from the original email
3. Keep the response professional and appropriate
4. Do not include subject line or email headers
5. Write only the email body text
"""
    
    if important_info:
        prompt += "6. Incorporate the important information provided\n"
    
    prompt += "\nGenerate the email reply now:"
    
    return prompt


def _generate_template_response(
    email_text: str,
    tone: str,
    important_info: Optional[str]
) -> str:
    """
    Generate template-based response as fallback.
    
    Args:
        email_text: Original email
        tone: Desired tone
        important_info: Additional context
        
    Returns:
        Template response string
    """
    templates = {
        "Professional": _professional_template,
        "Friendly": _friendly_template,
        "Apologetic": _apologetic_template,
        "Persuasive": _persuasive_template
    }
    
    template_func = templates.get(tone, _professional_template)
    return template_func(email_text, important_info)


def _professional_template(email_text: str, important_info: Optional[str]) -> str:
    """Professional tone template."""
    response = """Thank you for your email.

I appreciate you reaching out. """
    
    if important_info:
        response += f"""Regarding your inquiry, {important_info}

"""
    else:
        response += """I have reviewed your message and would like to respond to your inquiry.

"""
    
    response += """Please let me know if you need any additional information or clarification.

Best regards"""
    
    return response


def _friendly_template(email_text: str, important_info: Optional[str]) -> str:
    """Friendly tone template."""
    response = """Hi there!

Thanks so much for getting in touch! """
    
    if important_info:
        response += f"""I wanted to let you know that {important_info}

"""
    else:
        response += """I got your message and I'm happy to help!

"""
    
    response += """Feel free to reach out if you have any questions - I'm always here to help!

Cheers"""
    
    return response


def _apologetic_template(email_text: str, important_info: Optional[str]) -> str:
    """Apologetic tone template."""
    response = """Dear sender,

I sincerely apologize for any inconvenience this may have caused. """
    
    if important_info:
        response += f"""Please allow me to explain: {important_info}

"""
    else:
        response += """I understand your concern and want to make this right.

"""
    
    response += """I truly appreciate your patience and understanding in this matter.

With sincere apologies"""
    
    return response


def _persuasive_template(email_text: str, important_info: Optional[str]) -> str:
    """Persuasive tone template."""
    response = """Thank you for considering this opportunity.

I'm confident that this will be beneficial for all parties involved. """
    
    if important_info:
        response += f"""Specifically, {important_info}

"""
    else:
        response += """Let me outline the key benefits and value proposition.

"""
    
    response += """I believe this is an excellent opportunity and I look forward to moving forward together.

Best regards"""
    
    return response


def test_gemini_connection(api_key: str) -> tuple[bool, str]:
    """
    Test Gemini API connection.
    
    Args:
        api_key: Gemini API key
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Try a simple generation
        response = model.generate_content("Say 'API connection successful' if you can read this.")
        
        if response.text:
            return True, "✅ Gemini API connection successful!"
        else:
            return False, "⚠️ API responded but returned empty text"
            
    except ImportError:
        return False, "❌ google-generativeai package not installed"
    except Exception as e:
        return False, f"❌ API connection failed: {str(e)}"
