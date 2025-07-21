import os
import logging
from google import genai
from google.genai import types

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "fallback-key"))

def generate_psychological_summary(responses, stress_score, age):
    """Generate a personalized psychological summary using Gemini AI"""
    try:
        # Prepare the prompt with user data
        prompt = create_psychological_prompt(responses, stress_score, age)
        
        # Generate response using Gemini
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        return response.text or "Unable to generate psychological summary at this time."
    
    except Exception as e:
        logging.error(f"Error generating Gemini summary: {e}")
        return generate_fallback_summary(stress_score, age)

def create_psychological_prompt(responses, stress_score, age):
    """Create a detailed prompt for Gemini AI"""
    
    # Analyze response patterns
    personality_responses = [responses.get(f'q{i}', 'A') for i in range(1, 11)]
    stress_responses = [responses.get(f'q{i}', 'Low') for i in range(11, 16)]
    
    high_stress_count = sum(1 for r in personality_responses if r in ['D', 'E'])
    low_stress_count = sum(1 for r in personality_responses if r in ['A', 'B'])
    
    prompt = f"""
    You are a professional psychologist providing a personalized mental wellness assessment. 
    Based on the following data, create a comprehensive psychological summary:

    USER PROFILE:
    - Age: {age}
    - Stress Score: {stress_score}/10
    - High-stress indicators: {high_stress_count}/10
    - Low-stress indicators: {low_stress_count}/10

    STRESS LEVEL RESPONSES:
    {', '.join(stress_responses)}

    PERSONALITY/BEHAVIORAL PATTERNS:
    Based on 10 personality questions, the user showed varied responses indicating their current mental state and coping mechanisms.

    Please provide a personalized analysis , each in new line, including:
    1. Current Mental State Assessment
    2. Stress Management Insights
    3. Behavioral Patterns Observed
    4. Personalized Recommendations for Improvement
    5. Coping Strategies Tailored to Their Profile

    Keep the tone professional yet empathetic, and provide actionable insights that can help improve their mental wellness. Ensure the format is clear and concise , no unnecessary symbols , emojis or special charcaters 
    Limit the response to 300-400 words.
    """
    
    return prompt

def generate_fallback_summary(stress_score, age):
    """Generate a fallback summary when Gemini is not available"""
    if stress_score <= 3:
        return f"""
        Based on your assessment, you appear to be managing stress relatively well. At {age} years old, 
        maintaining good mental health practices is important for long-term wellness. Your current stress 
        level suggests you have developed effective coping mechanisms. Continue with regular self-care 
        activities and mindfulness practices to maintain this positive state.
        """
    elif stress_score <= 6:
        return f"""
        Your assessment indicates moderate stress levels that are common for someone your age ({age}). 
        This suggests you may benefit from incorporating additional stress management techniques into 
        your daily routine. Consider practicing meditation, regular exercise, or speaking with a mental 
        health professional to develop better coping strategies.
        """
    else:
        return f"""
        Your assessment shows elevated stress levels that may require immediate attention. At {age} years old, 
        it's important to address these concerns promptly. Consider reaching out to a mental health professional 
        for personalized support. In the meantime, focus on basic self-care: adequate sleep, regular meals, 
        and gentle exercise can help manage acute stress symptoms.
        """
